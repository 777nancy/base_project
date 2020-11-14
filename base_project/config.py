# Standard Library
import copy
import logging
import os

from dotenv import load_dotenv

from base_project.utils import config_reader


class ConfigError(TypeError):
    pass


logger = logging.getLogger(__name__)


class Config(object):
    _initialized = False

    @property
    def SAMPLE_DB(self):
        return copy.deepcopy(self._SAMPLE_DB)

    @property
    def MARKET_DB(self):
        return copy.deepcopy(self._MARKET_DB)

    @property
    def MAIL_CONFIG(self):
        return copy.deepcopy(self._MAIL_CONFIG)

    @property
    def LOGGING_CONFIG(self):
        return copy.deepcopy(self._LOGGING_CONFIG)

    @property
    def RAKUTEN_CONFIG(self):
        return copy.deepcopy(self._RAKUTEN_CONFIG)

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via Constructor')

    @classmethod
    def __internal_new__(cls):
        instance = super().__new__(cls)
        cls.__init__(instance)
        return instance

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls.__internal_new__()

        return cls._instance

    def __init__(self):
        ######################################################################
        # プロジェクト名
        ###########################################################################
        self.PROJECT_NAME = 'base_project'

        ###########################################################################
        # プロジェクトに関するディレクトリのパス
        ###########################################################################
        self.PROJECT_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.CONFIG_ROOT_PATH = os.path.join(self.PROJECT_ROOT_PATH, 'config')
        self.LIB_ROOT_PATH = os.path.join(self.PROJECT_ROOT_PATH, 'lib')
        self.TEMPLATES_ROOT_PATH = os.path.join(self.PROJECT_ROOT_PATH, 'templates')
        self.SQL_ROOT_PATH = os.path.join(self.PROJECT_ROOT_PATH, 'sql')

        ###########################################################################
        # 環境設定ファイルの読み込み
        # .envファイルは下記以降の設定が反映
        ###########################################################################

        # ${PROJECT_NAME}_ENVIRONMENTの設定
        env_file_name = f'{os.getenv(f"{self.PROJECT_NAME.upper()}_ENVIRONMENT", "test")}.env'
        env_file_path = os.path.join(self.CONFIG_ROOT_PATH, env_file_name)
        load_dotenv(env_file_path)

        ###########################################################################
        # データベースの設定
        ###########################################################################

        template_db_url = '{rdbms}://{user}:{password}@{host}:{port}/{dbname}'

        self.SAMPLE_DB_URL = template_db_url.format(
            rdbms='mysql+pymysql',
            user=os.getenv('SAMPLE_DB_USER'),
            password=os.getenv('SAMPLE_DB_PASSWORD'),
            host=os.getenv('SAMPLE_DB_HOST'),
            port=os.getenv('SAMPLE_DB_PORT'),
            dbname=os.getenv('SAMPLE_DB_DBNAME')
        )

        self._SAMPLE_DB = {
            'rdbms': 'MySQL',
            'url': self.SAMPLE_DB_URL,
            'pool_size': os.getenv('SAMPLE_DB_MINCONN'),
            'max_overflow': os.getenv('SAMPLE_DB_MAXCONN'),
        }

        self.MARKET_DB_URL = template_db_url.format(
            rdbms='postgresql',
            user=os.getenv('MARKET_DB_USER'),
            password=os.getenv('MARKET_DB_PASSWORD'),
            host=os.getenv('MARKET_DB_HOST'),
            port=os.getenv('MARKET_DB_PORT'),
            dbname=os.getenv('MARKET_DB_DBNAME')
        )

        self._MARKET_DB = {
            'rdbms': 'PostgreSQL',
            'url': self.MARKET_DB_URL,
            'max_overflow': os.getenv('MARKET_DB_MAXCONN'),
            'pool_size': os.getenv('MARKET_DB_MINCONN'),
        }

        ###########################################################################
        # メールの設定
        ###########################################################################

        self._MAIL_CONFIG = {
            'smtp_host': os.getenv('SMTP_HOST'),
            'smtp_port': os.getenv('SMTP_PORT'),
            'user': os.getenv('SMTP_USER'),
            'password': os.getenv('SMTP_PASSWORD')
        }

        ###########################################################################
        # slackの設定
        ###########################################################################

        self.SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

        ###########################################################################
        # 楽天の設定
        ###########################################################################

        self._RAKUTEN_CONFIG = {
            'user': os.getenv('RAKUTEN_USER'),
            'password': os.getenv('RAKUTEN_PASSWORD')
        }

        ###########################################################################
        # ログの設定
        ###########################################################################

        log_root_path = os.path.join(self.PROJECT_ROOT_PATH, 'log')

        self._LOGGING_CONFIG = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '%(asctime)s : %(threadName)s : %(module)s : %(funcName)s : %(levelname)s : %(message)s'
                }
            },
            'handlers': {
                'StreamHandler': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'simple',
                    'stream': 'ext://sys.stdout'
                },
                'logFileHandler': {
                    'class': 'logging.FileHandler',
                    'level': 'DEBUG',
                    'formatter': 'simple',
                    'filename': os.path.join(log_root_path, '{file_name}.log'),
                    'mode': 'w',
                    'encoding': 'utf-8'
                }
            },
            'root': {
                'level': 'DEBUG',
                'handlers': [
                    'StreamHandler',
                    'logFileHandler'
                ]
            }
        }

        self._initialized = True

    def overwrite(self, params):
        """コンフィグを上書きする

        Args:
            params: {key: value}の辞書

        """

        for k, v in params.items():

            if k not in self.__dict__:
                raise KeyError('config: {} is not exits'.format(k))

            self.__dict__[k] = v

            logger.info('config: {} is overwritten'.format(k))

    def __setattr__(self, key, value):
        if self._initialized:
            raise ConfigError("Can't bind constant ({}={})".format(key, value))
        else:
            super().__setattr__(key, value)


