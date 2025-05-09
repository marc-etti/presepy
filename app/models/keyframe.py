from app import db
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

#####################################################################
# Keyframe Model
# This model represents a keyframe in the DMX system.
# id: Unique identifier for the keyframe.
# channel_id: Foreign key referencing the device to which the keyframe belongs.
# phase_id: Foreign key referencing the phase to which the keyframe belongs.
# description: Description of the keyframe ("Inizio", "Fine", "Intermedio").
# position: Position of the keyframe in the phase (0-100%).
# value: Value of the keyframe (0-255).

class Keyframe(db.Model):
    __tablename__ = 'keyframe'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey('channel.id'), nullable=False)
    phase_id: Mapped[int] = mapped_column(ForeignKey('phase.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, channel_id, phase_id, description, position, value) -> None:
        self.channel_id = channel_id
        self.phase_id = phase_id
        self.description = description
        self.position = position
        self.value = value

    def __repr__(self) -> str:
        return f'<Keyframe {self.description} of Channel {self.channel_id} in Phase {self.phase_id}>'
    
    def add_keyframe(self, channel_id, phase_id, description, position, value):
        """Aggiunge un keyframe al faro."""
        # Controllo se i dati sono validi
        if position < 0 or position > 100:
            raise ValueError("La posizione del keyframe deve essere compresa tra 0 e 100.")
        if value < 0 or value > 255:
            raise ValueError("Il valore del keyframe deve essere compreso tra 0 e 255.")
        # Controllo se il keyframe esiste già
        kf = Keyframe.query.filter_by(
            channel_id=channel_id,
            phase_id=phase_id,
            position=position,
        ).first()
        if kf is not None:
            raise ValueError(f"Il keyframe {kf} esiste già nel database.")
        
        # Aggiungo il keyframe al database
        kf = Keyframe(channel_id, phase_id, description, position, value)
        db.session.add(kf)
        db.session.commit()

    def edit_keyframe(self, id, position, value):
        """Modifica un keyframe esistente."""
        # Controllo se i dati sono validi
        if position < 0 or position > 100:
            raise ValueError("La posizione del keyframe deve essere compresa tra 0 e 100.")
        if value < 0 or value > 255:
            raise ValueError("Il valore del keyframe deve essere compreso tra 0 e 255.")
        
        # Modifico il keyframe nel database
        kf = Keyframe.query.get(id)
        if kf is None:
            raise ValueError(f"Il keyframe con id {id} non esiste nel database.")
        
        kf.position = position
        kf.value = value
        db.session.commit()

    def get_keyframes_by_channel(self, channel_id):
        """Restituisce tutti i keyframe di un canale."""
        return Keyframe.query.filter_by(channel_id=channel_id).all()