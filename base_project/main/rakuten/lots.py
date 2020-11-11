import contextlib
import logging
import os
import time

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from base_project import config, slack
from base_project.main.base import base
from base_project.utils import time_util, util

logger = logging.getLogger(__name__)

LOGIN_URL = 'https://grp01.id.rakuten.co.jp/rms/nid/vc?__event=login&service_id=top'
LOTS_URLS = [
   #  'https://rd.rakuten.co.jp/c/?R2=https%3A%2F%2Fwww%2Einfoseek%2Eco%2Ejp%2FLuckylot&D2=1008.0.100371.0.11066920.2&C3=9816d6f687e5d3a610ac9559ec3d33089d03e855',
    'https://rd.rakuten.co.jp/c/?R2=http%3A%2F%2Fbooks%2Erakuten%2Eco%2Ejp%2Fevent%2Fluckly%2Dkuji%2F%3Fscid%3Dwi%5Fgrp%5Fgmx%5Fbks%5Frjl&D2=1008.0.100371.0.11045245.2&C3=92f41babd2a964f6f36babdfc1a24c4ce94108b6',
]


class Lots(base.BasicLogic):

    def __init__(self):
        super().__init__()

        self._slack_notificator = slack.SlackNotificator(util.name2base_name(__name__))
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

            for url in LOTS_URLS:
                driver.get(url)
                time.sleep(3)
                driver.find_element_by_id('entry').click()
                time.sleep(30)

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
