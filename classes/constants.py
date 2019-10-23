import os
from datetime import datetime

VERSION = "0.1"
APP_NAME = "Loyalty System Manager"
APP_NAME_ABBR = "LSM"
APP_NAME_RUS = "Менеджер Системы Лояльности"
DESCRIPTION = "Простое решение для построения системы лояльности."
APP_SITE = "http://lpu53.ru/lsm"
COMPANY = 'ООО "Системная Интеграция"'
COMPANY_EMAIL = "samson@itnov.ru"
COPYRIGHT = "Все права защищены. (c) 2018-%s %s" % (datetime.now().year, COMPANY)

APP_NAME_WITHOUT_SPACES = APP_NAME.lower().replace(" ", "-")
CWD = os.getcwd()

PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # Каталог приложения
RESOURCES_PATH = os.path.join(PATH, "resources")

HOME_PATH = os.path.join(os.path.expanduser("~"))
USER_PATH = os.path.join(HOME_PATH, f".{APP_NAME_WITHOUT_SPACES}")
IMAGES_PATH = os.path.join(USER_PATH, "images")
BACKUP_PATH = os.path.join(USER_PATH, "backup")
PROJECTS_PATH = os.path.join(USER_PATH, "projects")

# Создаем пути, если они не существуют
for folder in [USER_PATH, IMAGES_PATH, BACKUP_PATH, PROJECTS_PATH]:
    if not os.path.exists(folder.encode("UTF-8")):
        os.makedirs(folder, exist_ok=True)
