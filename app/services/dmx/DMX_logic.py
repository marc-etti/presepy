from config import Config

import time
import threading
from app.services.dmx.DMX_data import DMXData
from app.services.dmx.state_manager import StateManager

from app.services.controllers.faro_controller import FaroController
from models import Device, Channel, Keyframe, Phase

# Creazione dell'istanza DMX
dmx = DMXData()

# Evento per la pausa del thread
pause_event = threading.Event()

# Istanza della classe StateManager
state_manager = StateManager()

# Fornisco l'evento di pausa al StateManager
state_manager.set_paused_event(pause_event)

# inizializzazione
faro1 = FaroController("Faro1", dmx)
faro2 = FaroController("Faro2", dmx)
faro3 = FaroController("Faro3", dmx)
faro4 = FaroController("Faro4", dmx)

def inizializzazione():
    """Inizializza l'interfaccia DMX."""
    pass


def main_dmx_function():
    """Funzione principale di gestione della giornata.
       aggiorna i valori istante per istante e in base alla fase del giorno"""
    
    # carico le fasi dal database ordinandole per nome
    phases = Phase.query.order_by(Phase.order).all()

    FREQUENCY = 1/2 # Frequenza di invio dei dati al dmx (44Hz)

    # Inizializzazione
    inizializzazione()

    while state_manager.is_on():                                # Controllo se il sistema è acceso
        
        for phase in phases:

            for istante in range(0, phase.duration/FREQUENCY):
                 
                if not state_manager.is_on():                           # Controllo l'evento di stop
                    break
                if not pause_event.is_set():                            # Controllo l'evento di pausa
                    print(f"Programma in pausa nel thread: {threading.current_thread().name}")
                    pause_event.wait()                                  # Mi metto in attesa finché l'evento di pausa non viene resettato
                    print(f"Programma ripreso nel thread: {threading.current_thread().name}")

                # Aggiorno i fari in base alla fase
                for faro in [faro1, faro2, faro3, faro4]:
                    faro.update(phase, istante, phase.duration)

                # Attendo il tempo di aggiornamento
                if istante < phase.duration/FREQUENCY - 1:
                    time.sleep(FREQUENCY)
                             
        print("Giornata terminata")

    # Chiusura
    print("Programma terminato")
    closing_function()

def closing_function():
    """Funzione di chiusura del programma."""
    dmx.close()
    print("Interfaccia DMX chiusa")