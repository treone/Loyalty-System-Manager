import sys

try:
    from classes import constants
    print("Загрузка модулей из текущего каталога: %s" % constants.PATH)
except ImportError:
    if hasattr(sys, "_MEIPASS"):
        sys.path.append(sys._MEIPASS)
    from classes import constants
    print("Загрузка модулей из каталога установки: %s" % constants.PATH)


from classes.app import App


if __name__ == "__main__":
    # Запуск основного потока
    app = App(sys.argv)
    sys.exit(app.run())
