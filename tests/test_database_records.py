__author__ = "Marc Concepcion"
__copyright__ = "Copyright 2021, Marc Concepcion"
__credits__ = ["Marc Concepcion"]
__maintainer__ = "Marc Concepcion"
__email__ = "marcanthonyconcepcion@gmail.com"
__status__ = "Demo"

import unittest
from decimal import Decimal

import database_records
from database_records import DatabaseRecords


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.expected_configuration = {'database': {'host': 'localhost', 'dbname': 'demo_database',
                                                    'user': 'user', 'password': 'password'}}
        self.expected_records = [{'index': 1, 'name': 'apple', 'weight': Decimal('200.03'), 'price': Decimal('40.05')},
                                 {'index': 2, 'name': 'banana', 'weight': Decimal('400.03'), 'price': Decimal('80.05')},
                                 {'index': 3, 'name': 'orange', 'weight': Decimal('193.57'), 'price': Decimal('45.75')},
                                 {'index': 4, 'name': 'grape', 'weight': Decimal('393.43'), 'price': Decimal('100.28')}]
        self.dut = DatabaseRecords.get()
        self.dut.bulk_edit('insert into `fruits` (`name`, `weight`, `price`) values (%(name)s, %(weight)s,%(price)s)',
                           [{key: record[key] for key in record if key != 'index'}
                            for record in self.expected_records])

    def tearDown(self):
        self.dut.edit('truncate table `fruits`')

    def test_config_in_database(self):
        self.assertEqual(database_records.HOST, self.expected_configuration['database']['host'])
        self.assertEqual(database_records.DBNAME, self.expected_configuration['database']['dbname'])
        self.assertEqual(database_records.USER, self.expected_configuration['database']['user'])
        self.assertEqual(database_records.PASSWORD, self.expected_configuration['database']['password'])

    def test_connection(self):
        self.dut.disconnect()
        self.assertFalse(self.dut.test_connection())
        with self.assertRaises(database_records.DatabaseError):
            next(self.dut.fetch('select %(number)s', {'number': 1}))
        self.dut.reconnect()
        self.assertTrue(self.dut.test_connection())

    def test_retrieve(self):
        expected_records = [tuple(record.values()) for record in self.expected_records]
        records = self.dut.fetch('select  * from `fruits`')
        index = 0
        for record in records:
            self.assertEqual(expected_records[index], record)
            index += 1
        self.assertEqual(len(expected_records), index)

    def test_update(self):
        self.expected_records[1 - 1]['name'] = 'Mandarin'
        self.dut.edit('update `fruits` set `name`= %(name)s where `index`= %(index)s',
                      {'name': 'Mandarin', 'index': 1})
        self.test_retrieve()

    def test_delete(self):
        del self.expected_records[3 - 1]
        self.dut.edit('delete from `fruits` where `name` = %(name)s', {'name': 'orange'})
        self.test_retrieve()

    def test_single_insert(self):
        new_record = {'index': 5, 'name': 'watermelon', 'weight': Decimal('555.55'), 'price': Decimal('70.00')}
        self.expected_records.append(new_record)
        self.dut.edit('insert into `fruits` (`name`, `weight`, `price`) values (%(name)s, %(weight)s,%(price)s)',
                      {key: new_record[key] for key in new_record if key != 'index'})
        self.test_retrieve()


if __name__ == '__main__':
    unittest.main()
