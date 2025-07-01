from flask import Blueprint
from controllers.comment_controller import *

comment_routes = Blueprint("comment_routes", __name__)

@comment_routes.route('/posts/<int:post_id>/comment', methods=['POST'])
def create_comment(post_id):
    return add_comment_by_post_id(post_id)

@comment_routes.route('/posts/<int:post_id>/comments', methods=['GET'])
def list_comments(post_id):
    return get_comments_by_post_id(post_id)

@comment_routes.route('/posts/<int:post_id>/comment/<int:comment_id>', methods=['GET'])
def list_comment_by_id(post_id,comment_id):
    return get_comment_by_id(post_id,comment_id)

@comment_routes.route('/posts/<int:post_id>/comment/<int:comment_id>', methods=['PUT'])
def update_comment_by_id(post_id,comment_id):
    return put_comment_by_id(post_id,comment_id)

@comment_routes.route('/posts/<int:post_id>/comment/<int:comment_id>', methods=['DELETE'])
def remove_comment_by_id(post_id,comment_id):
    return delete_comment_by_id(post_id,comment_id)