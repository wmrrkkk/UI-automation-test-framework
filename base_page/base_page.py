import configparser
import os
import time

import xlrd
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from base_page.logger import Logger


log1 = Logger(logger='Marongkuan').getlog()

class BasePage(object):
    PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    def __init__(self, driver):
        file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/config.ini'
        config = configparser.ConfigParser()
        config.read(file_path, encoding='utf-8')
        self.BaseUrl = config.get('testServer', 'URL')
        self.driver = driver
        log1.info(u'浏览器初始化成功')

    def _open_url(self, url=''):
        self.driver.get(self.BaseUrl.format(url))

    @staticmethod
    def get_img(self):
        path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/test_report/'
        time_stamp = time.strftime('%Y%m%d_%H%M%S')
        img_name = path + time_stamp + '.png'
        try:
            self.driver.save_screenshot(img_name)
            print('screenshot:', time_stamp, '.png')
            log1.info(u'截图成功：%s'%img_name)
        except BaseException:
            print('截图失败！！！')
            log1.error(u'截图失败！！！')

    def find_element(self, selector):
        by = selector[0]
        value = selector[1]
        try:
            WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element(by, value).is_displayed())
            log1.info(u'元素定位成功。定位方式：%s，使用的值%s：' % (by, value))
            return self.driver.find_element(by, value)
        except Exception as e:
            print(e)
            self.get_img(self)
            log1.error(u"报错信息：", exc_info=1)
            raise e

    def find_elements(self, selector):
        by = selector[0]
        value = selector[1]
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(selector))
            return self.driver.find_elements(by, value)
        except Exception:
            print(Exception)
            self.get_img(self)
            raise Exception

    def type(self, selector, value):
        element = self.find_element(selector)
        element.clear()
        try:
            element.send_keys(value)
            print('输入的内容：%s' % value)
        except BaseException:
            print('内容输入报错')
            self.get_img(self)

    def on_click(self, selector):
        element = self.find_element(selector)
        try:
            element.click()
        except BaseException as e:
            print(e)
            self.get_img(self)

    def double_click(self, selector):
        element = self.find_element(selector)
        try:
            chain = ActionChains(self.driver)
            chain.double_click(element).perform()
        except BaseException as e:
            print(e)
            self.get_img(self)

    def choice_checkbox(self, selector):
        element = self.find_element(selector)
        try:
            element.send_keys(Keys.SPACE)
        except BaseException:
            self.get_img(self)

    def send_keys(self, selector, content, is_clear=True, is_click=True):
        element = self.find_element(selector)
        try:
            if is_clear is True:
                element.clear()
            if is_click is True:
                element.click()
            element.send_keys(content)
        except BaseException:
            print('输入内容报错')
            self.get_img(self)

    def clear(self, selector):
        element = self.find_element(selector)
        try:
            element.clear()
        except BaseException:
            print('清空元素失败')
            self.get_img(self)

    def getText(self, selector):
        element = self.find_element(selector)
        try:
            return element.text
        except BaseException:
            print('获取文本信息')
            self.get_img(self)

    def getAlertText(self):
        try:
            return self.driver.switch_to.alert.text
        except BaseException:
            print('获取alert内容')
            self.get_img(self)

    def clickAlert(self, accept=0):
        try:
            if accept == 0:
                self.driver.switch_to.alert.accept()
            else:
                self.driver.switch_to.alert.dismiss()
        except BaseException:
            print('点击alert弹窗')
            self.get_img(self)

    @staticmethod
    def read_table(file_path, sheet_no):
        data = xlrd.open_workbook(file_path)
        table = data.sheets()[sheet_no]
        return table

    @staticmethod
    def read_xls(file_path, sheet_no):
        table = BasePage.read_table(file_path, sheet_no)
        for args in range(1, table.nrows):
            yield table.row_values(args)

    @staticmethod
    def __locate(name, tag, file_path, sheet_no=0):
        table = BasePage.read_table(file_path, sheet_no)
        for i in range(1, table.nrows):
            if name in table.row_values(i):
                if tag == "loc":
                    return tuple(table.row_values(i)[1:3])
                elif tag == "value":
                    return table.row_values(i)[2:3][0]

    @staticmethod
    def locate(path):
        def func(name):
            return BasePage.__locate(name, "loc", path)

        return func

    @staticmethod
    def ele_value(path):
        def func(name):
            return BasePage.__locate(name, "value", path)

        return func

    def exists_element(self, *loc):
        try:
            WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element(*loc).is_displayed())
        except exceptions.NoSuchElementException as e:
            print(e)
            print("%s没有查找到元素%s" % (self.__class__.__name__, loc))
            self.get_img(self)
            return False
        else:
            return True

    def sleep(self, seconds):
        time.sleep(seconds)
        print('暂停%d秒' % seconds)

    def get_title(self):
        title = self.driver.title
        return title

    def quit(self):
        self.driver.quit()
