from flask import Flask
from routes.post_routes import posts_routes
from config import Config
from models import db
from routes.ai_routes import ai_routes
from routes.comment_routes import comment_routes
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(posts_routes)
    app.register_blueprint(ai_routes)
    app.register_blueprint(comment_routes)
    app.config.from_object(Config)
    db.init_app(app)

    return app