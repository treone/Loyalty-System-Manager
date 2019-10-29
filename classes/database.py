from classes.app import get_app
from classes.logger import log
from classes.database_mysql import DatabaseMySQL

app = get_app()


class Database:
    def __init__(self):
        driver_name = app.settings.value("settings_db/driver_name", 'mysql')
        self.driver = None
        if driver_name == 'mysql':
            self.driver = DatabaseMySQL()

    def connect(self):
        self.driver.connect()

    def user_log_in(self, login, password):
        return self.driver.user_log_in(login, password)

    def test(self):
        log.info('Тест подключения к базе данных')
        print(self.user_log_in('Админ', '123qwe'))
