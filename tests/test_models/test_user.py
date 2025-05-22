import pytest
from app.models import User
from app import db

@pytest.fixture(scope="module")
def user_data():
    return {
        "username": "testuser",
        "password": "testpassword",
        "is_admin": False,
        "is_active": True
    }

def test_user_creation(user_data, app):
    with app.app_context():
        user = User(**user_data)
        user.add()
        user_from_db = db.session.get(User, user.id)

        assert user_from_db is not None
        assert user_from_db.id is not None
        assert user_from_db.username == user_data["username"]
        assert user_from_db.is_admin == user_data["is_admin"]
        assert user_from_db.is_active == user_data["is_active"]

def test_user_update(user_data, app):
    with app.app_context():
        user = User(**user_data)
        user.add()

        user.is_active = False
        user.update()

        updated_user = db.session.get(User, user.id)

        assert updated_user.is_active == False

def test_user_deletion(user_data, app):
    with app.app_context():
        user = User(**user_data)
        user.add()

        user.delete()
        deleted_user = db.session.get(User, user.id)
        assert deleted_user is None

def test_user_repr(user_data, app):
    with app.app_context():
        user = User(**user_data)
        user.add()

        assert repr(user) == f"<User {user.username}>"

def test_set_password(user_data, app):
    with app.app_context():
        user = User(**user_data)
        old_password = user.password
        user.add()
        new_password = "newpassword"
        user.set_password(new_password)
        user.update()

        user_from_db = db.session.get(User, user.id)

        assert user_from_db.check_password(new_password) == True
        assert user_from_db.check_password(old_password) == False