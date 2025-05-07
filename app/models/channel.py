from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

#####################################################################
# Channel Model
# This model represents a DMX channel in the DMX system.
# id: Unique identifier for the channel.
# device_id: Foreign key referencing the device to which the channel belongs.
# channel_number: Number of the channel within the device. (1 to 512)
# channel_type: Type of the channel (e.g., led_red, led_green).
# channel_value: Current value of the channel (0-255).


class Channel(db.Model):
    __tablename__ = 'channel'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id'), nullable=False)
    channel_number: Mapped[int] = mapped_column(Integer, nullable=False)
    channel_type: Mapped[str] = mapped_column(String(80), nullable=False)
    channel_value: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, device_id, channel_number, channel_type, channel_value) -> None:
        self.device_id = device_id
        self.channel_number = channel_number
        self.channel_type = channel_type
        self.channel_value = channel_value

    def __repr__(self) -> str:
        return f'<Channel {self.channel_number} of Device {self.device_id}>'