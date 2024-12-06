import json, os

class FaroController:
    """Classe per la gestione dei fari."""

    MAX_VALUE = 255
    MIN_VALUE = 0
    
    def __init__(self, dmx_instance, channel=None, value=0, name=None):
        """Inizializza il faro."""
        if channel is None:
            raise ValueError("Il canale del faro non può essere nullo")
        self.dmx = dmx_instance             # Istanza del DMX
        self.channel = channel              # Canale del faro
        self.value = value                  # Intensità del faro
        self.name = name                    # Nome del faro
        self.dmx.set_channel(self.channel, self.value)
        
    def increase(self, value):
        """Aumenta il valore del faro."""
        self.value = round(self.dmx.get_channel(self.channel) + value)
        if self.value > 255:
            self.value = 255
        self.dmx.set_channel(self.channel, self.value)

    def decrease(self, value):
        """Diminuisce il valore del faro."""
        self.value = round(self.dmx.get_channel(self.channel) - value)
        if self.value < 0:
            self.value = 0
        self.dmx.set_channel(self.channel, self.value)

    def proportional_value(self, current_step, total_steps):
        """Calcola il valore del faro in base al passo corrente e il numero di passi totali."""
        self.value = round(self.MAX_VALUE * (current_step / total_steps))
        if self.value > 255:
            self.value = 255
        if self.value < 0:
            self.value = 0
        self.dmx.set_channel(self.channel, self.value)

    def set_value(self, value):
        """Imposta il valore del faro."""
        self.value = value
        self.dmx.set_channel(self.channel, self.value)

    def get_value(self) -> int:
        """Restituisce il valore del faro."""
        return self.dmx.get_channel(self.channel)
    
    def write_data_on_json(self, file_path):
        """Scrive i dati del faro su un file JSON."""
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
        existing_data[self.name] = {
            'channel': self.channel,
            'value': self.value
        }

        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)



    def init_from_json(self, file_path):
        """Inizializza il faro da un file JSON."""
        with open(file_path, 'r') as file:
            if os.path.exists(file_path):
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
            if self.name in data:
                print(f"Caricamento dati di {self.name}")
                self.channel = data[self.name]['channel']
                self.value = data[self.name]['value']
                self.dmx.set_channel(self.channel, self.value)
