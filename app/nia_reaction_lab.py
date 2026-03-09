from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore, QtGui, QtWidgets

from nia_device import NIAReader, probe_nia


pg.setConfigOptions(antialias=True)
APP_DIR = Path(__file__).resolve().parent
EXPORT_ROOT = APP_DIR / "exports"
EXPORT_ROOT.mkdir(parents=True, exist_ok=True)


TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "language": "Language",
        "backend": "Backend",
        "connect": "Connect",
        "disconnect": "Disconnect",
        "capture": "Capture reaction bundle",
        "mark": "Add marker",
        "clear": "Clear notes",
        "title": "NIA Conversation Reaction Lab",
        "subtitle": "Live signal view for human reactions during AI conversations",
        "status_streaming": "🟢 NIA streaming",
        "status_detected": "🟡 NIA detected",
        "status_missing": "⚪ NIA not detected",
        "status_error": "🔴 Read error",
        "device_probe": "Device status",
        "metric_backend": "Backend",
        "metric_packets": "Packets",
        "metric_samples": "Samples",
        "metric_packets_s": "Packets/s",
        "metric_samples_s": "Samples/s",
        "metric_rms": "RMS",
        "metric_peak": "Peak-to-peak",
        "panel_wave": "Waveform",
        "panel_spectrum": "Spectrum",
        "panel_bands": "Band activity",
        "panel_aura": "Signal aura",
        "panel_notes": "Conversation context",
        "panel_markers": "Markers",
        "prompt": "Prompt / situation",
        "reply": "AI reply / excerpt",
        "tag": "Self tag (optional)",
        "notes": "Personal notes (optional)",
        "session": "Session name",
        "save_path": "Export folder",
        "saved": "Reaction bundle saved.",
        "saved_title": "Saved",
        "saved_error": "Could not save export bundle.",
        "saved_error_title": "Save error",
        "marker_added": "Marker added",
        "detected_details": "Probe",
        "bands_title": "6–30 Hz bands",
        "aura_title": "Signal shape",
        "bundle_name": "Bundle",
        "markers_empty": "No markers yet.",
        "placeholder_prompt": "What happened in the conversation at this moment?",
        "placeholder_reply": "Paste the relevant AI answer excerpt here.",
        "placeholder_tag": "example: irritated, calm, surprised, tense, fascinated",
        "placeholder_notes": "Anything you noticed in yourself.",
        "help_line": "Use a marker when something in the conversation triggers a visible inner reaction.",
        "export_open": "Open export folder",
    },
    "de": {
        "language": "Sprache",
        "backend": "Backend",
        "connect": "Verbinden",
        "disconnect": "Trennen",
        "capture": "Reaktionspaket speichern",
        "mark": "Marker setzen",
        "clear": "Notizen leeren",
        "title": "NIA Conversation Reaction Lab",
        "subtitle": "Live-Signalansicht für menschliche Reaktionen während KI-Gesprächen",
        "status_streaming": "🟢 NIA aktiv verbunden",
        "status_detected": "🟡 NIA erkannt",
        "status_missing": "⚪ NIA nicht erkannt",
        "status_error": "🔴 Lesefehler",
        "device_probe": "Gerätestatus",
        "metric_backend": "Backend",
        "metric_packets": "Pakete",
        "metric_samples": "Samples",
        "metric_packets_s": "Pakete/s",
        "metric_samples_s": "Samples/s",
        "metric_rms": "RMS",
        "metric_peak": "Peak-to-Peak",
        "panel_wave": "Wellenform",
        "panel_spectrum": "Spektrum",
        "panel_bands": "Bandaktivität",
        "panel_aura": "Signal-Aura",
        "panel_notes": "Gesprächskontext",
        "panel_markers": "Marker",
        "prompt": "Prompt / Situation",
        "reply": "KI-Antwort / Auszug",
        "tag": "Selbst-Tag (optional)",
        "notes": "Eigene Notizen (optional)",
        "session": "Sitzungsname",
        "save_path": "Export-Ordner",
        "saved": "Reaktionspaket gespeichert.",
        "saved_title": "Gespeichert",
        "saved_error": "Exportpaket konnte nicht gespeichert werden.",
        "saved_error_title": "Speicherfehler",
        "marker_added": "Marker gesetzt",
        "detected_details": "Probe",
        "bands_title": "6–30 Hz Bänder",
        "aura_title": "Signalform",
        "bundle_name": "Paket",
        "markers_empty": "Noch keine Marker.",
        "placeholder_prompt": "Was ist in diesem Moment im Gespräch passiert?",
        "placeholder_reply": "Hier den relevanten KI-Antwortauszug einfügen.",
        "placeholder_tag": "z. B.: irritiert, ruhig, überrascht, angespannt, fasziniert",
        "placeholder_notes": "Alles, was dir an dir selbst aufgefallen ist.",
        "help_line": "Setze einen Marker, wenn im Gespräch eine spürbare innere Reaktion entsteht.",
        "export_open": "Export-Ordner öffnen",
    },
    "fr": {
        "language": "Langue",
        "backend": "Backend",
        "connect": "Connecter",
        "disconnect": "Déconnecter",
        "capture": "Enregistrer le paquet de réaction",
        "mark": "Ajouter un marqueur",
        "clear": "Effacer les notes",
        "title": "NIA Conversation Reaction Lab",
        "subtitle": "Vue en direct des signaux humains pendant une conversation avec une IA",
        "status_streaming": "🟢 NIA en flux actif",
        "status_detected": "🟡 NIA détecté",
        "status_missing": "⚪ NIA non détecté",
        "status_error": "🔴 Erreur de lecture",
        "device_probe": "État de l'appareil",
        "metric_backend": "Backend",
        "metric_packets": "Paquets",
        "metric_samples": "Échantillons",
        "metric_packets_s": "Paquets/s",
        "metric_samples_s": "Échantillons/s",
        "metric_rms": "RMS",
        "metric_peak": "Crête à crête",
        "panel_wave": "Forme d'onde",
        "panel_spectrum": "Spectre",
        "panel_bands": "Activité des bandes",
        "panel_aura": "Aura du signal",
        "panel_notes": "Contexte de conversation",
        "panel_markers": "Marqueurs",
        "prompt": "Prompt / situation",
        "reply": "Réponse IA / extrait",
        "tag": "Auto-étiquette (optionnel)",
        "notes": "Notes personnelles (optionnel)",
        "session": "Nom de session",
        "save_path": "Dossier d'export",
        "saved": "Paquet de réaction enregistré.",
        "saved_title": "Enregistré",
        "saved_error": "Impossible d'enregistrer le paquet d'export.",
        "saved_error_title": "Erreur d'enregistrement",
        "marker_added": "Marqueur ajouté",
        "detected_details": "Probe",
        "bands_title": "Bandes 6–30 Hz",
        "aura_title": "Forme du signal",
        "bundle_name": "Paquet",
        "markers_empty": "Aucun marqueur pour l'instant.",
        "placeholder_prompt": "Que s'est-il passé dans la conversation à ce moment ?",
        "placeholder_reply": "Collez ici l'extrait pertinent de la réponse IA.",
        "placeholder_tag": "ex.: irrité, calme, surpris, tendu, fasciné",
        "placeholder_notes": "Tout ce que vous avez remarqué en vous-même.",
        "help_line": "Ajoutez un marqueur quand la conversation déclenche une réaction intérieure visible.",
        "export_open": "Ouvrir le dossier d'export",
    },
    "zh_cn": {
        "language": "语言",
        "backend": "后端",
        "connect": "连接",
        "disconnect": "断开",
        "capture": "保存反应包",
        "mark": "添加标记",
        "clear": "清空备注",
        "title": "NIA Conversation Reaction Lab",
        "subtitle": "用于观察人与 AI 对话时生理反应的实时信号界面",
        "status_streaming": "🟢 NIA 正在传输",
        "status_detected": "🟡 已检测到 NIA",
        "status_missing": "⚪ 未检测到 NIA",
        "status_error": "🔴 读取错误",
        "device_probe": "设备状态",
        "metric_backend": "后端",
        "metric_packets": "数据包",
        "metric_samples": "采样点",
        "metric_packets_s": "数据包/秒",
        "metric_samples_s": "采样点/秒",
        "metric_rms": "RMS",
        "metric_peak": "峰峰值",
        "panel_wave": "波形",
        "panel_spectrum": "频谱",
        "panel_bands": "频段活动",
        "panel_aura": "信号光环",
        "panel_notes": "对话上下文",
        "panel_markers": "标记",
        "prompt": "提示词 / 情境",
        "reply": "AI 回复 / 摘录",
        "tag": "自我标签（可选）",
        "notes": "个人备注（可选）",
        "session": "会话名称",
        "save_path": "导出文件夹",
        "saved": "反应包已保存。",
        "saved_title": "已保存",
        "saved_error": "无法保存导出包。",
        "saved_error_title": "保存错误",
        "marker_added": "已添加标记",
        "detected_details": "探测",
        "bands_title": "6–30 Hz 频段",
        "aura_title": "信号形态",
        "bundle_name": "包",
        "markers_empty": "暂时没有标记。",
        "placeholder_prompt": "此刻对话中发生了什么？",
        "placeholder_reply": "在此粘贴相关的 AI 回复片段。",
        "placeholder_tag": "例如：烦躁、平静、惊讶、紧张、着迷",
        "placeholder_notes": "记录你注意到的任何自身反应。",
        "help_line": "当对话触发明显的内在反应时，请添加标记。",
        "export_open": "打开导出文件夹",
    },
    "ru": {
        "language": "Язык",
        "backend": "Бэкенд",
        "connect": "Подключить",
        "disconnect": "Отключить",
        "capture": "Сохранить пакет реакции",
        "mark": "Добавить маркер",
        "clear": "Очистить заметки",
        "title": "NIA Conversation Reaction Lab",
        "subtitle": "Живой просмотр сигналов человека во время диалога с ИИ",
        "status_streaming": "🟢 NIA передаёт сигнал",
        "status_detected": "🟡 NIA обнаружен",
        "status_missing": "⚪ NIA не обнаружен",
        "status_error": "🔴 Ошибка чтения",
        "device_probe": "Состояние устройства",
        "metric_backend": "Бэкенд",
        "metric_packets": "Пакеты",
        "metric_samples": "Сэмплы",
        "metric_packets_s": "Пакеты/с",
        "metric_samples_s": "Сэмплы/с",
        "metric_rms": "RMS",
        "metric_peak": "Пик-пик",
        "panel_wave": "Осциллограмма",
        "panel_spectrum": "Спектр",
        "panel_bands": "Активность полос",
        "panel_aura": "Аура сигнала",
        "panel_notes": "Контекст разговора",
        "panel_markers": "Маркеры",
        "prompt": "Промпт / ситуация",
        "reply": "Ответ ИИ / фрагмент",
        "tag": "Самометка (необязательно)",
        "notes": "Личные заметки (необязательно)",
        "session": "Имя сессии",
        "save_path": "Папка экспорта",
        "saved": "Пакет реакции сохранён.",
        "saved_title": "Сохранено",
        "saved_error": "Не удалось сохранить пакет экспорта.",
        "saved_error_title": "Ошибка сохранения",
        "marker_added": "Маркер добавлен",
        "detected_details": "Проба",
        "bands_title": "Полосы 6–30 Гц",
        "aura_title": "Форма сигнала",
        "bundle_name": "Пакет",
        "markers_empty": "Пока нет маркеров.",
        "placeholder_prompt": "Что произошло в разговоре в этот момент?",
        "placeholder_reply": "Вставьте сюда нужный фрагмент ответа ИИ.",
        "placeholder_tag": "например: раздражён, спокоен, удивлён, напряжён, увлечён",
        "placeholder_notes": "Любые наблюдения о своём состоянии.",
        "help_line": "Ставьте маркер, когда разговор вызывает заметную внутреннюю реакцию.",
        "export_open": "Открыть папку экспорта",
    },
}

