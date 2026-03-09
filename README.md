# NIA Conversation Reaction Lab


## English

### What this app is
This application is a small Windows tool for people who still own an **OCZ Neural Impulse Actuator (NIA)** and want to view the incoming signal in real time while talking to an AI. It is meant as a practical reaction log: the signal can be watched, marked at important moments, and saved together with the current conversation context.

### What you need
You need Windows 10 or Windows 11, a working OCZ NIA, Python 3, and permission to install the required Python packages. In some systems the device may already be readable as HID. If not, the included WinUSB driver template can be used as a starting point.

### How to use it
Connect the NIA, start `app\run_windows.bat`, and wait until the window appears. The app shows whether the device is detected or not. Press **Connect** to start reading. Enter the conversation situation, the relevant AI reply, and optional personal notes. When something in the conversation causes a visible inner reaction, press **Add marker**. When you want to keep that moment, press **Capture reaction bundle**. The app saves a screenshot, the current waveform, the recent raw samples, the markers, and a JSON file with the text context.

### What the project is for
The goal is not medical diagnosis and not mind reading. The goal is to keep a structured record of human reactions during AI conversations so that later analysis can compare language, timing, and signal changes.

Note: Early Beta Version (use on your own risk!)

<img width="700" height="478" alt="Interface" src="https://github.com/user-attachments/assets/c95ff0bb-db06-48f0-a716-3099ddcca23e" />

<img width="908" height="478" alt="NIA" src="https://github.com/user-attachments/assets/babac22e-b591-44e7-8ff5-5836008bfe38" />

---

## Deutsch

### Wozu die App da ist
Diese Anwendung ist ein kleines Windows-Werkzeug für Menschen, die noch einen **OCZ Neural Impulse Actuator (NIA)** besitzen und das ankommende Signal während eines Gesprächs mit einer KI in Echtzeit sehen möchten. Sie ist als praktisches Reaktionsprotokoll gedacht: Das Signal kann beobachtet, an wichtigen Stellen markiert und zusammen mit dem Gesprächskontext gespeichert werden.

### Was man benötigt
Benötigt werden Windows 10 oder Windows 11, ein funktionierender OCZ NIA, Python 3 und die Möglichkeit, die nötigen Python-Pakete zu installieren. Auf manchen Systemen lässt sich das Gerät bereits direkt als HID lesen. Falls nicht, liegt eine WinUSB-Treibervorlage als Ausgangsbasis bei.

### Bedienung
NIA anschließen, `app\run_windows.bat` starten und warten, bis das Fenster erscheint. Die App zeigt an, ob das Gerät erkannt wurde oder nicht. Mit **Verbinden** beginnt das Einlesen. Danach können Gesprächssituation, relevanter KI-Antwortauszug und optionale Notizen eingetragen werden. Wenn im Gespräch eine spürbare innere Reaktion auftritt, wird mit **Marker setzen** eine Stelle markiert. Mit **Reaktionspaket speichern** werden Screenshot, Wellenform, aktuelle Rohdaten, Marker und eine JSON-Datei mit dem Gesprächskontext gesichert.

### Worum es dabei geht
Das Projekt ist nicht für medizinische Diagnosen gedacht und nicht zum Gedankenlesen. Es soll einen strukturierten Mitschnitt menschlicher Reaktionen in KI-Gesprächen liefern, damit später Sprache, Zeitpunkt und Signalveränderungen miteinander verglichen werden können.

---

## Français

### À quoi sert l'application
Cette application est un petit outil Windows destiné aux personnes qui possèdent encore un **OCZ Neural Impulse Actuator (NIA)** et souhaitent voir le signal reçu en temps réel pendant une conversation avec une IA. Elle sert de journal de réaction pratique : le signal peut être observé, marqué à des moments importants et enregistré avec le contexte de la conversation.

### Ce qu'il faut
Il faut Windows 10 ou Windows 11, un OCZ NIA fonctionnel, Python 3 et la possibilité d'installer les paquets Python nécessaires. Sur certains systèmes, l'appareil peut déjà être lu en HID. Sinon, le modèle de pilote WinUSB fourni peut servir de base.

