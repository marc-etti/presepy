###################################
# Controller del faro
# CANALI:
# 0 - Luminosità (0-255)
###################################

from app.models import Device, Channel, Keyframe, Phase
from app.utils.interpolation import interpolate_value

class FaroController:
    """Classe per la gestione dei fari."""

    def __init__(self, name, dmx_instance) -> None:
        """Inizializza il faro con i dati del database.
        param name: Nome del faro
        param dmx_instance: Istanza del DMX"""
        if not name:
            raise ValueError("Il nome del faro non può essere vuoto.")
        if not dmx_instance:
            raise ValueError("L'istanza del DMX non può essere vuota.")
        
        # carico il device faro dal database
        self.device = Device.query.filter_by(name=name).first()
        if self.device is None:
            raise ValueError(f"Il faro con nome {name} non esiste nel database.")
        
        # carico i canali associati al faro dal database
        self.channels = Channel.query.filter_by(device_id=self.device.id).order_by(Channel.number).all()
        if not self.channels:
            raise ValueError(f"Il faro con nome {name} non ha canali associati nel database.")
        
        # carico le fasi dell'universo DMX dal database
        self.phases = Phase.query.order_by(Phase.order).all()
        if not self.phases:
            raise ValueError("Fasi non trovate nel database.")

        # per ogni fase e per ogni canale del faro, carico i keyframe associati
        self.keyframes = {}
        for phase in self.phases:
            self.keyframes[phase.id] = {}
            for channel in self.channels:
                kfs=Keyframe.query.filter_by(
                    channel_id=channel.id,
                    phase_id=phase.id
                    ).order_by(Keyframe.position).all()
                if len(kfs) < 2:
                    raise ValueError(
                        f"Il faro {name} richiede almeno 2 keyframe per il canale {channel.number} "
                        f"nella fase {phase.name} (trovati {len(kfs)})")
                
                self.keyframes[phase.id][channel.id] = list(zip(kfs, kfs[1:]))

        self.dmx = dmx_instance             # Istanza del DMX

    def update(self, phase, time, total_time):
        """Aggiorna il faro in base alla fase e l'istante."""
        if self.device is None:
            raise ValueError("Il faro non è stato inizializzato correttamente.")
        if self.device.status == "on":
            for channel in self.channels:
                for keyframe, next_keyframe in self.keyframes[phase.id][channel.id]:
                    # Calcola il tempo di inizio e fine del keyframe
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
        else:
            # Se il faro è spento non faccio nulla
            pass


    def __repr__(self):
        """Restituisce una rappresentazione del faro."""
        return f"Faro {self.device.name} con ID {self.device.id}"+\
            f" e canali {[channel.number for channel in self.channels]}"+\
            f" e keyframes {self.keyframes}"