from datetime import datetime
from . import db


class Post(db.Model):
    __tablename__ = 'posts' # special property

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    hearts = db.Column(db.Integer, default=0)
    sentiment = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self): # representation of how the object will be displayed
        return f'<Post {self.id}: {self.title}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
