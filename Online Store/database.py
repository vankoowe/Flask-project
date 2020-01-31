import sqlite3

DataBase_NAME = 'store.db'

conn = sqlite3.connect(DataBase_NAME)

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS users 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        phone_number INTEGER NOT NULL
    )
''')

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS offer
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        seller_id INTEGER,
        date TEXT NOT NULL,
        active INTEGER NOT NULL,
        buyer_id INTEGER NOT NULL,
        FOREIGN KEY(buyer_id) REFERENCES users(id),
        FOREIGN KEY(seller_id) REFERENCES users(id)
    )
''')

conn.commit()

class DataBase:
    def __enter__(self):
        self.conn = sqlite3.connect(DataBase_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()