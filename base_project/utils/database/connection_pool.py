from abc import ABCMeta, abstractmethod

from psycopg2 import pool


class DatabaseConnectionPool(metaclass=ABCMeta):

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def return_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def close_all_connections(self):
        pass


class PgConnectionPool(DatabaseConnectionPool):

    def __init__(self, minconn, maxconn, **kwargs):
        self.__connection_pool = pool.SimpleConnectionPool(minconn=minconn, maxconn=maxconn, **kwargs)

    def get_connection(self):
        return self.__connection_pool.getconn()

    def return_connection(self, connection):
        self.__connection_pool.putconn(connection)

    def close_all_connections(self):
        self.__connection_pool.closeall()
