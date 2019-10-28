from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QDialog
from classes import ui_util
from classes.app import get_app

app = get_app()


class License(QDialog):
    """Окно 'Лицензия'"""
    def __init__(self):
        QDialog.__init__(self, parent=app.main_window)

        ui_util.load_ui(self, 'license')
        ui_util.init_ui(self)

        # Инициализация лицензии
        license_file = QFile(':/license.txt')
        license_file.open(QFile.ReadOnly)
        license_text = bytes(license_file.readAll()).decode('UTF-8')
        self.text_browser.setText(license_text)
        license_file.close()

        # Прокручиваем текст в начало документа
        cursor = self.text_browser.textCursor()
        cursor.setPosition(0)
        self.text_browser.setTextCursor(cursor)
