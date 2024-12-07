import os, json
from config import Config

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
            self.isOn = False
            self.current_phase = 'inizializzazione'
            self.istante = 0

    def is_on(self):
        """Restituisce True se il sistema è acceso, False altrimenti."""
        return self.isOn
    
    def turn_on(self):
        """Accende il sistema."""
        if not self.isOn:
            self.isOn = True
        else:
            print("Il sistema è già acceso.")

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
    
    def write_data_on_json(self, file_path):
        """Scrive i dati dello state manager su un file JSON."""
        # Controlla se il file esiste e ha contenuto valido
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
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

        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)
    
    #TODO: Implementare il meteo quando sarà possibile