class MailConfigReader(config_reader.JsonConfigReader):

    def __init__(self):

        config_root_path = Config.get_instance().CONFIG_ROOT_PATH
        mail_config_path = os.path.join(config_root_path, 'mail_config.json')
        super(MailConfigReader, self).__init__(mail_config_path)

    def get_subject_by_id(self, subject_id):

        subject_property = self._get_property_by_id('subjects', subject_id)

        return subject_property.get('subject')

    def get_addresses_by_id(self, address_id):

        address_property = self._get_property_by_id('addresses', address_id)

        return address_property.get('from'), address_property.get('to'), address_property.get(
            'profile'), address_property.get('cc'), address_property.get('bcc')

    def _get_property_by_id(self, property_name, target_id):

        properties = self.get_property(property_name)

        for prop in properties:
            if prop.get('id') == int(target_id):
                return prop


class ProcessDefinitionReader(config_reader.JsonConfigReader):

    def __init__(self):
        config_root_path = Config.get_instance().CONFIG_ROOT_PATH
        mail_config_path = os.path.join(config_root_path, 'process_definition.json')
        super(ProcessDefinitionReader, self).__init__(mail_config_path)

    def get_process_definition_by_name(self, process_name):

        processes = self.get_property('processes')

        for process in processes:
            if process.get('name') == process_name:
                module_path = process.get('modulePath')
                class_name = process.get('className')
                arguments = process.get('arguments')

                if arguments:
                    arguments_dict = {}

                    for argument in arguments:
                        arguments_dict[argument.get('name')] = argument.get('value')
                else:
                    arguments_dict = None

                return module_path, class_name, arguments_dict

        raise ValueError('process name: {} does not exist'.format(process_name))


class PipelineDefinitionReader(config_reader.JsonConfigReader):

    def __init__(self, pipeline_definition_file_name):
        config_root_path = Config.get_instance().CONFIG_ROOT_PATH
        mail_config_path = os.path.join(config_root_path, 'pipeline', pipeline_definition_file_name)
        super(PipelineDefinitionReader, self).__init__(mail_config_path)

    def get_pipeline(self):
        pipeline = self.get_property('pipeline')

        return sorted(pipeline, key=lambda x: x['processId'])


if __name__ == '__main__':
    pdr = PipelineDefinitionReader('pipeline_definition.json')

    print(pdr.get_pipeline())
