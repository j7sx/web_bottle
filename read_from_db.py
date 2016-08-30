import sqlite3

db = sqlite3.connect("site.db")
cur = db.cursor()
cur.execute("select * from users")
res = cur.fetchall()
for i in res:
    for j in i:
        print j
db.close()