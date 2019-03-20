import sqlite3

conn = sqlite3.connect('mybd.bd')
cursor = conn.cursor()


cursor.executescript("""
			BEGIN TRANSACTION;


            CREATE TABLE "orders" (
				`id`    INTEGER PRIMARY KEY,
				`client_name`    TEXT,
				`order_text`    TEXT
                );
                COMMIT;
                """)
conn.commit()
