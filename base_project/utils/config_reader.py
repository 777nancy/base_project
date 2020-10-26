import json
from abc import ABCMeta, abstractmethod


class BaseConfigReader(metaclass=ABCMeta):

    @abstractmethod
    def get_property(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass


class JsonConfigReader(BaseConfigReader):

    def __init__(self, config_path):
        with open(config_path, mode='r') as fin:
            self.config = json.load(fin)

    def get_property(self, *args):
        json_property = self.config
        for arg in args:
            sub_json_property = json_property.get(arg)

            if sub_json_property is None:
                raise KeyError('{} is not found'.format(arg))

            json_property = sub_json_property

        return json_property

    def to_dict(self):

        return self.config
