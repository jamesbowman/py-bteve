import struct
import time
import spidriver

FF = b'\xff'

def hexdump(s):
    def toprint(c):
        if 32 <= c < 127:
            return chr(c)
        else:
            return "."
    def hexline(s):
        bb = struct.unpack("16B", s)
        return (" ".join(["%02x" % c for c in bb]).ljust(49) +
                "|" +
                "".join([toprint(c) for c in bb]).ljust(16) +
                "|")
    return "\n".join([hexline(s[i:i+16]) for i in range(0, len(s), 16)])

class SDCard:
    def __init__(self, s, sel, unsel):
        self.s = s
        self.sel = sel
        self.unsel = unsel

        self.unsel()
        s.write(10 * FF)
        
        while True:
            self.cmd(0)
            r1 = self.response()
            unsel()
            s.write(FF)
            print('r1', r1)
            if r1 == 1:
                break
            time.sleep(.02)

        self.cmd(8, 0x1aa, 0x87)
        self.sdhc = (self.sdR7() == 1)
        print('sdhc', self.sdhc)

        while True:
            self.appcmd(41, int(self.sdhc) << 30)
            r1 = self.R1()
            print('cmd41', r1)
            if (r1 & 1) == 0:
                break

        if self.sdhc:
            self.cmd(58)
            ocr = self.sdR3()
            print('OCR', hex(ocr))
            self.ccs = 1 & (ocr >> 30)

        self.unsel()

    def sec_rd(self, a):
        self.cmd17(a)
        sec = self.s.writeread(512 * FF)
        self.unsel()
        return sec

    def cmd(self, c, lba = 0, crc = 0x95):
        self.sel()
        self.s.write([
            0x40 | c,
            0xff & (lba >> 24),
            0xff & (lba >> 16),
            0xff & (lba >> 8),
            0xff & (lba),
            crc])

    def R1(self):
        r = self.response()
        self.unsel()
        self.s.write(FF)
        return r

    def sdR7(self):
        r = self.response()
        self.s.write(4 * FF)
        self.unsel()
        return r

    def sdR3(self):
        self.response()
        (r,) = struct.unpack(">I", self.s.writeread(4 * FF))
        self.s.write(FF)
        self.unsel()
        return r

    def response(self):
        (r,) = struct.unpack("B", self.s.writeread(FF))
        while (r & 0x80) != 0:
            (r,) = struct.unpack("B", self.s.writeread(FF))
        return r

    def appcmd(self, cc, lba = 0):
        self.cmd(55)
        self.R1()
        self.cmd(cc, lba)

    def cmd17(self, off):
        if self.ccs:
            self.cmd(17, off >> 9)
        else:
            self.cmd(17, off & ~511)
        self.R1()
        self.sel()
        while self.rd1() != 0xfe:
            pass

    def rd1(self):
        return struct.unpack("B", self.s.writeread(FF))[0]

class FAT:
    def __init__(self, sd):
        self.sd = sd

        sec0 = self.sd.sec_rd(0)
        print(hexdump(sec0))

if __name__ == "__main__":
    s = spidriver.SPIDriver("/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DO02C71A-if00-port0")
    s.unsel()
    s.seta(1)
    s.setb(1)

    sd = SDCard(s, lambda: s.seta(0), lambda: s.seta(1))
    FAT(sd)

    """
    s.seta(0)
    while 1:
        s.write(b'\x55')
    """
