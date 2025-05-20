import pytest
from app.models.keyframe import Keyframe
from app.models.channel import Channel
from app.models.device import Device
from app.models.phase import Phase
from app import db

@pytest.fixture(autouse=True)
def setup_database(app):
    with app.app_context():
        db.create_all()
        # Crea un device e una phase di esempio
        device = Device(name="TestDevice", type="light", subtype="LED", dmx_channels=3, status="on")
        device.add()
        phase = Phase(id=1, name="ALBA", duration=600, order=1)
        db.session.add(phase)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def channel(app):
    with app.app_context():
        device = Device.query.first()
        channel = Channel(device_id=device.id, number=1, type="led_red", value=128)
        channel.add()
        yield channel

@pytest.fixture
def phase(app):
    with app.app_context():
        return Phase.query.first()

@pytest.fixture
def keyframe_data(channel, phase):
    return {
        "channel_id": channel.id,
        "phase_id": phase.id,
        "description": "Inizio",
        "position": 0,
        "value": 100
    }

def test_create_keyframe(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)
        keyframe.add()
        assert keyframe.id is not None
        assert keyframe.channel_id == keyframe_data["channel_id"]
        assert keyframe.phase_id == keyframe_data["phase_id"]
        assert keyframe.description == keyframe_data["description"]
        assert keyframe.position == keyframe_data["position"]
        assert keyframe.value == keyframe_data["value"]

def test_keyframe_repr(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)
        keyframe.add()
        expected = f"<Keyframe {keyframe.description} of Channel {keyframe.channel_id} in Phase {keyframe.phase_id}>"
        assert repr(keyframe) == expected

def test_update_keyframe(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)
        keyframe.add()
        keyframe.value = 200
        keyframe.update()
        updated = db.session.get(Keyframe, keyframe.id)
        assert updated.value == 200

def test_delete_keyframe(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)
        keyframe.add()
        keyframe_id = keyframe.id
        keyframe.delete()
        deleted = db.session.get(Keyframe, keyframe_id)
        assert deleted is None

def test_keyframe_value_out_of_range(keyframe_data, app):
    with app.app_context():
        keyframe_data["value"] = 300
        keyframe = Keyframe(**keyframe_data)
        with pytest.raises(ValueError, match="Value 300 is out of range"):
            keyframe.add()

def test_keyframe_position_out_of_range(keyframe_data, app):
    with app.app_context():
        keyframe_data["position"] = 120
        keyframe = Keyframe(**keyframe_data)
        with pytest.raises(ValueError, match="Position 120 is out of range"):
            keyframe.add()

def test_keyframe_empty_description(keyframe_data, app):
    with app.app_context():
        keyframe_data["description"] = ""
        keyframe = Keyframe(**keyframe_data)
        with pytest.raises(ValueError, match="Description cannot be empty"):
            keyframe.add()

def test_keyframe_duplicate_position(keyframe_data, app):
    with app.app_context():
        keyframe1 = Keyframe(**keyframe_data)
        keyframe1.add()
        keyframe2 = Keyframe(**keyframe_data)
        with pytest.raises(ValueError, match="Keyframe already exists at position"):
            keyframe2.add()