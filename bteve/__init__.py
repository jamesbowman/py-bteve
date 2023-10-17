__version__ = '0.2.1'

from .gameduino_spidriver import GameduinoSPIDriver
Gameduino = GameduinoSPIDriver
from .registers import *
from .eve import align4, MoviePlayer
