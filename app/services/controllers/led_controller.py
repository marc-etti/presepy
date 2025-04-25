###################################
# Controller del LED RGB
# CANALI:
# 0 - Rosso
# 1 - Verde
# 2 - Blu
###################################

class LedController:
    """Classe per la gestione dei LED RGB."""

    def __init__(self, dmx, channel, name, red_value=0, green_value=0, blue_value=0, type="light", subtype="led_rgb") -> None:
        """Inizializza il LED RGB.
           param dmx: Istanza del DMX
           param channel: Indirizzo DMX del LED RGB
           param name: Nome del LED RGB
           param red_value: Valore del canale rosso (default: 0)
           param green_value: Valore del canale verde (default: 0)
           param blue_value: Valore del canale blu (default: 0)
           param type: Tipo del dispositivo (default: "light")
           param subtype: Sottotipo del dispositivo (default: "led_rgb")"""
        if channel is None or channel == 0:
            raise ValueError("Il canale del LED RGB non può essere zero o vuoto.")
        self.dmx = dmx
        self.channel = channel
        self.name = name
        self.red = red_value
        self.green = green_value
        self.blue = blue_value
        self.type = type
        self.subtype = subtype
        self.dmx.set_channel(self.channel, self.red)
        self.dmx.set_channel(self.channel + 1, self.green)
        self.dmx.set_channel(self.channel + 2, self.blue)

    def set_color(self, red, green, blue) -> None:
        """Imposta il colore del LED RGB.
           param red: Valore del canale rosso
           param green: Valore del canale verde
           param blue: Valore del canale blu"""
        self.dmx.set_channel(self.channel, red)
        self.dmx.set_channel(self.channel + 1, green)
        self.dmx.set_channel(self.channel + 2, blue)

    def increase_color(self, color, value) -> None:
        """Aumenta il valore del colore del LED RGB.
           param color: Colore da aumentare
           param value: Valore da aumentare"""
        if color == 'red':
            self.red = self.dmx.get_channel(self.channel) + value
            if self.red > 255:
                self.red = 255
            self.dmx.set_channel(self.channel, self.red)
        elif color == 'green':
            self.green = self.dmx.get_channel(self.channel + 1) + value
            if self.green > 255:
                self.green = 255
            self.dmx.set_channel(self.channel + 1, self.green)
        elif color == 'blue':
            self.blue = self.dmx.get_channel(self.channel + 2) + value
            if self.blue > 255:
                self.blue = 255
            self.dmx.set_channel(self.channel + 2, self.blue)

    def decrease_color(self, color, value) -> None:
        """Diminuisce il valore del colore del LED RGB.
           param color: Colore da diminuire
           param value: Valore da diminuire"""
        if color == 'red':
            self.red = self.dmx.get_channel(self.channel) - value
            if self.red < 0:
                self.red = 0
            self.dmx.set_channel(self.channel, self.red)
        elif color == 'green':
            self.green = self.dmx.get_channel(self.channel + 1) - value
            if self.green < 0:
                self.green = 0
            self.dmx.set_channel(self.channel + 1, self.green)
        elif color == 'blue':
            self.blue = self.dmx.get_channel(self.channel + 2) - value
            if self.blue < 0:
                self.blue = 0
            self.dmx.set_channel(self.channel + 2, self.blue)

    def to_dict(self) -> dict:
        """Restituisce un dizionario con i dati del LED RGB."""
        return {
            "name": self.name,
            "type": self.type,
            "subtype": self.subtype,
            "channel": self.channel,
            "red": self.red,
            "green": self.green,
            "blue": self.blue
        }
    
    def from_dict(self, data: dict) -> None:
        """Inizializza il LED RGB dai dati presenti nel dizionario."""
        self.name = data.get("name")
        self.channel = data.get("channel")
        self.red = data.get("red")
        self.green = data.get("green")
        self.blue = data.get("blue")
        self.dmx.set_channel(self.channel, self.red)
        self.dmx.set_channel(self.channel + 1, self.green)
        self.dmx.set_channel(self.channel + 2, self.blue)
        self.type = data.get("type")
        self.subtype = data.get("subtype")

    def __str__(self) -> str:
        """Restituisce una rappresentazione testuale del LED RGB."""
        return f"LED RGB: {self.name} (canale {self.channel}) - RGB({self.red}, {self.green}, {self.blue})"
