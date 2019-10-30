from classes.app import get_app
from classes.driver_mysql import DatabaseMySQL
from classes.decorators import with_connection
from classes.logger import log

app = get_app()


class Database:
    def __init__(self):
        self.driver = None
        self.driver_init()

    def driver_init(self):
        driver_name = app.settings.value("settings_db/driver_name", 'mysql')
        if driver_name == 'mysql':
            self.driver = DatabaseMySQL()

    def is_open(self):
        return self.driver.is_open()

    def connect(self):
        log.info('Подключаемся к базе данных')
        self.driver.connect()
        return self.driver.is_open()

    def disconnect(self):
        self.driver.disconnect_if_needed()

    def connection_is_open(self):
        return self.driver.connection is not None

    @with_connection
    def get_user_id(self, login, password):
        """Возвращает ID пользователя или False"""
        return self.driver.get_user_id(login, password)
