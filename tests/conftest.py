import os
import tempfile

import pytest
from datetime import datetime

from flaskr import create_app
from flaskr.extensions import db

from flaskr.models.post import Post
from flaskr.models.user import User
from flaskr.models.tag import Tag


@pytest.fixture(scope="function")
def app():
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()

    # create the app with common test config
    app = create_app(config_name="test", db_uri=f"sqlite:///{db_path}")

    # Assuming you have a create_app function to create your Flask app
    with app.app_context():
        db.drop_all()
        db.create_all()
        u1 = User(
            username="test",
            password="pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f",
        )
        db.session.add(u1)
        u2 = User(
            username="other",
            password="pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79",
        )
        db.session.add(u2)

        p1 = Post(title="test title", body="test\nbody", author_id=1, created_at=datetime(2018, 1, 1))
        p2 = Post(title="post2", body="body2", author_id=1, created_at=datetime(2018, 1, 1))
        t1 = Tag(name="tag1")
        t2 = Tag(name="tag2")
        p1.tags.append(t1)
        p1.tags.append(t2)
        p2.tags.append(t2)
        db.session.add(p1)
        db.session.add(p2)

        t3 = Tag(name="tag3")
        db.session.add(t3)

        db.session.commit()
        yield app
        db.session.remove()

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def session(app):
    with app.app_context():
        db.session.begin_nested()  # Start a nested transaction for each test
        yield db.session
        db.session.rollback()  # Rollback the nested transaction after each test


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post("/auth/login", data={"username": username, "password": password})

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
