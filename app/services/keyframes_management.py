from config import Config

from flask import Blueprint, render_template, flash, request, redirect, url_for

from sqlalchemy.orm import joinedload
from app.models import Device, Channel, Phase, Keyframe

# Creazione del Blueprint
keyframes_bp = Blueprint('keyframes', __name__)

@keyframes_bp.route('/keyframes_management/<int:device_id>', methods=['GET', 'POST'])
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
    
@keyframes_bp.route('/edit_keyframe_form/<int:device_id>/<int:phase_id>/<int:position>', methods=['GET'])
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

@keyframes_bp.route('/edit_keyframe', methods=['POST'])
def edit_keyframe():
    """
    Aggiorna un keyframe esistente nel database.
    """
    form_data = request.form
    for key, value in form_data.items():
        if key.startswith('slider-'):
            keyframe_id = int(key.split('-')[1])
            description = form_data.get(f'description-{keyframe_id}')
            keyframe = Keyframe.query.get(keyframe_id)
            if keyframe:
                keyframe.value = int(value)
                keyframe.description = description
                keyframe.update()
    device_id = int(form_data.get('device_id'))
    flash('Keyframe updated successfully', 'success')
    return redirect(url_for('keyframes.keyframes_management', device_id=device_id))

@keyframes_bp.route('/add_keyframe_form/<int:device_id>/<int:phase_id>', methods=['GET'])
def add_keyframe_form(device_id, phase_id):
    """
    Restituisce il form per aggiungere un keyframe.
    """
    device = Device.query.filter_by(id=device_id).first()
    channels = (
        Channel.query
        .filter_by(device_id=device_id)
        .order_by(Channel.number)
        .all()
    )
    phase = Phase.query.filter_by(id=phase_id).first()
    return render_template('keyframes_form.html', device=device, channels=channels, phase=phase)

@keyframes_bp.route('/add_keyframe', methods=['POST'])
def add_keyframe():
    """
    Aggiunge un nuovo keyframe al database.
    """
    form_data = request.form
    device_id = int(form_data.get('device_id'))
    phase_id = int(form_data.get('phase_id'))
    position = int(form_data.get('position'))
    
    new_keyframes = []
    for key, value in form_data.items():
        if key.startswith('slider-'):
            channel_id = int(key.split('-')[1])
            description = form_data.get(f'description-{channel_id}')
            new_keyframes.append(
                Keyframe(
                    channel_id=channel_id,
                    phase_id=phase_id,
                    description=description,
                    position=position,
                    value=int(value)
                )
            )
    # Check if the number of keyframes matches the number of channels
    device = Device.query.filter_by(id=device_id).first()
    channels_ids = [channel.id for channel in device.channels]
    if len(new_keyframes) != len(channels_ids):
        flash('Il numero di keyframe non corrisponde al numero di canali', 'error')
        return redirect(url_for('keyframes.keyframes_management', device_id=device_id))
    for keyframe in new_keyframes:
        try:
            keyframe.add()
        except Exception as e:
            flash(f'Error adding keyframe: {str(e)}', 'error')
            return redirect(url_for('keyframes.keyframes_management', device_id=device_id))
            
    flash('Keyframe aggiunto correttamente', 'success')
    return redirect(url_for('keyframes.keyframes_management', device_id=device_id))

@keyframes_bp.route('/delete_keyframe', methods=['POST'])
def delete_keyframe():
    """
    Elimina un keyframe esistente dal database.
    """
    form_data = request.form
    device_id = int(form_data.get('device_id'))
    phase_id = int(form_data.get('phase_id'))
    position = int(form_data.get('position'))
    
    device = Device.query.filter_by(id=device_id).first()

    channels_ids = [channel.id for channel in device.channels]

    keyframes = Keyframe.query.filter_by(
        phase_id=phase_id,
        position=position
    ).filter(Keyframe.channel_id.in_(channels_ids)).all()

    if len(keyframes) != len(channels_ids):
        flash('Il numero di keyframe da eliminare non corrisponde al numero di canali', 'error')
        return redirect(url_for('keyframes.keyframes_management', device_id=device_id))
    
    try:
        for keyframe in keyframes:
            keyframe.delete()
    except Exception as e:
        flash(f'Error deleting keyframe: {str(e)}', 'error')
        return redirect(url_for('keyframes.keyframes_management', device_id=device_id))

    flash('Keyframe deleted successfully', 'success')

    return redirect(url_for('keyframes.keyframes_management', device_id=device_id))