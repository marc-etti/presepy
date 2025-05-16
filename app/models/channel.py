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
    
    def update(self) -> None:
        """
        Update the channel in the database.
        """
        db.session.commit()

    def add(self) -> None:
        """
        Add the channel to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        """
        Delete the channel from the database.
        """
        db.session.delete(self)
        db.session.commit()