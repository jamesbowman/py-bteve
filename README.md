# py-eve

[![Build Status](https://travis-ci.org/jamesbowman/py-bteve.svg?branch=master)](https://travis-ci.org/jamesbowman/py-bteve)
[![Documentation Status](https://readthedocs.org/projects/bteve/badge/?version=latest)](https://bteve.readthedocs.io/en/latest/?badge=latest)

Python driver for BridgeTek's Eve GPU

## SPIDriver applications

Install the package and the optional adapter dependency in your Python environment.

```sh
python -m pip install -e '.[spidriver]'
```

`--port` selects the adapter. `--board` selects the display module. The default
connector, `cspidriver`, uses single SPI, mode 0, on SPIDriver, SPIDriver2 and
SPIDriverQ. Quoted port paths containing `~` work.

### Riverdi BT817

Check the controller and command FIFO before selecting a panel. This resets EVE,
reads the chip model and current timing registers, then verifies a memory CRC.
The dimensions shown after reset are register defaults and cannot identify the LCD.

```sh
python hwdiag.py --port ~/ports/usb-Excamera_spiq_ex5c3751 --board riverdi
```

For drawing, match the part number on the module to its Riverdi timing profile.
For example, a 5-inch Riverdi EVE4 using the IPS_50 timings runs with
`--board riverdi-ips50`. [5-inch module datasheet](https://download.riverdi.com/RVT50HQBNWC00-B/DS_RVT50HQBNWC00-B_Rev.1.7.pdf)

```sh
python helloworld.py --port ~/ports/usb-Excamera_spiq_ex5c3751 --board riverdi-ips50
```

| Board profile | Riverdi EVE4 timing set | Active pixels |
| --- | --- | --- |
| `riverdi-ips35` | IPS_35 | 320 × 240 |
| `riverdi-ips43` | IPS_43 | 480 × 272 |
| `riverdi-ips50` | IPS_50 | 800 × 480 |
| `riverdi-ips70` | IPS_70 | 1024 × 600 |
| `riverdi-ips101` | IPS_101 | 1280 × 800 |

The 5-inch profile uses a 24 MHz pixel clock and asserts DISP after the clock
is running. It waits 250 ms before enabling the backlight at 100% duty. To change
brightness after startup, call `gd.wr8(eve.REG_PWM_DUTY, duty)` with `bteve`
imported as `eve` and a duty from 0 to 128.
[5-inch LCD power sequencing, section 12.4](https://download.riverdi.com/RVT50HQTNWC00/DS_RVT50HQTNWC00_Rev.1.1.pdf#page=15)

The profiles default to an external oscillator. Add `--oscillator internal` for
modules that specify the internal oscillator. Riverdi startup uses an EVE host
reset over SPI. It sends no auxiliary-pin commands and assumes PD_N is released.
See [Riverdi's startup guide](https://riverdi.com/blog/getting-started-with-eve4-display-full-guide)
and [panel definitions](https://github.com/riverdi/riverdi-eve-lib/blob/main/riverdi_modules/modules.h).

### Gameduino

The default board, `gameduino`, uses the original flash configuration and auxiliary
pin setup. Existing invocations can omit `--board`.

```sh
python helloworld.py --port /dev/your-adapter
```

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
and verify its chip identity while skipping panel setup. Minimal startup still
runs the selected board's wake/reset sequence.
Arguments not consumed by the runner remain in `sys.argv` for the application.

Connectors live in the installed `connectors` package and are imported only when
selected. A connector exports `add_arguments(parser)` for its command-line
options and `EVE(**options)` for construction. Devices provide `init(minimal=False)`,
`finish()`, and `close()`. A new SPI connector can inherit `bteve.device.EVEDevice`, implement
`transfer(write_bytes, read_count=0)` with chip select held across both phases,
and assign a board profile to `self.board`. The existing
`bteve.gameduino_spidriver.GameduinoSPIDriver` class accepts an open adapter.

To add a display board on an existing connector, supply a Python object with
`wake(device)` for the host reset/clock sequence and `configure_display(device)`
for the panel, first display list, and backlight. Set `model` to the expected EVE
model (e.g. `817`) and optionally `system_frequency` to the selected clock in Hz.
The shared code checks chip readiness and model before display setup, then reads
the active dimensions into `device.w` and `device.h`. Pass the object directly
with `connectors.cspidriver.EVE(port, board=my_profile)`. Timing-only Riverdi
variants share the setup code in `bteve/riverdi.py`.

## Examples

These desktop examples accept the same connector, port and board options. The
commands below assume a Gameduino. For a Riverdi module, add its matching
`--board` option.

```sh
python examples/qix.py --port /dev/your-adapter
python examples/widgets.py --port /dev/your-adapter
python examples/sketch.py --port /dev/your-adapter
python examples/flashinfo.py --port /dev/your-adapter
python examples/rotoblinka.py --port /dev/your-adapter
python examples/bench.py --port /dev/your-adapter --size 262144 --chunk 4096
python examples/screenshot.py --port /dev/your-adapter --output capture.png
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

See [RELEASING.md](RELEASING.md) for instructions on publishing to PyPI with
Trusted Publishing and provenance.


