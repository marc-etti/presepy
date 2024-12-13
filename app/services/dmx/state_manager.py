import os, json
from config import Config
from threading import Event

class StateManager:
    """Classe per la gestione dello stato del sistema."""
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Metodo per creare un'istanza singola della classe."""
        if not cls._instance:
            cls._instance = super(StateManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Costruttore della classe."""
        if not hasattr(self, 'current_phase'):
            self.pause_event = None
            self.isOn = False
            self.current_phase = 'inizializzazione'
            self.istante = 0

    def is_on(self) -> bool:
        """Restituisce True se il sistema è acceso, False altrimenti."""
        return self.isOn
    
    def turn_on(self):
        """Accende il sistema."""
        if self.isOn:
            print("Il sistema è già acceso.")
        else:
            self.isOn = True

    def turn_off(self):
        """Spegne il sistema."""
        if self.isOn:
            self.isOn = False
        else:
            print("Il sistema è già spento.")

    def set_phase(self, phase):
        """Imposta la fase del giorno corrente."""
        self.current_phase = phase

    def get_phase(self):
        """Restituisce la fase del giorno corrente."""
        return self.current_phase
    
    def set_istante(self, istante):
        """Salva l'istante corrente."""
        self.istante = istante

    def get_istante(self):
        """Restituisce l'istante salvato."""
        return self.istante
    
    def set_paused_event(self, event: Event):
        """Imposta l'evento di pausa.
           param event: Evento di pausa."""
        self.pause_event = event
        self.pause_event.set()
    
    def pause(self):
        """Mette in pausa il sistema.
           Se il flag è True lo imposta a False, altrimenti dice che il sistema è già in pausa."""
        if self.pause_event.is_set():
            self.pause_event.clear()
        else:
            print("Il sistema è già in pausa.")

    def resume(self):
        """Riprende il sistema dalla pausa.
           Se il flag è False lo imposta a True, altrimenti dice che il sistema non è in pausa."""
        if not self.pause_event.is_set():
            self.pause_event.set()
        else:
            print("Il sistema non è in pausa.")
    
    #TODO: decidere se è il caso di spostare questa funzione in un'altra classe
    def get_devices_info(self):
        """Restituisce le informazioni sui dispositivi collegati presenti nel file data.json."""
        try:
            with open(Config.JSON_FILE, 'r') as file:
                data = json.load(file)
            if 'devices_info' not in data:
                print("Errore: Il file data.json non contiene la chiave 'devices_info'.")
                return []
            else:
                return data.get('devices_info', [])
        except FileNotFoundError:
            print("Errore: Il file data.json non è stato trovato.")
            return []
        except json.JSONDecodeError:
            print("Errore: Il file data.json è corrotto o non è un JSON valido.")
            return []
        except Exception as e:
            print(f"Errore inaspettato: {e}")
            return []
    
    def write_data_on_json(self):
        """Scrive i dati dello state manager su un file JSON."""
        # Controlla se il file esiste e ha contenuto valido
        if os.path.exists(Config.JSON_FILE):
            with open(Config.JSON_FILE, 'r') as file:
                try:
                    existing_data = json.load(file)  # Legge i dati esistenti
                except json.JSONDecodeError:
                    existing_data = {}  # Se il file è corrotto o vuoto, inizializza come dizionario vuoto
        else:
            existing_data = {}

        # Aggiorna o aggiungi i dati
        existing_data['stateManager'] = {
            'current_phase': self.current_phase,
            'istante': self.istante
        }

        with open(Config.JSON_FILE, 'w') as file:
            json.dump(existing_data, file, indent=4)
    
    #TODO: Implementare il meteo quando sarà possibile