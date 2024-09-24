import pika
import json
from models import Book, db
from config import Config

def consume_messages():
    connection = Config.get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue='book_updates')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"Received message: {data}")

        if data['action'] == 'add':
            existing_book = Book.query.filter_by(id=data['book_id']).first()
            if not existing_book:
                new_book = Book(
                    id=data['book_id'],
                    title=data['title'],
                    author=data['author'],
                    publisher=data['publisher'],
                    category=data['category'],
                    is_available=True
                )
                db.session.add(new_book)
                db.session.commit()
                print(f"New book added: {new_book.title}")
            else:
                print(f"Book {data['title']} already exists.")
        elif data['action'] == 'remove':
            book = Book.query.filter_by(id=data['book_id']).first()
            if book:
                db.session.delete(book)
                db.session.commit()
                print(f"Book removed: {book.title}")
            else:
                print(f"Book {data['book_id']} not found for removal.")

    channel.basic_consume(queue='book_updates', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages...')
    channel.start_consuming()
