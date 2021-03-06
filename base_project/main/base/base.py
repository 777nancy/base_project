from abc import ABCMeta, abstractmethod


class BasicLogic(metaclass=ABCMeta):
    """
    本プロジェクトの基底ロジック
    """
    @abstractmethod
    def run(self):
        """メイン処理
        """
        pass

    def do_after_exception(self, exception):
        """例外発生後に必ず実行する処理

        Args:
            exception: 例外

        """
        pass

    @staticmethod
    def cli(sys_argv):
        """コマンドライン引数を設定する

        Args:
            sys_argv: コマンドライン引数

        """
        pass

