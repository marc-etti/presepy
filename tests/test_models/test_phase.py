import pytest
from app.models import Phase
from app import db

@pytest.fixture(scope="module")
def phase_data():
    return {
        "name": "TestPhase",
        "duration": 10,
        "order": 5
    }

def test_phase_creation(phase_data, app):
    with app.app_context():
        phase = Phase(**phase_data)
        
        with pytest.raises(NotImplementedError):
            phase.add()

def test_phase_update(phase_data, app):
    with app.app_context():
        phase = Phase(**phase_data)
        
        with pytest.raises(NotImplementedError):
            phase.update()

def test_phase_deletion(phase_data, app):
    with app.app_context():
        phase = Phase(**phase_data)
        
        with pytest.raises(NotImplementedError):
            phase.delete()


def test_phase_repr(phase_data, app):
    with app.app_context():
        phase = Phase(**phase_data)
        
        assert repr(phase) == f"<Fase: {phase.name} di durata {phase.duration} secondi>"
        
def test_get_phases(app):
    with app.app_context():
        phases = Phase.get_phases()
        
        assert len(phases) > 0
        assert all(isinstance(phase, Phase) for phase in phases)
        assert all(phase.name is not None for phase in phases)
        assert all(phase.duration is not None for phase in phases)
        assert all(phase.order is not None for phase in phases)