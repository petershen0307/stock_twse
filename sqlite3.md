SQLite
====

#### 1. 如何確認xxx的table是否存在於SQLite的database中?
* sqlite有一個特殊的table叫做*SQLITE_MASTER*格式如下<br />
*type*永遠是'table', *name*會是table的名字
```sql
CREATE TABLE sqlite_master (
    type TEXT,
    name TEXT,
    tbl_name TEXT,
    rootpage INTEGER,
    sql TEXT
);
```
* 列出所有table名字
```sql
SELECT name FROM sqlite_master
WHERE type='table'
ORDER BY name;
```
* 列出特定名字的table
```sql
SELECT name FROM sqlite_master WHERE type="table" AND name="table_name"
```


#### 參考資料
* [sqlite.org Q&A (7)](https://www.sqlite.org/faq.html)
* [How do I check in SQLite whether a table exists?](http://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists)
* [sqlite的系统表sqlite_master](http://blog.csdn.net/xingfeng0501/article/details/7804378)
