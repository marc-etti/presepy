from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

#####################################################################
# Channel Model
# This model represents a DMX channel in the DMX system.
# id: Unique identifier for the channel.
# device_id: Foreign key referencing the device to which the channel belongs.
# number: Number of the channel within the device. (1 to 512)
# type: Type of the channel (e.g., led_red, led_green).
# value: Current value of the channel (0-255).


class Channel(db.Model):
    __tablename__ = 'channel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id'), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(80), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, device_id, number, type, value) -> None:
        self.device_id = device_id
        self.number = number
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f'<Channel {self.number} of Device {self.device_id}>'