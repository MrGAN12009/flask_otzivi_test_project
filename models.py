from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    replies = db.relationship('Reply', backref='review', cascade='all, delete-orphan', lazy='dynamic')


    def to_dict(self):
        return {
        'id': self.id,
        'author': self.author,
        'rating': self.rating,
        'content': self.content,
        'created_at': self.created_at.isoformat(),
        'replies': [r.to_dict() for r in self.replies.order_by(Reply.created_at.asc())]
        }


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def to_dict(self):
        return {
        'id': self.id,
        'review_id': self.review_id,
        'author': self.author,
        'content': self.content,
        'created_at': self.created_at.isoformat()
        }
