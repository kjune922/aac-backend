from flask import Blueprint, jsonify
from models import db, Category, Vocabulary

vocab_bp = Blueprint('vocab', __name__)

@vocab_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = []
    for cat in categories:
        result.append({
            "category_id": cat.category_id,
            "name": cat.name,
            "description": cat.description
        })
    return jsonify(result)


@vocab_bp.route('/vocabularies/<category_id>', methods=['GET'])
def get_vocabularies(category_id):
    vocab_list = Vocabulary.query.filter_by(category_id=category_id).all()
    result = []
    for v in vocab_list:
        result.append({
            "vocab_id": v.vocab_id,
            "text": v.text,
            "image_url": v.image_url
        })
    return jsonify(result)
