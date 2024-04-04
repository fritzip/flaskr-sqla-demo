from flaskr import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    comments = db.relationship("Comment", back_populates="author")
    posts = db.relationship("Post", back_populates="author")

    @hybrid_property
    def name(self):
        return self.username

    def __repr__(self):
        return f"<User {self.id}>"
