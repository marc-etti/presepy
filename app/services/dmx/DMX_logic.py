from config import Config
from app.utils.common import write_on_log

import time
from threading import Event
from app.services.dmx.DMX_data import DMXData
from app.services.dmx.state_manager import StateManager

from app.services.controllers.faro_controller import FaroController

# Frequenza di aggiornamento
FREQUENCY = 0.5

# Creazione dell'istanza DMX
dmx = DMXData()

# Evento per la gestione del thread
running_event = Event()

# Istanza della classe StateManager
state_manager = StateManager()

# Istanze dei controller
faro1 = FaroController(dmx, 1, 0, "Faro1")
faro2 = FaroController(dmx, 2, 0, "Faro2")
faro3 = FaroController(dmx, 3, 0, "Faro3")
faro4 = FaroController(dmx, 4, 0, "Faro4")

vettore_fari = [faro1, faro2, faro3, faro4]


def inizializzazione():
    """Inizializza l'interfaccia DMX."""
    faro1.init_from_json(Config.JSON_FILE)
    faro2.init_from_json(Config.JSON_FILE)
    faro3.init_from_json(Config.JSON_FILE)
    faro4.set_value(100)

def main_dmx_function():
    """Funzione principale per il controllo della giornata."""
    print("Programma avviato")

    # Inizializzazione
    inizializzazione()

    # Loop principale
    while running_event.is_set():
        alba(30, FREQUENCY)
        giorno(60, FREQUENCY)
        sera(30, FREQUENCY)
        notte(60, FREQUENCY)

    # Chiusura
    print("Programma terminato")
    closing_function()

def alba(duration = 30 , frequency = 0.5):
    """Funzione per la gestione dell'alba.
       Durata alba: 30 secondi
       Frequenza di aggiornamento: 0,5 secondi"""
    print("Alba")
    state_manager.set_phase("alba")
    total_steps = int(duration / frequency)
    for step in range(total_steps):
        if not running_event.is_set():
            break
        faro1.proportional_value(step, total_steps)
        faro2.proportional_value(step, total_steps)
        faro3.proportional_value(step, total_steps)
        faro4.proportional_value(step, total_steps)
        dmx.write_channels_on_log(Config.LOG_FILE)
        time.sleep(frequency)
    
def giorno(duration = 60, frequency = 0.5):
    """Funzione per la gestione del giorno.
       Durata giorno: 60 secondi
       Frequenza di aggiornamento: 0,5 secondi"""
    print("Giorno")
    state_manager.set_phase("GIORNO")
    total_steps = int(duration / frequency)
    for i in range(total_steps):
        if not running_event.is_set():
            break
        faro1.set_value(255)
        faro2.set_value(255)
        faro3.set_value(255)
        faro4.set_value(255)
        dmx.write_channels_on_log(Config.LOG_FILE)
        time.sleep(frequency)

def sera(duration = 30, frequency = 0.5):
    """Funzione per la gestione della sera.
       Durata sera: 30 secondi
       Frequenza di aggiornamento: 0,5 secondi"""
    print("Sera")
    state_manager.set_phase("SERA")
    total_steps = int(duration / frequency)
    for step in range(total_steps):
        if not running_event.is_set():
            break
        faro1.proportional_value(total_steps-step, total_steps)
        faro2.proportional_value(total_steps-step, total_steps)
        faro3.proportional_value(total_steps-step, total_steps)
        faro4.proportional_value(total_steps-step, total_steps)
        dmx.write_channels_on_log(Config.LOG_FILE)
        time.sleep(frequency)
        

def notte(duration = 60, frequency = 0.5):
    """Funzione per la gestione della notte.
       Durata notte: 60 secondi
       Frequenza di aggiornamento: 0,5 secondi"""
    print("Notte")
    state_manager.set_phase("NOTTE")
    total_steps  = int(duration / frequency)
    for step in range(total_steps):
        if not running_event.is_set():
            break
        faro1.set_value(0)
        faro2.set_value(0)
        faro3.set_value(0)
        faro4.set_value(0)
        dmx.write_channels_on_log(Config.LOG_FILE)
        time.sleep(frequency)

    
def closing_function():
    """Funzione di chiusura del programma."""
    faro1.write_data_on_json(Config.JSON_FILE)
    faro2.write_data_on_json(Config.JSON_FILE)
    faro3.write_data_on_json(Config.JSON_FILE)
    faro4.write_data_on_json(Config.JSON_FILE)
    dmx.close()
    print("Interfaccia DMX chiusa")