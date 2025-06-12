from config import Config

import time
import threading
from app.services.dmx.DMX_data import DMXData
from app.services.dmx.state_manager import StateManager

from app.services.controllers.faro_controller import FaroController
from app.models import Device, Phase

# Creazione dell'istanza DMX
dmx = DMXData()

# Evento per la pausa del thread
pause_event = threading.Event()

# Istanza della classe StateManager
state_manager = StateManager()

# Fornisco l'evento di pausa al StateManager
state_manager.set_paused_event(pause_event)

# Inizializzazione dei dispositivi di tipo "light"
def init_lights_from_db():
    """Inizializza i controller dei dispositivi di tipo "light" dal database."""
    
    lights = Device.query.filter_by(type="light").all()
    if not lights:
        print("Nessun dispositivo di tipo 'lights' trovato nel database")
        return []
    else:
        init_lights = []
        for light in lights:
            init_lights.append(
                FaroController(light.name, dmx)
            )
        return init_lights

def main_dmx_function(app):
    """Funzione principale di gestione della giornata.
       aggiorna i valori istante per istante e in base alla fase del giorno"""
    with app.app_context():

        FREQUENCY = 1/20 # Frequenza di invio dei dati al dmx (44Hz)

        phases = Phase.get_phases(active=True) # Carico le fasi dal database

        # Inizializzazione
        lights = init_lights_from_db() # Inizializzo i dispositivi dal database

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

                    # Aggiorno i devices in base alla fase
                    for light in lights:
                        light.update(phase, istante, istanti_totali)

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
    dmx.reset()  # Resetta i canali DMX
    # dmx.close()
    print("Interfaccia DMX chiusa")