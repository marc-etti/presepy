import pytest
from app import create_app, db
from config import TestConfig
from flask import url_for
from app.models import User, Device, Keyframe, Channel, Phase

@pytest.fixture
def app():
    """Creazione dell'app Flask per i test."""
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()

        # popolo le tabelle con dati di test
        users = [ 
            User(username="testuser1", password="password1", role='user', is_active=True),
            User(username="testuser2", password="password2", role='admin', is_active=True)
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()
        devices = [
            Device(name="TestDevice1", type="light", subtype="LED", dmx_channels=3, status="on"),
            Device(name="TestDevice2", type="light", subtype="Faro", dmx_channels=1, status="off"),
            Device(name="TestDevice3", type="light", subtype="Faro", dmx_channels=1, status="on")
        ]
        db.session.bulk_save_objects(devices)
        db.session.commit()

        devices = Device.query.all()

        channels = [
            Channel(device_id=devices[0].id, number=1, type="RED", value=255),
            Channel(device_id=devices[0].id, number=2, type="GREEN", value=128),
            Channel(device_id=devices[0].id, number=3, type="BLUE", value=0),
            Channel(device_id=devices[1].id, number=4, type="INTENSITY", value=255),
        ]
        db.session.bulk_save_objects(channels)
        db.session.commit()

        channels = Channel.query.all()

        phases = [
            Phase(id=1, name="TestPhase1", duration=120, order=1, status='active'),
            Phase(id=2, name="TestPhase2", duration=240, order=2, status='active'),
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
    """Crea un client di test."""
    return app.test_client()

@pytest.fixture()
def login(client):
    """Login fixture per autenticare un utente di test."""
    def do_login(username='testuser1', password='password1'):
        return client.post(
            url_for('auth.login'),
            data={'username': username, 'password': password},
            follow_redirects=True
        )
    return do_login