class ledRGB_JBsystem:
    """Classe per la gestione dei LED RGB di tipo JB system."""

    def __init__(self,
                 dmx,
                 channel,
                 name,
                 red_offset=0,
                 green_offset=1,
                 blue_offset=2,
                 dimmer_offset=3,
                 strobo_offset=4,
                 strobo_max_value=255,
                 strobo_min_value=0
                 ) -> None:
        """Inizializza il LED RGB di tipo JB system.
        param dmx: Istanza del DMX
        param channel: Indirizzo DMX del LED RGB
        param name: Nome del LED RGB
        param red_offset: Offset del canale rosso (default: 0)
        param green_offset: Offset del canale verde (default: 1)
        param blue_offset: Offset del canale blu (default: 2)
        param dimmer_offset: Offset del canale dimmer (default: 3)
        param strobo_offset: Offset del canale strobo (default: 4)
        param strobo_max_value: Valore massimo del canale strobo (default: 255)
        param strobo_min_value: Valore minimo del canale strobo (default: 0)"""
        if channel is None or channel == 0:
            raise ValueError("Il canale del LED RGB non può essere zero o vuoto.")
        self.dmx = dmx
        self.channel = channel
        self.name = name
        self.red_offset = red_offset
        self.green_offset = green_offset
        self.blue_offset = blue_offset
        self.dimmer_offset = dimmer_offset
        self.strobo_offset = strobo_offset
        self.strobo_max_value = strobo_max_value
        self.strobo_min_value = strobo_min_value
        self.red_value = 0
        self.green_value = 0
        self.blue_value = 0
        self.dimmer_value = 0
        self.strobo_value = 0

    def __str__(self) -> str:
        """Rappresentazione testuale del LED RGB."""
        return f"{self.name} (canale {self.channel})"
    
    def to_dict(self) -> dict:
        """Restituisce il LED RGB come dizionario."""
        return {
            'name': self.name,
            'channel': self.channel,
            'red_offset': self.red_offset,
            'green_offset': self.green_offset,
            'blue_offset': self.blue_offset,
            'dimmer_offset': self.dimmer_offset,
            'strobo_offset': self.strobo_offset,
            'strobo_max_value': self.strobo_max_value,
            'strobo_min_value': self.strobo_min_value,
            'red_value': self.red_value,
            'green_value': self.green_value,
            'blue_value': self.blue_value,
            'dimmer_value': self.dimmer_value,
            'strobo_value': self.strobo_value
        }
    
    def from_dict(self, data: dict) -> None:
        """Carica i dati del LED RGB da un dizionario."""
        self.name = data.get('name')
        self.channel = data.get('channel')
        self.red_offset = data.get('red_offset')
        self.green_offset = data.get('green_offset')
        self.blue_offset = data.get('blue_offset')
        self.dimmer_offset = data.get('dimmer_offset')
        self.strobo_offset = data.get('strobo_offset')
        self.strobo_max_value = data.get('strobo_max_value')
        self.strobo_min_value = data.get('strobo_min_value')
        self.red_value = data.get('red_value')
        self.green_value = data.get('green_value')
        self.blue_value = data.get('blue_value')
        self.dimmer_value = data.get('dimmer_value')
        self.strobo_value = data.get('strobo_value')

        