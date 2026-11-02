"""Display a greeting using the selected connector."""

import bteve as eve
import apprunner


def main(gd):
    gd.ClearColorRGB(0x20, 0x40, 0x20)
    gd.Clear()
    gd.cmd_text(gd.w // 2, gd.h // 2, 31, eve.OPT_CENTER, "Hello world")
    gd.swap()


if __name__ == "__main__":
    apprunner.run(main)
