#!/usr/bin/env python

crc_table = [
  0x00000000, 0x1db71064, 0x3b6e20c8, 0x26d930ac,
  0x76dc4190, 0x6b6b51f4, 0x4db26158, 0x5005713c,
  0xedb88320, 0xf00f9344, 0xd6d6a3e8, 0xcb61b38c,
  0x9b64c2b0, 0x86d3d2d4, 0xa00ae278, 0xbdbdf21c
]

def crc_update(crc, data):
    tbl_idx = crc ^ (data >> (0 * 4))
    crc = crc_table[tbl_idx & 0x0f] ^ (crc >> 4)
    tbl_idx = crc ^ (data >> (1 * 4))
    crc = crc_table[tbl_idx & 0x0f] ^ (crc >> 4)
    return crc & 0xffffffff

class PngWriter:
    def __init__(self, writef, w, h):
        self.writef = writef
        self.w = w
        self.h = h

        self.output = bytearray(64)
        self.nout = 0
        self.crc32 = 0
        self.b8s(bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))
        self.start_chunk(b"IHDR", 13)
        self.be32(w)
        self.be32(h)
        self.b8s(bytes([8, 2, 0, 0, 0]))
        self.end_chunk()

        self.bpl = 1 + 3 * w

        self.start_chunk(b"IDAT", 2 + h * (5 + self.bpl) + 4)
        self.b8(0x78)                       # Start DEFLATE blocks
        self.b8(0x01)
        self.i = 0                             # Pixel coordinate (0,0)
        self.j = 0
        self.s1 = 1                            # Seed the Adler CRC */
        self.s2 = 0
        self.writef(self.output[:self.nout])

    def b8(self, n):
        n &= 0xff
        self.output[self.nout] = n
        self.nout += 1
        self.crc32 = crc_update(self.crc32, n)

    # adler8: Output byte n and update the CRC32 and Adler CRC
    def adler8(self, n):
        self.b8(n)
        self.s1 = (self.s1 + n) % 65521
        self.s2 = (self.s2 + self.s1) % 65521

    # be32: Output 32-bit in big-endian
    def be32(self, n):
        self.b8(n >> 24)
        self.b8(n >> 16)
        self.b8(n >> 8)
        self.b8(n)

    # le16: Output 16-bit in little-endian
    def le16(self, n):
        self.b8(n)
        self.b8(n >> 8)

    # b8s: Output an array of bytes
    def b8s(self, b):
        for c in b:
            self.b8(c)

    def start_chunk(self, typecode, size):
        self.be32(size)
        self.crc32 = 0xffffffff
        self.b8s(typecode)

    def end_chunk(self):
        self.be32(~self.crc32)

    def rgb(self, r, g, b):
        self.nout = 0

        if (self.i == 0):                      # Start a block for each line 
            self.b8((self.j + 1) == self.h)    # 1 if last line, 0 otherwise 
            self.le16(self.bpl)                    # Bytes per line, and inverted 
            self.le16(~self.bpl)
            self.adler8(0)                       # Filter: none 

        self.adler8(r)                         # The pixel data itself 
        self.adler8(g)
        self.adler8(b)
        self.i += 1

        if (self.i == self.w):                   # End of line means end of block 
            self.i = 0
            self.j += 1
            if (self.j == self.h):               # Is this the last line? 
                self.be32((self.s2 << 16) + self.s1)   # Append the Adler CRC 
                self.end_chunk()                     # End of the IDAT chunk 
                self.start_chunk(b"IEND", 0)        # IEND chunk means end of file 
                self.end_chunk()
        self.writef(self.output[:self.nout])

if __name__ == "__main__":
    with open("foo.png", "wb") as pngf:
        p = PngWriter(pngf.write, 40, 25)
        for y in range(25):
            for x in range(40):
                p.rgb(0, 255, 0)
