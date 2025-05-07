from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

#####################################################################
# Keyframe Model
# This model represents a keyframe in the DMX system.
# id: Unique identifier for the keyframe.
# channel_id: Foreign key referencing the device to which the keyframe belongs.
# phase_id: Foreign key referencing the phase to which the keyframe belongs.
# name: Name of the keyframe.
# position: Position of the keyframe in the phase (0-100%).
# value: Value of the keyframe (0-255).

class Keyframe(db.Model):
    __tablename__ = 'keyframe'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey('channel.id'), nullable=False)
    phase_id: Mapped[int] = mapped_column(ForeignKey('phase.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)