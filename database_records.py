__author__ = "Marc Concepcion"
__copyright__ = "Copyright 2021, Marc Concepcion"
__credits__ = ["Marc Concepcion"]
__maintainer__ = "Marc Concepcion"
__email__ = "marcanthonyconcepcion@gmail.com"
__status__ = "Demo"

from typing import Final
import yaml
import mysql.connector

with open(r'resources\database_demo.yaml') as file:
    configuration = yaml.full_load(file)

HOST: Final = configuration['database']['host']
DBNAME: Final = configuration['database']['dbname']
USER: Final = configuration['database']['user']
PASSWORD: Final = configuration['database']['password']


class DatabaseRecords:

    def __init__(self):
        try:
            self.database = mysql.connector.connect(host=HOST, database=DBNAME,
                                                    user=USER, password=PASSWORD)
            self.cursor = self.database.cursor()
        except mysql.connector.errors.Error as database_error:
            raise DatabaseError('Database error. {details}'.format(details=database_error))

    def disconnect(self):
        self.database.disconnect()

    def test_connection(self):
        return self.database.is_connected()

    def reconnect(self):
        try:
            self.database.reconnect()
        except mysql.connector.errors.Error as database_error:
            raise DatabaseError('Database error. {details}'.format(details=database_error))

    def fetch(self, query, parameters=None):
        try:
            self.cursor.execute(operation=query, params=parameters)
            for result in self.cursor:
                yield result
        except mysql.connector.errors.Error as database_error:
            raise DatabaseError('Database error. {details}'.format(details=database_error))
        finally:
            self.cursor.reset()

    def edit(self, query, parameters=None):
        try:
            self.cursor.execute(operation=query, params=parameters)
            self.database.commit()
        except mysql.connector.errors.Error as database_error:
            self.database.rollback()
            raise DatabaseError('Database error. {details}'.format(details=database_error))

    def bulk_edit(self, query, parameter_sets):
        try:
            self.cursor.executemany(operation=query, seq_params=parameter_sets)
            self.database.commit()
        except mysql.connector.errors.Error as database_error:
            self.database.rollback()
            raise DatabaseError('Database error. {details}'.format(details=database_error))

    def transact_edit(self, queries):
        try:
            for query in queries:
                self.cursor.execute(operation=query['statement'], params=query['parameters'])
            self.database.commit()
        except mysql.connector.errors.Error as database_error:
            self.database.rollback()
            raise DatabaseError('Database error. {details}'.format(details=database_error))

    __instance__ = None

    @staticmethod
    def get():
        if DatabaseRecords.__instance__ is None:
            DatabaseRecords.__instance__ = DatabaseRecords()
        return DatabaseRecords.__instance__


class DatabaseError(Exception):
    pass
