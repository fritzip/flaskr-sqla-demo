from flaskr.extensions import db

from flaskr.models.association_tables import post_tags


class Tag(db.Model):
    """A tag for a post."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    posts = db.relationship("Post", secondary="post_tags", back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.name}>"

    def __str__(self):
        return self.name
