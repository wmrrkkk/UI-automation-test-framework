from base_page.base_page import BasePage


class BaiduPage(BasePage):
    file_path = BasePage.PATH + '/test_data/ele_baidu.xlsx'
    lc = BasePage.locate(file_path)
    text = lc('text')
    search = lc('search')

    def search_content(self, content=''):
        self.send_keys(self.text, content)
        self.on_click(self.search)
