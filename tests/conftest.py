import pytest
from app import create_app, db
from config import TestConfig

@pytest.fixture
def app():
    """Create a new app instance for testing."""
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
    
    yield app
        
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()