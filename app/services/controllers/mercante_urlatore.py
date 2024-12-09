# Classe per il controllo dei motori del "Mercante Urlatore"
# Motore Hs55

# Classe per il controllo del motore del basamento
class MercanteUrlatoreBasamento:
    def __init__(self, dmx, channel, name, current_position=0):
        self.dmx = dmx
        self.channel = channel
        self.name = name
        self.current_position = current_position
        self.escursione_massima = 120
        self.max_gradi_movimento = 85



# Classe per il controllo del motore del corpo
class MercanteUrlatoreCorpo:
    def __init__(self, dmx, channel, name, current_position=0):
        self.dmx = dmx
        self.channel = channel
        self.name = name
        self.current_position = current_position

