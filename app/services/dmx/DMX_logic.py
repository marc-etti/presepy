from config import Config

import time
import threading
from app.services.dmx.DMX_data import DMXData
from app.services.dmx.state_manager import StateManager

from app.services.controllers.faro_controller import FaroController
from app.models import Phase

# Creazione dell'istanza DMX
dmx = DMXData()

# Evento per la pausa del thread
pause_event = threading.Event()

# Istanza della classe StateManager
state_manager = StateManager()

# Fornisco l'evento di pausa al StateManager
state_manager.set_paused_event(pause_event)

# inizializzazione
faro1 = None
faro2 = None
faro3 = None
faro4 = None

def inizializzazione():
    """Inizializzazioene dei controller"""
    global faro1, faro2, faro3, faro4
    faro1 = FaroController("Faro1", dmx)
    print(f"Faro1: {faro1}")
    faro2 = FaroController("Faro2", dmx)
    print(f"Faro2: {faro2}")
    faro3 = FaroController("Faro3", dmx)
    print(f"Faro3: {faro3}")
    faro4 = FaroController("Faro4", dmx)
    print(f"Faro4: {faro4}")

def run_main_dmx_function(app):
    """Wrapper per la funzione principale di gestione della giornata."""
    with app.app_context():
        main_dmx_function()

def main_dmx_function():
    """Funzione principale di gestione della giornata.
       aggiorna i valori istante per istante e in base alla fase del giorno"""

    FREQUENCY = 1/2 # Frequenza di invio dei dati al dmx (44Hz)

    phases = Phase.get_phases() # Carico le fasi dal database

    # Inizializzazione
    inizializzazione()

    while state_manager.is_on():                                # Controllo se il sistema è acceso
        
        for phase in phases:

            # Controllo se il sistema è acceso
            if not state_manager.is_on():
                break

            for istante in range(0, 2*phase.duration):
                print(f"Fase: {phase.name} - Istante: {istante} - Durata: {phase.duration}")

                if not state_manager.is_on():                           # Controllo l'evento di stop
                    break
                if not pause_event.is_set():                            # Controllo l'evento di pausa
                    print(f"Programma in pausa nel thread: {threading.current_thread().name}")
                    pause_event.wait()                                  # Mi metto in attesa finché l'evento di pausa non viene resettato
                    print(f"Programma ripreso nel thread: {threading.current_thread().name}")

                # Aggiorno i fari in base alla fase
                for faro in [faro1, faro2, faro3, faro4]:
                    faro.update(phase, istante, phase.duration)

                # Aggiorno il DMX
                dmx.write_channels_on_log(Config.LOG_FILE)
                
                # Attendo il tempo di aggiornamento
                time.sleep(FREQUENCY)
                            
        print("Giornata terminata")

    # Chiusura
    print("Programma terminato")
    closing_function()

def closing_function():
    """Funzione di chiusura del programma."""
    dmx.close()
    print("Interfaccia DMX chiusa")