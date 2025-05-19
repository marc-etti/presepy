import pytest
from app.models.device import Device
from app import db

@pytest.fixture
def device():
    device = Device(
        name="Test Device",
        type="light",
        subtype="LED",
        dmx_channels=3,
        status="on"
    )
    yield device
    # Cleanup if needed
    db.session.rollback()

def test_device_repr(device):
    assert repr(device) == "<Device Test Device>"

def test_device_add_and_query(device):
    device.add()
    queried = Device.query.filter_by(name="Test Device").first()
    assert queried is not None
    assert queried.name == "Test Device"
    assert queried.type == "light"
    assert queried.subtype == "LED"
    assert queried.dmx_channels == 3
    assert queried.status == "on"
    # Cleanup
    queried.delete()

def test_device_update(device):
    device.add()
    device.status = "off"
    device.update()
    updated = Device.query.filter_by(name="Test Device").first()
    assert updated.status == "off"
    # Cleanup
    updated.delete()

def test_device_delete(device):
    device.add()
    device_id = device.id
    device.delete()
    deleted = Device.query.get(device_id)
    assert deleted is None

def test_device_unique_name_constraint(device):
    device.add()
    duplicate = Device(
        name="Test Device",
        type="light",
        subtype="LED",
        dmx_channels=3,
        status="on"
    )
    db.session.add(duplicate)
    with pytest.raises(Exception):
        db.session.commit()
    db.session.rollback()
    # Cleanup
    Device.query.filter_by(name="Test Device").first().delete()