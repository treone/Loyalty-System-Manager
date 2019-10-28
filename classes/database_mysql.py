import pymysql
from classes.app import get_app

app = get_app()


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
