import requests
import threading
from classes.app import get_app
from classes import constants
from classes.logger import log

app = get_app()


def get_current_version():
    """Возвращает текущую версию приложения"""
    t = threading.Thread(target=_get_version_from_http)
    t.start()


def _get_version_from_http():
    """Проверяет текущую версию приложения на сайте"""
    url = constants.APP_SITE + "/version.json"

    try:
        r = requests.get(url, headers={"user-agent": "%s-%s" % (constants.APP_NAME_WITHOUT_SPACES,
                                                                constants.VERSION)}, verify=False, timeout=5)
        app_version = r.json()["app_version"]
        app.main_window.found_version_signal.emit(app_version)
    except:
        log.error("Не удалось получить данные о версии с сайта %s" % url)
