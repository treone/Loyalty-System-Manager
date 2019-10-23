from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from classes import constants, ui_util
from classes.app import get_app
from view.license import License


class About(QDialog):
    """Окно 'О программе'"""
    def __init__(self):
        QDialog.__init__(self, parent=get_app().main_window)

        ui_util.load_ui(self, 'about')
        ui_util.init_ui(self)

        header_html = """
                <html><head/><body>
                    <p align="center" style="font-size: 4em; font-weight: bold;">
                        {app_name} (Версия: {version})
                    </p>
                    <p align="center" style="font-size: 2em;">
                        {description}
                    </p>
                </body></html>
            """.format(app_name=constants.APP_NAME_RUS, version=constants.VERSION, description=constants.DESCRIPTION)
        description_text = constants.DESCRIPTION
        description_html = """
            <html><head/><body>
                <hr />
                <p align="center" style="font-size: 2em;">
                    Почта для замечаний и предложений<br />
                    <a href="mailto:{email}"><span style="text-decoration: none; color:#55aaff;">{email}</span></a>
                </p>
            </body></html>""".format(description=description_text, email=constants.COMPANY_EMAIL)
        author_html = """
            <html><head/><body style="font-weight:400; font-style:normal;">
                <hr />
                <p align="center">
                    <span style="font-weight: bold;">%s</span>
                    <br />
                </p>
            </body></html>
        """ % constants.COPYRIGHT

        # Устанавливаем информацию о версии программы, авторе и описание
        self.lbl_about_description.setText(description_html)
        self.lbl_about_autor.setText(author_html)
        self.lbl_version.setText(header_html)
        self.lbl_version.setAlignment(Qt.AlignCenter)

    @staticmethod
    def btn_license_click():
        """Открыть окно 'Лицензия'"""
        win = License()
        win.exec_()
