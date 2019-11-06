from PyQt5.QtWidgets import QDialog, QMessageBox
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

        login = app.settings.value("registration/login", '')
        if login:
            self.edt_login.setText(login)
            self.edt_password.setFocus()

    def accept(self):
        login = self.edt_login.text()
        password = self.edt_password.text()
        app.settings.setValue("registration/login", login)

        if not app.db.is_open():
            app.db.open()

        if app.db.is_open():
            user_id = app.db.get_user_id(login, password)

            if user_id:
                app.user_is_registered.emit(user_id)
                QDialog.accept(self)
            else:
                log.warning('Введен неправильный логин или пароль')
                self.edt_password.clear()
                self.edt_password.setFocus()
                QMessageBox.critical(self, "Ошибка входа в систему", "Имя пользователя или пароль неверны.",
                                     QMessageBox.Close)
