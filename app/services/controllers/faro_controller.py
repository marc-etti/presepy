import json, os

class FaroController:
    """Classe per la gestione dei fari."""

    MAX_VALUE = 255
    MIN_VALUE = 0
    
    def __init__(self, dmx_instance, channel, value, name):
        """Inizializza il faro."""
        if channel is None or channel == 0:
            raise ValueError("Il canale del faro non può essere zero o vuoto.")
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
                    raise ValueError("Il file JSON non è valido.")
        else:
            raise FileNotFoundError(f"Il file {file_path} non esiste.")

        # Trova l'indice dell'oggetto se già esiste
        devices = existing_data.get("devices_info", [])
        if not isinstance(devices, list):
            raise ValueError("Il file JSON non contiene una lista di dispositivi.")

        for device in devices:
            if device.get("name") == self.name:
                # Aggiorna i dati esistenti
                device["channel"] = self.channel
                device["value"] = self.value
                break
        else:
            # Aggiungi un nuovo dispositivo se non esiste
            devices.append({
                "name": self.name,
                "channel": self.channel,
                "value": self.value
            })

        # Salva i dati aggiornati sul file
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)


    def init_from_json(self, file_path):
        """Inizializza un'istanza della classe dai dati in un file JSON."""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Il file {file_path} non esiste.")

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                raise ValueError("Il file JSON non è valido.")

        devices = data.get("devices_info", [])
        if devices == []:
            # Se non ci sono dispositivi, non fare nulla
            return
        elif not isinstance(devices, list):
            raise ValueError("Il file JSON non contiene una lista di dispositivi.")
        
        for device in devices:
            if device.get("name") == self.name:
                self.channel = device.get("channel", 0)
                self.value = device.get("value", 0)
                self.dmx.set_channel(self.channel, self.value)
                return
            
        raise ValueError(f"Il dispositivo {self.name} non è stato trovato nel file JSON.")
    
    #TODO: Generalizzare le funzioni per la lettura e scrittura dei dati su file JSON e spostarle in una classe a parte


    def __str__(self):
        """Restituisce una rappresentazione testuale del faro."""
        return f"Faro {self.name} - Canale: {self.channel}, Valore: {self.value}"