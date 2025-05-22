import pytest
from app.models import Device
from app import db

@pytest.fixture(scope="module")
def device_data():
    return {
        "name": "TestDevice",
        "type": "light",
        "subtype": "LED",
        "dmx_channels": 4,
        "status": "on"
    }

def test_device_creation(device_data, app):
    with app.app_context():
        device = Device(**device_data)
        device.add()

        assert device.id is not None
        assert device.name == device_data["name"]
        assert device.type == device_data["type"]
        assert device.subtype == device_data["subtype"]
        assert device.dmx_channels == device_data["dmx_channels"]
        assert device.status == device_data["status"]

def test_device_update(device_data, app):
    with app.app_context():
        device = Device(**device_data)
        device.add()
        device.status = "off"
        device.update()

        updated_device = db.session.get(Device, device.id)
        assert updated_device.status == "off"


def test_device_deletion(device_data, app):
    with app.app_context():
        device = Device(**device_data)
        device.add()

        device.delete()
        deleted_device = db.session.get(Device, device.id)
        assert deleted_device is None

def test_device_repr(device_data, app):
    with app.app_context():
        device = Device(**device_data)
        device.add()

        assert repr(device) == f"<Device {device.name}>"

def test_device_validation(device_data, app):
    with app.app_context():
        device = Device(**device_data)

        # Test invalid name
        device.name = ""
        with pytest.raises(ValueError):
            device.validate()

        # Test invalid type
        device.type = ""
        with pytest.raises(ValueError):
            device.validate()

        # Test invalid subtype
        device.subtype = ""
        with pytest.raises(ValueError):
            device.validate()

        # Test invalid dmx_channels
        device.dmx_channels = None
        with pytest.raises(ValueError):
            device.validate()

        # Test invalid status
        device.status = ""
        with pytest.raises(ValueError):
            device.validate()