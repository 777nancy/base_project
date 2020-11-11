import logging

from base_project.main.base import base

logger = logging.getLogger(__name__)


class Sample(base.BasicLogic):

    def __init__(self):
        super().__init__()
        logger.warning('no arguments')

    def run(self, *args, **kwargs):
        logger.warning('main process')
