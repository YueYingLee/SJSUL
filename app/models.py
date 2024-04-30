from app import db
from datetime import datetime
from sqlalchemy.types import Boolean, Date, DateTime, Float, Integer, Text, Time, Interval
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#from flask_security import RoleMixin
from app import login


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String, nullable=False, default='guest')
    registered_role = db.Column(db.String, nullable=False)
    approved = db.Column(db.Boolean, nullable=False, default=False)  # Approval status for admin
    #roles = db.relationship('Role',  backref='user', lazy = 'dynamic')
    #roles = db.relationship('Role', secondary=roles_users, backref='roled')
    #roles = db.relationship('Role', secondary='user_roles', backref='users')
    profile = db.relationship('Profile', backref = 'user', lazy = 'dynamic')   

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        print("self.password is: ")
        print(self.password)
        print("input password is: ")
        print(password)
        return check_password_hash(self.password, password)

    def __repr__(self): #for debugging process
        return f'<user {self.id}: {self.username}>'
    
'''#class Role(db.Model, RoleMixin):
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True) #This represents the name of role 

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)
'''


'''class UserRoles (db.Model):
    db.Column('id', db.Integer, primary_key=True)
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
'''

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    genre = db.Column(db.String(500), nullable=False)
    count = db.Column(db.Integer, nullable=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))