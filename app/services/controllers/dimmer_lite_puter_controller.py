# Controller del dimmer lite puter

class DimmerLitePuterController:
    """Classe per la gestione del dimmer lite puter."""

    def __init__(self, dmx_instance, channel, valueLum=0, valueRed=0, valueGreen=0, valueBlue=0):
        """Inizializza il dimmer lite puter."""
        self.dmx = dmx_instance             # Istanzia del DMX
        self.channelLuminosita = channel    # Canale della luminosità
        self.channelRed = channel + 1       # Canale del rosso
        self.channelGreen = channel + 2     # Canale del verde
        self.channelBlue = channel + 3      # Canale del blu
        self.valueLuminosita = valueLum     # Intensità della luminosità
        self.valueRed = valueRed            # Intensità del rosso
        self.valueGreen = valueGreen        # Intensità del verde
        self.valueBlue = valueBlue          # Intensità del blu