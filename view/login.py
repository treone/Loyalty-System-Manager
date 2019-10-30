from PyQt5.QtWidgets import QDialog
from classes import ui_util
from classes.app import get_app
from classes.logger import log

app = get_app()


class Login(QDialog):
    """Окно 'Регистрация в системе'"""
    def __init__(self):
        QDialog.__init__(self, parent=app.main_window)
        ui_util.load_ui(self, 'login')
        ui_util.init_ui(self)

        self.edt_login.setText(app.settings.value("registration/login", ''))

    def accept(self):
        login = self.edt_login.text()
        password = self.edt_password.text()
        QDialog.accept(self)
