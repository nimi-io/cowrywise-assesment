from flask import Blueprint, jsonify, request
from models import db, Book, User, Borrow
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__)

@admin.route('/api/v1/books', methods=['POST'])
def add_book():
    data = request.json
    
    check_book = Book.query.filter_by(title=data['title'], author=data['author']).first()

    if check_book:
        return jsonify({'message': 'Book already exists'}), 409

    new_book = Book(
        title=data['title'],
        author=data['author'],
        publisher=data['publisher'],
        category=data['category'],
        is_available=True
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added'}), 201

@admin.route('/api/v1/books/<int:id>', methods=['DELETE'])
def remove_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book removed'}), 200

@admin.route('/api/v1/users', methods=['GET'])
def list_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'email': user.email, 'firstname': user.firstname, 'lastname': user.lastname} for user in users]
    return jsonify(user_list), 200

@admin.route('/api/v1/users/borrowed-books', methods=['GET'])
def list_users_borrowed_books():
    borrows = Borrow.query.all()
    borrowed_list = [{'user_id': borrow.user_id, 'book_id': borrow.book_id, 'borrow_date': borrow.borrow_date, 'return_date': borrow.return_date} for borrow in borrows]
    return jsonify(borrowed_list), 200

@admin.route('/api/v1/books/unavailable', methods=['GET'])
def unavailable_books():
    books = Book.query.filter_by(is_available=False).all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'publisher': book.publisher, 'category': book.category} for book in books]
    return jsonify(book_list), 200
