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
# status: Status of the phase (active, deactivated, deleted).

class Phase(db.Model):
    __tablename__ = 'phase'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(80), nullable=False)

    # Relationships one to many with Keyframe
    keyframes: Mapped[list["Keyframe"]] = relationship("Keyframe", back_populates="phase") # type: ignore

    def __repr__(self) -> str:
        return f'<Fase: {self.name} di durata {self.duration} secondi>'
    
    def get_phases( active=False ) -> list:
        """
        Restituisce tutte le fasi ordinate.
        Se active è True, restituisce solo le fasi attive.
        """
        if active:
            phases = Phase.query.filter_by(status="active").order_by(Phase.order).all()
        else:
            phases = Phase.query.order_by(Phase.order).all()
        if not phases:
            raise ValueError("Nessuna fase trovata nel database")
        return phases
    
    def validate(self) -> None:
        """
        Valida gli attributi della fase.
        """
        if self.name is None or self.name.strip() == "":
            raise ValueError("Il nome della fase non può essere vuoto")
        if self.duration is None:
            raise ValueError("La durata della fase non può essere vuota")
        if self.duration <= 0:
            raise ValueError("La durata della fase deve essere maggiore di zero")
        if self.order is None:
            raise ValueError("L'ordine della fase non può essere vuoto")
        if not self.status:
            raise ValueError("Lo stato della fase non può essere vuoto")
        # Check if the name is not already in use by another phase
        if self.id is None:
            if db.session.query(Phase).filter_by(name=self.name).first() is not None:
                raise ValueError(f"Il nome della fase {self.name} è già in uso")
        else:
            if db.session.query(Phase).filter_by(name=self.name).filter(Phase.id != self.id).first() is not None:
                raise ValueError(f"Il nome della fase {self.name} è già in uso")

    def add(self) -> None:
        """
        Aggiunge la fase al database.
        """
        self.order = 0
        self.status = "deactivated"
        self.validate()
        db.session.add(self)
        db.session.commit()

    
    def update(self) -> None:
        """
        Aggiorna la fase nel database.
        """
        self.validate()
        db.session.commit()
        

    def delete(self) -> None:
        """
        Elimina la fase dal database.
        """
        self.status = "deleted"
        db.session.commit()

    def move_up_down(self, direction: str) -> None:
        """
        Cambia la posizione della fase nell'ordine.
        direction: "up" per spostare su, "down" per spostare giù.
        """
        if self.status != "active":
            raise ValueError("La fase deve essere attiva per poter essere spostata")
        
        if direction not in ["up", "down"]:
            raise ValueError("La direzione deve essere 'up' o 'down'")
        
        # Trovo la fase precedente o successiva
        if direction == "up":
            if self.order == 1:
                raise ValueError("La fase è già al primo posto e non può essere spostata su")
            # Trovo le fasi da spostare giù
            phase_to_move_down = db.session.query(Phase).filter(
                Phase.order < self.order,
                Phase.status == "active"
            ).order_by(Phase.order.desc()).first()
            if not phase_to_move_down:
                raise ValueError("Nessuna fase precedente trovata per lo spostamento")
            # Sposto la fase precedente giù
            phase_to_move_down.order += 1
            # Sposto la fase corrente su
            self.order -= 1
        else: # direction == "down"
            if self.order == db.session.query(Phase).filter_by(status="active").count():
                raise ValueError("La fase è già all'ultimo posto e non può essere spostata giù")
            phase_to_move_up = db.session.query(Phase).filter(
                Phase.order > self.order,
                Phase.status == "active"
            ).order_by(Phase.order).first()
            if not phase_to_move_up:
                raise ValueError("Nessuna fase successiva trovata per lo spostamento")
            # Sposto la fase successiva su
            phase_to_move_up.order -= 1
            # Sposto la fase corrente giù
            self.order += 1
        db.session.commit()

    def activate(self) -> None:
        """
        Attiva la fase.
        """
        order_count = db.session.query(Phase).filter_by(status="active").count()
        self.order = order_count + 1
        self.status = "active"
        db.session.commit()

    def deactivate(self) -> None:
        """
        Disattiva la fase.
        """
        self.status = "deactivated"
        phases_to_move_up = db.session.query(Phase).filter(
            Phase.order > self.order,
            Phase.status == "active"
        ).all()
        for phase in phases_to_move_up:
            phase.order -= 1
        self.order = 0
        db.session.commit()