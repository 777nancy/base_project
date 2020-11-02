import logging.config

from base_project import config


def initialize_logging(file_name='app'):
    logging_config = config.Config.get_instance().LOGGING_CONFIG
    log_file_path = logging_config['handlers']['logFileHandler']['filename']
    logging_config['handlers']['logFileHandler']['filename'] = log_file_path.format(file_name=file_name)
    logging.config.dictConfig(logging_config)
