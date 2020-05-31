import gameduino as GD
from eve import align4, EVE
import zlib

import dogfight

if __name__ == '__main__':
    from gameduino_spidriver import GameduinoSPIDriver
    gd = GameduinoSPIDriver()

    gd.init()

    flashdata = bytes(8192)
    atlas = {}
    
    (flashdata, atlas) = dogfight.flash(flashdata, atlas)

    BLK = 2**16
    for i in range(8192, len(flashdata), BLK):
        print(i, len(flashdata))
        b = flashdata[i:i + BLK]
        gd.cmd_inflate(0)
        gd.cc(align4(zlib.compress(b)))
        gd.cmd_flashupdate(i, 0, BLK)
    gd.finish()
