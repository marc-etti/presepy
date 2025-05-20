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
    description: Mapped[str] = mapped_column(String(80), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships many to one with Channel
    channel: Mapped["Channel"] = relationship("Channel", back_populates="keyframes") # type: ignore
    # Relationships many to one with Phase
    phase: Mapped["Phase"] = relationship("Phase", back_populates="keyframes") # type: ignore

    def __repr__(self) -> str:
        return f'<Keyframe {self.description} of Channel {self.channel.number} in Phase {self.phase.name}>'
    
    def validate(self) -> None:
        if not (0 <= self.value <= 255):
            raise ValueError(f"Il valore scelto: {self.value} è fuori dal range (0-255)")
        if not (0 <= self.position <= 100):
            raise ValueError(f"La posizione scelta: {self.position} è fuori dal range (0-100)")
        if not self.description:
            raise ValueError("Description cannot be empty")
        existing_keyframe = db.session.query(Keyframe).filter_by(
            channel_id=self.channel_id,
            phase_id=self.phase_id,
            position=self.position
        ).first()
        if existing_keyframe and (not hasattr(self, "id") or existing_keyframe.id != self.id):
            raise ValueError(
                f"Esiste già un keyframe nella posizione {self.position} per il canale {existing_keyframe.channel.number} nella fase {existing_keyframe.phase.name}"
            )
        
    def add(self) -> None:
        """
        Add the keyframe to the database.
        """
        self.validate()
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        """
        Update the keyframe in the database.
        """
        self.validate()
        db.session.commit()

    def delete(self) -> None:
        """
        Delete the keyframe from the database.
        """
        db.session.delete(self)
        db.session.commit()