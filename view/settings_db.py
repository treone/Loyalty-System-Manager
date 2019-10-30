from PyQt5.QtWidgets import QDialog
from classes import ui_util
from classes.app import get_app
from classes.logger import log

app = get_app()
drivers = ['mysql']


class SettingsDB(QDialog):
    """Окно 'Настройки БД'"""
    def __init__(self):
        QDialog.__init__(self, parent=app.main_window)
        ui_util.load_ui(self, 'settings_db')
        ui_util.init_ui(self)

        self._fill_settings_fields()

    def save_settings(self):
        log.info("Сохранение настроек подключения к БД.")
        app.settings.setValue("settings_db/driver_name", self._driver_name())
        app.settings.setValue("settings_db/server_name", self.edt_server_name.text())
        app.settings.setValue("settings_db/server_port", self.edt_server_port.value())
        app.settings.setValue("settings_db/database_name", self.edt_database_name.text())
        app.settings.setValue("settings_db/user_name", self.edt_user_name.text())
        app.settings.setValue("settings_db/edt_user_password", self.edt_user_password.text())

    def _driver_name(self):
        driver_index = self.cmb_driver_name.currentIndex()
        return drivers[driver_index]

    def _fill_settings_fields(self):
        # Заполняет поля диалогового окна значениями из настроек
        try:
            self._set_driver_name(app.settings.value("settings_db/driver_name", 'mysql'))
            self.edt_server_name.setText(app.settings.value("settings_db/server_name", 'localhost'))
            self.edt_server_port.setValue(app.settings.value("settings_db/server_port", 3306))
            self.edt_database_name.setText(app.settings.value("settings_db/database_name", ''))
            self.edt_user_name.setText(app.settings.value("settings_db/user_name", ''))
            self.edt_user_password.setText(app.settings.value("settings_db/edt_user_password", ''))
        except TypeError:
            log.error("Ошибка в сохраненных настройках подключения к БД.")

    def _set_driver_name(self, driver_name):
        driver_index = drivers.index(driver_name) if driver_name in drivers else 0
        self.cmb_driver_name.setCurrentIndex(driver_index)
