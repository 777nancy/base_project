import os

import pytest
from base_project import config
from base_project.utils import config_reader

CONFIG_ROOT_PATH = os.path.join(config.PROJECT_ROOT_PATH, 'tests', 'test_files', 'config')


class TestJsonConfigReader(object):

    @classmethod
    def setup_class(cls):
        cls.json_config_reader = config_reader.JsonConfigReader(os.path.join(CONFIG_ROOT_PATH, 'test_config.json'))

    def test_get_string_value(self):
        value = self.json_config_reader.get_property('test', 'string')
        assert type(value) is str
        assert value == 'string'

    def test_get_int_value(self):
        value = self.json_config_reader.get_property('test', 'int')
        assert type(value) is int
        assert value == 0

    def test_get_float_value(self):
        value = self.json_config_reader.get_property('test', 'float')
        assert type(value) is float
        assert value == 0.0

    def test_get_date(self):
        value = self.json_config_reader.get_property('test', 'date')
        assert type(value) is str
        assert value == '2001-01-23'

    def test_get_boolean_true(self):
        value = self.json_config_reader.get_property('test', 'boolean_true')
        assert type(value) is bool
        assert value is True

    def test_get_boolean_false(self):
        value = self.json_config_reader.get_property('test', 'boolean_false')
        assert type(value) is bool
        assert value is False

    def test_get_list(self):
        value = self.json_config_reader.get_property('test', 'list')
        assert type(value) is list
        assert value == ['a', 'b', 'c']

    def test_get_dict(self):
        value = self.json_config_reader.get_property('test', 'dict')
        assert type(value) is dict
        assert value == {'a': 1, 'b': 2, 'c': 3}

    def test_get_unknown_section(self):
        value = self.json_config_reader.get_property('unknown_section')
        assert value is None

    def test_get_unknown_key(self):
        value = self.json_config_reader.get_property('test', 'unknown_key')
        assert value is None

    def test_get_unknown_key_over_string(self):
        value = self.json_config_reader.get_property('test', 'string', 'unknown_key')
        assert value is None
