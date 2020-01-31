from database import DataBase
import hashlib
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User(object):

    def __init__(self, id, email, password, name, address, phone_number):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.address = address
        self.phone_number = phone_number

    def create(self):
        with DataBase() as db:
            values = (self.id,
                        self.email,
                        self.password,
                        self.name,
                        self.address,
                        self.phone_number)
            db.execute('''INSERT INTO users (id, email, password, name, address, phone_number)
            	VALUES (?, ?, ?, ?, ?, ?)''', values)
            return self

    @staticmethod    
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def get_user(id):
        with DataBase() as db:
            values = db.execute(
                '''
                    SELECT * FROM users
                    WHERE id=?
                ''', (id,)
            ).fetchone()

        return User(*values)

    @staticmethod
    def get_user_by_email(email):
        with DataBase() as db:
            id = db.execute(
                '''
                    SELECT id FROM users
                    WHERE email=?
                ''', (email,)).fetchone()

        return id[0]

    @staticmethod
    def find_by_email(email):
        with DataBase() as db:
            row = db.execute('SELECT * FROM users WHERE email = ?', (email, )).fetchone()
            return User(*row)

    @staticmethod
    def find_by_name(name):
        if not name:
            return None
        with DataBase() as db:
            row = db.execute('SELECT * FROM users WHERE name = ?', (name, )).fetchone()
            return User(*row)

    def generate_token(self):
        s = Serializer(SECRET_KEY, expires_in=300)
        return s.dumps({'name' : self.name})
    
    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return True