###################################
# Controller del faro
# CANALI:
# 0 - Luminosità
###################################


class FaroController:
    """Classe per la gestione dei fari."""

    MAX_VALUE = 255
    MIN_VALUE = 0
    
    def __init__(self, dmx_instance, channel, name, value=0, type="light", subtype="faro") -> None:
        """Inizializza il faro.
        param dmx_instance: Istanza del DMX
        param channel: Canale del faro
        param name: Nome del faro
        param value: Intensità del faro (default: 0)"""
        if channel is None or channel == 0:
            raise ValueError("Il canale del faro non può essere zero o vuoto.")
        self.dmx = dmx_instance             # Istanza del DMX
        self.channel = channel              # Canale del faro
        self.value = value                  # Intensità del faro
        self.name = name                    # Nome del faro
        self.dmx.set_channel(self.channel, self.value)
        self.type = type                    # Tipo del dispositivo
        self.subtype = subtype              # Sottotipo del dispositivo
        
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
    

    def to_dict(self) -> dict:
        """Restituisce un dizionario con i dati del faro."""
        return {
            "name": self.name,
            "channel": self.channel,
            "value": self.value,
            "type": self.type,
            "subtype": self.subtype
        }
    
    def from_dict(self, data: dict) -> None:
        """Inizializza il faro dai dati presenti nel dizionario."""
        self.name = data.get("name")
        self.channel = data.get("channel")
        self.value = data.get("value")
        self.dmx.set_channel(self.channel, self.value)

    def __str__(self) -> str:
        """Restituisce una rappresentazione testuale del faro.
           si invoca con print(faro) oppure str(faro)"""
        return f"Faro: {self.name} - Canale: {self.channel}, Valore: {self.value}"
    
