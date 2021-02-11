__version__ = '0.1.0'

from .gameduino_spidriver import GameduinoSPIDriver
Gameduino = GameduinoSPIDriver
from .registers import *
from .eve import align4
