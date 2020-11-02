import slackweb

from base_project import config
from base_project.utils import template_file_reader


class SlackNotificator(object):
    """
    プロジェクト内のSlackの通知を管理するクラス
    """

    def __init__(self, username):
        """コンストラクタ

        Args:
            username: ユーザ名
        """

        self._username = username
        self._config = config.Config.get_instance()
        self._slack = slackweb.Slack(url=self._config.SLACK_WEBHOOK_URL)

        self._template_file_reader = template_file_reader.TemplateFileReader(self._config.TEMPLATES_ROOT_PATH)

    def notify(self, text):
        """Slackへ通知する

        Args:
            text: 通知テキスト

        """
        self._slack.notify(username=self._username, text=text)

    def notify_from_file(self, file_path, params=None):
        """ファイルからテンプレートを読み込んでSlackへ通知する

        Args:
            file_path: ファイルパス
            params: コンテキスト

        """
        text = self._template_file_reader.read(file_path, params)
        self._slack.notify(username=self._username, text=text)
