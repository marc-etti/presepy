import pytest
from app.models.user import User
from app import db

@pytest.fixture(autouse=True)
def setup_database(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def user():
    user = User(username="testuser", password="testpass", is_admin=True)
    yield user
    db.session.rollback()

def test_user_repr(user, app):
    with app.app_context():
        assert repr(user) == "<User testuser>"

def test_user_password_hashing(user, app):
    with app.app_context():
        assert user.password != "testpass"
        assert user.check_password("testpass")
        assert not user.check_password("wrongpass")

def test_user_set_password(user, app):
    with app.app_context():
        user.set_password("newpass")
        assert user.check_password("newpass")
        assert not user.check_password("testpass")

def test_user_add_and_query(user, app):
    with app.app_context():
        user.add()
        queried = User.query.filter_by(username="testuser").first()
        assert queried is not None
        assert queried.username == "testuser"
        assert queried.is_admin is True
        assert queried.is_active is True
    # Cleanup
    queried.delete()

def test_user_update(user, app):
    with app.app_context():
        user.add()
        user.is_active = False
        user.update()
        updated = User.query.filter_by(username="testuser").first()
        assert updated.is_active is False
        # Cleanup
        updated.delete()

def test_user_delete(user, app):
    with app.app_context():
        user.add()
        user_id = user.id
        user.delete()
        deleted = db.session.get(User, user_id)
        assert deleted is None

def test_user_unique_username_constraint(user, app):
    with app.app_context():
        user.add()
        duplicate = User(username="testuser", password="anotherpass")
        db.session.add(duplicate)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()
        # Cleanup
        User.query.filter_by(username="testuser").first().delete()