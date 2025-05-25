from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ChatMessage
from services.llm import call_ai_model
from datetime import datetime
import uuid

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/messages', methods=['POST'])
@jwt_required()
def post_chat_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get("content")
    message_type = data.get("message_type", "text")

    # 1. 사용자 메시지 저장
    user_msg = ChatMessage(
        user_id=user_id,
        content=content,
        message_type=message_type,
        created_at=datetime.utcnow(),
        is_ai=False
    )
    db.session.add(user_msg)
    db.session.commit()

    # 2. AI 응답 생성
    ai_response = call_ai_model(content)

    # 3. AI 메시지 저장
    ai_msg = ChatMessage(
        user_id=user_id,
        content=ai_response,
        message_type="text",
        created_at=datetime.utcnow(),
        is_ai=True
    )
    db.session.add(ai_msg)
    db.session.commit()

    return jsonify({
        "message_id": user_msg.message_id,
        "content": user_msg.content,
        "created_at": user_msg.created_at,
        "is_ai": user_msg.is_ai,
        "response": {
            "message_id": ai_msg.message_id,
            "content": ai_msg.content,
            "created_at": ai_msg.created_at,
            "is_ai": ai_msg.is_ai
        }
    })

@chat_bp.route('/messages', methods=['GET'])
@jwt_required()
def get_chat_messages():
    user_id = get_jwt_identity()
    limit = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))

    query = (
        ChatMessage.query
        .filter_by(user_id=user_id)
        .order_by(ChatMessage.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    messages = []
    for msg in query.all():
        messages.append({
            "message_id": msg.message_id,
            "content": msg.content,
            "message_type": msg.message_type,
            "created_at": msg.created_at.isoformat(),
            "is_ai": msg.is_ai
        })

    return jsonify({
        "messages": messages,
        "total_count": ChatMessage.query.filter_by(user_id=user_id).count()
    })
