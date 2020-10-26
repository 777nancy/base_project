import argparse

from base_project.main.base import base


class Sample(base.BasicLogic):

    def __init__(self):
        super().__init__()
        print('no arguments')

    def main_process(self, *args, **kwargs):
        print('main process')

    def post_process(self, *args, **kwargs):
        print('post process')
