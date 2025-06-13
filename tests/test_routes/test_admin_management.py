import pytest
from flask import url_for

def test_admin_required(client):
    # Login come utente normale
    client.post(url_for('auth.login'),
        data={ 'username': 'test_user',
               'password': 'password_user'},
        follow_redirects=True
    )
    # Test di accesso alla pagina admin
    response = client.get(url_for('admin.dashboard'), follow_redirects=True)
    assert response.status_code == 403
    assert b'Non hai i permessi necessari per accedere a questa pagina.' in response.data

def test_admin_access(client):
    # Login come admin
    client.post(url_for('auth.login'),
        data={ 'username': 'test_admin',
               'password': 'password_admin'},
        follow_redirects=True
    )
    # Test di accesso alla pagina admin
    response = client.get(url_for('admin.dashboard'))
    assert response.status_code == 200
    assert b'Pannello Admin' in response.data
    assert b'Gestione Utenti' in response.data

def test_role_required(client):
    # Login come utente normale
    client.post(url_for('auth.login'),
        data={ 'username': 'test_user',
               'password': 'password_user'},
        follow_redirects=True
    )
    # Test di accesso alla pagina admin
    response = client.get(url_for('admin.dashboard'), follow_redirects=True)
    assert response.status_code == 403
    assert b'Non hai i permessi necessari per accedere a questa pagina.' in response.data

    # Login come admin
    client.post(url_for('auth.login'),
        data={ 'username': 'test_admin',
               'password': 'password_admin'},
        follow_redirects=True
    )
    # Test di accesso alla pagina admin
    response = client.get(url_for('admin.dashboard'))
    assert response.status_code == 200

def test_delete_account(client, login_admin):
    # Login come admin
    login_admin()
    
    # Test di eliminazione di un account
    response = client.post(url_for('admin.delete_account'), data={'user_id': '1'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'stato eliminato.' in response.data

def test_deactivate_account(client, login_admin):
    # Login come admin
    login_admin()
    
    # Test di disattivazione di un account
    response = client.post(url_for('admin.deactivate'), data={'user_id': '1'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'stato disattivato' in response.data

def test_delete_account_invalid_user(client, login_admin):
    # Login come admin
    login_admin()
    
    # Test di eliminazione di un account inesistente
    response = client.post(url_for('admin.delete_account'), data={'user_id': '999'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Utente non trovato.' in response.data

def test_deactivate_account_invalid_user(client, login_admin):
    # Login come admin
    login_admin()
    
    # Test di disattivazione di un account inesistente
    response = client.post(url_for('admin.deactivate'), data={'user_id': '999'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Utente non trovato.' in response.data

def test_delete_account_unauthorized(client):
    # Login come utente normale
    client.post(url_for('auth.login'),
        data={ 'username': 'test_user',
               'password': 'password_user'},
        follow_redirects=True
    )
    
    # Test di eliminazione senza permessi admin
    response = client.post(url_for('admin.delete_account'), data={'user_id': '1'}, follow_redirects=True)
    assert response.status_code == 403

def test_deactivate_account_unauthorized(client):
    # Login come utente normale
    client.post(url_for('auth.login'),
        data={ 'username': 'test_user',
               'password': 'password_user'},
        follow_redirects=True
    )
    
    # Test di disattivazione senza permessi admin
    response = client.post(url_for('admin.deactivate'), data={'user_id': '1'}, follow_redirects=True)
    assert response.status_code == 403

def test_admin_page_content(client, login_admin):
    # Login come admin
    login_admin()
    
    # Test del contenuto della pagina admin
    response = client.get(url_for('admin.dashboard'))
    assert response.status_code == 200
    assert b'test_user' in response.data
    assert b'test_admin' in response.data

def test_activate_account(client, login_admin):
    # Login come admin
    login_admin()
    
    # Test di attivazione di un account
    response = client.post(url_for('admin.activate'), data={'user_id': '4'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'stato attivato' in response.data