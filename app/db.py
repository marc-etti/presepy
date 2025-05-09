from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy()

def init_db():
    # Ottieni l'app corrente
    from app.models import User

def seed_development_db():
    from app.models import User, Device, Channel, Keyframe, Phase

    with current_app.app_context():
        db.drop_all()
        db.create_all()
    
        try:
            # Popolamento Tabella User
            users = [
                User(username='admin', password='admin', is_admin=True, is_active=True),
                User(username='user', password='user', is_admin=False, is_active=True)
            ]
            db.session.bulk_save_objects(users)
            db.session.commit()
            print("Users added successfully.")

            # Popolamento Tabella Device
            devices = [
                Device(name='Faro1', type='light', subtype='faro', dmx_address=1, dmx_channels=1, status='on'),
                Device(name='Faro2', type='light', subtype='faro', dmx_address=2, dmx_channels=1, status='on'),
                Device(name='Faro3', type='light', subtype='faro', dmx_address=3, dmx_channels=1, status='on'),
                Device(name='Faro4', type='light', subtype='faro', dmx_address=4, dmx_channels=1, status='on'),
                Device(name='LED1', type='light', subtype='led', dmx_address=5, dmx_channels=3, status='on')
            ]
            db.session.bulk_save_objects(devices)
            db.session.commit()
            print("Devices added successfully.")

            # Recupero gli ID dei dispositivi appena creati
            devices_in_db = db.session.query(Device).all()

            # Popolamento Tabella Channel
            channels = [
                Channel(device_id=devices_in_db[0].id, number=1, type='intensity', value=255),
                Channel(device_id=devices_in_db[1].id, number=2, type='intensity', value=255),
                Channel(device_id=devices_in_db[2].id, number=3, type='intensity', value=255),
                Channel(device_id=devices_in_db[3].id, number=4, type='intensity', value=255),
                # LED1 - 3 canali - RGB
                Channel(device_id=devices_in_db[4].id, number=5, type='RED', value=255),
                Channel(device_id=devices_in_db[4].id, number=6, type='BLUE', value=255),
                Channel(device_id=devices_in_db[4].id, number=7, type='GREEN', value=255)
            ]
            db.session.bulk_save_objects(channels)
            db.session.commit()
            print("Channels added successfully.")

            # Recupero gli ID dei canali appena creati
            channels_in_db = db.session.query(Channel).all()

            # Popolamento Tabella Phase
            phases = [
                Phase(name='ALBA', duration=30, order=1),
                Phase(name='GIORNO', duration=60, order=2),
                Phase(name='SERA', duration=30, order=3),
                Phase(name='NOTTE', duration=30, order=4)
            ]
            db.session.bulk_save_objects(phases)
            db.session.commit()
            print("Phases added successfully.")

            # Recupero gli ID delle fasi appena create
            phases_in_db = db.session.query(Phase).all()

            # Popolamento Tabella Keyframe
            keyframes = [
                # Faretto 1 - ALBA - inizio
                Keyframe(channel_id=channels_in_db[0].id, phase_id=phases_in_db[0].id, description='Faretto1_alba_inizio', position=0, value=0),
                # Faretto 1 - ALBA - fine
                Keyframe(channel_id=channels_in_db[0].id, phase_id=phases_in_db[0].id, description='Faretto1_alba_fine', position=100, value=255),
                # Faretto 1 - GIORNO - inizio
                Keyframe(channel_id=channels_in_db[0].id, phase_id=phases_in_db[1].id, description='Faretto1_giorno_inizio', position=0, value=255),
                # Faretto 1 - GIORNO - fine
                Keyframe(channel_id=channels_in_db[0].id, phase_id=phases_in_db[1].id, description='Faretto1_giorno_fine', position=100, value=255),
                # Faretto 1 - SERA - inizio
                Keyframe(channel_id=channels_in_db[0].id, phase_id=phases_in_db[2].id, description='Faretto1_sera_inizio', position=0, value=255),
                # Faretto 1 - SERA - fine
                Keyframe(channel_id=channels_in_db[0].id, phase_id=phases_in_db[2].id, description='Faretto1_sera_fine', position=100, value=0),
                # Faretto 1 - NOTTE - inizio
                Keyframe(channel_id=channels_in_db[0].id, phase_id=phases_in_db[3].id, description='Faretto1_notte_inizio', position=0, value=0),
                # Faretto 1 - NOTTE - fine
                Keyframe(channel_id=channels_in_db[0].id, phase_id=phases_in_db[3].id, description='Faretto1_notte_fine', position=100, value=0),
                # Faretto 2 - ALBA - inizio
                Keyframe(channel_id=channels_in_db[1].id, phase_id=phases_in_db[0].id, description='Faretto2_alba_inizio', position=0, value=0),
                # Faretto 2 - ALBA - fine
                Keyframe(channel_id=channels_in_db[1].id, phase_id=phases_in_db[0].id, description='Faretto2_alba_fine', position=100, value=255),
                # Faretto 2 - GIORNO - inizio
                Keyframe(channel_id=channels_in_db[1].id, phase_id=phases_in_db[1].id, description='Faretto2_giorno_inizio', position=0, value=255),
                # Faretto 2 - GIORNO - fine
                Keyframe(channel_id=channels_in_db[1].id, phase_id=phases_in_db[1].id, description='Faretto2_giorno_fine', position=100, value=255),
                # Faretto 2 - SERA - inizio
                Keyframe(channel_id=channels_in_db[1].id, phase_id=phases_in_db[2].id, description='Faretto2_sera_inizio', position=0, value=255),
                # Faretto 2 - SERA - fine
                Keyframe(channel_id=channels_in_db[1].id, phase_id=phases_in_db[2].id, description='Faretto2_sera_fine', position=100, value=0),
                # Faretto 2 - NOTTE - inizio
                Keyframe(channel_id=channels_in_db[1].id, phase_id=phases_in_db[3].id, description='Faretto2_notte_inizio', position=0, value=0),
                # Faretto 2 - NOTTE - fine
                Keyframe(channel_id=channels_in_db[1].id, phase_id=phases_in_db[3].id, description='Faretto2_notte_fine', position=100, value=0),
                # Faretto 3 - ALBA - inizio
                Keyframe(channel_id=channels_in_db[2].id, phase_id=phases_in_db[0].id, description='Faretto3_alba_inizio', position=0, value=0),
                # Faretto 3 - ALBA - fine
                Keyframe(channel_id=channels_in_db[2].id, phase_id=phases_in_db[0].id, description='Faretto3_alba_fine', position=100, value=255),
                # Faretto 3 - GIORNO - inizio
                Keyframe(channel_id=channels_in_db[2].id, phase_id=phases_in_db[1].id, description='Faretto3_giorno_inizio', position=0, value=255),
                # Faretto 3 - GIORNO - fine
                Keyframe(channel_id=channels_in_db[2].id, phase_id=phases_in_db[1].id, description='Faretto3_giorno_fine', position=100, value=255),
                # Faretto 3 - SERA - inizio
                Keyframe(channel_id=channels_in_db[2].id, phase_id=phases_in_db[2].id, description='Faretto3_sera_inizio', position=0, value=255),
                # Faretto 3 - SERA - fine
                Keyframe(channel_id=channels_in_db[2].id, phase_id=phases_in_db[2].id, description='Faretto3_sera_fine', position=100, value=0),
                # Faretto 3 - NOTTE - inizio
                Keyframe(channel_id=channels_in_db[2].id, phase_id=phases_in_db[3].id, description='Faretto3_notte_inizio', position=0, value=0),
                # Faretto 3 - NOTTE - fine
                Keyframe(channel_id=channels_in_db[2].id, phase_id=phases_in_db[3].id, description='Faretto3_notte_fine', position=100, value=0),
                # Faretto 4 - ALBA - inizio
                Keyframe(channel_id=channels_in_db[3].id, phase_id=phases_in_db[0].id, description='Faretto4_alba_inizio', position=0, value=0),
                # Faretto 4 - ALBA - fine
                Keyframe(channel_id=channels_in_db[3].id, phase_id=phases_in_db[0].id, description='Faretto4_alba_fine', position=100, value=255),
                # Faretto 4 - GIORNO - inizio
                Keyframe(channel_id=channels_in_db[3].id, phase_id=phases_in_db[1].id, description='Faretto4_giorno_inizio', position=0, value=255),
                # Faretto 4 - GIORNO - fine
                Keyframe(channel_id=channels_in_db[3].id, phase_id=phases_in_db[1].id, description='Faretto4_giorno_fine', position=100, value=255),
                # Faretto 4 - SERA - inizio
                Keyframe(channel_id=channels_in_db[3].id, phase_id=phases_in_db[2].id, description='Faretto4_sera_inizio', position=0, value=255),
                # Faretto 4 - SERA - fine
                Keyframe(channel_id=channels_in_db[3].id, phase_id=phases_in_db[2].id, description='Faretto4_sera_fine', position=100, value=0),
                # Faretto 4 - NOTTE - inizio
                Keyframe(channel_id=channels_in_db[3].id, phase_id=phases_in_db[3].id, description='Faretto4_notte_inizio', position=0, value=0),
                # Faretto 4 - NOTTE - fine
                Keyframe(channel_id=channels_in_db[3].id, phase_id=phases_in_db[3].id, description='Faretto4_notte_fine', position=100, value=0),
                # LED1 - ALBA - inizio - RGB
                Keyframe(channel_id=channels_in_db[4].id, phase_id=phases_in_db[0].id, description='LED1_rosso_alba_inizio', position=0, value=0),
                Keyframe(channel_id=channels_in_db[5].id, phase_id=phases_in_db[0].id, description='LED1_verde_alba_inizio', position=0, value=0),
                Keyframe(channel_id=channels_in_db[6].id, phase_id=phases_in_db[0].id, description='LED1_blu_alba_inizio', position=0, value=0),
                # LED1 - ALBA - fine - RGB
                Keyframe(channel_id=channels_in_db[4].id, phase_id=phases_in_db[0].id, description='LED1_rosso_alba_fine', position=100, value=255),
                Keyframe(channel_id=channels_in_db[5].id, phase_id=phases_in_db[0].id, description='LED1_verde_alba_fine', position=100, value=255),
                Keyframe(channel_id=channels_in_db[6].id, phase_id=phases_in_db[0].id, description='LED1_blu_alba_fine', position=100, value=255),
                # LED1 - GIORNO - inizio - RGB
                Keyframe(channel_id=channels_in_db[4].id, phase_id=phases_in_db[1].id, description='LED1_rosso_giorno_inizio', position=0, value=255),
                Keyframe(channel_id=channels_in_db[5].id, phase_id=phases_in_db[1].id, description='LED1_verde_giorno_inizio', position=0, value=255),
                Keyframe(channel_id=channels_in_db[6].id, phase_id=phases_in_db[1].id, description='LED1_blu_giorno_inizio', position=0, value=255),
                # LED1 - GIORNO - fine - RGB
                Keyframe(channel_id=channels_in_db[4].id, phase_id=phases_in_db[1].id, description='LED1_rosso_giorno_fine', position=100, value=255),
                Keyframe(channel_id=channels_in_db[5].id, phase_id=phases_in_db[1].id, description='LED1_verde_giorno_fine', position=100, value=255),
                Keyframe(channel_id=channels_in_db[6].id, phase_id=phases_in_db[1].id, description='LED1_blu_giorno_fine', position=100, value=255),
                # LED1 - SERA - inizio - RGB
                Keyframe(channel_id=channels_in_db[4].id, phase_id=phases_in_db[2].id, description='LED1_rosso_sera_inizio', position=0, value=255),
                Keyframe(channel_id=channels_in_db[5].id, phase_id=phases_in_db[2].id, description='LED1_verde_sera_inizio', position=0, value=255),
                Keyframe(channel_id=channels_in_db[6].id, phase_id=phases_in_db[2].id, description='LED1_blu_sera_inizio', position=0, value=255),
                # LED1 - SERA - fine - RGB
                Keyframe(channel_id=channels_in_db[4].id, phase_id=phases_in_db[2].id, description='LED1_rosso_sera_fine', position=100, value=0),
                Keyframe(channel_id=channels_in_db[5].id, phase_id=phases_in_db[2].id, description='LED1_verde_sera_fine', position=100, value=0),
                Keyframe(channel_id=channels_in_db[6].id, phase_id=phases_in_db[2].id, description='LED1_blu_sera_fine', position=100, value=0),
                # LED1 - NOTTE - inizio - RGB
                Keyframe(channel_id=channels_in_db[4].id, phase_id=phases_in_db[3].id, description='LED1_rosso_notte_inizio', position=0, value=0),
                Keyframe(channel_id=channels_in_db[5].id, phase_id=phases_in_db[3].id, description='LED1_verde_notte_inizio', position=0, value=0),
                Keyframe(channel_id=channels_in_db[6].id, phase_id=phases_in_db[3].id, description='LED1_blu_notte_inizio', position=0, value=0),
                # LED1 - NOTTE - fine - RGB
                Keyframe(channel_id=channels_in_db[4].id, phase_id=phases_in_db[3].id, description='LED1_rosso_notte_fine', position=100, value=0),
                Keyframe(channel_id=channels_in_db[5].id, phase_id=phases_in_db[3].id, description='LED1_verde_notte_fine', position=100, value=0),
                Keyframe(channel_id=channels_in_db[6].id, phase_id=phases_in_db[3].id, description='LED1_blu_notte_fine', position=100, value=0)
            ]
            db.session.bulk_save_objects(keyframes)
            db.session.commit()
            print("Keyframes added successfully.")

        except Exception as e:
            # Rollback in caso di errore
            db.session.rollback()
            print(f"Error occurred while adding data: {e}")

        finally:    
            # Chiudi la sessione
            db.session.close()
            print("Database seeded successfully.")

