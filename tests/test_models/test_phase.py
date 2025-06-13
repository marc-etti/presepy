import pytest
from app.models import Phase
from app import db

@pytest.fixture(scope="module")
def phase_data():
    return {
        "name": "Test_New_Phase",
        "duration": 100,
    }

@pytest.fixture(scope="module")
def phase_data_for_validation():
    return {
        "name": "Test_Phase_With_Order",
        "duration": 150,
        "order": 1,
        "status": "active"
    }

def test_phase_creation(phase_data, app):
    with app.app_context():
        phase = Phase(**phase_data)
        phase.add()

        phase_from_db = db.session.get(Phase, phase.id)
        assert phase_from_db is not None
        assert phase_from_db.id is not None
        assert phase_from_db.name == phase_data["name"]
        assert phase_from_db.duration == phase_data["duration"]

def test_phase_update(phase_data, app):
    with app.app_context():
        phase = Phase(**phase_data)
        phase.add()

        # Update the phase
        phase.name = "Updated_Phase"
        phase.duration = 200
        phase.update()

        updated_phase = db.session.get(Phase, phase.id)
        assert updated_phase.name == "Updated_Phase"
        assert updated_phase.duration == 200

def test_phase_deletion(phase_data, app):
    with app.app_context():
        phase = Phase(**phase_data)
        
        phase.add()
        phase.delete()
        deleted_phase = db.session.get(Phase, phase.id)
        assert deleted_phase.status == "deleted"

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

def test_get_phases_active(app):
    with app.app_context():
        phases = Phase.get_phases(active=True)
        
        assert len(phases) > 0
        assert all(isinstance(phase, Phase) for phase in phases)
        assert all(phase.status == "active" for phase in phases)
        assert all(phase.name is not None for phase in phases)
        assert all(phase.duration is not None for phase in phases)
        assert all(phase.order is not None for phase in phases)

def test_phase_validation(phase_data_for_validation, app):
    with app.app_context():
        phase = Phase(**phase_data_for_validation)

        # Test valid phase
        phase.validate()

        # Test invalid name
        phase.name = ""
        with pytest.raises(ValueError, match="Il nome della fase non può essere vuoto"):
            phase.validate()
        phase.name = "Test_New_Phase"

        # Test invalid duration
        phase.duration = -1
        with pytest.raises(ValueError, match="La durata della fase deve essere maggiore di zero"):
            phase.validate()
        phase.duration = 100

        # Test invalid order
        phase.order = None
        with pytest.raises(ValueError, match="L'ordine della fase non può essere vuoto"):
            phase.validate()
        phase.order = 1
        # Test invalid status
        phase.status = None
        with pytest.raises(ValueError, match="Lo stato della fase non può essere vuoto"):
            phase.validate()
        phase.status = "active"
        # Test duplicate name
        duplicate_phase = Phase(name=phase.name, duration=50)
        duplicate_phase.add()
        with pytest.raises(ValueError, match=f"Il nome della fase {phase.name} è già in uso"):
            phase.validate()
