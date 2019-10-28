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

    def test(self):
        log.info('Тест подключения к базе данных')
        self.connect()
        if self.driver.connection:
            try:
                with self.driver.connection.cursor() as cursor:
                    sql = "SELECT `id`, `password` FROM `Person` WHERE `login`=%s"
                    cursor.execute(sql, ('админ',))
                    result = cursor.fetchone()
                    print(result)
            finally:
                self.driver.connection.close()
