import pytest
from flask import url_for
from app.models import Keyframe
from app import db

def test_keyframes_management_requires_login(client):
    response = client.get(url_for('keyframes.keyframes_management', device_id=1), follow_redirects=True)
    assert b'Login' in response.data or response.status_code == 200

def test_keyframes_management_page(client, login_user):
    login_user()
    response = client.get(url_for('keyframes.keyframes_management', device_id=1))
    assert response.status_code == 200
    assert b'Gestione Keyframes' in response.data

def test_edit_keyframe_form_page(client, login_expert):
    login_expert()
    response = client.get(url_for('keyframes.edit_keyframe_form', device_id=1, phase_id=1, position=0))
    assert response.status_code == 200
    assert b'Modifica Keyframe' in response.data

def test_edit_keyframe(app, client, login_expert):
    with app.app_context():
        old_value = db.session.query(Keyframe).filter_by(phase_id=1, position=0, channel_id=1).first().value
        login_expert()
        response = client.post(
            url_for('keyframes.edit_keyframe'),
            data={
                'device_id': 1,
                'phase_id': 1,
                'position': 0,
                'channel_id': 1,
                'slider-1': 255,
                'description-1': 'Test Description',
            },
            follow_redirects=True
        )
        new_value = db.session.query(Keyframe).filter_by(phase_id=1, position=0, channel_id=1).first().value
    assert response.status_code == 200
    assert b'Keyframe aggiornato correttamente' in response.data
    assert old_value != new_value
    assert new_value == 255

def test_edit_keyframe_not_found(client, login_expert):
    login_expert()
    response = client.get(url_for('keyframes.edit_keyframe_form', device_id=1, phase_id=1, position=999))
    assert response.status_code == 200
    assert b'Keyframe non trovato' in response.data

def test_add_keyframe_form_page(client, login_expert):
    login_expert()
    response = client.get(url_for('keyframes.add_keyframe_form', device_id=1, phase_id=1), follow_redirects=True)
    assert response.status_code == 200
    assert b'Aggiungi Keyframe' in response.data

def test_add_keyframe(client, login_expert):
    login_expert()
    response = client.post(
        url_for('keyframes.add_keyframe'),
        data={
            'device_id': 1,
            'phase_id': 1,
            'position': 50,
            'channel_id': 1,
            'slider-1': 128,
            'description-1': 'Test Description',
            'slider-2': 64,
            'description-2': 'Test Description 2',
            'slider-3': 32,
            'description-3': 'Test Description 3'
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Keyframe aggiunto correttamente' in response.data

def test_delete_keyframe(client, login_expert):
    login_expert()
    response = client.post(
        url_for('keyframes.delete_keyframe'),
        data={
            'device_id': 1,
            'phase_id': 1,
            'position': 0,
            'channel_id': 1
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Keyframe eliminato correttamente' in response.data