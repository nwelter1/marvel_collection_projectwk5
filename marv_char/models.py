from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Imports for Secrets Module (Provided by Python)
import secrets 

# Imports for Login Manager and the UserMixin
from flask_login import LoginManager, UserMixin

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

    
class User(db.Model,UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy = True)
    
    def __init__(self, email, name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.name = name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)


    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been created and added to database!'


class Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(200))
    date_created = date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)




    def __init__(self,name, description, comics_appeared_in, super_power, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.user_token = user_token


    def __repr__(self):
        return f'The following Character has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()


# Creation of API Schema via the marshmallow package
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comics_appeared_in', 'super_power']



character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)
