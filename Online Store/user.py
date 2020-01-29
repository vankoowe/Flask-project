from database import DataBase
import hashlib
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User(object):

    def __init__(self, id, email, password, username, address, phone_number):
        self.id = id
        self.email = email
        self.password = password
        self.username = username
        self.address = address
        self.phone_number = phone_number

    def create(self):
        with DataBase() as db:
            values = (self.email,
                      self.password,
                      self.name,
                      self.adress,
                      self.phone)
            db.execute('''INSERT INTO users (email, password, username, address, phone_number)
            	VALUES (?, ?, ?, ?, ?)''', values)
            return self

    @staticmethod    
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()
    
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
        s = Serializer(SECRET_KEY, expires_in=600)
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