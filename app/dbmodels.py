#name (db here) depends on the definition in init
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), unique = True)
    password = db.Column(db.String(128))
    friends = db.relationship('Friends',backref="user",lazy='dynamic')
    """Define the class constructor"""
    def __init__(self, email, password):
        self.email = email
        self.password = password
    def __str__(self):
        return self.email + ' ' + self.password + ' ' + str(self.id)

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    age = db.Column(db.Integer)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'))
    def __init__(self, name, address, age, user_id):
        self.name = name
        self.address = address
        self.age = age
        self.user_id = user_id
    def __str__(self):
        return self.name + ' ' + self.address + ' ' + str(self.age) + ' ' + str(self.user_id)