import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flaskr.extensions import db, migrate, login_manager

# Important references for setup, do not remove even if unused
from flaskr.models.post import Post
from flaskr.models.comment import Comment
from flaskr.models.tag import Tag
from flaskr.models.user import User
from flaskr.models.association_tables import post_tags


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    if not os.getenv("FLASK_ENV"):
        load_dotenv(".flaskenv")

    database_path = os.path.join(app.instance_path, "flaskr.sqlite")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=database_path,
    )

    # initialize the app with the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ensure the database exists
    with app.app_context():
        db.create_all()

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # apply the blueprints to the app
    from flaskr import auth
    from flaskr import blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
