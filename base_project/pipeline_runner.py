"""
process_definition.jsonで定義された処理を実行する
"""
import argparse
import logging
from concurrent import futures
from importlib import import_module
import contextlib
from base_project import config, log
from base_project.utils import time_util
from base_project.utils.database import connection_pool

logger = logging.getLogger(__name__)


class PipelineRunner(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description='pipeline runner',
                                         usage='process_runner.py <pipeline_definition_file_name>')

        parser.add_argument('pipeline_definition_file_name', help='pipeline definition file name')
        args = parser.parse_args()

        # ログの設定
        log_file_name = f'{args.pipeline_definition_file_name}_{time_util.get_microsecond_now()}'
        log.initialize_logging(log_file_name)

        pipeline_def_config = config.PipelineDefinitionReader(args.pipeline_definition_file_name)

        pipeline_list = pipeline_def_config.get_pipeline()

        unique_process = set()

        def get_unique_process(pipeline):

            for _process in pipeline:
                p = _process.get('process')
                if type(p) is str:
                    unique_process.add(p)
                else:
                    get_unique_process(p)

        get_unique_process(pipeline_list)

        self._process_definition = {}

        process_def_config = config.ProcessDefinitionReader()

        for process_name in unique_process:
            module_path, class_name, arguments = process_def_config.get_process_definition_by_name(process_name)

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

            self._process_definition[process_name] = {
                'process_class': processor_cls,
                'arguments': arguments
            }

        with contextlib.ExitStack() as stack:
            stack.callback(connection_pool.ConnectionPoolManager.close_connection_pools)
            for process in pipeline_list:
                process_def = process.get('process')
                if type(process_def) is list:
                    future_list = []
                    multiprocess_num = min(int(process.get('multiprocessNum')), len(process_def))
                    with futures.ProcessPoolExecutor(multiprocess_num) as executor:
                        for p in process_def:
                            p_def = p.get('process')
                            future = executor.submit(self._run_process, process_def=p_def)
                            future_list.append(future)
                    futures.as_completed(future_list)
                else:
                    self._run_process(process_def)

    def _run_process(self, process_def):
        process_def = self._process_definition.get(process_def)
        process_cls = process_def.get('process_class')
        arguments = process_def.get('arguments')

        if arguments:
            logger.info('arguments')
            for k, v in arguments.items():
                logger.info(f'{k}: {v}')

            processor = process_cls(**arguments)
        else:
            processor = process_cls()

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
    PipelineRunner()
