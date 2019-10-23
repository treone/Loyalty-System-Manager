from classes.logger import log


def exception_handler(exception_type, exception_value, exception_traceback):
    """Обработчик для всех необработанных исключений"""
    log.error('Необработанное Исключение', exc_info=(exception_type, exception_value, exception_traceback))
