import os
import time
import xml.etree.ElementTree
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic
from classes.app import get_app
from classes.constants import PATH
from classes.logger import log

DEFAULT_THEME_NAME = "Material"


def load_ui(window, ui_name):
    """Загружаем *.ui файл, а также XML версию файла"""
    # Пытаемся загрузить UI файл 5 раз
    # Этот хак пытается избежать распространенной ошибки, которая может возникнуть из за состояния гонки.
    # [zipimport.ZipImportError: can't decompress data; zlib not available]
    # Эта ошибка возникает только при использовании cx_Freeze для запуска приложения.

    path = os.path.join(PATH, 'view', 'ui', ui_name + '.ui')
    error = None
    for attempt in range(1, 6):
        try:
            # Загрузка UI из файла
            uic.loadUi(path, window)
            # UI файл успешно загружен, поэтому очищаем все ранее обнаруженные ошибки
            error = None
            break
        except Exception as ex:
            # Следим за ошибкой
            error = ex
            time.sleep(0.1)

    # Возбуждаем ошибку, если есть
    if error:
        raise error

    # Сохраняем XML дерево для дальнейшего анализа
    window.uiTree = xml.etree.ElementTree.parse(path)


def init_element(window, elem):
    """Инициализировать иконки элемента"""
    name = ''
    if hasattr(elem, 'objectName'):
        name = elem.objectName()
        connect_auto_events(window, elem, name)

    # Установить иконку, если возможно
    if hasattr(elem, 'setIcon') and name != '':  # Есть своя иконка
        setup_icon(window, elem, name)


def setup_icon(window, elem, name, theme_name=None):
    """Используя xml окна, установить значок для данного элемента. Если передано имя темы, загрузить значок из нее"""
    type_filter = 'action'
    if isinstance(elem, QWidget):  # Поиск виджета с именем вместо этого
        type_filter = 'widget'
    # Найти набор иконок в дереве (если есть)
    iconset = window.uiTree.find('.//' + type_filter + '[@name="' + name + '"]/property[@name="icon"]/iconset')
    if iconset is not None or theme_name:
        if not theme_name:
            theme_name = iconset.get('theme', '')
        # Получить иконку (текущая тема или версия по умолчанию)
        icon = get_icon(theme_name)
        if icon:
            elem.setIcon(icon)


def get_icon(theme_name):
    """Получить либо иконку от текущей темы, либо версию по умолчанию (для пользовательских значков).
    Возвращает None если ничего не найдено или пустое имя."""
    if theme_name:
        has_icon = QIcon.hasThemeIcon(theme_name)
        fallback_icon, fallback_path = get_default_icon(theme_name)
        if has_icon or fallback_icon:
            return QIcon.fromTheme(theme_name, fallback_icon)
    return None


def get_default_icon(theme_name):
    """Возвращает QIcon или QIcon по умолчанию, если ОС не поддерживает темы"""
    start_path = ":/icons/" + DEFAULT_THEME_NAME + "/"
    icon_path = search_dir(start_path, theme_name)
    return QIcon(icon_path), icon_path


def search_dir(base_path, theme_name):
    """Поиск названия темы"""
    # Поиск по каждой записи в каталоге
    base_dir = QDir(base_path)
    for e in base_dir.entryList():
        # Путь к текущему элементу
        path = base_dir.path() + "/" + e
        base_filename = e.split('.')[0]

        # Если файл соответствует имени темы, возвращаем
        if base_filename == theme_name:
            return path

        # Если это каталог, выполняем поиск в нем
        inner_dir = QDir(path)
        if inner_dir.exists():
            res = search_dir(path, theme_name)
            if res:
                return res
    # Если совпадений не найдено, возвращаем None
    return None


def connect_auto_events(window, elem, name):
    """Соединить все евенты в *.ui файлах с соответствующими именами методов"""
    # Проверить все слоты
    if hasattr(elem, 'trigger'):
        func_name = name + "_trigger"
        if hasattr(window, func_name) and callable(getattr(window, func_name)):
            elem.triggered.connect(getattr(window, func_name))
    if hasattr(elem, 'click'):
        func_name = name + "_click"
        if hasattr(window, func_name) and callable(getattr(window, func_name)):
            elem.clicked.connect(getattr(window, func_name))


def init_ui(window):
    """Инициализация всех дочерних виджетов и экшенов окна"""
    log.info('Инициализация пользовательского интерфейса для {} ({})'.format(window.objectName(), window.windowTitle()))

    try:
        if hasattr(window, 'setWindowTitle') and window.windowTitle() != "":
            window.setWindowTitle(window.windowTitle())
            # Центрирование окна
            center(window)

        # Обходим все виджеты
        for widget in window.findChildren(QWidget):
            init_element(window, widget)

        # Обходим все экшены
        for action in window.findChildren(QAction):
            init_element(window, action)
    except:
        log.error('Не удалось инициализировать элемент в {}'.format(window.objectName()))


def center(window):
    """Центрирование виджета"""
    log.info('Центрирование окна "{}"'.format(window.windowTitle()))
    frame_gm = window.frameGeometry()
    center_point = get_app().main_window.frameGeometry().center()
    frame_gm.moveCenter(center_point)
    window.move(frame_gm.topLeft())
