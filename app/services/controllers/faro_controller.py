###################################
# Controller del faro
# CANALI:
# 0 - Luminosità (0-255)
###################################
from app.models import Device, Channel, Keyframe

from app.utils.interpolation import interpolate_value

class FaroController:
    """Classe per la gestione dei fari."""

    def __init__(self, name, dmx_instance) -> None:
        """Inizializza il faro con i dati del database.
        param name: Nome del faro
        param dmx_instance: Istanza del DMX"""
        if not name:
            raise ValueError("Il nome del faro non può essere vuoto.")
        
        # carico il device faro dal database
        self.device = Device.query.filter_by(name=name).first()
        if self.device is None:
            raise ValueError(f"Il faro con nome {name} non esiste nel database.")
        
        # carico i canali associati al faro dal database
        self.channels = Channel.query.filter_by(device_id=self.device.id).all()
        if not self.channels:
            raise ValueError(f"Il faro con nome {name} non ha canali associati nel database.")
        
        # carico i keyframe associati ai canali del faro dal database
        self.keyframes = Keyframe.query.filter(Keyframe.channel_id.in_([channel.id for channel in self.channels])).all()
        if not self.keyframes:
            raise ValueError(f"Il faro con nome {name} non ha keyframe associati nel database.")
        
        self.dmx = dmx_instance             # Istanza del DMX

    def update(self, phase, time, total_time):
        """Aggiorna il faro in base alla fase e l'istante."""
        for channel in self.channels:
            keyframes = [ kf for kf in self.keyframes if kf.channel_id == channel.id and kf.phase_id == phase.id ]
            for keyframe, next_keyframe in zip(keyframes, keyframes[1:]):
                start_time = keyframe.position * total_time / 100
                end_time = next_keyframe.position * total_time / 100
                if start_time <= time <= end_time:
                    # Interpolazione del valore del canale
                    value = interpolate_value( 
                        keyframe.value,
                        next_keyframe.value,
                        start_time,
                        end_time,
                        time
                    )
                    self.dmx.set_channel(channel.number, value)
                    break

    def __repr__(self):
        """Restituisce una rappresentazione del faro."""
        return f"Faro {self.device.name} con ID {self.device.id} e canali {[channel.number for channel in self.channels]}" +\
               f" e keyframe {[keyframe.description for keyframe in self.keyframes]}"