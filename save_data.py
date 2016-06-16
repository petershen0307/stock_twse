import sqlite3


conn = sqlite3.connect('test.db')
c = conn.cursor()

# c.execute('''create table test
#         (id int primary key,
#         sort int,
#         name text)''')

# c.execute('''insert into test values (1, 1, 'kk')''')

c.execute('SELECT name FROM test ORDER BY sort')
print(c.fetchone())
print(c.fetchone())
c.execute('SELECT * FROM test')
print(c.fetchall())
c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="test"')
print(c.fetchone())
conn.commit()
conn.close()


def initial_daily_table(stock_id):
    table_name = 'daily'
    # sqlite3.connect() will create xxx.db if xxx.db doesn't exist
    db_connection = sqlite3.connect(str(stock_id) + '.db')
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="{}"'.format(table_name))
    if db_cursor.fetchone() is None:
        # 'daily' table not exist in current db, create it
        db_cursor.execute('''CREATE TABLE daily (
                             Date DATETIME,
                             Trading_Volume INTEGER,
                             Closing_Price INTEGER)''')
