from config import Config

import time
from threading import Event
from app.services.dmx.DMX_instance import dmx
from app.services.controllers.led_controller import LedController

from app.services.controllers.faro_controller import FaroController


led_controller = LedController(dmx, 1)


# Evento per la gestione del thread
running_event = Event()

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
    while running_event.is_set():
        led_controller.increase_color('red', 1)
        led_controller.increase_color('green', 1)
        led_controller.increase_color('blue', 1)
        dmx.write_channels_on_log(Config.LOGS_FOLDER  + 'dmx_log.log')
        time.sleep(0.5)

def main_dmx_function():
    # inizializzazione
    faro1 = FaroController(dmx, 1, 255)
    faro2 = FaroController(dmx, 2, 255)
    faro3 = FaroController(dmx, 3, 255)
    faro4 = FaroController(dmx, 4, 255)

    while running_event.is_set():
    
        faro1.increase(1)
        faro2.increase(1)
        faro3.increase(1)
        faro4.increase(1)
        dmx.write_channels_on_log(Config.LOGS_FOLDER  + 'dmx_log.log')
        time.sleep(0.5)

    # Spegnimento
    # Salvo lo stato nel file json
    # dmx.write_channels_on_json(Config.JSON_FOLDER + 'dmx.json')