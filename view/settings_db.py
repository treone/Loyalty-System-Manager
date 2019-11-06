from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox
from classes import ui_util
from classes.app import get_app
from classes.database import Database
from classes.logger import log
from classes.utils import encrypt, decrypt

app = get_app()
dbms = ['QMYSQL', 'QPSQL']


class SettingsDB(QDialog):
    """Окно 'Настройки БД'"""
    def __init__(self):
        QDialog.__init__(self, parent=app.main_window)
        ui_util.load_ui(self, 'settings_db')
        ui_util.init_ui(self)

        self._fill_settings_fields()

    def save_settings(self):
        log.info("Сохранение настроек подключения к БД.")
        app.settings.setValue("settings_db/dbms", self._dbms())
        app.settings.setValue("settings_db/server_name", self.edt_server_name.text())
        app.settings.setValue("settings_db/server_port", self.edt_server_port.value())
        app.settings.setValue("settings_db/database_name", self.edt_database_name.text())
        app.settings.setValue("settings_db/user_name", self.edt_user_name.text())
        password = self.edt_user_password.text()
        encrypted_password = encrypt(password)
        app.settings.setValue("settings_db/edt_user_password", encrypted_password)

    def _dbms(self):
        driver_index = self.cmb_dbms.currentIndex()
        return dbms[driver_index]

    def _fill_settings_fields(self):
        # Заполняет поля диалогового окна значениями из настроек
        try:
            self._set_dbms(app.settings.value("settings_db/dbms", 'QMYSQL'))
            self.edt_server_name.setText(app.settings.value("settings_db/server_name", 'localhost'))
            self.edt_server_port.setValue(app.settings.value("settings_db/server_port", 3306))
            self.edt_database_name.setText(app.settings.value("settings_db/database_name", ''))
            self.edt_user_name.setText(app.settings.value("settings_db/user_name", ''))
            password = app.settings.value("settings_db/edt_user_password", None)
            if password:
                decrypted_password = decrypt(password)
                self.edt_user_password.setText(decrypted_password)
        except TypeError:
            log.error("Ошибка в сохраненных настройках подключения к БД.")

    def _set_dbms(self, dbms):
        driver_index = dbms.index(dbms) if dbms in dbms else 0
        self.cmb_dbms.setCurrentIndex(driver_index)

    @pyqtSlot()
    def btn_check_click(self):
        settings = dict(
            dbms=self._dbms(),
            host=self.edt_server_name.text(),
            port=self.edt_server_port.value(),
            db=self.edt_database_name.text(),
            user=self.edt_user_name.text(),
            password=self.edt_user_password.text(),
        )
        db = Database()
        db.open(settings=settings)
        if db.is_open():
            QMessageBox.information(self, "Успех!", "Соединение успешно установлено.", QMessageBox.Close)
