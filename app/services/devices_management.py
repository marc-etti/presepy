from config import Config

from flask import Blueprint, jsonify, render_template, flash, request, redirect, url_for

from sqlalchemy.orm import joinedload
from app.models import Device, Channel, Phase, Keyframe

from app.services.devices_utils.lights_utils import get_lights

# Creazione del Blueprint
devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/get_lights_info', methods=['GET'])
def get_lights_info():
    lights = get_lights()
    return jsonify(lights)

@devices_bp.route('/get_devices_info', methods=['GET'])
def get_devices_info():
    """
    Restituisce tutti i dispositivi presenti nel database.
    """
    devices = Device.query.all()
    return render_template('devices_management.html', devices=devices)

@devices_bp.route('/keyframes_management/<int:device_id>', methods=['GET', 'POST'])
def keyframes_management(device_id):
    """
    Restituisce le informazioni di un dispositivo specifico.
    """
    device = Device.query.filter_by(id=device_id).first()
    phases = Phase.query.order_by(Phase.order).all()
    channels = (
        Channel.query
        .filter_by(device_id=device_id)
        .order_by(Channel.number)
        .options(joinedload(Channel.keyframes))
        .all()
    )

    for channel in channels:
        channel.keyframes.sort(key=lambda x: x.position)
    
    return render_template('keyframes_management.html', device=device, phases=phases, channels=channels)
    
@devices_bp.route('/edit_keyframe_form/<int:device_id>/<int:phase_id>/<int:position>', methods=['GET'])
def edit_keyframe_form(device_id, phase_id, position):
    """
    Restituisce il form per modificare un keyframe.
    """
    device = Device.query.filter_by(id=device_id).first()
    
    channels_ids = [channel.id for channel in device.channels]
    keyframes = (
        Keyframe.query
        .filter_by(phase_id=phase_id, position=position)
        .filter(Keyframe.channel_id.in_(channels_ids))
        .order_by(Keyframe.channel_id)
        .all()
    )
    if not keyframes:
        flash('Keyframe not found', 'error')
        return render_template('keyframes_management.html', device=device)
    
    return render_template('keyframes_form.html', device=device, keyframes=keyframes)

@devices_bp.route('/update_keyframe', methods=['POST'])
def update_keyframe():
    form_data = request.form
    for key, value in form_data.items():
        if key.startswith('slider-'):
            keyframe_id = int(key.split('-')[1])
            keyframe = Keyframe.query.get(keyframe_id)
            if keyframe:
                keyframe.value = value
                keyframe.update()
    device_id = int(form_data.get('device_id'))
    flash('Keyframe updated successfully', 'success')
    return redirect(url_for('devices.keyframes_management', device_id=device_id))