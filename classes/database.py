from classes.app import get_app
from classes.logger import log

app = get_app()


class Database:
    pass

    def test(self):
        log.info('Тест подключения к базе данных')
