class LedController:
    def __init__(self, dmx, dmxAddress) -> None:
        self.dmx = dmx
        self.dmxAddress = dmxAddress
        self.red = dmx.get_channel(dmxAddress)
        self.green = dmx.get_channel(dmxAddress + 1)
        self.blue = dmx.get_channel(dmxAddress + 2)

    def set_color(self, red, green, blue) -> None:
        self.dmx.set_channel(self.dmxAddress, red)
        self.dmx.set_channel(self.dmxAddress + 1, green)
        self.dmx.set_channel(self.dmxAddress + 2, blue)

    def increase_color(self, color, value) -> None:
        if color == 'red':
            self.red = self.dmx.get_channel(self.dmxAddress) + value
            if self.red > 255:
                self.red = 255
            self.dmx.set_channel(self.dmxAddress, self.red)
        elif color == 'green':
            self.green = self.dmx.get_channel(self.dmxAddress + 1) + value
            if self.green > 255:
                self.green = 255
            self.dmx.set_channel(self.dmxAddress + 1, self.green)
        elif color == 'blue':
            self.blue = self.dmx.get_channel(self.dmxAddress + 2) + value
            if self.blue > 255:
                self.blue = 255
            self.dmx.set_channel(self.dmxAddress + 2, self.blue)

    def decrease_color(self, color, value) -> None:
        if color == 'red':
            self.red = self.dmx.get_channel(self.dmxAddress) - value
            if self.red < 0:
                self.red = 0
            self.dmx.set_channel(self.dmxAddress, self.red)
        elif color == 'green':
            self.green = self.dmx.get_channel(self.dmxAddress + 1) - value
            if self.green < 0:
                self.green = 0
            self.dmx.set_channel(self.dmxAddress + 1, self.green)
        elif color == 'blue':
            self.blue = self.dmx.get_channel(self.dmxAddress + 2) - value
            if self.blue < 0:
                self.blue = 0
            self.dmx.set_channel(self.dmxAddress + 2, self.blue)
