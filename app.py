from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from models import db


jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from routes.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/api/v1/chat')
    

    from routes.vocab import vocab_bp
    app.register_blueprint(vocab_bp, url_prefix='/api/v1')
    
    return app

app = create_app()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
