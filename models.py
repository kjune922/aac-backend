from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    message_id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String, default="text")  # 예: text, aac
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_ai = db.Column(db.Boolean, default=False)

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    vocabularies = db.relationship('Vocabulary', backref='category', lazy=True)


class Vocabulary(db.Model):
    __tablename__ = 'vocabularies'

    vocab_id = db.Column(db.String, primary_key=True)
    text = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    category_id = db.Column(db.String, db.ForeignKey('categories.category_id'), nullable=False)
