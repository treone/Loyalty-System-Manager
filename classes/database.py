import hashlib

from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

from classes.app import get_app
from classes.decorators import with_connection, with_wait_cursor
from classes.logger import log
from classes.utils import get_connection_settings

app = get_app()


class Database:
    def __init__(self):
        self.connection = QtSql.QSqlDatabase()

    @with_wait_cursor
    def open(self, settings=None, show_errors=True):
        """Открыть соединение с БД"""
        if self.is_open():
            self.close()
        if settings is None:
            settings = get_connection_settings()
        log.info('Подключаемся к базе данных')
        self.connection = QtSql.QSqlDatabase.addDatabase(settings["dbms"])
        self.connection.setHostName(settings["host"])
        self.connection.setPort(settings["port"])
        self.connection.setDatabaseName(settings["db"])
        self.connection.setUserName(settings["user"])
        self.connection.setPassword(settings["password"])
        ok = self.connection.open()
        if ok:
            return True
        else:
            error = (f'Database: {self.connection.lastError().databaseText()}\n'
                     f'Driver: {self.connection.lastError().driverText()}')
            log.warning(error)
            if show_errors:
                app.restoreOverrideCursor()
                QMessageBox.critical(app.main_window, "Ошибка!", error, QMessageBox.Close)
            return False

    def is_open(self):
        """Открыто ли соединение с БД"""
        return True if self.connection and self.connection.isOpen() else False

    def close(self):
        """Закрыть соединение с БД"""
        if self.is_open():
            log.info('Закрываем подключение к базе данных')
            self.connection.close()

    def get_user_id(self, login, password):
        """Возвращает ID пользователя или False"""
        hashed_password = hashlib.md5(password.encode("utf-8")).hexdigest()  # Пароли в базе хранятся в виде MD5 хэшей
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
        """Получение Фамилии И.О. пользователя"""
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
