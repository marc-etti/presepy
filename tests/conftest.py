import pytest
from app import create_app, db
from config import TestConfig

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.from_object(TestConfig)
    with app.app_context():
        yield app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="session")
def _db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()