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
def inizializzazione():
    """Inizializzazione dei controller"""
    faro1 = FaroController("Faro1", dmx)
    faro2 = FaroController("Faro2", dmx)
    faro3 = FaroController("Faro3", dmx)
    faro4 = FaroController("Faro4", dmx)
    led1 = FaroController("LED1", dmx)

    # Lista dei device divisi per tipo
    devices = {
        "faro": [faro1, faro2, faro3, faro4],
        "led": [led1]
    }
    return devices

def main_dmx_function(app):
    """Funzione principale di gestione della giornata.
       aggiorna i valori istante per istante e in base alla fase del giorno"""
    with app.app_context():

        FREQUENCY = 1/20 # Frequenza di invio dei dati al dmx (44Hz)

        phases = Phase.get_phases() # Carico le fasi dal database

        # Inizializzazione
        devices = inizializzazione()

        while state_manager.is_on():                                # Controllo se il sistema è acceso
            
            for phase in phases:
                # Controllo se il sistema è acceso
                if not state_manager.is_on():
                    break
                state_manager.set_phase(phase.name)                 # Imposto la fase corrente
                istanti_totali = int(phase.duration/FREQUENCY) # Calcolo il numero totale di istanti per la fase
                for istante in range(0, istanti_totali): # Per ogni fase, aggiorno i valori istante per istante
                    print(f"Fase: {phase.name} - Istante: {istante} di {istanti_totali} - Tempo: {phase.duration} secondi")

                    if not state_manager.is_on():                           # Controllo l'evento di stop
                        break
                    if not pause_event.is_set():                            # Controllo l'evento di pausa
                        print(f"Programma in pausa nel thread: {threading.current_thread().name}")
                        pause_event.wait()                                  # Mi metto in attesa finché l'evento di pausa non viene resettato
                        print(f"Programma ripreso nel thread: {threading.current_thread().name}")

                    # Aggiorno i fari in base alla fase
                    for faro in devices["faro"]:
                        faro.update(phase, istante, istanti_totali)
                    
                    for led in devices["led"]:
                        led.update(phase, istante, istanti_totali)

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