import argparse
import logging.config
import sys
from importlib import import_module

from base_project import log
from base_project.utils import time_util


class CLI(object):
    """
    本プロジェクのエントリポイント
    """

    def __init__(self):
        # コマンドライン引数の取得
        parser = argparse.ArgumentParser(description='cli runner',
                                         usage='cli.py <module_path> <class_name> [<args>]')

        parser.add_argument('module_path', help='module path')
        parser.add_argument('class_name', help='class name')
        args = parser.parse_args(sys.argv[1:3])

        # ログの設定
        log_file_name = f'{args.class_name}_{time_util.get_microsecond_now()}'
        log.initialize_logging(log_file_name)
        logger = logging.getLogger(__name__)

        logger.info('モジュール: {}'.format(args.module_path))
        logger.info('クラス: {}'.format(args.class_name))

        # 実行するクラスのインスタンスを生成
        try:
            module = import_module(args.module_path)
        except ModuleNotFoundError as e:
            logger.exception(e)
            raise
        try:
            processor_cls = getattr(module, args.class_name)
        except AttributeError as e:
            logger.exception(e)
            raise

        processor_args = processor_cls.cli(sys.argv[3:])
        if processor_args:
            logger.info('command line args')
            for k, v in processor_args.__dict__.items():
                logger.info(f'{k}: {v}')

            processor = processor_cls(**processor_args.__dict__)
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


if __name__ == '__main__':
    CLI()
