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

## Examples

These desktop examples use the same connector and port options:

```sh
python examples/qix.py --port ~/ports/usb-Excamera_spiq_ex5c3751
python examples/widgets.py --port ~/ports/usb-Excamera_spiq_ex5c3751
python examples/sketch.py --port ~/ports/usb-Excamera_spiq_ex5c3751
python examples/flashinfo.py --port ~/ports/usb-Excamera_spiq_ex5c3751
python examples/rotoblinka.py --port ~/ports/usb-Excamera_spiq_ex5c3751
python examples/bench.py --port ~/ports/usb-Excamera_spiq_ex5c3751 --size 262144 --chunk 4096
python examples/screenshot.py --port ~/ports/usb-Excamera_spiq_ex5c3751 --output capture.png
```

- `qix` animates colored line trails using the configured display dimensions.
- `widgets` demonstrates touch controls and scales its layout to fit the panel.
- `sketch` starts EVE's touchscreen drawing engine, which remains active after
  the script exits. Running another example resets it. Touch examples use the
  panel's existing touch configuration.
- `flashinfo` reads the JEDEC and unique IDs and restores the original flash
  attachment mode, including fast mode when it was active.
- `rotoblinka` loads the included PNGs relative to its source file, so it also
  works when launched by absolute path from another directory.
- `bench` measures RAM_G write and read rates, checks the complete readback, and
  verifies EVE's CRC against the host. It overwrites RAM_G starting at address 0.
  Use `--file filename` for a file payload instead of generated data; the limit
  is 1 MiB.
- `screenshot` draws a test pattern and saves the actual panel rendering as PNG.
  Capture temporarily stops the display clock and restores it on completion,
  error, or Ctrl-C. Its `screenshot(gd, filename)` function can also capture the
  current display from another application.

Animated examples run until Ctrl-C. For application-specific options that
appear in `--help`, pass `add_arguments=configure_parser` to `apprunner.run`;
the application then receives `(gd, args)`. Existing `(gd)` callbacks continue
to work without that option.

## To release

    python -m pip install --upgrade build
    python -m build
    python -m twine upload dist/*


