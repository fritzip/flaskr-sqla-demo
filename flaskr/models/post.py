from datetime import datetime
from flaskr.extensions import db
from sqlalchemy.sql import func

from flaskr.models.tag import Tag
from flaskr.models.user import User
from flaskr.models.comment import Comment
from flaskr.models.association_tables import post_tags


class Post(db.Model):
    """A post written by a user."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(300))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    author = db.relationship("User", back_populates="posts")
    tags = db.relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = db.relationship("Comment", back_populates="post")

    def __repr__(self):
        return f"<Post {self.id}>"
