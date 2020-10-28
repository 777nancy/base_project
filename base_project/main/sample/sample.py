import argparse

from base_project.main.base import base


class Sample(base.BasicLogic):

    def __init__(self, carrier, service_type, status, version):
        super().__init__()
        print(carrier, service_type, status, version)

    def run(self, *args, **kwargs):
        print('main process')

    @staticmethod
    def cli(sys_argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--carrier', required=True)
        parser.add_argument('-t', '--service-type', required=True)
        parser.add_argument('-s', '--status', required=True)
        parser.add_argument('-v', '--version', required=True)

        return parser.parse_args(sys_argv)
