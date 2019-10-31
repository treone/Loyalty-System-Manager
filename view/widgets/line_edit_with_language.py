from ctypes import *
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, Qt, QEvent
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget


class LineEditWithLanguage(QLineEdit):
    """QLineEdit, в котором отображается раскладка клавиатуры"""

    def __init__(self, parent):
        QLineEdit.__init__(self, parent=parent)
        self._init_language_detector()
        self.keyboard_layout = get_keyboard_layout()

    def _init_language_detector(self):
        # Инициализация и запуск детектора раскладки клавиатуры
        self.ktd = KeyboardLayoutDetector()
        self.ktd.keyboard_layout_changed.connect(self.language_changed)
        self.ktd.start()

    @pyqtSlot(str)
    def language_changed(self, language):
        # Слот для сигнала о смене раскладки клавиатуры
        self.keyboard_layout = language
        self.repaint()

    def paintEvent(self, event):
        QLineEdit.paintEvent(self, event)
        painter = QPainter()
        painter.begin(self)
        rect = self.rect()
        rect.moveLeft(-8)
        painter.drawText(rect, Qt.AlignVCenter | Qt.AlignRight, self.keyboard_layout)
        painter.end()


class KeyboardLayoutDetector(QtCore.QThread):
    """Отдельный поток для отслеживания измененния раскладки клавиатуры"""
    keyboard_layout_changed = QtCore.pyqtSignal(str)  # Раскладка клавиатуры изменилась

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.running = False
        self.previous_language = get_keyboard_layout()

    def __del__(self):
        self.wait(5000)

    def run(self):
        self.running = True
        while self.running:
            self.msleep(100)
            current_language = get_keyboard_layout()
            if current_language != self.previous_language:
                self.keyboard_layout_changed.emit(current_language)
                self.previous_language = current_language
        self.running = False


class RECT(Structure):
    _fields_ = [
        ("left", c_ulong),
        ("top", c_ulong),
        ("right", c_ulong),
        ("bottom", c_ulong)
    ]


class GUITHREADINFO(Structure):
    _fields_ = [
        ("cbSize", c_ulong),
        ("flags", c_ulong),
        ("hwndActive", c_ulong),
        ("hwndFocus", c_ulong),
        ("hwndCapture", c_ulong),
        ("hwndMenuOwner", c_ulong),
        ("hwndMoveSize", c_ulong),
        ("hwndCaret", c_ulong),
        ("rcCaret", RECT)
    ]


def get_keyboard_layout():
    """Возвращает раскладку клавиатуры"""
    user32 = windll.user32
    russian = 68748313

    gti = GUITHREADINFO(cbSize=sizeof(GUITHREADINFO))
    user32.GetGUIThreadInfo(0, byref(gti))
    dw_thread = user32.GetWindowThreadProcessId(gti.hwndActive, 0)
    language = user32.GetKeyboardLayout(dw_thread)

    return 'РУС' if language == russian else 'EN'
