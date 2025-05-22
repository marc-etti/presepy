import pytest
from app.models import Keyframe
from app import db

@pytest.fixture(scope="module")
def keyframe_data():
    return {
        "channel_id": 1,
        "phase_id": 1,
        "description": "Intermedia",
        "position": 50,
        "value": 0
    }

def test_keyframe_creation(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)
        keyframe.add()

        assert keyframe.id is not None
        assert keyframe.channel_id == keyframe_data["channel_id"]
        assert keyframe.phase_id == keyframe_data["phase_id"]
        assert keyframe.description == keyframe_data["description"]
        assert keyframe.position == keyframe_data["position"]
        assert keyframe.value == keyframe_data["value"]

def test_keyframe_update(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)
        keyframe.add()
        keyframe.value = 255
        keyframe.update()

        updated_keyframe = db.session.get(Keyframe, keyframe.id)
        assert updated_keyframe.value == 255

def test_keyframe_deletion(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)
        keyframe.add()

        keyframe.delete()
        deleted_keyframe = db.session.get(Keyframe, keyframe.id)
        assert deleted_keyframe is None

def test_keyframe_repr(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)
        keyframe.add()

        assert repr(keyframe) == f"<Keyframe {keyframe.description} of Channel {keyframe.channel.number} in Phase {keyframe.phase.name}>"

def test_keyframe_validation(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)

        # Test invalid value
        keyframe.value = 300
        with pytest.raises(ValueError):
            keyframe.validate()

        # Test invalid position
        keyframe.value = 255
        keyframe.position = -10
        with pytest.raises(ValueError):
            keyframe.validate()

        # Test empty description
        keyframe.position = 50
        keyframe.description = ""
        with pytest.raises(ValueError):
            keyframe.validate()

        # Test duplicate keyframe
        existing_keyframe = Keyframe(**keyframe_data)
        existing_keyframe.add()
        with pytest.raises(ValueError):
            keyframe.validate()

def test_keyframe_delete(keyframe_data, app):
    with app.app_context():
        keyframe = Keyframe(**keyframe_data)
        keyframe.add()

        keyframe.delete()
        deleted_keyframe = db.session.get(Keyframe, keyframe.id)
        assert deleted_keyframe is None

def test_duplicate_keyframe_creation(keyframe_data, app):
    with app.app_context():
        keyframe1 = Keyframe(**keyframe_data)
        keyframe1.add()

        keyframe2 = Keyframe(**keyframe_data)
        
        with pytest.raises(ValueError):
            keyframe2.add()

def test_keyframe_update_with_duplicate(keyframe_data, app):
    with app.app_context():
        keyframe1 = Keyframe(**keyframe_data)
        keyframe1.add()

        keyframe2 = Keyframe(**keyframe_data)
        keyframe2.position = 45
        keyframe2.add()

        # Update keyframe2 to have the same position as keyframe1
        keyframe2.position = keyframe1.position
        with pytest.raises(ValueError):
            keyframe2.update()