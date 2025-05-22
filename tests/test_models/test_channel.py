import pytest
from app.models import Channel
from app import db

@pytest.fixture(scope="module")
def channel_data():
    return {
        "device_id": 2,
        "number": 4,
        "type": "INTENSITY",
        "value": 0
    }

def test_channel_creation(channel_data, app):
    with app.app_context():
        channel = Channel(**channel_data)
        channel.add()

        channel_from_db = db.session.get(Channel, channel.id)

        assert channel_from_db is not None
        assert channel_from_db.id is not None
        assert channel_from_db.device_id == channel_data["device_id"]
        assert channel_from_db.number == channel_data["number"]
        assert channel_from_db.type == channel_data["type"]
        assert channel_from_db.value == channel_data["value"]

def test_channel_update(channel_data, app):
    with app.app_context():
        channel = Channel(**channel_data)
        channel.add()

        channel.value = 255
        channel.update()

        updated_channel = db.session.get(Channel, channel.id)

        assert updated_channel.value == 255

def test_channel_deletion(channel_data, app):
    with app.app_context():
        channel = Channel(**channel_data)
        channel.add()

        channel.delete()
        deleted_channel = db.session.get(Channel, channel.id)
        assert deleted_channel is None

def test_channel_repr(channel_data, app):
    with app.app_context():
        channel = Channel(**channel_data)
        channel.add()

        assert repr(channel) == f'<Canale numero: {channel.number} associato al dispositivo: {channel.device.name}>'

def test_channel_validation(channel_data, app):
    with app.app_context():
        channel = Channel(**channel_data)

        # Test invalid number
        channel.number = 600
        with pytest.raises(ValueError):
            channel.validate()
        channel.number = 4

        # Test invalid value
        channel.value = 300
        with pytest.raises(ValueError):
            channel.validate()
        channel.value = 0

        # Test empty type
        channel.type = ""
        with pytest.raises(ValueError):
            channel.validate()

        