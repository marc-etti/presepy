from app.services.dmx.DMX import DMX
from app.services.controllers.led_controller import LedController

myDMX = DMX()
myLedController = LedController(0, 0, 0, myDMX, 1)


