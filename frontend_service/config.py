import os
import pika

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5433/library_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
    @staticmethod
    def get_rabbitmq_connection():
        parameters = pika.URLParameters(Config.RABBITMQ_URL)
        connection = pika.BlockingConnection(parameters)
        return connection
