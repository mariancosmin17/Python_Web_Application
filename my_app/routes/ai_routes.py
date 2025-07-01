from flask import Blueprint
from controllers.ai_controller import analyze_sentiment_ro

ai_routes = Blueprint("ai_routes", __name__)

@ai_routes.route('/sentiment/ro', methods=['POST'])
def sentiment_romania():
    return analyze_sentiment_ro()
