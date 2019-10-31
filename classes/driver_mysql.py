import hashlib
import pymysql
from PyQt5.QtWidgets import QMessageBox

from classes.app import get_app
from classes.logger import log
from classes.utils import decrypt

app = get_app()


def hash_it(string):
    return hashlib.md5(string.encode("utf-8")).hexdigest()


class DatabaseMySQL:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __del__(self):
        self.disconnect_if_needed()

    @property
    def connection_settings(self):
        password = app.settings.value("settings_db/edt_user_password", None)
        decrypted_password = decrypt(password) if password else ''
        return dict(
            host=app.settings.value("settings_db/server_name", 'localhost'),
            port=app.settings.value("settings_db/server_port", 3306),
            db=app.settings.value("settings_db/database_name", ''),
            user=app.settings.value("settings_db/user_name", ''),
            password=decrypted_password,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
        )

    def is_open(self):
        return True if self.connection and self.connection.open else False

    def connect(self):
        try:
            self.connection = pymysql.connect(**self.connection_settings)
            self.cursor = self.connection.cursor()
        except pymysql.err.OperationalError as e:
            log.warning(f'При подключении к базе данных возникла ошибка\n'
                        f'{" "*21}{e.args[1]}\n'
                        f'{" "*21}Код ошибки: {e.args[0]}')
            QMessageBox.critical(app.main_window, "Ошибка!", f"{e.args[1]}", QMessageBox.Close)
            print(e)

    def disconnect_if_needed(self):
        if self.is_open():
            log.info('Закрываем подключение к базе данных')
            self.connection.close()

    def get_user_id(self, login, password):
        self.connect()
        if self.connection:
            with self.connection:
                cursor = self.connection.cursor()
                hashed_password = hash_it(password)
                sql = f"""
                    SELECT `id` FROM `Person` WHERE 
                        `login`    = %s AND 
                        `password` = %s AND 
                        `deleted`  = 0 AND 
                        `retired`  = 0 AND 
                        ( `retireDate` IS NULL OR `retireDate` > CURDATE() )
                """
                rows = cursor.execute(sql, (login, hashed_password))
                # Подходящая запись в базе должна быть одна и только одна
                if rows != 1:
                    return False
                result = cursor.fetchone()
                return result.get('id', False)
        else:
            return False
