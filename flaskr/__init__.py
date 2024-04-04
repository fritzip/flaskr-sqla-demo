import os
from dotenv import load_dotenv
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flaskr.extensions import db, migrate, login_manager
from flaskr.config import DevelopmentConfig, TestConfig, ProductionConfig

# Important references for setup, do not remove even if unused
from flaskr.models.post import Post
from flaskr.models.comment import Comment
from flaskr.models.tag import Tag
from flaskr.models.user import User
from flaskr.models.association_tables import post_tags


def create_app(config_name="dev", db_uri=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    # Select the appropriate configuration based on the config_name parameter
    if config_name == "dev":
        print("Using development configuration.")
        app.config.from_object(DevelopmentConfig)
    elif config_name == "test":
        print("Using test configuration.")
        app.config.from_object(TestConfig)
        if db_uri:
            app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    elif config_name == "prod":
        print("Using production configuration.")
        app.config.from_object(ProductionConfig)
    else:
        raise ValueError("Invalid configuration name. Use 'dev', 'test', or 'prod'.")

    # initialize the app with the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # ensure the database directory exists
    try:
        database_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
        database_path = Path(database_uri.replace("sqlite:///", ""))
        database_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating database directory: {e}")

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
