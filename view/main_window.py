import webbrowser
from PyQt5.QtCore import Qt, QByteArray, pyqtSlot, pyqtSignal, QTranslator
from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QSizePolicy, QWidget, QToolButton
from classes import ui_util, constants
from classes.app import get_app
from classes.logger import log
from classes.version import get_current_version

app = get_app()


class MainWindow(QMainWindow):
    """Главное окно"""
    found_version_signal = pyqtSignal(str)

    def __init__(self):
        QMainWindow.__init__(self)

        # Руссифицируем QT диалоги
        log.info("Установка руссификации интерфейса QT")
        qt_base_translator = QTranslator(app)
        if qt_base_translator.load(":/i18n/qtbase_ru.qm"):
            app.installTranslator(qt_base_translator)
        else:
            log.error("Ошибка при установке руссификации интерфейса QT.")

        ui_util.load_ui(self, 'main_window')
        ui_util.init_ui(self)

        # Получить данные о текущей версии приложения через HTTP
        self.found_version_signal.connect(self.found_current_version)
        get_current_version()

        # Восстановить настройки расположения окна
        self.not_fullscreen_window_state = Qt.WindowNoState  # Переменная для хранения состояния до входа в полный экран
        self.restore_window_settings()

        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        # После инициализации приложения вызываем окно регистрации пользователя в системе
        app.app_loading_is_complete.connect(self.action_connect_db_trigger)
        app.user_is_registered.connect(self.when_user_is_registered)

        self.show()

    @pyqtSlot(str)
    def found_current_version(self, new_version):
        """Обработка полученного ответа о текущей версии приложения на сайте"""
        log.info('Текущая версия приложения:  %s (На сайте: %s)' % (constants.VERSION, new_version))

        # Сравнение версий (алфавитное сравнение строк версий должно работать нормально)
        if constants.VERSION < new_version:
            # Добавить разделитель и кнопку "Новая версия доступна" на панели инструментов (по умолчанию скрыта)
            spacer = QWidget(self)
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.toolbar.addWidget(spacer)

            # Установить текст для QAction
            self.action_update_app.setVisible(True)
            self.action_update_app.setText("Доступно обновление")
            self.action_update_app.setToolTip("Ваша версия: <b>{}</b><br>"
                                              "Доступна: <b>{}</b>".format(constants.VERSION, new_version))

            # Добавить кнопку Обновление доступно (с иконкой и текстом)
            update_button = QToolButton()
            update_button.setDefaultAction(self.action_update_app)
            update_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.toolbar.addWidget(update_button)

    def closeEvent(self, event):
        log.info("------------------ Выключение ------------------")
        app.db.disconnect()
        self.save_window_settings()
        app.processEvents()
        event.accept()

    def action_update_app_trigger(self, event):
        try:
            webbrowser.open(constants.DOWNLOAD_URL)
            log.info("Успешно открыта страница скачивания новой версии")
        except:
            QMessageBox.warning(self, "Ошибка!", "Не удается открыть страницу загрузки обновления!<br>"
                                                 "Попробуйте сделать это вручную:<br>"
                                                 "<a href='{url}'>{url}</a>".format(url=constants.DOWNLOAD_URL))

    def restore_window_settings(self):
        """Загрузка настроек размера и положения окна"""
        log.info("Загружаем настройки главного окна")
        self.restoreGeometry(app.settings.value("Geometry", QByteArray()))
        self.restoreState(app.settings.value("Window State", QByteArray()))

        # Устанавливаем флаги в меню в соответствии с состояниями элементов
        self.action_view_toolbar.setChecked(self.toolbar.isVisibleTo(self))
        self.action_fullscreen.setChecked(self.isFullScreen())

    def save_window_settings(self):
        """Сохранение настроек размера и положения окна"""
        log.info("Сохраняем настройки главного окна")
        app.settings.setValue("Geometry", self.saveGeometry())
        app.settings.setValue("Window State", self.saveState())

    @pyqtSlot()
    def action_fullscreen_trigger(self):
        """Переключить режим полного экрана"""
        if not self.isFullScreen():
            # Сохраняем состояние окна, чтобы можно было вернуться к нему
            self.not_fullscreen_window_state = self.windowState()
            self.showFullScreen()
        else:
            self.setWindowState(self.not_fullscreen_window_state)

    @pyqtSlot()
    def action_about_trigger(self):
        """Отобразить диалог 'О программе'"""
        from view.about import About
        win = About()
        win.exec_()

    @pyqtSlot()
    def action_settings_db_trigger(self):
        """Отобразить диалог 'Настройки БД'"""
        from view.settings_db import SettingsDB
        win = SettingsDB()
        dialog = win.exec_()
        if dialog:
            win.save_settings()

    @pyqtSlot()
    def action_connect_db_trigger(self):
        """Регистрация пользователя в системе"""
        from view.login import Login
        win = Login()
        win.exec_()

    @pyqtSlot(int)
    def when_user_is_registered(self, user_id):
        # Метод вызывается при регистрации пользователя в системе
        log.info(f'Вход в систему осуществлен с ID: {user_id}')
        app.user_id = user_id
        self.lbl_user_fio.setText(app.db.get_person_fio())

        # TODO: Удалить
        from classes.decorators import with_wait_cursor
        from classes.decorators import display_execution_time
        @with_wait_cursor
        @display_execution_time
        def show_demo():
            # Создаем модель
            sqm = QSqlQueryModel(parent=self)
            sqm.setQuery('SELECT id, lastName, firstName, patrName, birthDate, sex, notes '
                         'FROM Client WHERE deleted = 0 AND deathDate IS NULL')
            # Задаем заголовки для столбцов модели
            sqm.setHeaderData(1, Qt.Horizontal, 'Фамилия')
            sqm.setHeaderData(2, Qt.Horizontal, 'Имя')
            sqm.setHeaderData(3, Qt.Horizontal, 'Отчество')
            sqm.setHeaderData(4, Qt.Horizontal, 'Дата рождения')
            sqm.setHeaderData(5, Qt.Horizontal, 'Пол')
            sqm.setHeaderData(6, Qt.Horizontal, 'Примечание')
            # Задаем для таблицы только что созданную модель
            self.clients_table.setModel(sqm)
            self.clients_table.hideColumn(0)
            self.clients_table.resizeColumnsToContents()
            self.clients_table.horizontalHeader().setStretchLastSection(True)
            self.clients_table.horizontalHeader().setHighlightSections(False)
            # self.clients_table.verticalHeader().hide()
            row_count = str(sqm.rowCount())
            self.lbl_suitable_customers_count.setText(row_count)
            self.lbl_selected_customers_count.setText(row_count)
        show_demo()

    @pyqtSlot(float)
    def show_execution_time(self, time=0.0):
        # Метод вызывается для отображения времени выполнения зарпоса
        self.lbl_execution_time.setText(f'{time:.2f}c')
