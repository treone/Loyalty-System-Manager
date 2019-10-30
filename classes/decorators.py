from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMessageBox

from classes.app import get_app

app = get_app()


def with_wait_cursor(func):
    """Сменить курсор на 'Ожидающий' на время выполнения функции."""

    def wrapper(*args, **kwargs):
        app.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            return func(*args, **kwargs)
        finally:
            app.restoreOverrideCursor()

    return wrapper


def with_connection(func):
    """Выполнять функцию необходимо при подключении к базе данных."""
    def wrapper(*args, **kwargs):
        if not app.db.is_open():
            success = app.db.connect()
            if not success:
                return False
        return func(*args, **kwargs)

    return wrapper
