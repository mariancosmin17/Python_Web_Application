from flask import jsonify, request
from models import Post, db
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from services import (
    create_post, get_post, get_all_posts,
    update_post, delete_post,
    like_post_by_id, love_post_by_id,
    get_post_likes, get_post_hearts)

model_name = "clapAI/modernBERT-base-multilingual-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def add_post():
    try:
        data = request.get_json()

        content = data.get("content")
        content2 = content.strip()
        if not content:
            return "Content cannot be empty", 400
        if len(content) < 10:
            return "Content must be at least 10 characters long.", 400

        result = sentiment_pipeline(content2)[0]

        post = Post(content=data["content"],sentiment=result["label"])
        post.save()

        return jsonify({
            'id': post.id,
            'content': post.content,
            'sentiment': post.sentiment,
            'likes': post.likes,
            'hearts': post.hearts,
            'created_at': post.created_at
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


def get_post_by_id(post_id):
    post = get_post(post_id)
    if post:
        return jsonify(post), 200
    return jsonify({"message": "Post not found"}), 404


def get_posts():
    posts = get_all_posts()
    if not posts:
        return jsonify([]), 200
    return jsonify(posts), 200


def put_post_by_id(post_id):
    try:
        data = request.get_json()
        updated_post = update_post(post_id, data)
        return jsonify(updated_post), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete_post_by_id(post_id):
    try:
        result = delete_post(post_id)
        if result.get("message") == "Post not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def like_post(post_id):
    result = like_post_by_id(post_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Post not found"}), 404


def get_likes(post_id):
    result = get_post_likes(post_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Post not found"}), 404


def love_post(post_id):
    result = love_post_by_id(post_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Post not found"}), 404


def get_hearts(post_id):
    result = get_post_hearts(post_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Post not found"}), 404
