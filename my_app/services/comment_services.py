from models import Post,Comment, db
def get_comments_raw_by_post_id(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return [
        {
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
            "post_id": comment.post_id
        } for comment in comments
    ]
