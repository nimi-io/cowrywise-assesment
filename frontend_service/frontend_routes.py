from flask import Blueprint, jsonify, request
from models import  BorrowSchema, ReturnBookSchema, UserSchema, db, Book, User, Borrow
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError

# from forms import UserForm 

frontend = Blueprint('frontend', __name__)

@frontend.route('/api/v1/users/enroll', methods=['POST'])
def enroll_user():    
    schema = UserSchema()  
    try:    
      
        data = schema.load(request.json)


        check_user = User.query.filter_by(email=data['email']).first()
        if check_user:
            return jsonify({'message': 'User already Enrolled'}), 409


        new_user = User(
            email=data['email'],
            firstname=data['firstname'],
            lastname=data['lastname']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User enrolled'}), 201
     
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400  
    except Exception as e:
        return jsonify({'message': str(e)}), 50

@frontend.route('/api/v1/books', methods=['GET'])
def list_books():
    books = Book.query.filter_by(is_available=True).all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'publisher': book.publisher, 'category': book.category} for book in books]
    return jsonify(book_list), 200

@frontend.route('/api/v1/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'publisher': book.publisher,
        'category': book.category
    }), 200

@frontend.route('/api/v1/books/borrow/<int:id>', methods=['POST'])
def borrow_book(id):
  schema = BorrowSchema()
  try:
        data = schema.load(request.json)
        book = Book.query.get_or_404(id)
        if not book.is_available:
            return jsonify({'message': 'Book not available'}), 400

        book.is_available = False
        new_borrow = Borrow(
            user_id=data['user_id'],
            book_id=book.id,
            days=data['days'],
            borrow_date=datetime.utcnow(),
            return_date=datetime.utcnow() + timedelta(days=data['days'])
        )
        db.session.add(new_borrow)
        db.session.commit()
        return jsonify({'message': 'Book borrowed successfully'}), 200
  except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
  except Exception as e:
        return jsonify({'message': str(e)}), 500

@frontend.route('/api/v1/books/return/<int:id>', methods=['POST'])
def return_book(id):
    schema = ReturnBookSchema()
    try:
        data = schema.load(request.json)
        book = Book.query.get_or_404(id)

        borrow = Borrow.query.filter_by(book_id=book.id, user_id=data['user_id']).first()
        if not borrow:
            return jsonify({'message': 'Book not borrowed by this user'}), 400

        book.is_available = True
        db.session.delete(borrow)
        db.session.commit()

        return jsonify({'message': 'Book returned successfully'}), 200
    
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500