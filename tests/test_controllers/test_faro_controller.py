import pytest
from unittest.mock import Mock
from app.services.controllers.faro_controller import FaroController
import re

@pytest.fixture
def mock_dmx():
    """Crea un'istanza mock del DMX."""
    dmx = Mock()
    dmx.set_channel = Mock()
    return dmx


def test_faro_controller_init_success(app, mock_dmx):
    """Test che verifica l'inizializzazione corretta del FaroController."""
    with app.app_context():
        faroTest = FaroController("TestDevice1", mock_dmx)
        assert faroTest.device is not None

def test_faro_controller_init_invalid_name(mock_dmx):
    """Test che verifica l'errore per nome del faro vuoto."""
    with pytest.raises(ValueError, match="Il nome del faro non può essere vuoto."):
        FaroController("", mock_dmx)

def test_faro_controller_init_invalid_dmx(mock_dmx):
    """Test che verifica l'errore per istanza DMX vuota."""
    with pytest.raises(ValueError, match="L'istanza del DMX non può essere vuota."):
        FaroController("TestDevice1", None)

def test_faro_controller_init_device_not_found(app, mock_dmx):
    """Test che verifica l'errore se il faro non esiste nel database."""
    with app.app_context():
        with pytest.raises(ValueError, match="Il faro con nome TestDevice99 non esiste nel database."):
            FaroController("TestDevice99", mock_dmx)

def test_faro_controller_init_no_channels(app, mock_dmx):
    """Test che verifica l'errore se il faro non ha canali associati."""
    with app.app_context():
        with pytest.raises(ValueError, match="Il faro con nome TestDevice3 non ha canali associati nel database."):
            FaroController("TestDevice3", mock_dmx)

def test_faro_controller_no_keyframes(app, mock_dmx):
    """Test che verifica il funzionamento del faro anche in assenza di keyframes."""
    with app.app_context():
        faroTest = FaroController("TestDevice2", mock_dmx)
        phase = faroTest.phases[0]
        faroTest.update(phase=phase, time=100, total_time=1000)
        assert mock_dmx.set_channel.call_count == len(faroTest.channels)

def test_faro_controller_update_success(app, mock_dmx):
    """Test che verifica l'aggiornamento del faro."""
    with app.app_context():
        faroTest = FaroController("TestDevice1", mock_dmx)
        phase = faroTest.phases[0]
        faroTest.update(phase=phase, time=100, total_time=1000)
        assert mock_dmx.set_channel.call_count == len(faroTest.channels)

def test_faro_controller_update_device_off(app, mock_dmx):
    """Test che verifica che il faro non aggiorni i canali se lo stato è 'off'."""
    with app.app_context():
        faroTest = FaroController("TestDevice1", mock_dmx)
        faroTest.device.status = "off"
        phase = faroTest.phases[0]
        faroTest.update(phase=phase, time=100, total_time=1000)
        mock_dmx.set_channel.assert_not_called()

def test_faro_controller_repr(app, mock_dmx):
    """Test che verifica la rappresentazione del FaroController."""
    with app.app_context():
        faroTest = FaroController("TestDevice1", mock_dmx)
        repr_str = repr(faroTest)
        assert "Faro TestDevice1 con ID 1" in repr_str