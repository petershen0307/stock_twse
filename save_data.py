import sqlite3
import os


def open_daily_table(stock_id):
    table_name = 'daily'
    db_folder = 'stock_db'
    if not os.path.exists(db_folder):
        os.mkdir(db_folder)
    # sqlite3.connect() will create xxx.db if xxx.db doesn't exist
    db_connection = sqlite3.connect(os.path.join(db_folder, str(stock_id) + '.db'))
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="{}"'.format(table_name))
    if db_cursor.fetchone() is None:
        # 'daily' table not exist in current db, create it
        db_cursor.execute('''CREATE TABLE {} (
                             Date DATETIME PRIMARY KEY,
                             Trading_Volume INTEGER,
                             Closing_Price REAL)'''.format(table_name))
    return db_connection, db_cursor, table_name


def insert_daily_info(stock_id, daily_info):
    # '成交股數', '收盤價'的值都是str, 再存到db的時候轉成int與float
    # daily_info should be a dict of [{'日期': str, '成交股數': str('123,123'), '收盤價': str('123.123')}]*n
    date = '日期'
    trading_volume = '成交股數'
    closing_price = '收盤價'
    db_connection, db_cursor, table_name = open_daily_table(stock_id)
    for every_date in daily_info:
        print(every_date)
        db_cursor.execute('''INSERT OR IGNORE INTO {table_name} (Date, Trading_Volume, Closing_Price)
                             VALUES ('{date}',
                             {trading_volume},
                             {closing_price})'''.format(table_name=table_name,
                                                        date=every_date[date],
                                                        trading_volume=int(every_date[trading_volume].replace(',', '')),
                                                        closing_price=float(every_date[closing_price])))
    db_connection.commit()
    db_connection.close()
