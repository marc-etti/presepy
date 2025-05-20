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
        return f'<Channel {self.number} of Device {self.device_id}>'
    
    def add(self) -> None:
        """
        Add the channel to the database.
        """
        # Check if the channel number is valid (1 to 512)
        if not (1 <= self.number <= 512):
            raise ValueError(f"Channel number {self.number} is out of range (1-512)")
        # Check if the value is valid (0-255)
        if not (0 <= self.value <= 255):
            raise ValueError(f"Value {self.value} is out of range (0-255)")
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        """
        Update the channel in the database.
        """
        # Check if the channel number is valid (1 to 512)
        if not (1 <= self.number <= 512):
            raise ValueError(f"Channel number {self.number} is out of range (1-512)")
        # Check if the value is valid (0-255)
        if not (0 <= self.value <= 255):
            raise ValueError(f"Value {self.value} is out of range (0-255)")
        # Check if the channel exists in the database
        existing_channel = db.session.get(Channel, self.id)
        if not existing_channel:
            raise ValueError(f"Channel with id {self.id} does not exist")
        db.session.commit()

    def delete(self) -> None:
        """
        Delete the channel from the database.
        """
        db.session.delete(self)
        db.session.commit()