import os

from dotenv import load_dotenv

###########################################################################
# プロジェクト名
###########################################################################
PROJECT_NAME = 'base_project'

###########################################################################
# プロジェクトに関するディレクトリのパス
###########################################################################
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
CONFIG_ROOT_PATH = os.path.join(PROJECT_ROOT, 'config')
LIB_ROOT_PATH = os.path.join(PROJECT_ROOT, 'lib')
TEMPLATES_ROOT_PATH = os.path.join(PROJECT_ROOT, 'templates')

###########################################################################
# 環境設定ファイルの読み込み
# .envファイルは下記以降の設定が反映
###########################################################################

# ${PROJECT_NAME}_ENVIRONMENTの設定
env_file_name = f'{os.getenv(f"{PROJECT_NAME.upper()}_ENVIRONMENT", "test")}.env'
env_file_path = os.path.join(CONFIG_ROOT_PATH, env_file_name)
load_dotenv(env_file_path)

###########################################################################
# データベースの設定
###########################################################################

SAMPLE_DB = {
    'host': os.getenv('SAMPLE_DB_HOST'),
    'port': os.getenv('SAMPLE_DB_PORT'),
    'user': os.getenv('SAMPLE_DB_USER'),
    'password': os.getenv('SAMPLE_DB_PASSWORD'),
    'dbname': os.getenv('SAMPLE_DB_DBNAME'),
    'minconn': os.getenv('SAMPLE_DB_MINCONN', 1),
    'maxconn': os.getenv('SAMPLE_DB_MAXCONN', 1),
}

###########################################################################
# メールの設定
###########################################################################

MAIL_CONFIG = {
    'host': os.getenv('SMTP_HOST'),
    'port': os.getenv('SMTP_PORT'),
    'password': os.getenv('SMTP_PASSWORD')
}

###########################################################################
# slackの設定
###########################################################################

SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

###########################################################################
# 楽天の設定
###########################################################################

RAKUTEN_USER = os.getenv('RAKUTEN_USER')
RAKUTEN_PASSWORD = os.getenv('RAKUTEN_PASSWORD')


###########################################################################
# ログの設定
###########################################################################

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s : %(threadName)s : %(levelname)s : %(message)s'
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
            'filename': '../log/{file_name}.log',
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
