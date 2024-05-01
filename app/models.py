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
    
    borrowHistory= db.relationship('BorrowHistory', backref = 'user', lazy = 'dynamic')
    #profile = db.relationship('Profile', backref = 'user', lazy = 'dynamic')   

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
    

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(500), nullable = False)
    genre = db.Column(db.String(500), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    borrowHistory= db.relationship('BorrowHistory', backref = 'books', lazy = 'dynamic')
    def __repr__(self): #for debugging process
        return f'<books {self.id}: {self.title}>'
    
class BorrowHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)

    #user = db.relationship('User', backref=db.backref('borrow_history', lazy=True))
    #book = db.relationship('Books', backref=db.backref('borrow_history', lazy=True))

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))