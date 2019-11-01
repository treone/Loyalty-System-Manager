import hashlib
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox
from classes.app import get_app
from classes.decorators import with_wait_cursor
from classes.logger import log
from classes.utils import decrypt

app = get_app()


def hash_it(string):
    return hashlib.md5(string.encode("utf-8")).hexdigest()


class DatabaseMySQL:
    def __init__(self):
        self.connection = None

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
        )

    def is_open(self):
        return True if self.connection and self.connection.isOpen() else False

    @with_wait_cursor
    def connect(self, settings=None):
        if settings is None:
            settings = self.connection_settings

        self.connection = QSqlDatabase.addDatabase("QMYSQL")
        self.connection.setHostName(settings["host"])
        self.connection.setPort(settings["port"])
        self.connection.setDatabaseName(settings["db"])
        self.connection.setUserName(settings["user"])
        self.connection.setPassword(settings["password"])
        connect = self.connection.open()
        if not connect:
            error = self.connection.lastError().databaseText()
            log.warning(error)
            app.restoreOverrideCursor()
            QMessageBox.critical(app.main_window, "Ошибка!", error, QMessageBox.Close)

    def disconnect_if_needed(self):
        if self.is_open():
            log.info('Закрываем подключение к базе данных')
            self.connection.close()

    def get_user_id(self, login, password):
        hashed_password = hash_it(password)
        query = QSqlQuery()
        query.prepare("""
            SELECT `id` FROM `Person` WHERE 
                `login`    = :login AND 
                `password` = :password AND 
                `deleted`  = 0 AND 
                `retired`  = 0 AND 
                ( `retireDate` IS NULL OR `retireDate` > CURDATE() )
            """)
        query.bindValue(':login', login)
        query.bindValue(':password', hashed_password)
        if query.exec_() and query.size() == 1:
            query.first()
            return query.value('id')
        else:
            return False

    def get_person_fio(self):
        query = QSqlQuery()
        query.prepare("""SELECT `lastName`, `firstName`, `patrName` FROM `Person` WHERE `id` = :id""")
        query.bindValue(':id', app.user_id)
        if query.exec_() and query.first():
            last_name = query.value('lastName') if query.value('firstName') else ''
            first_name = query.value('firstName')[0] + '.' if query.value('firstName') else ''
            patr_name = query.value('patrName')[0] + '.' if query.value('patrName') else ''
            fio = ' '.join([last_name, first_name, patr_name])
            return fio
        else:
            return 'Без имени'
