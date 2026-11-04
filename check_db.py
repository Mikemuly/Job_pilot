import sqlite3

conn = sqlite3.connect("jobpilot.db")
rows = conn.execute("select name from sqlite_master where type ='table'").fetchall()
print (rows)
