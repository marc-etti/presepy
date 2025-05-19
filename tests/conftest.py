import pytest
from app import create_app
from app import db

@pytest.fixture(scope='session')
def app():
    """
    Create a Flask application instance for testing.
    """
    app = create_app(config_class='config.TestConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()