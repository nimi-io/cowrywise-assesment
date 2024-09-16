from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    borrowed_books = db.relationship('Borrow', backref='user', lazy=True)
class UserSchema(Schema):
    email = fields.Email(required=True, error_messages={'required': 'Email is required.'})
    firstname = fields.Str(required=True, error_messages={'required': 'First name is required.'})
    lastname = fields.Str(required=True, error_messages={'required': 'Last name is required.'})

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    borrowings = db.relationship('Borrow', backref='book', lazy=True)

class BookSchema(Schema):
    title = fields.Str(required=True, error_messages={'required': 'Title is required.'})
    author = fields.Str(required=True, error_messages={'required': 'Author is required.'})
    publisher = fields.Str(required=True, error_messages={'required': 'Publisher is required.'})
    category = fields.Str(required=True, error_messages={'required': 'Category is required.'})
    available = fields.Boolean(default=True)

class Borrow(db.Model):
    __tablename__ = 'borrows'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    days = db.Column(db.Integer, nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)

class BorrowSchema(Schema):
    user_id = fields.Int(required=True, error_messages={'required': 'User ID is required.'})
    # book_id = fields.Int(required=True, error_messages={'required': 'Book ID is required.'})
    days = fields.Int(required=True, error_messages={'required': 'Number of days is required.'})

class ReturnBookSchema(Schema):
    user_id = fields.Int(required=True, error_messages={'required': 'User ID is required.'})
