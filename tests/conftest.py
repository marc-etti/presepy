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
            User(username="test_user", password="password_user", role='user', is_active=True),
            User(username="test_admin", password="password_admin", role='admin', is_active=True),
            User(username="test_expert", password="password_expert", role='expert', is_active=True),
            User(username="test_inactive", password="password_inactive", role='user', is_active=False)
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
            Phase(id=3, name="TestPhase3", duration=180, order=3, status='active'),
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
def login_user(client):
    """Login fixture per autenticare un utente di tipo user."""
    def do_login(username='test_user', password='password_user'):
        return client.post(
            url_for('auth.login'),
            data={'username': username, 'password': password},
            follow_redirects=True
        )
    return do_login

@pytest.fixture()
def login_admin(client):
    """Login fixture per autenticare un utente di tipo admin."""
    def do_login(username='test_admin', password='password_admin'):
        return client.post(
            url_for('auth.login'),
            data={'username': username, 'password': password},
            follow_redirects=True
        )
    return do_login

@pytest.fixture()
def login_expert(client):
    """Login fixture per autenticare un utente di tipo expert."""
    def do_login(username='test_expert', password='password_expert'):
        return client.post(
            url_for('auth.login'),
            data={'username': username, 'password': password},
            follow_redirects=True
        )
    return do_login