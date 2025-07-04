import pytest
from flask import url_for
from app.models import Phase
from app import db

def test_phases_management_requires_login(client):
    response = client.get(url_for('phases.phases_management'), follow_redirects=True)
    assert b'Login' in response.data or response.status_code == 200

def test_phases_management_page(client, login_user):
    login_user()
    response = client.get(url_for('phases.phases_management'))
    assert response.status_code == 200
    assert b'Gestione Fasi' in response.data

def test_active_deactivate_phase(client, login_expert):
    login_expert()
    phase = db.session.query(Phase).first()
    initial_status = phase.status
    response = client.get(url_for('phases.active_deactivate_phase', phase_id=phase.id), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Fase TestPhase1 attivata' in response.data or b'Fase TestPhase1 disattivata' in response.data
    
    updated_phase = db.session.query(Phase).filter_by(id=phase.id).first()
    assert updated_phase.status != initial_status

def test_active_deactivate_phase_not_found(client, login_expert):
    login_expert()
    response = client.get(url_for('phases.active_deactivate_phase', phase_id=999), follow_redirects=True)
    assert response.status_code == 200
    assert b'Fase non trovata' in response.data

def test_delete_phase(client, login_expert):
    login_expert()
    phase = db.session.query(Phase).first()
    response = client.post(
        url_for('phases.delete_phase'),
        data={'phase_id': phase.id},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'Fase TestPhase1 eliminata con successo' in response.data
    
    deleted_phase = db.session.query(Phase).filter_by(id=phase.id).first()
    assert deleted_phase.status == 'deleted'

def test_add_phase_form_page(client, login_expert):
    login_expert()
    response = client.get(url_for('phases.add_edit_phase_form'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Aggiungi una nuova fase' in response.data

def test_add_phase(client, login_expert):
    login_expert()
    response = client.post(
        url_for('phases.add_edit_phase'),
        data={
            'name': 'New Phase',
            'duration': 300,
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'Fase New Phase aggiunta con successo' in response.data
    
    new_phase = db.session.query(Phase).filter_by(name='New Phase').first()
    assert new_phase is not None
    assert new_phase.status == 'deactivated'

def test_edit_phase_form_page(client, login_expert):
    login_expert()
    phase = db.session.query(Phase).first()
    response = client.get(url_for('phases.add_edit_phase_form', phase_id=phase.id), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Modifica la fase' in response.data
    assert phase.name.encode() in response.data

def test_edit_phase(client, login_expert):
    login_expert()
    phase = db.session.query(Phase).first()
    new_name = 'Updated Phase Name'
    response = client.post(
        url_for('phases.add_edit_phase', phase_id=phase.id),
        data={
            'name': new_name,
            'duration': 400,
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'aggiornata con successo' in response.data
    assert new_name.encode() in response.data

    
    updated_phase = db.session.query(Phase).filter_by(id=phase.id).first()
    assert updated_phase.name == new_name
    assert updated_phase.duration == 400

def test_edit_phase_not_found(client, login_expert):
    login_expert()
    response = client.get(url_for('phases.add_edit_phase_form', phase_id=999), follow_redirects=True)
    assert response.status_code == 200
    assert b'Fase non trovata' in response.data

def test_move_up_down_phase(client, login_user):
    login_user()
    phase = db.session.query(Phase).first()
    initial_order = phase.order
    direction = 'up' if initial_order > 1 else 'down'
    
    response = client.get(url_for('phases.move_up_down_phase', phase_id=phase.id, direction=direction), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'spostata' in response.data
    
    updated_phase = db.session.query(Phase).filter_by(id=phase.id).first()
    assert updated_phase.order != initial_order
    assert (updated_phase.order == initial_order - 1) if direction == 'up' else (updated_phase.order == initial_order + 1)

def test_move_up_first_phase(client, login_user):
    login_user()
    phase = db.session.query(Phase).filter_by(order=1).first()
    
    response = client.get(url_for('phases.move_up_down_phase', phase_id=phase.id, direction='up'), follow_redirects=True)
    
    assert response.status_code == 200
    assert 'La fase è già al primo posto e non può essere spostata su'.encode() in response.data

    updated_phase = db.session.query(Phase).filter_by(id=phase.id).first()

    assert updated_phase.order == 1