"""Draw a test pattern and capture the live display to a PNG file."""

from pathlib import Path
import random

import apprunner
import bteve as eve
import minpng


def add_arguments(parser):
    parser.add_argument("-o", "--output", type=Path, default=Path("screenshot.png"),
                        help="Output PNG filename (default: screenshot.png)")


def screenshot(gd, filename):
    """Capture the current display without changing its display list."""
    filename = Path(filename).expanduser()
    with filename.open("wb") as output:
        png = minpng.PngWriter(output.write, gd.w, gd.h)
        def handle_line(rgb):
            for i in range(0, len(rgb), 3):
                png.rgb(rgb[i], rgb[i + 1], rgb[i + 2])
        gd.screenshot(handle_line)
    print("Saved {} ({} x {})".format(filename, gd.w, gd.h))


def main(gd, args):
    rng = random.Random(8)
    gd.ClearColorRGB(0x18, 0x20, 0x30)
    gd.Clear()
    gd.VertexFormat(2)
    gd.Begin(eve.POINTS)
    for _ in range(100):
        gd.ColorRGB(rng.randrange(256), rng.randrange(256), rng.randrange(256))
        gd.PointSize(rng.randrange(4, max(5, min(gd.w, gd.h) // 12)))
        gd.Vertex2f(rng.randrange(gd.w), rng.randrange(gd.h))
    gd.ColorRGB(255, 255, 255)
    gd.cmd_text(gd.w // 2, 24, 27, eve.OPT_CENTER, "Live EVE screenshot")
    gd.swap()
    screenshot(gd, args.output)


if __name__ == "__main__":
    apprunner.run(main, add_arguments=add_arguments)
