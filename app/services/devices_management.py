from config import Config

from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required

from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from app.models import Device, Channel, Phase, Keyframe
from app import db

# Creazione del Blueprint
devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/devices_management/', methods=['GET', 'POST'])
@login_required
def devices_management():
    devices = (
        Device.query
        .order_by(Device.id)
        .options(joinedload(Device.channels))
        .all()
    )
    return render_template('devices_management.html', devices=devices)

@devices_bp.route('/turn_on_off_device/<int:device_id>', methods=['GET'])
@login_required
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
@login_required
def add_device_form(form_data=None):
    """
    Mostra il form per aggiungere un dispositivo.
    """
    return render_template('devices_form.html', form_data=form_data)

@devices_bp.route('/add_device/', methods=['POST'])
@login_required
def add_device():
    """
    Aggiunge un dispositivo al database.
    """
    form_data = request.form

    try:
        required_fields = ['name', 'type', 'subtype', 'dmx_channels']
        if not all(form_data.get(field) for field in required_fields):
            raise ValueError("Tutti i campi del dispositivo sono obbligatori")

        name = form_data.get('name')
        type = form_data.get('type')
        subtype = form_data.get('subtype')
        dmx_channels = int(form_data.get('dmx_channels'))
        # status = form_data.get('status')
        status = "on"
    
        # Recupero gli indirizzi dei canali dal form
        channels = []
        for i in range(1, dmx_channels + 1):
            channel_data = {
                'type' : form_data.get(f'channel-type-{i}'),
                'number' : form_data.get(f'channel-number-{i}'),
                'value' : form_data.get(f'channel-value-{i}')
            }

            if None in channel_data.values():
                raise ValueError(f"Dati mancanti per il canale {i}")

            channels.append({
                'type': channel_data['type'],
                'number': int(channel_data['number']),
                'value': int(channel_data['value'])
            })


        # Creazione del dispositivo e dei canali
        with db.session.begin_nested():
            device = Device(
                name=name,
                type=type,
                subtype=subtype,
                dmx_channels=dmx_channels,
                status=status
            )
            device.validate()

            db.session.add(device)
            db.session.flush()

            for channel in channels:
                new_channel = Channel(
                    device_id=device.id,
                    type=channel['type'],
                    number=channel['number'],
                    value=channel['value']
                )
                new_channel.validate()
                db.session.add(new_channel)

        # Commit delle modifiche
        db.session.commit()
   
        flash(f'Dispositivo {device.name} aggiunto con successo', 'success')
        return redirect(url_for('devices.devices_management'))
    
    except ValueError as ve:
        db.session.rollback()
        flash(f'Errore di validazione: {str(ve)}', 'error')
        return render_template('devices_form.html', form_data=form_data)

    except SQLAlchemyError as sae:
        db.session.rollback()
        flash(f'Errore del database: {str(sae)}', 'error')
        return render_template('devices_form.html', form_data=form_data)

    except Exception as e:
        db.session.rollback()
        flash(f'Errore imprevisto: {str(e)}', 'error')
        return render_template('devices_form.html', form_data=form_data)

@devices_bp.route('/edit_device_form/<int:device_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def edit_device():
    """
    Modifica un dispositivo esistente nel database.
    """
    try:
        # Recupera i dati dal form
        form_data = request.form
        device_id = int(form_data.get('device_id'))
        name = form_data.get('name')
        type = form_data.get('type')
        subtype = form_data.get('subtype')
    
        if not all([name, type, subtype]):
            raise ValueError("Tutti i campi del dispositivo sono obbligatori")

        # Recupera il dispositivo dal database
        device = db.session.query(Device).filter_by(id=device_id).first()
        if not device:
            raise ValueError(f"Dispositivo con ID {device_id} non trovato")
 
        # Aggiornamento dei dati del dispositivo
        device.name = name
        device.type = type
        device.subtype = subtype
        device.validate()

        # Aggiornamento dei canali
        for channel in device.channels:
            channel_number = int(form_data.get(f'channel-number-{channel.id}'))
            channel_type = form_data.get(f'channel-type-{channel.id}')
            channel_value = int(form_data.get(f'channel-value-{channel.id}'))

            if not all([channel_number, channel_type, channel_value]):
                raise ValueError(f"Tutti i campi del canale {channel.id} sono obbligatori")

            channel.number = channel_number
            channel.type = channel_type
            channel.value = channel_value
            channel.validate()

        # Salvataggio delle modifiche
        db.session.commit()

        flash(f'Dispositivo {name} modificato con successo', 'success')
        return redirect(url_for('devices.devices_management'))

    except ValueError as ve:
        db.session.rollback()
        flash(f'Errore di validazione: {str(ve)}', 'error')
        return redirect(url_for('devices.edit_device_form', device_id=device_id))
    
    except SQLAlchemyError as sae:
        db.session.rollback()
        flash(f'Errore del database durante l\'aggiornamento: {str(sae)}', 'error')
        return redirect(url_for('devices.edit_device_form', device_id=device_id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Errore imprevisto durante l\'aggiornamento del dispositivo: {str(e)}', 'error')
        return redirect(url_for('devices.edit_device_form', device_id=device_id))


@devices_bp.route('/delete_device', methods=['POST'])
@login_required
def delete_device():
    """
    Elimina un dispositivo dal database.
    """
    device_id = int(request.form.get('device_id'))
    device = db.session.query(Device).filter_by(id=device_id).first()
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