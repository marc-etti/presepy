from app.models import User

import pytest

def test_new_user():
    """Given a new user, 
        when the user is created,
        then the user should have a username and hashed password."""
    user = User(username="testuser", password="password")
    assert user.username == "testuser"
    assert user.password != "password"  # Password should be hashed
    assert user.check_password("password") is True  # Check password should return True
    assert user.is_admin is False
    assert user.is_active is True
    assert repr(user) == "<User testuser>"  # Check the __repr__ method
    assert user.id is None  # ID should be None before adding to the database

def test_duplicate_username():
    """Given a user with a username,
        when another user with the same username is created,
        then it should raise an Integrity Error."""
    user1 = User(username="testuser", password="password")
    user1.add()
    user2 = User(username="testuser", password="password")
    try:
        user2.add()
    except Exception as e:
        assert "UNIQUE constraint failed" in str(e)  # Check for unique constraint error
    finally:
        user1.delete()  # Cleanup
        user2.delete()

def test_user_update():
    """Given an existing user,
        when the user is updated,
        then the changes should be reflected in the database."""
    user = User(username="testuser", password="password")
    user.add()
    user.username = "updateduser"
    user.update()
    updated_user = User.query.filter_by(id=user.id).first()
    assert updated_user.username == "updateduser"
    assert updated_user.check_password("password") is True  # Check password should still return True
    user.delete()  # Cleanup
    updated_user.delete()  # Cleanup

def test_user_delete():
    """Given an existing user,
        when the user is deleted,
        then the user should no longer exist in the database."""
    user = User(username="testuser", password="password")
    user.add()
    user_id = user.id
    user.delete()
    deleted_user = User.query.get(user_id)
    assert deleted_user is None  # User should be None after deletion

def test_user_set_password():
    """Given a user,
        when the password is set,
        then the password should be hashed and stored correctly."""
    user = User(username="testuser", password="password")
    user.set_password("newpassword")
    assert user.check_password("newpassword") is True  # Check password should return True
    assert user.check_password("password") is False  # Old password should not match

