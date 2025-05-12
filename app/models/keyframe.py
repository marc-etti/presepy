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