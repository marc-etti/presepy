from flask import url_for

def test_index(client):
    response = client.get(url_for('dmx.index'))
    assert response.status_code == 200
    assert b'Presepy' in response.data
    assert b'Login' in response.data
    assert b'Registrati' in response.data

def test_index_logged_in(client, login):
    login()
    response = client.get(url_for('dmx.index'))
    assert response.status_code == 200
    assert b'Presepy' in response.data
    assert b'Logout' in response.data
    assert b'Il mio profilo' in response.data

def test_dmx_management_requires_login(client):
    response = client.get(url_for('dmx.dmx_management'), follow_redirects=True)
    assert b'Devi essere autenticato per accedere a questa pagina.' in response.data
    assert b'Login' in response.data

def test_dmx_management_page(client, login):
    login()
    response = client.get(url_for('dmx.dmx_management'))
    assert response.status_code == 200
    assert b'Pagina di gestione DMX' in response.data

