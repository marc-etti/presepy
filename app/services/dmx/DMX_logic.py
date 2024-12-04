from config import Config
from app.utils.common import write_on_log

import time
from threading import Event
from app.services.dmx.DMX_data import DMXData
from app.services.dmx.state_manager import StateManager
from app.services.controllers.led_controller import LedController

from app.services.controllers.faro_controller import FaroController

# Creazione dell'istanza DMX
dmx = DMXData()

# Evento per la gestione del thread
running_event = Event()

# Istanza della classe StateManager
state_manager = StateManager()

def inizializzazione_test():
    """Inizializza l'interfaccia DMX."""
    dmx.set_channel(1, 255)
    dmx.set_channel(2, 255)
    dmx.set_channel(3, 255)
    dmx.set_channel(4, 255)
    dmx.set_channel(5, 255)
    dmx.set_channel(6, 255)
    dmx.set_interval(7, 20, 20)

def main_dmx_function_test():
    led_controller = LedController(dmx, 1)
    while running_event.is_set():
        led_controller.increase_color('red', 1)
        led_controller.increase_color('green', 1)
        led_controller.increase_color('blue', 1)
        dmx.write_channels_on_log(Config.LOGS_FOLDER  + 'dmx_log.log')
        time.sleep(0.5)

def main_dmx_function():
    """Funzione principale per il controllo dei fari DMX."""

    # inizializzazione
    faro1 = FaroController(dmx, 1, 255)
    faro2 = FaroController(dmx, 2, 255)
    faro3 = FaroController(dmx, 3, 255)
    faro4 = FaroController(dmx, 4, 255)
    fari = [faro1, faro2, faro3, faro4]

    # Sequenza delle fasi
    phases = [
        ("ALBA", [100, 80, 50, 30], 10),   # Valori target e durata (secondi)
        ("GIORNO", [255, 200, 150, 100], 20),
        ("SERA", [80, 50, 30, 20], 10),
        ("NOTTE", [0, 0, 0, 0], 20)
    ]

    # Loop principale

    while running_event.is_set():
    
        for phase, targets, duration in phases:
            if not running_event.is_set():
                break
            state_manager.set_phase(phase)
            print(f"Inizio fase {phase}")
            write_on_log(f"INIZIO FASE {phase}", Config.LOGS_FOLDER + 'dmx_log.log')
            gradual_transition(fari, targets, duration)
        dmx.write_channels_on_log(Config.LOGS_FOLDER  + 'dmx_log.log')
        time.sleep(0.5)

    # Chiusura
    print("Programma terminato")
    closing_function()

def gradual_transition(fari, targets, duration):
    steps = 50
    delay = duration / steps

    for i in range(steps):
        if not running_event.is_set():
            break
        for faro, target in zip(fari, targets):
            faro.set_value(int(faro.get_value() + (target - faro.get_value()) / steps))
        dmx.write_channels_on_log(Config.LOGS_FOLDER  + 'dmx_log.log')
        time.sleep(delay)

        

def closing_function():
    """Funzione di chiusura del programma."""
    # Salvo lo stato nel file json
    # dmx.write_channels_on_json(Config.JSON_FOLDER + 'dmx.json')
    dmx.close()
    print("Interfaccia DMX chiusa")