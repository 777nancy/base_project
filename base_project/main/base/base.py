from abc import ABCMeta, abstractmethod


class BasicLogic(metaclass=ABCMeta):
    """
    本プロジェクトの基底ロジック
    """
    def __init__(self, **kwargs):
        """コンストラクタ

        Args:
            **kwargs: cliで設定した名前でコマンドライン引数がコンストラクタの引数として渡される。
            コマンドライン引数が設定されていない場合は引数はない。
        """
        pass

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
