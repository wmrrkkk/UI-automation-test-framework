import configparser
import os

from selenium import webdriver


class BrowserEngine(object):
    def __init__(self, browser=None):
        file_path = os.path.abspath(os.path.dirname(
            os.path.dirname(__file__))) + '/config.ini'
        config = configparser.ConfigParser()
        config.read(file_path, encoding='utf-8')
        if browser is None:
            self._browser_type = config.get('browserType', 'browserName')
        else:
            self._browser_type = browser
        self._driver = None

    def init_driver(self):
        if self._browser_type.lower() == 'chrome':
            self._driver = webdriver.Chrome()
        elif self._browser_type.lower() == 'firefox':
            self._driver = webdriver.Firefox()
        elif self._browser_type.lower() == 'ie':
            self._driver = webdriver.Ie()
        elif self._browser_type.lower() == 'edge':
            self._driver = webdriver.Edge()
        else:
            ValueError('传入的浏览器类型有误，目前仅支持Chrome/Firefox/IE/Edge浏览器')
        self._driver.maximize_window()
        return self._driver
