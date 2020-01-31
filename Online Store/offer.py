from database import DataBase
from user import User
from datetime import date

class Offer:
    def __init__(self, id, title, description, price, seller_id, date=date.today(), active=1, buyer_id=0):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.seller_id = seller_id
        self.date = date
        self.active = active
        self.buyer_id = buyer_id
        

    @staticmethod
    def all():
        with DataBase() as db:
            rows = db.execute('SELECT * FROM offer').fetchall()
            return [Offer(*row) for row in rows]

    @staticmethod
    def sold_ads(id):
        with DataBase() as db:
            values = (id,)
            rows = db.execute('SELECT * FROM offer WHERE seller_id = ? AND active = 0', values).fetchall()
            return [Offer(*row) for row in rows]

    @staticmethod
    def find(id):
        with DataBase() as db:
            row = db.execute(
                'SELECT * FROM offer WHERE id = ?',
                (id,)
            ).fetchone()
            return Offer(*row)

    @staticmethod
    def find_by_seller_id(seller_id):
        with DataBase() as db:
            rows = db.execute(
                'SELECT * FROM offer WHERE seller_id = ?',
                (seller_id,)
            ).fetchall()
            return [Offer(*row) for row in rows]

    @staticmethod
    def seller_name_by_id(seller_id):
        with DataBase() as db:
            name = db.execute(
                'SELECT name FROM users WHERE id = ?',
                (seller_id,)
            ).fetchone()
            return name[0]

    @staticmethod
    def buyer_name_by_id(buyer_id):
        with DataBase() as db:
            name = db.execute(
                'SELECT name FROM users WHERE id = ?',
                (buyer_id,)
            ).fetchone()
            return name[0]

    @staticmethod
    def buyer_info_by_id(buyer_id):
        with DataBase() as db:
            row = db.execute(
                'SELECT * FROM users WHERE id = ?',
                (buyer_id,)
            ).fetchone()
            return User(*row)       


    def create(self):
        with DataBase() as db:
            values = (self.id, self.title, self.description, self.price,self.seller_id, self.date, self.active, self.buyer_id)
            db.execute('''
                INSERT INTO offer (id, title, description, price, seller_id, date, active, buyer_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', values)
            return self

    def buy(self, buyer_id):
        with DataBase() as db:
            values = (buyer_id, self.id)
            db.execute('''UPDATE offer SET active = 0, buyer_id = ? WHERE id = ?''', values)
            self.active = 0
            self.buyer_id = buyer_id
            return self

    def delete(self):
        with DataBase() as db:
            db.execute('DELETE FROM offer WHERE id = ?', (self.id,))

    def save(self):
        with DataBase() as db:
            values = (
                self.title,
                self.description,
                self.price,
                self.date,
                self.id
            )
            db.execute(
                '''UPDATE offer
                SET title = ?, description = ?, price = ?, date = ?
                WHERE id = ?''', values)
            return self