from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

#####################################################################
# Device Model
# This model represents a device in the DMX system.
# id: Unique identifier for the device.
# name: Name of the device.
# type: Type of the device (e.g., light, mechanical, audio).
# subtype: Subtype of the device (e.g., LED, speaker).
# dmx_channels: Number of DMX channels used by the device.
# status: Status of the device (e.g., on, off, error).
# 

class Device(db.Model):
    __tablename__ = 'device'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    type: Mapped[str] = mapped_column(String(80), nullable=False)
    subtype: Mapped[str] = mapped_column(String(80), nullable=False)
    dmx_channels: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(80), nullable=False)

    # Relationships one to many with Channel
    channels: Mapped[list["Channel"]] = relationship("Channel", back_populates="device", cascade="all, delete-orphan") # type: ignore

    def __repr__(self) -> str:
        return f'<Device {self.name}>'
    
    def validate(self) -> None:
        """
        Validate the device attributes.
        """
        if not self.name:
            raise ValueError("Il nome del dispositivo non può essere vuoto")
        if not self.type:
            raise ValueError("Il tipo del dispositivo non può essere vuoto")
        if not self.subtype:
            raise ValueError("Il sottotipo del dispositivo non può essere vuoto")
        if not self.dmx_channels:
            raise ValueError("Il numero di canali dmx del dispositivo non può essere vuoto")
        if not self.status:
            raise ValueError("Lo stato del dispositivo non può essere vuoto")
        # Check if the name is not already in use by another device
        if self.id is None:
            if db.session.query(Device).filter_by(name=self.name).first() is not None:
                raise ValueError(f"Il nome del dispositivo {self.name} è già in uso")
        else:
            if db.session.query(Device).filter_by(name=self.name).filter(Device.id != self.id).first() is not None:
                raise ValueError(f"Il nome del dispositivo {self.name} è già in uso")
            
    
    def add(self) -> None:
        """
        Add the device to the database.
        """
        self.validate()
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        """
        Update the device in the database.
        """
        self.validate()
        db.session.commit()

    def delete(self) -> None:
        """
        Delete the device from the database.
        """
        db.session.delete(self)
        db.session.commit()