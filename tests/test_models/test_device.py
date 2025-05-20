import pytest
from app.models.device import Device
from app import db

@pytest.fixture(autouse=True)
def setup_database(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def device_data():
    return {
        "name": "TestDevice",
        "type": "light",
        "subtype": "LED",
        "dmx_channels": 3,
        "status": "on"
    }

def test_create_device(device_data, app):
    with app.app_context():
        device = Device(**device_data)
        device.add()
        assert device.id is not None
        assert device.name == device_data["name"]
        assert device.type == device_data["type"]
        assert device.subtype == device_data["subtype"]
        assert device.dmx_channels == device_data["dmx_channels"]
        assert device.status == device_data["status"]

def test_update_device(device_data, app):
    with app.app_context():
        device = Device(**device_data)
        device.add()
        device.name = "UpdatedDevice"
        device.status = "off"
        device.update()
        updated = db.session.get(Device, device.id)
        assert updated.name == "UpdatedDevice"
        assert updated.status == "off"

def test_delete_device(device_data, app):
    with app.app_context():
        device = Device(**device_data)
        device.add()
        device_id = device.id
        device.delete()
        deleted = db.session.get(Device, device_id)
        assert deleted is None

def test_device_repr(device_data, app):
    with app.app_context():
        device = Device(**device_data)
        assert repr(device) == f"<Device {device_data['name']}>"