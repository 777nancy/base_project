"""
process_definition.jsonで定義された処理を実行する
"""
import argparse
import logging
from importlib import import_module

from base_project import config, log
from base_project.utils import time_util
from base_project.utils.database import connection_pool


class ProcessRunner(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description='process runner',
                                         usage='process_runner.py <process_name>')

        parser.add_argument('process_name', help='process name in process_definition.json')
        args = parser.parse_args()

        # ログの設定
        log_file_name = f'{args.process_name}_{time_util.get_microsecond_now()}'
        log.initialize_logging(log_file_name)
        logger = logging.getLogger(__name__)

        process_def_config = config.ProcessDefinitionReader()
        module_path, class_name, arguments = process_def_config.get_process_definition_by_name(args.process_name)

        logger.info('モジュール: {}'.format(module_path))
        logger.info('クラス: {}'.format(class_name))

        # 実行するクラスのインスタンスを生成
        try:
            module = import_module(module_path)
        except ModuleNotFoundError as e:
            logger.exception(e)
            raise
        try:
            processor_cls = getattr(module, class_name)
        except AttributeError as e:
            logger.exception(e)
            raise

        if arguments:
            logger.info('arguments')
            for k, v in arguments.items():
                logger.info(f'{k}: {v}')

            processor = processor_cls(**arguments)
        else:
            processor = processor_cls()

        # 処理を実行
        try:
            logger.info('start main_process')
            processor.run()
            logger.info('end main_process')
        except Exception as e:
            logger.exception(e)
            processor.do_after_exception(e)
            raise
        finally:
            connection_pool.ConnectionPoolManager.close_connection_pools()


if __name__ == '__main__':
    ProcessRunner()
