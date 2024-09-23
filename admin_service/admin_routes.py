from flask import Blueprint, jsonify, request
from models import BookSchema, db, Book, User, Borrow
from datetime import datetime, timedelta
# from redis import Redis 
import pika
import json
import threading

admin = Blueprint('admin', __name__)

# redis_client = Config.redis_client
# redis_client = Redis(host='redis', port=6379)




def publish_message(channel_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue=channel_name)
    channel.basic_publish(exchange='', routing_key=channel_name, body=json.dumps(message))
    connection.close()

@admin.route('/api/v1/books', methods=['POST'])
def add_book():
    schema = BookSchema()
    try:
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

        publish_message('book_updates', {
            'action': 'add',
            'book_id': new_book.id,
            'title': new_book.title,
            'author': new_book.author,
            'publisher': new_book.publisher,
            'category': new_book.category
        })

        return jsonify({'message': 'Book added'}), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@admin.route('/api/v1/books/<int:id>', methods=['DELETE'])
def remove_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()

    publish_message('book_updates', {
        'action': 'remove',
        'book_id': id
    })

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
