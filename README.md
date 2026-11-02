# py-eve

[![Build Status](https://travis-ci.org/jamesbowman/py-bteve.svg?branch=master)](https://travis-ci.org/jamesbowman/py-bteve)
[![Documentation Status](https://readthedocs.org/projects/bteve/badge/?version=latest)](https://bteve.readthedocs.io/en/latest/?badge=latest)

Python driver for BridgeTek's Eve GPU

## SPIDriver applications

Install the package and the optional SPIDriver dependency with the Python
environment you use for your applications:

```sh
python -m pip install -e '.[spidriver]'
python hwdiag.py -c cspidriver --port ~/ports/usb-Excamera_spiq_ex5c3751
python helloworld.py -c cspidriver --port ~/ports/usb-Excamera_spiq_ex5c3751
```

`cspidriver` is the default connector. It supports SPIDriver, SPIDriver2, and
SPIDriverQ through spidriver 2.0.0 or later. Q is explicitly put into single SPI
mode; all adapters use clock mode 0. The serial port is required rather than
hardcoded. Quoted paths containing `~` also work.

The diagnostic wakes/resets EVE, reports its ID and display dimensions, and
checks a command-generated memory CRC against a host calculation. It skips
display setup. The hello-world example uses the existing Gameduino startup,
which reads the display configuration from external flash. It does not program
flash. Other boards may need their own display initialization.

Applications supply a function accepting the connected device:

```python
import apprunner

def main(gd):
    gd.Clear()
    gd.cmd_text(gd.w // 2, gd.h // 2, 31, 0, "Hello")
    gd.swap()

if __name__ == "__main__":
    apprunner.run(main)
```

The runner initializes the device, calls the application, waits for pending
commands, and closes the connection. It also closes on initialization or
application errors. Use `--minimal` (or `run(main, minimal=True)`) to boot EVE
without loading the display configuration from flash. Minimal startup still
sends the wake/reset commands; it is not a passive connection to a running app.
Arguments not consumed by the runner remain in `sys.argv` for the application.

Connectors live in the installed `connectors` package and are imported only when
selected. A connector exports `add_arguments(parser)` for its command-line
options and `EVE(**options)` for construction. Devices provide `init(minimal=False)`,
`finish()`, and `close()`. SPI connectors can inherit the existing Gameduino
protocol and implement `transfer(write_bytes, read_count=0)`, keeping chip select
asserted across both phases. The existing `bteve.gameduino_spidriver.GameduinoSPIDriver`
class remains available for callers that supply their own adapter object.

## To release

    python -m pip install --upgrade build
    python -m build
    python -m twine upload dist/*


