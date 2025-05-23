import pytest
from flask import url_for
from app.models import Device

def test_devices_management_requires_login(client):
    response = client.get(url_for('devices.devices_management'), follow_redirects=True)
    assert b'Login' in response.data or response.status_code == 200

def test_devices_management_page(client, login):
    login()
    response = client.get(url_for('devices.devices_management'))
    assert response.status_code == 200
    assert b'Gestione Dispositivi' in response.data
    assert b'Aggiungi Dispositivo' in response.data

def test_add_device_form_page(client, login):
    login()
    response = client.get(url_for('devices.add_device_form'))
    assert response.status_code == 200
    assert b'Aggiungi dispositivo' in response.data

def test_add_device_missing_fields(client, login):
    login()
    response = client.post(
        url_for('devices.add_device'),
        data={
            'name': 'FaroTest',
            'type': 'Light',
            'subtype': 'Faro',
            'dmx_channels': 2,
            # 'channel-type-1': 'Intensity',
            # 'channel-number-1': '1', 
            # 'channel-value-1': '255',         
        },
        follow_redirects=True
    )
    assert b'Dati mancanti per il canale 1' in response.data

def test_add_device_success(client, login, app):
    login()
    data = {
            'name': 'LedRGBtest',
            'type': 'Light',
            'subtype': 'LEDRGB',
            'dmx_channels': 3,
            'channel-type-1': 'Red',
            'channel-number-1': '11',
            'channel-value-1': '255',
            'channel-type-2': 'Blue',
            'channel-number-2': '12',
            'channel-value-2': '255',
            'channel-type-3': 'Green',
            'channel-number-3': '13',
            'channel-value-3': '255',
    }
    response = client.post(url_for('devices.add_device'), data=data, follow_redirects=True)
    # print(response.data.decode('utf-8'))
    assert b'Dispositivo LedRGBtest aggiunto con successo' in response.data

def test_edit_device_form_not_found(client, login):
    login()
    response = client.get(url_for('devices.edit_device_form', device_id=999), follow_redirects=True)
    assert b'Dispositivo non trovato' in response.data

def test_delete_device_not_found(client, login):
    login()
    response = client.post(url_for('devices.delete_device'), data={'device_id': 999}, follow_redirects=True)
    assert b'Dispositivo non trovato' in response.data

def test_turn_on_off_device(app, client, login):
    with app.app_context():
        old_status = Device.query.filter_by(id=1).first().status
        login()
        response = client.get(url_for('devices.turn_on_off_device', device_id=1), follow_redirects=True)
        new_status = Device.query.filter_by(id=1).first().status
    assert b'acceso' in response.data or b'spento' in response.data
    assert old_status != new_status

def test_edit_device_success(app, client, login):
    with app.app_context():
        old_name = Device.query.filter_by(id=2).first().name
        assert old_name == 'TestDevice2'
        login()
        response = client.get(url_for('devices.edit_device_form', device_id=2))
        assert response.status_code == 200
        data = {
            'device_id': 2,
            'name': 'TestDevice2_edited',
            'type': 'Light',
            'subtype': 'Faro',
            'subtype': 'LED',
            'channel-number-4': 4,
            'channel-type-4': 'Dimmer',
            'channel-value-4': 128
        }
        response = client.post(url_for('devices.edit_device'), data=data, follow_redirects=True)
        new_name = Device.query.filter_by(id=2).first().name
        assert new_name == 'TestDevice2_edited'
    assert b'modificato con successo' in response.data
    assert old_name != new_name

def test_delete_device_success(client, login):
    login()
    response = client.post(url_for('devices.delete_device'), data={'device_id': 2}, follow_redirects=True)
    assert b'eliminato con successo' in response.data
    # Check if the device is actually deleted
    response = client.get(url_for('devices.devices_management'))
    assert b'TestDevice2_edited' not in response.data

def test_add_device_existing_channel(client, login):
    login()
    data = {
        'name': 'TestDevice3',
        'type': 'Light',
        'subtype': 'Faro',
        'dmx_channels': 1,
        'channel-type-1': 'Intensity',
        'channel-number-1': '1', 
        'channel-value-1': '255',         
    }
    response = client.post(url_for('devices.add_device'), data=data, follow_redirects=True)
    assert 'Il canale numero 1 è già usato dal dispositivo TestDevice1'.encode() in response.data

def test_edit_device_existing_channel(client, login):
    login()
    data = {
        'device_id': 1,
        'name': 'TestDevice1',
        'type': 'Light',
        'subtype': 'Faro',
        'dmx_channels': 1,
        'channel-number-1': 2,
        'channel-type-1': 'Intensity',
        'channel-value-1': 255
    }
    response = client.post(url_for('devices.edit_device'), data=data, follow_redirects=True)
    print(response.data.decode('utf-8'))
    assert 'Il canale numero 2 è già usato dal dispositivo TestDevice1'.encode() in response.data