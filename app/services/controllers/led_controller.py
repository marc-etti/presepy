class LedController:
    def __init__(self, dmx, dmxAddress):
        self.dmx = dmx
        self.dmxAddress = dmxAddress
        self.red = dmx.get_channel(dmxAddress)
        self.green = dmx.get_channel(dmxAddress + 1)
        self.blue = dmx.get_channel(dmxAddress + 2)

    def set_color(self, red, green, blue, dmx):
        self.red = red
        self.green = green
        self.blue = blue
        self.dmx = dmx
        self.dmx.set_channel(self.dmxAddress, red)
        self.dmx.set_channel(self.dmxAddress + 1, green)
        self.dmx.set_channel(self.dmxAddress + 2, blue)

    def increase_color(self, color, value, dmx):
        self.dmx = dmx
        if color == 'red':
            self.red = dmx.get_channel(self.dmxAddress) 
            self.dmx.set_channel(self.dmxAddress, self.red + value)
        elif color == 'green':
            self.green = dmx.get_channel(self.dmxAddress + 1)
            self.dmx.set_channel(self.dmxAddress + 1, self.green + value)
        elif color == 'blue':
            self.blue = dmx.get_channel(self.dmxAddress + 2)
            self.dmx.set_channel(self.dmxAddress + 2, self.blue + value)

    def decrease_color(self, color, value, dmx):
        self.dmx = dmx
        if color == 'red':
            self.red -= value
            self.dmx.set_channel(self.dmxAddress, self.red)
        elif color == 'green':
            self.green -= value
            self.dmx.set_channel(self.dmxAddress + 1, self.green)
        elif color == 'blue':
            self.blue -= value
            self.dmx.set_channel(self.dmxAddress + 2, self.blue)

