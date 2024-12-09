from config import Config
from app.utils.common import write_device_info_on_json, init_device_from_json

import time
from threading import Event
from app.services.dmx.DMX_data import DMXData
from app.services.dmx.state_manager import StateManager

from app.services.controllers.faro_controller import FaroController

# Creazione dell'istanza DMX
dmx = DMXData()

# Evento per la gestione del thread
running_event = Event()

# Istanza della classe StateManager
state_manager = StateManager()

# inizializzazione
faro1 = FaroController(dmx, 1, "Faro1", 1)
faro2 = FaroController(dmx, 2, "Faro2", 1)
faro3 = FaroController(dmx, 3, "Faro3", 1)
faro4 = FaroController(dmx, 4, "Faro4", 1)
faro5 = FaroController(dmx, 5, "Faro5", 1)

def inizializzazione():
    """Inizializza l'interfaccia DMX."""
    init_device_from_json(faro1)
    init_device_from_json(faro2)
    init_device_from_json(faro3)
    faro4.set_value(100)
    init_device_from_json(faro5)


def main_dmx_function():
    """Funzione principale di gestione della giornata.
       aggiorna i valori istante per istante e in base alla fase del giorno"""
    
    # Costanti
    FREQUENCY = 1/2 # Frequenza di invio dei dati al dmx (44Hz)
    DURATA_ALBA = 30
    DURATA_GIORNO = 60
    DURATA_SERA = 30
    DURATA_NOTTE = 60
    DURATA_TOTALE = DURATA_ALBA + DURATA_GIORNO + DURATA_SERA + DURATA_NOTTE
    ISTANTI_TOTALI = int(DURATA_TOTALE / FREQUENCY)
    ISTANTI_ALBA = int(DURATA_ALBA / FREQUENCY)                     # Da 0 a ISTANTI_ALBA
    ISTANTI_GIORNO = ISTANTI_ALBA + int(DURATA_GIORNO / FREQUENCY)  # Da ISTANTI_ALBA a ISTANTI_GIORNO
    ISTANTI_SERA = ISTANTI_GIORNO + int(DURATA_SERA / FREQUENCY)    # Da ISTANTI_GIORNO a ISTANTI_SERA
    ISTANTI_NOTTE = ISTANTI_SERA + int(DURATA_NOTTE / FREQUENCY)    # Da ISTANTI_SERA a ISTANTI_NOTTE

    # Inizializzazione
    inizializzazione()

    while running_event.is_set():                                   # Ciclo principale
        
        for istante in range(ISTANTI_TOTALI):

            start_time = time.time()                                # Salvo il tempo di inizio

            if not running_event.is_set():                          # Controllo se il programma è in esecuzione
                break                                               # Se non è in esecuzione esco dal ciclo
            if istante < ISTANTI_ALBA:                                              # ALBA
                if istante == 0:                                    # Controllo se è l'istante iniziale
                    print("Alba in corso")                          # Stampo il messaggio di inizio alba
                    state_manager.set_phase("ALBA")                 # Imposto la fase del giorno
                faro1.proportional_value(istante, ISTANTI_ALBA)
                faro2.proportional_value(istante, ISTANTI_ALBA)
                faro3.proportional_value(istante, ISTANTI_ALBA)
                faro4.proportional_value(istante, ISTANTI_ALBA)
            elif istante < ISTANTI_GIORNO:                                          # GIORNO
                if istante == ISTANTI_ALBA:
                    print("Giorno in corso")
                    state_manager.set_phase("GIORNO")
                faro1.set_value(255)
                faro2.set_value(255)
                faro3.set_value(255)
                faro4.set_value(255)
            elif istante < ISTANTI_SERA:                                            # SERA
                if istante == ISTANTI_GIORNO:
                    print("Sera in corso")
                    state_manager.set_phase("SERA")
                faro1.proportional_value(ISTANTI_SERA - istante, ISTANTI_SERA - ISTANTI_GIORNO)
                faro2.proportional_value(ISTANTI_SERA - istante, ISTANTI_SERA - ISTANTI_GIORNO)
                faro3.proportional_value(ISTANTI_SERA - istante, ISTANTI_SERA - ISTANTI_GIORNO)
                faro4.proportional_value(ISTANTI_SERA - istante, ISTANTI_SERA - ISTANTI_GIORNO)
            elif istante < ISTANTI_NOTTE:                                           # NOTTE
                if istante == ISTANTI_SERA:
                    print("Notte in corso")
                    state_manager.set_phase("NOTTE")
                faro1.set_value(0)
                faro2.set_value(0)
                faro3.set_value(0)
                faro4.set_value(0)
            if Config.DEBUG:
                dmx.write_channels_on_log(Config.LOG_FILE)
            else:
                dmx.send(Config.DMX_PORT)
            stop_time = time.time()                                 # Salvo il tempo di fine
            sleep_time = FREQUENCY - (stop_time - start_time)       # Calcolo il tempo di attesa per mantenere la frequenza
            if sleep_time < 0:                                      # Controllo se il tempo di attesa è negativo
                sleep_time = 0                                      # Se negativo lo imposto a 0
                raise ValueError("Tempo di attesa negativo")        # Lancio un'eccezione
            time.sleep(sleep_time)
        print("Giornata terminata")

    # Chiusura
    print("Programma terminato")
    state_manager.set_istante(istante)
    closing_function()

def closing_function():
    """Funzione di chiusura del programma."""
    state_manager.write_data_on_json()
    write_device_info_on_json(faro1)
    write_device_info_on_json(faro2)
    write_device_info_on_json(faro3)
    write_device_info_on_json(faro4)
    write_device_info_on_json(faro5)
    dmx.close()
    print("Interfaccia DMX chiusa")