import pytest
from app.models.channel import Channel
from app import db
from app.models import channel

@pytest.fixture(autouse=True)
def setup_database(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def channel_instance(device, app):
    with app.app_context():
        ch = Channel(device_id=device.id, number=1, type="led_red", value=100)
        return ch
    
@pytest.fixture
def device_instance(app):
    with app.app_context():
        # Assuming you have a Device model and a way to create a device
        device = channel.Device(name="TestDevice", type="light", subtype="LED", dmx_channels=3, status="on")
        device.add()
        return device

@pytest.fixture
def keyframe_instance(channel_instance, app):
    with app.app_context():
        # Assuming you have a Keyframe model and a way to create a keyframe
        keyframe = channel.Keyframe(channel_id=channel_instance.id, phase_id=1, description="Test", position=0, value=100)
        return keyframe
    
@pytest.fixture
def phase_instance(app):
    with app.app_context():
        # Assuming you have a Phase model and a way to create a phase
        phase = channel.Phase(id=1, name="ALBA", duration=600, order=1)
        db.session.add(phase)
        db.session.commit()
        return phase


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        # Rollback and remove all data before each test
        db.session.rollback()
        for tbl in reversed(db.metadata.sorted_tables):
            db.session.execute(tbl.delete())
        db.session.commit()
        yield
        db.session.rollback()
        for tbl in reversed(db.metadata.sorted_tables):
            db.session.execute(tbl.delete())
        db.session.commit()

def test_channel_repr(channel_instance, app):
    with app.app_context():
        assert repr(channel_instance) == f'<Channel 1 of Device 1>'

def test_add_valid_channel(channel_instance, app):
    with app.app_context():
        channel_instance.add()
        ch = db.session.get(Channel, channel_instance.id)
        assert ch is not None
        assert ch.number == 1
        assert ch.value == 100

@pytest.mark.parametrize("number", [0, 513])
def test_add_invalid_channel_number(channel_instance, number, app):
    with app.app_context():
        channel_instance.number = number
        with pytest.raises(ValueError, match="Channel number .* is out of range"):
            channel_instance.add()

@pytest.mark.parametrize("value", [-1, 256])
def test_add_invalid_channel_value(channel_instance, value, app):
    with app.app_context():
        channel_instance.value = value
        with pytest.raises(ValueError, match="Value .* is out of range"):
            channel_instance.add()

def test_update_valid_channel(channel_instance, app):
    with app.app_context():
        channel_instance.add()
        channel_instance.value = 200
        channel_instance.update()
        ch = db.session.get(Channel, channel_instance.id)
        assert ch.value == 200

def test_update_invalid_channel_number(channel_instance, app):
    with app.app_context():
        channel_instance.add()
        channel_instance.number = 0
        with pytest.raises(ValueError):
            channel_instance.update()

def test_update_invalid_channel_value(channel_instance, app):
    with app.app_context():
        channel_instance.add()
        channel_instance.value = 300
        with pytest.raises(ValueError):
            channel_instance.update()

def test_update_nonexistent_channel(channel_instance, app):
    with app.app_context():
        # Not added to DB, so update should fail
        channel_instance.id = 9999
        with pytest.raises(ValueError, match="Channel with id 9999 does not exist"):
            channel_instance.update()

def test_delete_channel(channel_instance, app):
    with app.app_context():
        channel_instance.add()
        channel_instance.delete()
        ch = db.session.get(Channel, channel_instance.id)
        assert ch is None