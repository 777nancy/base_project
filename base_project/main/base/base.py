from abc import ABCMeta, abstractmethod


class BasicLogic(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass

    def do_in_exception(self, exception):
        pass

    @staticmethod
    def cli(sys_argv):
        pass
