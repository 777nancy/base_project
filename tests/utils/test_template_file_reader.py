import os

from base_project import config
from base_project.utils import template_file_reader

TEMPLATES_ROOT_PATH = os.path.join(config.PROJECT_ROOT_PATH, 'tests', 'test_files', 'templates')


class TestTemplateFileReader(object):

    @classmethod
    def setup_class(cls):
        cls.template_file_reader = template_file_reader.TemplateFileReader(TEMPLATES_ROOT_PATH)

    def test_read_no_params(self):
        assert self.template_file_reader.read('no_params.txt') == 'content'

    def test_read_with_params(self):
        assert self.template_file_reader.read('with_params.txt',
                                              {'file_name': 'with_params.txt'}) == 'This is with_params.txt'
