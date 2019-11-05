from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
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
        result = func(*args, **kwargs)
        return result

    return wrapper


def display_execution_time(func):
    """Декоратор, выводящий время, которое заняло выполнение функции."""
    import time
    def wrapper(*args, **kwargs):

        start_time = time.clock()
        result = func(*args, **kwargs)
        end_time = time.clock()
        execution_time = end_time - start_time
        app.main_window.show_execution_time(execution_time)
        return result

    return wrapper


