from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, List, Optional


NIA_VENDOR_ID = 0x1234
NIA_PRODUCT_ID = 0x0000
NIA_USB_ENDPOINT = 0x81
NIA_PACKET_SIZE = 64
NIA_INTERFACE = 0
MAX_SAMPLES_PER_PACKET = 16


class PacketParser:
    @staticmethod
    def normalize_packet(raw: bytes | List[int]) -> bytes:
        packet = bytes(raw)
        if len(packet) == 65:
            packet = packet[1:]
        return packet

    @staticmethod
    def parse_samples(raw: bytes | List[int]) -> List[int]:
        packet = PacketParser.normalize_packet(raw)
        if len(packet) < 55:
            return []

        sample_count = int(packet[54])
        if sample_count <= 0:
            return []
        sample_count = min(sample_count, MAX_SAMPLES_PER_PACKET)

        samples: List[int] = []
        for idx in range(sample_count):
            base = idx * 3
            if base + 2 >= len(packet):
                break
            value = packet[base] | (packet[base + 1] << 8) | (packet[base + 2] << 16)
            if value & 0x800000:
                value -= 0x1000000
            samples.append(value)
        return samples


class DeviceBackendError(RuntimeError):
    pass


@dataclass
class ProbeResult:
    found_any: bool = False
    hid_found: bool = False
    usb_found: bool = False
    hid_count: int = 0
    summary: str = ""
    error: str = ""


