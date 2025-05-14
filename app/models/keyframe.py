from app import db
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    # Relationships many to one with Channel
    channel: Mapped["Channel"] = relationship("Channel", back_populates="keyframes") # type: ignore
    # Relationships many to one with Phase
    phase: Mapped["Phase"] = relationship("Phase", back_populates="keyframes") # type: ignore

    def __repr__(self) -> str:
        return f'<Keyframe {self.description} of Channel {self.channel_id} in Phase {self.phase_id}>'
        
    
    def update(self) -> None:
        """
        Update the keyframe in the database.
        """
        # TODO: implement control logic to update the keyframe
        db.session.commit()

    def add(self) -> None:
        """
        Add the keyframe to the database.
        """
        # Controllo che il valore sia compreso tra 0 e 255
        if not (0 <= self.value <= 255):
            raise ValueError(f"Value {self.value} is out of range (0-255)")
        # Controllo che la posizione sia compresa tra 0 e 100
        if not (0 <= self.position <= 100):
            raise ValueError(f"Position {self.position} is out of range (0-100)")
        # Controllo che la descrizione non sia vuota
        if not self.description:
            raise ValueError("Description cannot be empty")
        # Controllo che non esista già un keyframe nella stessa posizione
        existing_keyframe = Keyframe.query.filter_by(
            channel_id=self.channel_id,
            phase_id=self.phase_id,
            position=self.position
        ).first()
        if existing_keyframe:
            raise ValueError(f"Keyframe already exists at position {self.position} for channel {self.channel_id} in phase {self.phase_id}")

        db.session.add(self)
        db.session.commit()