from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

#####################################################################
# Phase Model
# This model represents a phase in the DMX system.
# id: Unique identifier for the phase.
# name: Name of the phase. (ALBA, GIORNO, SERA, NOTTE)
# duration: Duration of the phase in seconds.
# order: Order of the phase

class Phase(db.Model):
    __tablename__ = 'phase'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, name, duration) -> None:
        self.name = name
        self.duration = duration

    def __repr__(self) -> str:
        return f'<Phase {self.name}>'