class BaseBackend:
    backend_name = "Unknown"

    def open(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def read_packet(self, timeout_ms: int = 25) -> bytes:
        raise NotImplementedError


class HidBackend(BaseBackend):
    backend_name = "HID"

    def __init__(self) -> None:
        self._device = None
        self._path: Optional[bytes] = None

    def open(self) -> None:
        try:
            import hid  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise DeviceBackendError(f"hid backend unavailable: {exc}") from exc

        devices = hid.enumerate(NIA_VENDOR_ID, NIA_PRODUCT_ID)
        if not devices:
            raise DeviceBackendError("OCZ NIA not found via HID enumeration.")

        devices.sort(key=lambda d: (-(d.get("max_input_report_len") or 0), d.get("interface_number", 999)))
        chosen = devices[0]
        self._path = chosen.get("path")
        if not self._path:
            raise DeviceBackendError("HID device found, but no device path was exposed.")

        dev = hid.device()
        dev.open_path(self._path)
        dev.set_nonblocking(False)
        self._device = dev

    def close(self) -> None:
        if self._device is not None:
            try:
                self._device.close()
            except Exception:
                pass
        self._device = None

    def read_packet(self, timeout_ms: int = 25) -> bytes:
        if self._device is None:
            raise DeviceBackendError("HID device is not open.")
        data = self._device.read(NIA_PACKET_SIZE + 1, timeout_ms)
        if not data:
            return b""
        return bytes(data)


class PyUsbBackend(BaseBackend):
    backend_name = "PyUSB/WinUSB"

    def __init__(self) -> None:
        self._usb_core = None
        self._usb_util = None
        self._device = None

    def open(self) -> None:
        try:
            import usb.core  # type: ignore
            import usb.util  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise DeviceBackendError(f"pyusb backend unavailable: {exc}") from exc

        self._usb_core = usb.core
        self._usb_util = usb.util
        dev = usb.core.find(idVendor=NIA_VENDOR_ID, idProduct=NIA_PRODUCT_ID)
        if dev is None:
            raise DeviceBackendError("OCZ NIA not found via PyUSB.")

        self._device = dev
        try:
            dev.set_configuration()
        except Exception:
            pass

        try:
            if dev.is_kernel_driver_active(NIA_INTERFACE):
                dev.detach_kernel_driver(NIA_INTERFACE)
        except Exception:
            pass

        try:
            self._usb_util.claim_interface(dev, NIA_INTERFACE)
        except Exception:
            pass

    def close(self) -> None:
        if self._device is not None and self._usb_util is not None:
            try:
                self._usb_util.release_interface(self._device, NIA_INTERFACE)
            except Exception:
                pass
            try:
                self._usb_util.dispose_resources(self._device)
            except Exception:
                pass
        self._device = None

    def read_packet(self, timeout_ms: int = 25) -> bytes:
        if self._device is None:
            raise DeviceBackendError("PyUSB device is not open.")
        try:
            data = self._device.read(NIA_USB_ENDPOINT, NIA_PACKET_SIZE, timeout=timeout_ms)
            return bytes(data)
        except Exception:
            return b""


@dataclass
class ReaderStats:
    backend_name: str = "Disconnected"
    packets: int = 0
    samples: int = 0
    packets_per_second: float = 0.0
    samples_per_second: float = 0.0
    last_error: str = ""
    connected: bool = False
    started_at: float = field(default_factory=time.perf_counter)


def probe_nia() -> ProbeResult:
    result = ProbeResult()
    messages: List[str] = []
    errors: List[str] = []

    try:
        import hid  # type: ignore

        devices = hid.enumerate(NIA_VENDOR_ID, NIA_PRODUCT_ID)
        if devices:
            result.found_any = True
            result.hid_found = True
            result.hid_count = len(devices)
            details = []
            for item in devices[:3]:
                iface = item.get("interface_number", "?")
                product = item.get("product_string") or "NIA"
                details.append(f"{product} / iface {iface}")
            messages.append("HID: " + ", ".join(details))
        else:
            messages.append("HID: none")
    except Exception as exc:
        errors.append(f"HID probe failed: {exc}")

    try:
        import usb.core  # type: ignore

        dev = usb.core.find(idVendor=NIA_VENDOR_ID, idProduct=NIA_PRODUCT_ID)
        if dev is not None:
            result.found_any = True
            result.usb_found = True
            messages.append(f"USB: bus {getattr(dev, 'bus', '?')} addr {getattr(dev, 'address', '?')}")
        else:
            messages.append("USB: none")
    except Exception as exc:
        errors.append(f"USB probe failed: {exc}")

    result.summary = " | ".join(messages)
    result.error = " | ".join(errors)
    return result


class NIAReader:
    def __init__(self) -> None:
        self._buffer: Deque[int] = deque(maxlen=131072)
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._backend: Optional[BaseBackend] = None
        self._stats = ReaderStats()

    def start(self, preferred_backend: str = "auto") -> None:
        self.stop()
        self._stop.clear()
        self._stats = ReaderStats(started_at=time.perf_counter())
        self._thread = threading.Thread(target=self._run, args=(preferred_backend,), daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.5)
        self._thread = None
        if self._backend is not None:
            try:
                self._backend.close()
            except Exception:
                pass
        self._backend = None
        self._stats.connected = False
        self._stats.backend_name = "Disconnected"

    def _backend_candidates(self, preferred_backend: str) -> List[BaseBackend]:
        pref = preferred_backend.lower().strip()
        if pref == "hid":
            return [HidBackend(), PyUsbBackend()]
        if pref == "pyusb":
            return [PyUsbBackend(), HidBackend()]
        return [HidBackend(), PyUsbBackend()]

    def _connect_backend(self, preferred_backend: str) -> BaseBackend:
        errors: List[str] = []
        for backend in self._backend_candidates(preferred_backend):
            try:
                backend.open()
                self._stats.backend_name = backend.backend_name
                self._stats.connected = True
                self._stats.last_error = ""
                return backend
            except Exception as exc:
                errors.append(f"{backend.backend_name}: {exc}")
        self._stats.connected = False
        self._stats.backend_name = "Unavailable"
        self._stats.last_error = " | ".join(errors) if errors else "No backend candidates tried."
        raise DeviceBackendError(self._stats.last_error)

    def _run(self, preferred_backend: str) -> None:
        try:
            self._backend = self._connect_backend(preferred_backend)
        except Exception:
            return

        window_start = time.perf_counter()
        window_packets = 0
        window_samples = 0

        while not self._stop.is_set():
            try:
                raw = self._backend.read_packet(25)
                if not raw:
                    continue
                samples = PacketParser.parse_samples(raw)
                if not samples:
                    continue
                with self._lock:
                    self._buffer.extend(samples)
                self._stats.packets += 1
                self._stats.samples += len(samples)
                window_packets += 1
                window_samples += len(samples)

                now = time.perf_counter()
                elapsed = now - window_start
                if elapsed >= 0.5:
                    self._stats.packets_per_second = window_packets / elapsed
                    self._stats.samples_per_second = window_samples / elapsed
                    window_start = now
                    window_packets = 0
                    window_samples = 0
            except Exception as exc:
                self._stats.last_error = str(exc)
                self._stats.connected = False
                break

        if self._backend is not None:
            try:
                self._backend.close()
            except Exception:
                pass
        self._backend = None
        self._stats.connected = False

    def get_recent_samples(self, count: int = 8192) -> List[int]:
        with self._lock:
            if count >= len(self._buffer):
                return list(self._buffer)
            return list(self._buffer)[-count:]

    def clear_buffer(self) -> None:
        with self._lock:
            self._buffer.clear()

    def stats(self) -> ReaderStats:
        return ReaderStats(
            backend_name=self._stats.backend_name,
            packets=self._stats.packets,
            samples=self._stats.samples,
            packets_per_second=self._stats.packets_per_second,
            samples_per_second=self._stats.samples_per_second,
            last_error=self._stats.last_error,
            connected=self._stats.connected,
            started_at=self._stats.started_at,
        )
