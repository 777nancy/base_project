import contextlib
import os
import time

import chromedriver_binary
import mimesis
from base_project import config, slack
from base_project.main.base import base
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

LOGIN_URL = 'https://grp03.id.rakuten.co.jp/rms/nid/login?service_id=r12&return_url=login?tool_id=1&tp=&id='
WEB_SEARCH_URL = 'https://websearch.rakuten.co.jp'


class WebSearch(base.BasicLogic):

    def __init__(self):
        super().__init__()

        self.slack_notificator = slack.SlackNotificator()

    def run(self):
        text = mimesis.Text()
        word_list = [text.word() for _ in range(30)]
        options = Options()

        add_on_path = os.path.join(config.LIB_ROOT_PATH, 'extension_4_655_0_0.crx')
        options.add_extension(add_on_path)
        driver = webdriver.Chrome(options=options)

        with contextlib.ExitStack() as stack:
            stack.callback(driver.quit)
            driver.get(LOGIN_URL)

            user_id_element = driver.find_element_by_xpath('//*[@id="loginInner_u"]')
            user_id_element.send_keys(config.RAKUTEN_USER)
            time.sleep(3)
            password_element = driver.find_element_by_xpath('//*[@id="loginInner_p"]')
            password_element.send_keys(config.RAKUTEN_PASSWORD)
            time.sleep(3)
            login_submit = driver.find_element_by_xpath('//*[@id="loginInner"]/p[1]/input')
            login_submit.click()
            time.sleep(3)
            if 'login' in driver.current_url:
                raise ValueError('user id or password is incorrect')

            for search_word in word_list:
                driver.get(WEB_SEARCH_URL)
                search_window = driver.find_element_by_xpath('//*[@id="search-input"]')
                search_window.send_keys(search_word)
                time.sleep(3)
                search_submit = driver.find_element_by_xpath('//*[@id="search-submit"]')
                search_submit.click()
                time.sleep(3)

        self.slack_notificator.notify('web_search', '処理が正常終了しました')

    def do_in_exception(self, exception):
        self.slack_notificator.notify_exception(__name__, exception)
