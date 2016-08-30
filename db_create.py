#--*--coding: utf-8--*--
#!/usr/bin/python2

import sqlite3

db = sqlite3.connect("site.db")
cur = db.cursor()
cur.execute("create table if not exists users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
login varchar(100), password varchar(100), email varchar(100), last_ip varchar(100))")
db.commit()
db.close()