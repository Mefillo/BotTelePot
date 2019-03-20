import sqlite3
uname = "argruino"
conn = sqlite3.connect('mybd.bd')
cursor = conn.cursor()
try:

    cursor.execute("PRAGMA table_info(orders)")
    cursor.execute("SELECT * FROM orders")

    print(cursor.fetchall())
    conn.commit()
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for name in res:
        print (name[0])

except sqlite3.DatabaseError as err:
    print("Error: ", err)
print(cursor.fetchall())
