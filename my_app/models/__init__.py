from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .post import Post
from .comment import Comment