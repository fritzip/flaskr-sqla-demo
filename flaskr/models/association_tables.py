from flaskr.extensions import db

post_tags = db.Table(
    "post_tags",
    db.Column(
        "post_id",
        db.Integer,
        db.ForeignKey("post.id", ondelete="CASCADE"),
    ),
    db.Column(
        "tag_id",
        db.Integer,
        db.ForeignKey("tag.id", ondelete="CASCADE"),
    ),
    db.UniqueConstraint("post_id", "tag_id"),
)
