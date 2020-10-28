import json
from abc import ABCMeta, abstractmethod


class ConfigReader(metaclass=ABCMeta):
    """
    コンフィグファイルを読み込むクラスのインターフェース
    """

    @abstractmethod
    def get_property(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass


class JsonConfigReader(ConfigReader):
    """
    JSON形式のコンフィグファイル読み込みクラス
    """

    def __init__(self, config_path):
        """コンストラクタ

        Args:
            config_path: コンフィグファイルのパス
        """
        with open(config_path, mode='r') as fin:
            self.config = json.load(fin)

    def get_property(self, *args):
        """引数から値を取得する

        Args:
            *args: キー

        Returns:
            キーから取得される値
        """
        if self.config is list:
            return None

        json_property = self.config
        for arg in args:
            sub_json_property = json_property.get(arg)

            if sub_json_property is None:
                raise KeyError('{} is not found'.format(arg))

            json_property = sub_json_property

        return json_property

    def to_dict(self):
        """コンフィグファイルの内容を辞書で返却する

        Returns:
            辞書
        """
        return self.config
