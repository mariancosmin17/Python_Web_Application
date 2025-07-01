from datetime import datetime

from . import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    sentiment = db.Column(db.Text)
    post_id = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'post_id': self.post_id
        }

    def __repr__(self):
        return f'<Comment {self.id}: {self.content}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
