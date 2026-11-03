"""Read flash IDs and restore the original flash attachment mode."""

import apprunner
import bteve as eve


def flashinfo(gd):
    status = gd.rd32(eve.REG_FLASH_STATUS)
    if status not in (1, 2, 3):
        raise RuntimeError("Flash is unavailable (status {})".format(status))

    def read_id(command, count):
        gd.cmd_flashspidesel()
        gd.cmd_flashspitx(bytes([command]))
        gd.cmd_flashspirx(0, count)
        gd.cmd_flashspidesel()
        gd.finish()
        return gd.rd(0, count)

    gd.cmd_flashdetach()
    try:
        jedec = read_id(0x9f, 3)
        uid = read_id(0x4b, 12)[4:]  # Four dummy bytes precede the unique ID.
    finally:
        gd.cmd_flashspidesel()
        if status >= 2:
            gd.cmd_flashattach()
        if status == 3:
            gd.cmd_flashfast()
            result = gd.result()
            if result:
                raise RuntimeError("Could not restore flash fast mode: 0x{:x}".format(result))
        gd.finish()

    restored = gd.rd32(eve.REG_FLASH_STATUS)
    if restored != status:
        raise RuntimeError("Flash status changed: {} -> {}".format(status, restored))
    gd.ClearColorRGB(0x00, 0x20, 0x40)
    gd.Clear()
    gd.ColorRGB(255, 255, 255)
    for y, label, data in ((40, "Flash ID", jedec), (80, "Unique ID", uid)):
        message = label + ": " + ":".join("{:02X}".format(b) for b in data)
        print(message)
        gd.cmd_text(16, y, 27, 0, message)
    message = "Flash mode restored: {}".format(restored)
    print(message)
    gd.cmd_text(16, 120, 27, 0, message)
    gd.swap()


if __name__ == "__main__":
    apprunner.run(flashinfo)
