import pytest
from app import db
from app.models import Channel
from app.models import Device

@pytest.fixture(autouse=True)
def setup_database(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def device_instance(app):
    with app.app_context():
        # Assuming you have a Device model and a way to create a device
        device = Device(name="TestDevice", type="light", subtype="LED", dmx_channels=3, status="on")
        device.add()
        return device
    
@pytest.fixture
def channel_instance(device_instance, app):
    with app.app_context():
        channel_instance = Channel(device_id=device_instance.id, number=1, type="led_red", value=128)
        channel_instance.add()
        return channel_instance

@pytest.fixture
def channel_data(device_instance):
    return {
        "device_id": device_instance.id,
        "number": 2,
        "type": "led_red",
        "value": 128
    }

def test_channel_repr(channel_instance, app):
    with app.app_context():
        assert repr(channel_instance) == f'<Channel 1 of Device 1>'

def test_add_valid_channel(channel_data, app):
    with app.app_context():
        channel_instance = Channel(**channel_data)
        channel_instance.add()
        ch = db.session.get(Channel, channel_instance.id)
        assert ch is not None
        assert ch.number == channel_data["number"]
        assert ch.device_id == channel_data["device_id"]
        assert ch.type == channel_data["type"]
        assert ch.value == channel_data["value"]
    

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