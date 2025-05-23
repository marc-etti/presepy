import pytest
from flask import url_for

def test_register_get(client):
    response = client.get(url_for('auth.register'))
    assert response.status_code == 200
    assert b'Register' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data

def test_register_post(client):
    response = client.post(url_for('auth.register'),
        data={ 'username': 'testuser',
               'password': 'password'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Registrazione completata per testuser.'.encode('utf-8') in response.data

def test_register_post_existing_username(client):
    response = client.post(url_for('auth.register'), 
        data={  'username': 'testuser1',
                'password': 'password1'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Il nome testuser1 è già in uso.'.encode('utf-8') in response.data

def test_login_get(client):
    response = client.get(url_for('auth.login'))
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data

def test_login_post(client):
    response = client.post(url_for('auth.login'),
        data={ 'username': 'testuser1',
               'password': 'password1'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Il mio profilo' in response.data
    assert b'Logout' in response.data

def test_login_post_invalid_username(client):
    response = client.post(url_for('auth.login'),
        data={ 'username': 'invaliduser',
               'password': 'password1'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Username non trovato.' in response.data

def test_login_post_invalid_password(client):
    response = client.post(url_for('auth.login'),
        data={ 'username': 'testuser1',
               'password': 'invalidpassword'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Password errata.' in response.data

def test_logout(client):
    # Login 
    client.post(url_for('auth.login'),
        data={ 'username': 'testuser1',
               'password': 'password1'},
        follow_redirects=True
    )

    # Test del logout
    response = client.get(url_for('auth.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Registrati' in response.data
    assert b'Logout' not in response.data

def test_profile(client):
    # Login 
    client.post(url_for('auth.login'),
        data={ 'username': 'testuser1',
               'password': 'password1'},
        follow_redirects=True
    )
    # Test per la profile page
    response = client.get(url_for('auth.profile'))
    assert response.status_code == 200
    assert b'Benvenuto testuser1' in response.data

def test_admin_required(client):
    # Login come utente normale
    client.post(url_for('auth.login'),
        data={ 'username': 'testuser1',
               'password': 'password1'},
        follow_redirects=True
    )
    # Test di accesso alla pagina admin
    response = client.get(url_for('auth.admin'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Non hai i permessi per accedere a questa pagina.' in response.data

def test_admin_access(client):
    # Login come admin
    client.post(url_for('auth.login'),
        data={ 'username': 'testuser2',
               'password': 'password2'},
        follow_redirects=True
    )
    # Test di accesso alla pagina admin
    response = client.get(url_for('auth.admin'))
    assert response.status_code == 200
    assert b'Pannello Admin' in response.data
    assert b'Gestione Utenti' in response.data