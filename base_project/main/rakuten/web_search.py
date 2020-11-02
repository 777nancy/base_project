import contextlib
import logging
import os
import time

import chromedriver_binary
import mimesis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from base_project import config, slack
from base_project.main.base import base
from base_project.utils import time_util, util

logger = logging.getLogger(__name__)

LOGIN_URL = 'https://grp03.id.rakuten.co.jp/rms/nid/login?service_id=r12&return_url=login?tool_id=1&tp=&id='
WEB_SEARCH_URL = 'https://websearch.rakuten.co.jp'


class WebSearch(base.BasicLogic):

    def __init__(self):
        super().__init__()

        self._slack_notificator = slack.SlackNotificator(__name__)
        self._config = config.Config.get_instance()
        self._start_time = None

    def run(self):

        self._start_time = time_util.get_timestamp_now()

        options = Options()

        add_on_path = os.path.join(self._config.LIB_ROOT_PATH, 'extension_4_655_0_0.crx')
        options.add_extension(add_on_path)
        driver = webdriver.Chrome(options=options)

        with contextlib.ExitStack() as stack:
            stack.callback(driver.quit)
            driver.get(LOGIN_URL)

            logger.info('ログイン開始')
            user_id_element = driver.find_element_by_xpath('//*[@id="loginInner_u"]')
            user_id_element.send_keys(self._config.RAKUTEN_CONFIG.get('user'))
            time.sleep(3)
            password_element = driver.find_element_by_xpath('//*[@id="loginInner_p"]')
            password_element.send_keys(self._config.RAKUTEN_CONFIG.get('password'))
            time.sleep(3)
            login_submit = driver.find_element_by_xpath('//*[@id="loginInner"]/p[1]/input')
            login_submit.click()
            time.sleep(3)
            if 'login' in driver.current_url:
                raise ValueError('user id or password is incorrect')
            logger.info('ログイン完了')

            text = mimesis.Text()
            logger.info('検索開始')
            for i in range(35):
                driver.get(WEB_SEARCH_URL)
                search_window = driver.find_element_by_xpath('//*[@id="search-input"]')
                search_word = text.word()
                logger.info('検索ワード: {}'.format(search_word))
                search_window.send_keys(search_word)
                time.sleep(3)
                search_submit = driver.find_element_by_xpath('//*[@id="search-submit"]')
                search_submit.click()
                time.sleep(3)
            logger.info('検索完了')

        # slackへ通知
        end_time = time_util.get_timestamp_now()
        context = {
            'start_time': self._start_time,
            'end_time': end_time
        }

        self._slack_notificator.notify_from_file(os.path.join('slack', 'rakuten', 'success.txt'), context)

    def do_after_exception(self, exception):

        # slackへエラー通知
        end_time = time_util.get_timestamp_now()
        context = {
            'start_time': self._start_time,
            'end_time': end_time,
            'traceback': util.exception2str(exception)
        }
        self._slack_notificator.notify_from_file(os.path.join('slack', 'utils', 'error.txt'), context)