### Utilisation
Branchez le NIA, lancez `app\run_windows.bat`, puis attendez l'ouverture de la fenêtre. L'application indique si l'appareil est détecté ou non. Appuyez sur **Connecter** pour commencer la lecture. Saisissez ensuite la situation de la conversation, l'extrait pertinent de la réponse de l'IA et d'éventuelles notes personnelles. Quand un passage du dialogue provoque une réaction intérieure visible, utilisez **Ajouter un marqueur**. Quand vous voulez conserver ce moment, utilisez **Enregistrer le paquet de réaction**. L'application enregistre une capture d'écran, la forme d'onde, les derniers échantillons bruts, les marqueurs et un fichier JSON avec le contexte textuel.

### But du projet
Le but n'est ni le diagnostic médical ni la lecture des pensées. Le but est de conserver une trace structurée des réactions humaines pendant des conversations avec une IA afin de comparer ensuite le langage, le moment et les variations du signal.

---

## 简体中文

### 这个程序是做什么的
这个程序是一个小型 Windows 工具，面向仍然拥有 **OCZ Neural Impulse Actuator (NIA)** 的用户，用来在与 AI 对话时实时查看设备传来的信号。它的定位是“反应记录器”：你可以观察信号、在重要时刻打标记，并把这些内容和对话上下文一起保存。

### 需要什么
需要 Windows 10 或 Windows 11、一台可工作的 OCZ NIA、Python 3，以及安装所需 Python 包的权限。在某些系统中，设备可能已经可以通过 HID 直接读取。如果不行，压缩包里附带了一个 WinUSB 驱动模板作为起点。

### 如何使用
连接 NIA，运行 `app\run_windows.bat`，等待窗口出现。程序会显示设备是否被检测到。点击 **连接** 开始读取。随后填写当时的对话情境、相关的 AI 回复片段，以及可选的个人备注。当对话中的某一段引发了明显的内在反应时，点击 **添加标记**。当你想把这个时刻保存下来时，点击 **保存反应包**。程序会保存界面截图、波形图、最近的原始采样、标记列表，以及带有文本上下文的 JSON 文件。

### 这个项目的目的
它不是医疗诊断工具，也不是读心术。它的目的，是为人与 AI 对话时的反应建立结构化记录，方便之后把语言内容、时间点和信号变化放在一起分析。

---

## Русский

### Что это за приложение
Это небольшая программа для Windows для тех, у кого ещё есть **OCZ Neural Impulse Actuator (NIA)** и кто хочет видеть поступающий сигнал в реальном времени во время разговора с ИИ. Приложение задумано как практический журнал реакции: сигнал можно наблюдать, отмечать важные моменты и сохранять вместе с контекстом разговора.

### Что нужно
Нужны Windows 10 или Windows 11, рабочий OCZ NIA, Python 3 и возможность установить необходимые Python-пакеты. На некоторых системах устройство уже читается как HID. Если нет, в архиве есть шаблон WinUSB-драйвера как отправная точка.

### Как пользоваться
Подключите NIA, запустите `app\run_windows.bat` и дождитесь появления окна. Программа показывает, обнаружено устройство или нет. Нажмите **Подключить**, чтобы начать чтение. Затем введите ситуацию разговора, нужный фрагмент ответа ИИ и при желании личные заметки. Когда какой-то момент диалога вызывает заметную внутреннюю реакцию, нажмите **Добавить маркер**. Когда вы хотите сохранить этот момент, нажмите **Сохранить пакет реакции**. Программа сохранит снимок окна, форму сигнала, последние сырые сэмплы, список маркеров и JSON-файл с текстовым контекстом.

### Для чего нужен проект
Это не медицинская диагностика и не чтение мыслей. Задача проекта — сохранять структурированные записи человеческих реакций во время разговоров с ИИ, чтобы потом можно было сопоставлять текст, момент реакции и изменения сигнала.
