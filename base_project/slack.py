import traceback

import slackweb
from base_project import config


class SlackNotificator(object):

    def __init__(self):
        self._slack = slackweb.Slack(url=config.SLACK_WEBHOOK_URL)

    def notify(self, username, text):
        self._slack.notify(username=username, text=text)

    def notify_exception(self, username, exception):
        text = 'エラーが発生しました\n'
        trace_back = ''.join(traceback.TracebackException.from_exception(exception).format())
        self._slack.notify(username=username, text=text+trace_back)
