import pytest
from app import create_app, db
from config import TestConfig
from app.models import User, Device, Keyframe, Channel, Phase

@pytest.fixture
def app():
    """Create a new app instance for testing."""
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()

        # populate the database with test data
        users = [ 
            User(username="testuser1", password="password1", is_admin=False, is_active=True),
            User(username="testuser2", password="password2", is_admin=True, is_active=True)
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()
        devices = [
            Device(name="TestDevice1", type="light", subtype="LED", dmx_channels=3, status="on"),
            Device(name="TestDevice2", type="light", subtype="Faro", dmx_channels=1, status="off")
        ]
        db.session.bulk_save_objects(devices)
        db.session.commit()

        devices = Device.query.all()

        channels = [
            Channel(device_id=devices[0].id, number=1, type="RED", value=255),
            Channel(device_id=devices[0].id, number=2, type="GREEN", value=128),
            Channel(device_id=devices[0].id, number=3, type="BLUE", value=0),
        ]
        db.session.bulk_save_objects(channels)
        db.session.commit()

        channels = Channel.query.all()

        phases = [
            Phase(name="TestPhase1", duration=10, order=1),
            Phase(name="TestPhase2", duration=20, order=2),
        ]
        db.session.bulk_save_objects(phases)
        db.session.commit()

        phases = Phase.query.all()

        keyframes = [
            Keyframe(channel_id=channels[0].id, phase_id=phases[0].id, description="Inizio", position=0, value=0),
            Keyframe(channel_id=channels[1].id, phase_id=phases[0].id, description="Inizio", position=0, value=0),
            Keyframe(channel_id=channels[2].id, phase_id=phases[0].id, description="Inizio", position=0, value=0),
            Keyframe(channel_id=channels[0].id, phase_id=phases[0].id, description="Fine", position=100, value=255),
            Keyframe(channel_id=channels[1].id, phase_id=phases[0].id, description="Fine", position=100, value=255),
            Keyframe(channel_id=channels[2].id, phase_id=phases[0].id, description="Fine", position=100, value=255),
            Keyframe(channel_id=channels[0].id, phase_id=phases[1].id, description="Inizio", position=0, value=0),
            Keyframe(channel_id=channels[1].id, phase_id=phases[1].id, description="Inizio", position=0, value=0),
            Keyframe(channel_id=channels[2].id, phase_id=phases[1].id, description="Inizio", position=0, value=0),
            Keyframe(channel_id=channels[0].id, phase_id=phases[1].id, description="Fine", position=100, value=255),
            Keyframe(channel_id=channels[1].id, phase_id=phases[1].id, description="Fine", position=100, value=255),
            Keyframe(channel_id=channels[2].id, phase_id=phases[1].id, description="Fine", position=100, value=255),
        ]

        db.session.bulk_save_objects(keyframes)
        db.session.commit()

    yield app
        
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()