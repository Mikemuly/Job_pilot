import sqlite3

conn = sqlite3.connect("jobpilot.db")
conn.execute("DROP TABLE IF EXISTS application")
conn.commit()
print(conn.execute("select name from sqlite_master where type='table'").fetchall())