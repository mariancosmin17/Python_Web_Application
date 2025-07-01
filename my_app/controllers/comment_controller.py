from flask import jsonify, request
from models import Comment,Post, db
#de adaugat Ai pentru comentariu

def add_comment_by_post_id(post_id):
    try:
        data = request.get_json()

        post = db.session.get(Post, post_id)
        if not post:
            raise ValueError("Post with id:"+ str(post_id) +" doesn't exist")

        content = data.get("content")
        if not content:
            return "Content cannot be empty", 400

        comment = Comment(content=data["content"], post_id=post_id)
        comment.save()

        return jsonify({
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at,
            'updated_at': comment.updated_at,
            'post_id':post_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

def get_comments_by_post_id(post_id):
    try:
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"message": f"Post with id {post_id} does not exist"}), 404

        comments = Comment.query.filter_by(post_id=post_id).all()
        if not comments:
            return jsonify([]), 200

        return jsonify([
            {
                "id": comment.id,
                "content": comment.content,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at,
                "post_id": comment.post_id
            } for comment in comments
        ]), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def get_comment_by_id(post_id, comment_id):
    try:
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"message": f"Post with id {post_id} does not exist"}), 404

        comment = db.session.get(Comment, comment_id)
        if not comment:
            return jsonify({"message": f"Comment with id {comment_id} does not exist"}), 404

        if comment.post_id != post_id:
            return jsonify({"message": f"Comment {comment_id} does not belong to post {post_id}"}), 400

        return jsonify({
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "post_id": comment.post_id
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def put_comment_by_id(post_id, comment_id):
    try:
        data = request.get_json()

        if not data or not len(data):
            return jsonify({"message": "Payload cannot be empty"}), 400

        content = data.get("content")
        if content is None or len(content.strip()) == 0:
            return jsonify({"message": "Comment content must not be empty"}), 400

        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"message": f"Post with id {post_id} does not exist"}), 404

        comment = db.session.get(Comment, comment_id)
        if not comment:
            return jsonify({"message": f"Comment with id {comment_id} does not exist"}), 404

        if comment.post_id != post_id:
            return jsonify({"message": f"Comment {comment_id} does not belong to post {post_id}"}), 400

        # Actualizează conținutul și timpul
        comment.content = content.strip()
        comment.updated_at = db.func.now()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return jsonify({
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "post_id": comment.post_id
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

def delete_comment_by_id(post_id, comment_id):
    try:
        post = db.session.get(Post, post_id)
        if not post:
            return jsonify({"message": f"Post with id {post_id} does not exist"}), 404

        comment = db.session.get(Comment, comment_id)
        if not comment:
            return jsonify({"message": f"Comment with id {comment_id} does not exist"}), 404

        if comment.post_id != post_id:
            return jsonify({"message": f"Comment {comment_id} does not belong to post {post_id}"}), 400

        db.session.delete(comment)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return jsonify({"message": "Comment deleted successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
