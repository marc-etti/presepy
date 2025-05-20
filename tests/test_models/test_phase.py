import pytest
from app.models.phase import Phase
from app import db

@pytest.fixture(autouse=True)
def setup_database(app):
    with app.app_context():
        db.create_all()
        # Inserisci alcune fasi di esempio
        phase1 = Phase(id=1, name="ALBA", duration=600, order=1)
        phase2 = Phase(id=2, name="GIORNO", duration=3600, order=2)
        phase3 = Phase(id=3, name="SERA", duration=900, order=3)
        phase4 = Phase(id=4, name="NOTTE", duration=3600, order=4)
        db.session.add_all([phase1, phase2, phase3, phase4])
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()

def test_phase_repr(app):
    with app.app_context():
        phase = Phase.query.filter_by(name="ALBA").first()
        assert repr(phase) == "<Phase ALBA>"

def test_get_phases(app):
    with app.app_context():
        phases = Phase.get_phases()
        assert len(phases) == 4
        assert [p.name for p in phases] == ["ALBA", "GIORNO", "SERA", "NOTTE"]

def test_add_not_implemented(app):
    with app.app_context():
        phase = Phase.query.first()
        with pytest.raises(NotImplementedError):
            phase.add()

def test_delete_not_implemented(app):
    with app.app_context():
        phase = Phase.query.first()
        with pytest.raises(NotImplementedError):
            phase.delete()

def test_update_phase(app):
    with app.app_context():
        phase = Phase.query.filter_by(name="ALBA").first()
        phase.duration = 700
        phase.update()
        updated = Phase.query.filter_by(name="ALBA").first()
        assert updated.duration == 700