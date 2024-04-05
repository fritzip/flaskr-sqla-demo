import pytest

from flaskr.extensions import db

from flaskr.models.post import Post
from flaskr.models.user import User
from flaskr.models.tag import Tag
from flaskr.models.association_tables import post_tags


def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"test title" in response.data
    assert b"by test on 2018-01-01" in response.data
    assert b"test\nbody" in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize("path", ("/create", "/1/update", "/1/delete"))
def test_login_required(client, path):
    response = client.post(path)
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        p = Post.query.get(1)
        p.author_id = 2
        db.session.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize("path", ("/3/update", "/3/delete"))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "body": ""})

    with app.app_context():
        count = db.session.query(Post).count()
        assert count == 3


def test_update(client, auth, app):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", "body": ""})

    with app.app_context():
        post = Post.query.get(1)
        assert post.title == "updated"


@pytest.mark.parametrize("path", ("/create", "/1/update"))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        post = Post.query.get(1)
        assert post is None


def test_create_post_with_tag(client, auth, app):
    auth.login()
    with app.app_context():
        nb_tags_before = db.session.query(Tag).count()
        client.post("/create", data={"title": "created", "body": "body", "tags": "new_tag1, new_tag2"})
        nb_tags_after = db.session.query(Tag).count()
        assert nb_tags_after == nb_tags_before + 2


def test_update_post_with_tag(client, auth, app):
    auth.login()
    with app.app_context():
        client.post("/1/update", data={"title": "updated", "body": "body", "tags": "new_tag1, new_tag2, new_tag3"})
        assert len(db.session.query(Post).get(1).tags) == 3


def test_delete_post_with_tag(client, auth, app):
    auth.login()
    with app.app_context():
        assert db.session.query(post_tags).count() > 0
        assert len(db.session.query(Tag).all()) == 3
        client.post("/1/delete")
        assert db.session.query(post_tags).count() == 1
        assert len(db.session.query(Post).all()) == 1
        # check no tags are deleted
        assert len(db.session.query(Tag).all()) == 3


def test_delete_all_tags(client, auth, app):
    auth.login()
    with app.app_context():
        assert len(db.session.query(Tag).all()) == 3
        # delete all tags
        tags = db.session.query(Tag).all()
        for tag in tags:
            db.session.delete(tag)
        db.session.commit()

        assert len(db.session.query(Tag).all()) == 0
        assert len(db.session.query(post_tags).all()) == 0
        assert len(db.session.query(Post).all()) == 2
        assert len(db.session.query(Post).get(1).tags) == 0


def test_create_post_with_existing_tag(client, auth, app):
    auth.login()
    with app.app_context():
        nb_tags_before = db.session.query(Tag).count()
        client.post("/create", data={"title": "created", "body": "body", "tags": "tag1, tag2"})
        nb_tags_after = db.session.query(Tag).count()
        assert nb_tags_after == nb_tags_before


def test_delete_user_set_null_post(client, auth, app):
    with app.app_context():
        #  get a post from the user
        post = Post.query.filter(Post.author_id == 1).first()
        post_id = post.id
        assert post is not None

        # delete user
        db.session.delete(db.session.query(User).get(1))
        db.session.commit()

        # check that the post has been deleted
        post = db.session.query(Post).get(post_id)
        assert post is not None
        assert post.author_id is None
        # check that the user has been deleted
        assert db.session.query(User).get(1) is None


# expected failure - known bug
@pytest.mark.xfail
def test_post_updated_at_updated(client, auth, app):
    auth.login()
    with app.app_context():
        post = Post.query.get(1)
        updated_at = post.updated_at
        client.post("/1/update", data={"title": "updated", "body": "body"})
        post = Post.query.get(1)
        assert post.updated_at > updated_at
        assert post.created_at < post.updated_at
