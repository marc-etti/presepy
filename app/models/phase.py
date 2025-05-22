from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    # Relationships one to many with Keyframe
    keyframes: Mapped[list["Keyframe"]] = relationship("Keyframe", back_populates="phase") # type: ignore

    def __repr__(self) -> str:
        return f'<Fase: {self.name} di durata {self.duration} secondi>'
    
    def get_phases() -> list:
        """Restituisce tutte le fasi."""
        return Phase.query.order_by(Phase.order).all()
    
    def add(self) -> None:
        """
        Aggiunge la fase al database.
        """
        raise NotImplementedError("La funzione add non è ancora implementata")
    
    def update(self) -> None:
        """
        Aggiorna la fase nel database.
        """
        raise NotImplementedError("La funzione update non è ancora implementata")
    
    def delete(self) -> None:
        """
        Elimina la fase dal database.
        """
        raise NotImplementedError("La funzione delete non è ancora implementata")
            
