import argparse

from base_project.main.base import base


class Sample(base.BasicLogic):

    def __init__(self):
        super().__init__()
        print('no arguments')

    def run(self, *args, **kwargs):
        print('main process')
