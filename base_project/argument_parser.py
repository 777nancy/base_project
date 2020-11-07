import argparse


def database_parser():
    """本プロジェクト内のパーサ

    """
    parser = argparse.ArgumentParser(add_help=False)
    database_group = parser.add_argument_group('database settings')

    database_group.add_argument('-u', '--user')
    database_group.add_argument('-pw', '--password')
    database_group.add_argument('-ht', '--host')
    database_group.add_argument('-p', '--port')
    database_group.add_argument('-d', '--dbname')
    database_group.add_argument('--pool-size')
    database_group.add_argument('--max-overflow')

    return parser

