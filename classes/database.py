from classes.app import get_app
from classes.driver_mysql import DatabaseMySQL
from classes.decorators import with_connection
from classes.logger import log

app = get_app()


class Database:
    def __init__(self, driver_name=None):
        self.driver = None
        driver_name = driver_name if driver_name is not None else app.settings.value("settings_db/driver_name", 'mysql')
        self.driver_init(driver_name)

    def driver_init(self, driver_name):
        if driver_name == 'mysql':
            self.driver = DatabaseMySQL()

    @property
    def connection_settings(self):
        """Возвращает настройки соединения"""
        return self.driver.connection_settings

    def is_open(self):
        return self.driver.is_open()

    def connect(self, settings=None):
        """Подключиться к базе данных"""
        log.info('Подключаемся к базе данных')
        self.driver.connect(settings)
        return self.driver.is_open()

    def disconnect(self):
        self.driver.disconnect_if_needed()

    def connection_is_open(self):
        return self.driver.connection is not None

    @with_connection
    def get_user_id(self, login, password):
        """Возвращает ID пользователя или False"""
        return self.driver.get_user_id(login, password)
