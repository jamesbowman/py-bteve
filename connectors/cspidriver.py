"""Single-SPI connection for SPIDriver, SPIDriver2, and SPIDriverQ."""

import os

from spidriver import SPIDriver

from bteve.gameduino_spidriver import GameduinoSPIDriver, SPIDriverDevice
from bteve.riverdi import RIVERDI_PROFILES


def add_arguments(parser):
    parser.add_argument("-p", "--port", required=True,
                        help="SPIDriver serial port (supports ~)")
    parser.add_argument("--board", choices=["gameduino", *RIVERDI_PROFILES],
                        default="gameduino", help="Display board or panel profile")
    parser.add_argument("--oscillator", choices=["internal", "external"],
                        help="Override the profile's EVE clock source")


def EVE(port, board="gameduino", oscillator=None):
    """Open a named board or a custom board profile. Call init() to boot it."""
    if isinstance(board, str) and board != "gameduino":
        try:
            board = RIVERDI_PROFILES[board]
        except KeyError:
            raise ValueError("Unknown display board: " + board) from None
    if oscillator is not None:
        if not hasattr(board, "with_oscillator"):
            raise ValueError("This board does not support an oscillator override")
        board = board.with_oscillator(oscillator)

    driver = SPIDriver(os.path.expanduser(os.fspath(port)))
    try:
        if board == "gameduino":
            device = GameduinoSPIDriver(driver)
        else:
            device = SPIDriverDevice(driver, board)
        # Q may have been left in dual/quad mode by a previous application.
        if driver.product == "spidriverq":
            driver.set_width(1)
        driver.setmode(0)
        return device
    except BaseException:
        driver.close()
        raise
