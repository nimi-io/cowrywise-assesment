
import threading
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from frontend_routes import frontend
from config import Config
from flask_migrate import Migrate
from models import db
from consumer import consume_messages

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(frontend)

with app.app_context():
    db.create_all()


consumer_thread = threading.Thread(target=consume_messages)
consumer_thread.daemon = True
consumer_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
