"""Single-SPI connection for SPIDriver, SPIDriver2, and SPIDriverQ."""

import os

from spidriver import SPIDriver

from bteve.gameduino_spidriver import GameduinoSPIDriver


def add_arguments(parser):
    parser.add_argument("-p", "--port", required=True,
                        help="SPIDriver serial port (supports ~)")


class EVE(GameduinoSPIDriver):
    """Open the adapter. Call init() to boot EVE, then close() when finished."""

    def __init__(self, port):
        driver = SPIDriver(os.path.expanduser(os.fspath(port)))
        try:
            super().__init__(driver)
            # Q may have been left in dual/quad mode by a previous application.
            if driver.product == "spidriverq":
                driver.set_width(1)
            driver.setmode(0)
            self.setmodel(816)
        except BaseException:
            driver.close()
            raise

    def close(self):
        try:
            self.d.unsel()
        finally:
            self.d.close()
