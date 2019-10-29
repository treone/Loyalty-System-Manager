import hashlib

import pymysql
from classes.app import get_app

app = get_app()


def hash_it(string):
    return hashlib.md5(string.encode("utf-8")).hexdigest()


class DatabaseMySQL:
    def __init__(self):
        self.connection = None

    @property
    def connection_settings(self):
        return dict(
            host=app.settings.value("settings_db/server_name", 'localhost'),
            port=app.settings.value("settings_db/server_port", 3306),
            db=app.settings.value("settings_db/database_name", ''),
            user=app.settings.value("settings_db/user_name", ''),
            password=app.settings.value("settings_db/edt_user_password", ''),
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
        )

    def connect(self):
        self.connection = pymysql.connect(**self.connection_settings)

    def user_log_in(self, login, password):
        self.connect()
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    hashed_password = hash_it(password)
                    sql = f"""
                        SELECT `id` FROM `Person` WHERE 
                            `login`    = %s AND 
                            `password` = %s AND 
                            `deleted`  = 0 AND 
                            `retired`  = 0 AND 
                            ( `retireDate` IS NULL OR `retireDate` > CURDATE() )
                    """
                    cursor.execute(sql, (login, hashed_password))
                    result = cursor.fetchone()
                    return bool(result)
            finally:
                self.connection.close()
        else:
            return False
