"""Measure verified RAM_G write/read throughput using generated data or a file."""

from binascii import crc32
from pathlib import Path
import time

import apprunner
import bteve as eve

RAM_G_SIZE = 1024 * 1024


def add_arguments(parser):
    parser.add_argument("--size", type=int, default=256 * 1024,
                        help="Generated payload size in bytes (default: 262144)")
    parser.add_argument("--chunk", type=int, default=4096,
                        help="Transfer chunk size in bytes (default: 4096)")
    parser.add_argument("--file", type=Path,
                        help="Use this file instead of generated data (at most 1 MiB)")


def benchmark(gd, args):
    if not 0 < args.chunk <= RAM_G_SIZE:
        raise ValueError("--chunk must be between 1 and 1048576")
    if args.file:
        with args.file.expanduser().open("rb") as source:
            data = source.read(RAM_G_SIZE + 1)
    else:
        if not 0 < args.size <= RAM_G_SIZE:
            raise ValueError("--size must be between 1 and 1048576")
        data = (bytes(range(256)) * ((args.size + 255) // 256))[:args.size]
    if not 0 < len(data) <= RAM_G_SIZE:
        raise ValueError("Payload must contain between 1 and 1048576 bytes")

    gd.finish()
    start = time.perf_counter()
    for offset in range(0, len(data), args.chunk):
        gd.wr(offset, data[offset:offset + args.chunk])
    gd.rd32(eve.REG_ID)  # Read barrier: include delivery of the final serial write.
    write_time = time.perf_counter() - start

    start = time.perf_counter()
    actual = bytearray()
    for offset in range(0, len(data), args.chunk):
        actual.extend(gd.rd(offset, min(args.chunk, len(data) - offset)))
    read_time = time.perf_counter() - start
    if actual != data:
        raise RuntimeError("RAM_G readback differs from the payload")
    expected_crc = crc32(data) & 0xffffffff
    gd.cmd_memcrc(0, len(data), 0)
    if gd.result() != expected_crc:
        raise RuntimeError("EVE memory CRC differs from the host CRC")

    lines = [
        "Payload: {} bytes, chunk: {}".format(len(data), args.chunk),
        "Write: {:.1f} KiB/s ({:.3f} s)".format(len(data) / write_time / 1024, write_time),
        "Read: {:.1f} KiB/s ({:.3f} s)".format(len(data) / read_time / 1024, read_time),
        "Readback and CRC verified: {:08X}".format(expected_crc),
    ]
    gd.ClearColorRGB(0x18, 0x20, 0x30)
    gd.Clear()
    gd.ColorRGB(255, 255, 255)
    for index, line in enumerate(lines):
        print(line)
        gd.cmd_text(16, 32 + index * 40, 27, 0, line)
    gd.swap()


if __name__ == "__main__":
    apprunner.run(benchmark, add_arguments=add_arguments)
