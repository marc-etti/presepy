class FaroController:
    """Classe per la gestione dei fari."""
    
    def __init__(self, dmx_instance, channel, value=0):
        """Inizializza il faro."""
        self.dmx = dmx_instance             # Istanzia del DMX
        self.channel = channel    # Canale del faro
        self.value = value        # Intensità del faro
        self.dmx.set_channel(self.channel, self.value)
        
    def increase(self, value):
        """Aumenta il valore del faro."""
        self.value = self.dmx.get_channel(self.channel) + value
        if self.value > 255:
            self.value = 255
        self.dmx.set_channel(self.channel, self.value)

    def decrease(self, value):
        """Diminuisce il valore del faro."""
        self.value = self.dmx.get_channel(self.channel) - value
        if self.value < 0:
            self.value = 0
        self.dmx.set_channel(self.channel, self.value)

    def set_value(self, value):
        """Imposta il valore del faro."""
        self.value = value
        self.dmx.set_channel(self.channel, self.value)

    def get_value(self):
        """Restituisce il valore del faro."""
        return self.value