from PyQt5.QtWidgets import QDialog
from classes import ui_util
from classes.app import get_app

app = get_app()


class SettingsDB(QDialog):
    """Окно 'Настройки БД'"""
    def __init__(self):
        QDialog.__init__(self, parent=app.main_window)

        ui_util.load_ui(self, 'settings_db')
        ui_util.init_ui(self)

        self.cmb_driver_name.setCurrentText(app.settings.value("Geometry", ''))
