from config import Config

from flask import Blueprint, render_template, flash, request, redirect, url_for

from sqlalchemy.orm import joinedload
from app.models import Device, Channel, Phase, Keyframe

# Creazione del Blueprint
devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/devices_management/', methods=['GET', 'POST'])
def devices_management():
    devices = (
        Device.query
        .order_by(Device.id)
        .options(joinedload(Device.channels))
        .all()
    )
    return render_template('devices_management.html', devices=devices)

@devices_bp.route('/turn_on_off_device/<int:device_id>', methods=['GET'])
def turn_on_off_device(device_id):
    """
    Accende o spegne un dispositivo.
    """
    device = Device.query.filter_by(id=device_id).first()
    if device:
        if device.status == "on":
            device.status = "off"
            flash(f"Dispositivo {device.name} spento", 'success')
        else:
            device.status = "on"
            flash(f"Dispositivo {device.name} acceso", 'success')
        device.update()
    else:
        flash('Dispositivo non trovato', 'error')
    
    return redirect(url_for('devices.devices_management'))