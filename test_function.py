import unittest
from get_info import parse_stock_daily_info_specific_column


class TestCase(unittest.TestCase):
    def test_parsing_specific_columns(self):
        with open('test_table.html', mode='r', encoding='utf-8') as f:
            result = {'日期': ['105/06/01', '105/06/02', '105/06/03', '105/06/04', '105/06/06', '105/06/07', '105/06/08'],
                      '成交股數': ['511,371', '471,110', '207,014', '277,500', '322,703', '407,301', '211,470'],
                      '收盤價': ['31.75', '31.60', '31.60', '31.90', '31.75', '31.85', '32.00']}
            self.assertEqual(parse_stock_daily_info_specific_column(f.read()), result)


if '__main__' == __name__:
    unittest.main()
