from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

#####################################################################
# Channel Model
# This model represents a DMX channel in the DMX system.
# id: Unique identifier for the channel.
# device_id: Foreign key referencing the device to which the channel belongs.
# number: Number of the channel within the device. (1 to 512)
# type: Type of the channel (e.g., led_red, led_green).
# value: Default value of the channel (0-255).


class Channel(db.Model):
    __tablename__ = 'channel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id'), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(80), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships many to one with Device
    device: Mapped["Device"] = relationship("Device", back_populates="channels") # type: ignore

    # Relationships one to many with Keyframe
    keyframes: Mapped[list["Keyframe"]] = relationship("Keyframe", back_populates="channel") # type: ignore

    def __repr__(self) -> str:
        return f'<Canale numero: {self.number} associato al dispositivo: {self.device.name}>'
    
    def validate(self) -> None:
        """
        Validate the channel attributes.
        """
        # Check if the channel number is not already in use by another device
        if self.id is None:
            existing_channel = db.session.query(Channel).filter_by(number=self.number).first()
            if existing_channel is not None: 
                raise ValueError(f"Il canale numero {existing_channel.number} è già usato dal dispositivo {existing_channel.device.name}")
        else:
            existing_channel = db.session.query(Channel).filter_by(number=self.number).filter(Channel.id != self.id).first()
            if existing_channel:
                raise ValueError(f"Il canale numero {existing_channel.number} è già usato dal dispositivo {existing_channel.device.name}")
        # Check if the channel number is valid (1 to 512)
        if not (1 <= self.number <= 512):
            raise ValueError(f"Il numero del canale scelto: {self.number} è fuori dal range (1-512)")
        # Check if the value is valid (0-255)
        if not (0 <= self.value <= 255):
            raise ValueError(f"Il valore scelto: {self.value} è fuori dal range (0-255)")
        # Check if the type is not empty
        if not self.type:
            raise ValueError("Il tipo del canale non può essere vuoto")
    
    def add(self) -> None:
        """
        Add the channel to the database.
        """
        self.validate()
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        """
        Update the channel in the database.
        """
        self.validate()
        db.session.commit()

    def delete(self) -> None:
        """
        Delete the channel from the database.
        """
        db.session.delete(self)
        db.session.commit()