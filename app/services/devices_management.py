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

@devices_bp.route('/add_device_form/', methods=['GET', 'POST'])
def add_device_form(form_data=None):
    """
    Mostra il form per aggiungere un dispositivo.
    """
    return render_template('devices_form.html', form_data=form_data)

@devices_bp.route('/add_device/', methods=['POST'])
def add_device():
    """
    Aggiunge un dispositivo al database.
    """
    form_data = request.form

    name = form_data.get('name')
    type = form_data.get('type')
    subtype = form_data.get('subtype')
    dmx_channels = int(form_data.get('dmx_channels'))
    # status = form_data.get('status')
    status = "on"

    if not name or not type or not subtype or not dmx_channels or not status:
        flash('Tutti i campi sono obbligatori', 'error')
        return render_template('devices_form.html', form_data=form_data)

    # Verifica se il nome del dispositivo esiste già
    existing_device = Device.query.filter_by(name=name).first()
    if existing_device:
        flash('Nome del dispositivo già usato', 'error')
        return render_template('devices_form.html', form_data=form_data)
    
    # Recupero gli indirizzi dei canali dal form
    channels = []
    for i in range(1, dmx_channels + 1):
        channel_type = form_data.get(f'channel-type-{i}')
        channel_number = form_data.get(f'channel-number-{i}')
        channel_value = form_data.get(f'channel-value-{i}')
        if channel_type and channel_number and channel_value:
            channels.append({
                'type': channel_type,
                'number': channel_number,
                'value': channel_value
            })
        else:
            flash('Tutti i campi dei canali sono obbligatori', 'error')
            print(f"Errore nei valori: {channel_type}, {channel_number}, {channel_value}")

            return render_template('devices_form.html', form_data=form_data)
    
    # Controllo se gli indirizzi dei canali non siano già utilizzati
    for channel in channels:
        existing_channel = Channel.query.filter_by(number=channel['number']).first()
        if existing_channel:
            flash(f'Il canale {channel["number"]} è già utilizzato', 'error')
            return render_template('devices_form.html', form_data=form_data)
    
    # Crea un nuovo dispositivo lo aggiunge al database e ottene il suo ID
    new_device = Device(
        name=name,
        type=type,
        subtype=subtype,
        dmx_channels=dmx_channels,
        status=status
    )
    try:
        new_device.add()
    except Exception as e:
        flash(f'Errore durante l\'aggiunta del dispositivo: {e}', 'error')
        return render_template('devices_form.html', form_data=form_data)
    flash(f'Dispositivo {name} aggiunto con successo', 'success')

    # Aggiungi i canali associati al dispositivo
    for channel in channels:
        new_channel = Channel(
            device_id=new_device.id,
            number=int(channel['number']),
            type=channel['type'],
            value=int(channel['value'])
        )
        try:
            new_channel.add()
        except Exception as e:
            flash(f'Errore durante l\'aggiunta del canale: {e}', 'error')
            return render_template('devices_form.html', form_data=form_data)
    flash(f'Canali per il dispositivo {name} aggiunti con successo', 'success')

    return redirect(url_for('devices.devices_management'))


@devices_bp.route('/delete_device', methods=['POST'])
def delete_device():
    """
    Elimina un dispositivo dal database.
    """
    device_id = int(request.form.get('device_id'))
    device = Device.query.filter_by(id=device_id).first()
    if device:
        # Elimina i canali e i keyframes associati al dispositivo
        channels = Channel.query.filter_by(device_id=device.id).all()
        for channel in channels:
            keyframes = Keyframe.query.filter_by(channel_id=channel.id).all()
            if keyframes:   
                for keyframe in keyframes:
                    # Elimina i keyframes associati al canale
                    keyframe.delete()
            # Elimina il canale
            channel.delete()
        # Elimina il dispositivo
        device.delete()
        flash(f'Dispositivo {device.name} eliminato con successo', 'success')
    else:
        flash('Dispositivo non trovato', 'error')
    
    return redirect(url_for('devices.devices_management'))

@devices_bp.route('/edit_device_form/<int:device_id>', methods=['GET', 'POST'])
def edit_device_form(device_id):
    """
    Mostra il form per modificare un dispositivo.
    """
    device = Device.query.filter_by(id=device_id).first()
    if not device:
        flash('Dispositivo non trovato', 'error')
        return redirect(url_for('devices.devices_management'))
    
    channels = (
        Channel.query
        .filter_by(device_id=device_id)
        .order_by(Channel.number)
        .all()
    )
    
    return render_template('devices_form.html', device=device, channels=channels)

@devices_bp.route('/edit_device', methods=['POST'])
def edit_device():
    """
    Modifica un dispositivo esistente nel database.
    """
    form_data = request.form
    device_id = int(form_data.get('device_id'))
    name = form_data.get('name')
    type = form_data.get('type')
    subtype = form_data.get('subtype')

    if not name or not type or not subtype:
        flash('Tutti i campi sono obbligatori', 'error')
        return redirect(url_for('devices.edit_device_form', device_id=device_id))
    
    # Verifica se il nome del dispositivo esiste già
    existing_device = Device.query.filter_by(name=name).first()
    if existing_device and existing_device.id != device_id:
        flash('Nome del dispositivo già usato', 'error')
        return redirect(url_for('devices.edit_device_form', device_id=device_id))
    
    # Modifica il dispositivo e aggiorna il database
    device = Device.query.filter_by(id=device_id).first()
    if device:
        device.name = name
        device.type = type
        device.subtype = subtype
    else:
        flash('Dispositivo non trovato', 'error')
        return redirect(url_for('devices.devices_management'))
    
    # Modifica i canali associati al dispositivo
    for channel in device.channels:
        channel_number = int(form_data.get(f'channel-number-{channel.id}'))
        # controllo se il canale non sia già utilizzato
        existing_channel = Channel.query.filter_by(number=channel_number).first()
        if existing_channel and existing_channel.id != channel.id:
            flash(f'Il canale {channel_number} è già utilizzato', 'error')
            return redirect(url_for('devices.edit_device_form', device_id=device_id))

        channel_type = form_data.get(f'channel-type-{channel.id}')
        channel_value = int(form_data.get(f'channel-value-{channel.id}'))

        if channel_number and channel_type and channel_value:
            channel.number = channel_number
            channel.type = channel_type
            channel.value = channel_value
            try:
                channel.update()
            except Exception as e:
                flash(f'Errore durante l\'aggiornamento del canale: {e}', 'error')
                return redirect(url_for('devices.edit_device_form', device_id=device_id))

    # Aggiorno il dispositivo       
    try: 
        device.update()
    except Exception as e:
        flash(f'Errore durante l\'aggiornamento del dispositivo: {e}', 'error')
        return redirect(url_for('devices.edit_device_form', device_id=device_id))
    # Flash success message
    flash(f'Dispositivo {name} modificato con successo', 'success')

    return redirect(url_for('devices.devices_management'))