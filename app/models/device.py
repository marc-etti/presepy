from app import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

#####################################################################
# Device Model
# This model represents a device in the DMX system.
# id: Unique identifier for the device.
# name: Name of the device.
# type: Type of the device (e.g., light, mechanical, audio).
# subtype: Subtype of the device (e.g., LED, speaker).
# dmx_address: DMX address of the device.
# dmx_channels: Number of DMX channels used by the device.
# status: Status of the device (e.g., on, off, error).
# 

class Device(db.Model):
    __tablename__ = 'device'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String(80), nullable=False)
    subtype: Mapped[str] = mapped_column(String(80), nullable=False)
    dmx_address: Mapped[int] = mapped_column(Integer, nullable=False)
    dmx_channels: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(80), nullable=False)

    def __init__(self, name, type, subtype, dmx_address, dmx_channels, status) -> None:
        self.name = name
        self.type = type
        self.subtype = subtype
        self.dmx_address = dmx_address
        self.dmx_channels = dmx_channels
        self.status = status

    def __repr__(self) -> str:
        return f'<Device {self.name}>'
    
