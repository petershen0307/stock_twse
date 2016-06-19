import unittest
import os
import get_info
import save_data


class TestCaseParser(unittest.TestCase):
    def open_test_data(self):
        test_file_path = os.path.join('test_data', 'test_table.html')
        if not os.path.exists(test_file_path):
            raise FileNotFoundError(test_file_path, 'can not find test file')
        return open(test_file_path, mode='r', encoding='utf-8')

    def test_parsing_columns_first(self):
        with self.open_test_data() as f:
            result = {'日期': ['105/06/01', '105/06/02', '105/06/03', '105/06/04', '105/06/06', '105/06/07', '105/06/08'],
                      '成交股數': ['511,371', '471,110', '207,014', '277,500', '322,703', '407,301', '211,470'],
                      '收盤價': ['31.75', '31.60', '31.60', '31.90', '31.75', '31.85', '32.00']}
            self.assertEqual(get_info.parse_stock_daily_info_column_first(f.read()), result)

    def test_parsing_row_first(self):
        with self.open_test_data() as f:
            result = [{'日期': '105/06/01', '成交股數': '511,371', '收盤價': '31.75'},
                      {'日期': '105/06/02', '成交股數': '471,110', '收盤價': '31.60'},
                      {'日期': '105/06/03', '成交股數': '207,014', '收盤價': '31.60'},
                      {'日期': '105/06/04', '成交股數': '277,500', '收盤價': '31.90'},
                      {'日期': '105/06/06', '成交股數': '322,703', '收盤價': '31.75'},
                      {'日期': '105/06/07', '成交股數': '407,301', '收盤價': '31.85'},
                      {'日期': '105/06/08', '成交股數': '211,470', '收盤價': '32.00'}]
            self.assertEqual(get_info.parse_stock_daily_info_row_first(f.read()), result)


class TestCaseDB(unittest.TestCase):
    def test_db_insert(self):
        stock_id = 1234
        test_data = [{'日期': '105/06/01', '成交股數': '511,371', '收盤價': '31.75'},
                     {'日期': '105/06/02', '成交股數': '471,110', '收盤價': '31.60'},
                     {'日期': '105/06/03', '成交股數': '207,014', '收盤價': '31.60'},
                     {'日期': '105/06/04', '成交股數': '277,500', '收盤價': '31.90'},
                     {'日期': '105/06/06', '成交股數': '322,703', '收盤價': '31.75'},
                     {'日期': '105/06/07', '成交股數': '407,301', '收盤價': '31.85'},
                     {'日期': '105/06/08', '成交股數': '211,470', '收盤價': '32.00'}]
        save_data.insert_daily_info(stock_id, test_data)
        db_connection, db_cursor, db_table_name = save_data.open_daily_table(stock_id)
        db_cursor.execute('SELECT * FROM {}'.format(db_table_name))
        print(db_cursor.fetchone())
        db_connection.close()


if '__main__' == __name__:
    unittest.main()