LANG_LABELS = {
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "zh_cn": "简体中文",
    "ru": "Русский",
}

BANDS = [(6, 9), (9, 12), (12, 15), (15, 20), (20, 25), (25, 30)]


class BandsWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.values = [0.0] * 6
        self.labels = [f"{lo}–{hi}" for lo, hi in BANDS]
        self.setMinimumHeight(200)

    def set_values(self, values: List[float]) -> None:
        self.values = list(values[:6]) + [0.0] * max(0, 6 - len(values))
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # noqa: N802
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect().adjusted(8, 8, -8, -8)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor("#0e1625"))
        painter.drawRoundedRect(rect, 18, 18)

        bars_rect = rect.adjusted(16, 18, -16, -18)
        bar_width = bars_rect.width() / 6.0
        max_val = max(1.0, max(self.values) * 1.15)
        colors = [
            QtGui.QColor("#42e8ff"),
            QtGui.QColor("#59ffcf"),
            QtGui.QColor("#84ff72"),
            QtGui.QColor("#ffd166"),
            QtGui.QColor("#ff9f5c"),
            QtGui.QColor("#ff62a5"),
        ]

        for i, value in enumerate(self.values):
            x = bars_rect.left() + i * bar_width + 8
            track = QtCore.QRectF(x, bars_rect.top() + 10, bar_width - 16, bars_rect.height() - 38)
            painter.setBrush(QtGui.QColor(255, 255, 255, 20))
            painter.drawRoundedRect(track, 10, 10)

            fill_height = 0.0 if max_val <= 0 else (value / max_val) * track.height()
            fill = QtCore.QRectF(track.left(), track.bottom() - fill_height, track.width(), fill_height)
            grad = QtGui.QLinearGradient(fill.topLeft(), fill.bottomLeft())
            grad.setColorAt(0.0, colors[i].lighter(130))
            grad.setColorAt(1.0, colors[i].darker(140))
            painter.setBrush(grad)
            painter.drawRoundedRect(fill, 10, 10)

            painter.setPen(QtGui.QColor("#dfe8ff"))
            painter.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.DemiBold))
            painter.drawText(QtCore.QRectF(track.left() - 8, track.bottom() + 6, track.width() + 16, 18), QtCore.Qt.AlignCenter, self.labels[i])


class AuraWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.values = [0.0] * 6
        self.phase = 0.0
        self.setMinimumHeight(240)

    def set_values(self, values: List[float]) -> None:
        self.values = list(values[:6]) + [0.0] * max(0, 6 - len(values))
        self.phase += 0.07
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # noqa: N802
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect().adjusted(8, 8, -8, -8)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor("#0d1523"))
        painter.drawRoundedRect(rect, 18, 18)

        center = rect.center()
        max_radius = min(rect.width(), rect.height()) * 0.36
        base = max(1.0, max(self.values) * 1.15)
        pulse = 0.5 + 0.5 * math.sin(self.phase)

        painter.setBrush(QtGui.QColor(66, 232, 255, 26 + int(38 * pulse)))
        painter.drawEllipse(center, max_radius * 0.85, max_radius * 0.85)
        painter.setBrush(QtGui.QColor(255, 95, 162, 26 + int(28 * pulse)))
        painter.drawEllipse(center, max_radius * 0.48, max_radius * 0.48)

        colors = [
            QtGui.QColor("#42e8ff"),
            QtGui.QColor("#59ffcf"),
            QtGui.QColor("#84ff72"),
            QtGui.QColor("#ffd166"),
            QtGui.QColor("#ff9f5c"),
            QtGui.QColor("#ff62a5"),
        ]
        points = []
        for i, value in enumerate(self.values):
            angle = math.radians(-90 + i * 60)
            radius = max_radius * (0.35 + 0.6 * (value / base if base else 0.0))
            x = center.x() + math.cos(angle) * radius
            y = center.y() + math.sin(angle) * radius
            p = QtCore.QPointF(x, y)
            points.append(p)
            painter.setPen(QtGui.QPen(colors[i], 3))
            painter.drawLine(center, p)
            painter.setBrush(colors[i])
            painter.drawEllipse(p, 5, 5)

        poly = QtGui.QPolygonF(points)
        painter.setPen(QtGui.QPen(QtGui.QColor("#d9ecff"), 1.2))
        painter.setBrush(QtGui.QColor(67, 231, 255, 34 + int(58 * pulse)))
        painter.drawPolygon(poly)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.reader = NIAReader()
        self.language_code = "en"
        self._band_values = [0.0] * 6
        self._last_features: Dict[str, float] = {}
        self._last_probe_summary = ""

        self.setWindowTitle("NIA Conversation Reaction Lab")
        self.resize(1460, 950)
        self._build_ui()
        self._apply_style()
        self.retranslate()

        self.refresh_timer = QtCore.QTimer(self)
        self.refresh_timer.setInterval(33)
        self.refresh_timer.timeout.connect(self.refresh)
        self.refresh_timer.start()

        self.probe_timer = QtCore.QTimer(self)
        self.probe_timer.setInterval(1250)
        self.probe_timer.timeout.connect(self.update_probe_status)
        self.probe_timer.start()
        self.update_probe_status()

    def tr(self, key: str) -> str:
        return TRANSLATIONS[self.language_code].get(key, key)

    def _build_ui(self) -> None:
        root = QtWidgets.QWidget()
        self.setCentralWidget(root)
        outer = QtWidgets.QVBoxLayout(root)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(12)

        header = QtWidgets.QFrame()
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(18, 12, 18, 12)
        header_layout.setSpacing(12)

        title_box = QtWidgets.QVBoxLayout()
        self.title_label = QtWidgets.QLabel()
        self.title_label.setObjectName("TitleLabel")
        self.subtitle_label = QtWidgets.QLabel()
        self.subtitle_label.setObjectName("SubtitleLabel")
        self.help_label = QtWidgets.QLabel()
        self.help_label.setObjectName("SubtitleLabel")
        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)
        title_box.addWidget(self.help_label)
        header_layout.addLayout(title_box, 1)

        self.language_caption = QtWidgets.QLabel()
        self.language_combo = QtWidgets.QComboBox()
        for code, label in LANG_LABELS.items():
            self.language_combo.addItem(label, code)
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)

        self.backend_caption = QtWidgets.QLabel()
        self.backend_combo = QtWidgets.QComboBox()
        self.backend_combo.addItems(["Auto", "HID", "PyUSB"])
        self.backend_combo.setMinimumWidth(110)

        self.connect_btn = QtWidgets.QPushButton()
        self.connect_btn.clicked.connect(self.toggle_connection)
        self.capture_btn = QtWidgets.QPushButton()
        self.capture_btn.clicked.connect(self.capture_bundle)
        self.marker_btn = QtWidgets.QPushButton()
        self.marker_btn.clicked.connect(self.add_marker)
        self.clear_btn = QtWidgets.QPushButton()
        self.clear_btn.clicked.connect(self.clear_notes)

        controls = QtWidgets.QVBoxLayout()
        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(self.language_caption)
        row1.addWidget(self.language_combo)
        row1.addSpacing(8)
        row1.addWidget(self.backend_caption)
        row1.addWidget(self.backend_combo)
        row1.addSpacing(8)
        row1.addWidget(self.connect_btn)
        row1.addWidget(self.marker_btn)
        row1.addWidget(self.capture_btn)
        row1.addWidget(self.clear_btn)
        controls.addLayout(row1)

        row2 = QtWidgets.QHBoxLayout()
        self.status_chip = QtWidgets.QLabel()
        self.status_chip.setObjectName("StatusChip")
        self.probe_label = QtWidgets.QLabel()
        self.probe_label.setObjectName("ProbeLabel")
        self.error_label = QtWidgets.QLabel("")
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.setWordWrap(True)
        row2.addWidget(self.status_chip)
        row2.addWidget(self.probe_label, 1)
        row2.addWidget(self.error_label, 2)
        controls.addLayout(row2)
        header_layout.addLayout(controls)
        outer.addWidget(header)

        metrics = QtWidgets.QHBoxLayout()
        metrics.setSpacing(12)
        self.metric_captions: Dict[str, QtWidgets.QLabel] = {}
        self.metric_values: Dict[str, QtWidgets.QLabel] = {}
        for key in ["backend", "packets_s", "samples_s", "packets", "samples", "rms", "peak"]:
            card = self.make_metric_card(key)
            metrics.addWidget(card)
        outer.addLayout(metrics)

        body = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        outer.addWidget(body, 1)

        left = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        self.wave_plot = pg.PlotWidget()
        self.wave_plot.setBackground((0, 0, 0, 0))
        self.wave_plot.showGrid(x=True, y=True, alpha=0.18)
        self.wave_plot.setMenuEnabled(False)
        self.wave_plot.setMouseEnabled(x=False, y=False)
        self.wave_plot.addLegend(offset=(10, 10))
        self.wave_curve = self.wave_plot.plot(pen=pg.mkPen("#43e7ff", width=2.1), name="Signal")

        self.fft_plot = pg.PlotWidget()
        self.fft_plot.setBackground((0, 0, 0, 0))
        self.fft_plot.showGrid(x=True, y=True, alpha=0.18)
        self.fft_plot.setMenuEnabled(False)
        self.fft_plot.setMouseEnabled(x=False, y=False)
        self.fft_plot.setXRange(0, 40)
        self.fft_curve = self.fft_plot.plot(pen=pg.mkPen("#ff5fa2", width=2.0))

        self.bands_widget = BandsWidget()
        self.aura_widget = AuraWidget()

        lower_grid = QtWidgets.QGridLayout()
        lower_grid.setSpacing(12)
        lower_grid.addWidget(self.wrap_panel("panel_spectrum", self.fft_plot), 0, 0)
        lower_grid.addWidget(self.wrap_panel("panel_aura", self.aura_widget), 0, 1)
        lower_grid.addWidget(self.wrap_panel("panel_bands", self.bands_widget), 1, 0, 1, 2)

        left_layout.addWidget(self.wrap_panel("panel_wave", self.wave_plot), 3)
        left_layout.addLayout(lower_grid, 2)

        right = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        notes_panel = QtWidgets.QFrame()
        notes_panel.setObjectName("Panel")
        notes_layout = QtWidgets.QVBoxLayout(notes_panel)
        notes_layout.setContentsMargins(14, 12, 14, 12)
        self.notes_title = QtWidgets.QLabel()
        self.notes_title.setObjectName("PanelTitle")
        notes_layout.addWidget(self.notes_title)

        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignLeft)
        form.setContentsMargins(0, 4, 0, 0)
        self.session_caption = QtWidgets.QLabel()
        self.session_edit = QtWidgets.QLineEdit("default-session")
        self.prompt_caption = QtWidgets.QLabel()
        self.prompt_edit = QtWidgets.QPlainTextEdit()
        self.prompt_edit.setMinimumHeight(105)
        self.reply_caption = QtWidgets.QLabel()
        self.reply_edit = QtWidgets.QPlainTextEdit()
        self.reply_edit.setMinimumHeight(120)
        self.tag_caption = QtWidgets.QLabel()
        self.tag_edit = QtWidgets.QLineEdit()
        self.notes_caption = QtWidgets.QLabel()
        self.notes_edit = QtWidgets.QPlainTextEdit()
        self.notes_edit.setMinimumHeight(95)
        self.path_caption = QtWidgets.QLabel()
        self.path_label = QtWidgets.QLabel(str(EXPORT_ROOT))
        self.path_label.setWordWrap(True)
        self.open_export_btn = QtWidgets.QPushButton()
        self.open_export_btn.clicked.connect(self.open_export_folder)
        form.addRow(self.session_caption, self.session_edit)
        form.addRow(self.prompt_caption, self.prompt_edit)
        form.addRow(self.reply_caption, self.reply_edit)
        form.addRow(self.tag_caption, self.tag_edit)
        form.addRow(self.notes_caption, self.notes_edit)
        form.addRow(self.path_caption, self.path_label)
        notes_layout.addLayout(form)
        notes_layout.addWidget(self.open_export_btn, 0, QtCore.Qt.AlignRight)

        marker_panel = QtWidgets.QFrame()
        marker_panel.setObjectName("Panel")
        marker_layout = QtWidgets.QVBoxLayout(marker_panel)
        marker_layout.setContentsMargins(14, 12, 14, 12)
        self.markers_title = QtWidgets.QLabel()
        self.markers_title.setObjectName("PanelTitle")
        marker_layout.addWidget(self.markers_title)
        self.marker_list = QtWidgets.QListWidget()
        marker_layout.addWidget(self.marker_list, 1)

        right_layout.addWidget(notes_panel, 3)
        right_layout.addWidget(marker_panel, 2)

        body.addWidget(left)
        body.addWidget(right)
        body.setStretchFactor(0, 3)
        body.setStretchFactor(1, 2)

    def make_metric_card(self, metric_key: str) -> QtWidgets.QFrame:
        frame = QtWidgets.QFrame()
        frame.setObjectName("MetricCard")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(14, 12, 14, 12)
        caption = QtWidgets.QLabel()
        caption.setObjectName("MetricCaption")
        value = QtWidgets.QLabel("–")
        value.setObjectName("MetricValue")
        layout.addWidget(caption)
        layout.addWidget(value)
        self.metric_captions[metric_key] = caption
        self.metric_values[metric_key] = value
        return frame

    def wrap_panel(self, title_key: str, widget: QtWidgets.QWidget) -> QtWidgets.QFrame:
        frame = QtWidgets.QFrame()
        frame.setObjectName("Panel")
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(14, 12, 14, 12)
        title = QtWidgets.QLabel()
        title.setObjectName("PanelTitle")
        title.setProperty("tr_key", title_key)
        layout.addWidget(title)
        layout.addWidget(widget, 1)
        return frame

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background: #0a0f18;
                color: #e5ecff;
                font-family: 'Segoe UI';
                font-size: 10pt;
            }
            QFrame#Panel, QFrame#MetricCard, QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #111827, stop:1 #0b1320);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
            }
            QLabel#TitleLabel {
                font-size: 19pt;
                font-weight: 700;
                color: #f7f9ff;
            }
            QLabel#SubtitleLabel {
                color: #98a6c9;
            }
            QLabel#StatusChip {
                padding: 8px 14px;
                border-radius: 13px;
                background: #2d3648;
                color: #d8e3ff;
                font-weight: 700;
            }
            QLabel#ProbeLabel {
                color: #9cb3d9;
            }
            QLabel#ErrorLabel {
                color: #ffb2c8;
            }
            QLabel#MetricCaption {
                color: #8ea1c8;
                font-size: 9pt;
            }
            QLabel#MetricValue {
                font-size: 16pt;
                font-weight: 700;
                color: #ffffff;
            }
            QLabel#PanelTitle {
                font-size: 11pt;
                font-weight: 700;
                color: #dfe6ff;
                padding-bottom: 4px;
            }
            QLineEdit, QPlainTextEdit, QListWidget, QComboBox {
                background: #0f1726;
                border: 1px solid #344866;
                border-radius: 12px;
                padding: 8px 10px;
            }
            QPushButton {
                background: #17304d;
                border: 1px solid #355a86;
                border-radius: 12px;
                padding: 8px 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #214065;
            }
            QPushButton:pressed {
                background: #132a41;
            }
            QListWidget::item {
                padding: 6px 8px;
            }
            """
        )

    def retranslate(self) -> None:
        self.title_label.setText(self.tr("title"))
        self.subtitle_label.setText(self.tr("subtitle"))
        self.help_label.setText(self.tr("help_line"))
        self.language_caption.setText(self.tr("language") + ":")
        self.backend_caption.setText(self.tr("backend") + ":")
        self.connect_btn.setText(self.tr("disconnect") if self.reader.stats().connected else self.tr("connect"))
        self.capture_btn.setText(self.tr("capture"))
        self.marker_btn.setText(self.tr("mark"))
        self.clear_btn.setText(self.tr("clear"))
        self.notes_title.setText(self.tr("panel_notes"))
        self.markers_title.setText(self.tr("panel_markers"))
        self.session_caption.setText(self.tr("session"))
        self.prompt_caption.setText(self.tr("prompt"))
        self.reply_caption.setText(self.tr("reply"))
        self.tag_caption.setText(self.tr("tag"))
        self.notes_caption.setText(self.tr("notes"))
        self.path_caption.setText(self.tr("save_path"))
        self.open_export_btn.setText(self.tr("export_open"))
        self.prompt_edit.setPlaceholderText(self.tr("placeholder_prompt"))
        self.reply_edit.setPlaceholderText(self.tr("placeholder_reply"))
        self.tag_edit.setPlaceholderText(self.tr("placeholder_tag"))
        self.notes_edit.setPlaceholderText(self.tr("placeholder_notes"))
        if self.marker_list.count() == 0:
            self.marker_list.addItem(self.tr("markers_empty"))
            self.marker_list.item(0).setFlags(QtCore.Qt.NoItemFlags)

        for metric_key, caption in self.metric_captions.items():
            caption.setText(self.tr(f"metric_{metric_key}"))
        for label in self.findChildren(QtWidgets.QLabel, options=QtCore.Qt.FindChildrenRecursively):
            key = label.property("tr_key")
            if key:
                label.setText(self.tr(str(key)))

    def on_language_changed(self) -> None:
        code = self.language_combo.currentData()
        if not code:
            return
        self.language_code = str(code)
        self.retranslate()
        self.update_probe_status()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # noqa: N802
        self.reader.stop()
        super().closeEvent(event)

    def toggle_connection(self) -> None:
        stats = self.reader.stats()
        if stats.connected:
            self.reader.stop()
        else:
            self.reader.start(self.backend_combo.currentText().lower())
        self.retranslate()
        self.update_probe_status()

    def clear_notes(self) -> None:
        self.prompt_edit.clear()
        self.reply_edit.clear()
        self.tag_edit.clear()
        self.notes_edit.clear()

    def open_export_folder(self) -> None:
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(str(EXPORT_ROOT)))

    def add_marker(self) -> None:
        now = datetime.now().strftime("%H:%M:%S")
        text = self.tag_edit.text().strip() or self.tr("marker_added")
        item_text = f"{now} — {text}"
        if self.marker_list.count() == 1 and self.marker_list.item(0).flags() == QtCore.Qt.NoItemFlags:
            self.marker_list.clear()
        self.marker_list.addItem(item_text)
        self.marker_list.scrollToBottom()

    def update_probe_status(self) -> None:
        probe = probe_nia()
        self._last_probe_summary = probe.summary
        if self.reader.stats().connected:
            self.status_chip.setText(self.tr("status_streaming"))
            self.status_chip.setStyleSheet("background:#123927; color:#a5ffd2; padding:8px 14px; border-radius:13px; font-weight:700;")
        elif self.reader.stats().last_error:
            self.status_chip.setText(self.tr("status_error"))
            self.status_chip.setStyleSheet("background:#4a2029; color:#ffcad7; padding:8px 14px; border-radius:13px; font-weight:700;")
        elif probe.found_any:
            self.status_chip.setText(self.tr("status_detected"))
            self.status_chip.setStyleSheet("background:#554210; color:#ffe6a3; padding:8px 14px; border-radius:13px; font-weight:700;")
        else:
            self.status_chip.setText(self.tr("status_missing"))
            self.status_chip.setStyleSheet("background:#2d3648; color:#d8e3ff; padding:8px 14px; border-radius:13px; font-weight:700;")

        probe_text = probe.summary or ""
        if probe.error:
            probe_text = (probe_text + " | " + probe.error).strip(" |")
        self.probe_label.setText(f"{self.tr('device_probe')}: {probe_text}")

    def refresh(self) -> None:
        stats = self.reader.stats()
        self.metric_values["backend"].setText(stats.backend_name)
        self.metric_values["packets_s"].setText(f"{stats.packets_per_second:,.1f}")
        self.metric_values["samples_s"].setText(f"{stats.samples_per_second:,.1f}")
        self.metric_values["packets"].setText(f"{stats.packets:,}")
        self.metric_values["samples"].setText(f"{stats.samples:,}")
        self.error_label.setText(stats.last_error)
        self.connect_btn.setText(self.tr("disconnect") if stats.connected else self.tr("connect"))

        samples = self.reader.get_recent_samples(8192)
        if len(samples) < 64:
            self.wave_curve.setData([])
            self.fft_curve.setData([], [])
            self.bands_widget.set_values([0.0] * 6)
            self.aura_widget.set_values([0.0] * 6)
            self.metric_values["rms"].setText("0.0")
            self.metric_values["peak"].setText("0.0")
            self.update_probe_status()
            return

        arr = np.asarray(samples, dtype=np.float64)
        arr -= np.mean(arr)
        rms = float(np.sqrt(np.mean(arr ** 2)))
        peak = float(np.max(arr) - np.min(arr))
        self.metric_values["rms"].setText(f"{rms:,.1f}")
        self.metric_values["peak"].setText(f"{peak:,.1f}")

        wave = arr
        if len(wave) > 1400:
            step = max(1, len(wave) // 1400)
            wave = wave[::step]
        self.wave_curve.setData(wave)

        sr = stats.samples_per_second if stats.samples_per_second > 100 else 3906.0
        windowed = arr * np.hanning(len(arr))
        spectrum = np.fft.rfft(windowed)
        freqs = np.fft.rfftfreq(len(windowed), d=1.0 / sr)
        mag = np.abs(spectrum)
        mask = freqs <= 40.0
        self.fft_curve.setData(freqs[mask], mag[mask])

        values = []
        band_energy = {}
        for lo, hi in BANDS:
            band_mask = (freqs >= lo) & (freqs < hi)
            val = float(np.mean(mag[band_mask])) if np.any(band_mask) else 0.0
            values.append(val)
            band_energy[f"{lo}-{hi}"] = val
        self._band_values = values
        self.bands_widget.set_values(values)
        self.aura_widget.set_values(values)
        self._last_features = {
            "rms": rms,
            "peak_to_peak": peak,
            "sample_rate_estimate": float(sr),
            **band_energy,
        }
        self.update_probe_status()

    def capture_bundle(self) -> None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session = self.session_edit.text().strip() or "default-session"
        safe_session = "".join(ch if ch.isalnum() or ch in ("-", "_") else "-" for ch in session).strip("-") or "default-session"
        bundle_dir = EXPORT_ROOT / f"{safe_session}_{stamp}"
        try:
            bundle_dir.mkdir(parents=True, exist_ok=False)
            screenshot_path = bundle_dir / "ui_screenshot.png"
            waveform_path = bundle_dir / "waveform.png"
            json_path = bundle_dir / "reaction_bundle.json"
            csv_path = bundle_dir / "samples.csv"
            markers_path = bundle_dir / "markers.txt"

            self.grab().save(str(screenshot_path))
            self.wave_plot.grab().save(str(waveform_path))

            samples = self.reader.get_recent_samples(12000)
            with csv_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["sample_index", "value"])
                for i, value in enumerate(samples):
                    writer.writerow([i, value])

            markers = []
            for i in range(self.marker_list.count()):
                item = self.marker_list.item(i)
                if item.flags() == QtCore.Qt.NoItemFlags:
                    continue
                markers.append(item.text())
            markers_path.write_text("\n".join(markers), encoding="utf-8")

            payload = {
                "bundle_created": datetime.now().isoformat(timespec="seconds"),
                "session_name": session,
                "language": self.language_code,
                "backend_requested": self.backend_combo.currentText(),
                "reader_stats": self.reader.stats().__dict__,
                "device_probe": self._last_probe_summary,
                "prompt": self.prompt_edit.toPlainText().strip(),
                "ai_reply_excerpt": self.reply_edit.toPlainText().strip(),
                "self_tag": self.tag_edit.text().strip(),
                "notes": self.notes_edit.toPlainText().strip(),
                "markers": markers,
                "signal_features": self._last_features,
                "band_values": self._band_values,
                "files": {
                    "ui_screenshot": screenshot_path.name,
                    "waveform": waveform_path.name,
                    "samples_csv": csv_path.name,
                    "markers": markers_path.name,
                },
            }
            json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            QtWidgets.QMessageBox.information(self, self.tr("saved_title"), f"{self.tr('saved')}\n\n{bundle_dir}")
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self, self.tr("saved_error_title"), f"{self.tr('saved_error')}\n\n{exc}")


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("NIA Conversation Reaction Lab")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
