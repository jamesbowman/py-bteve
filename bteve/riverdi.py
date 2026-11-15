"""Initialization profiles for Riverdi EVE4 IPS displays with a BT817."""

import struct
import time
from collections import namedtuple

from . import registers as reg


# Timing values from the Module Initialization tables in Riverdi's datasheets.
# The 4.3-inch RVT43HLBNWC00-B specifies 0x032 (9 MHz) for REG_PCLK_FREQ.
# https://download.riverdi.com/RVT43HLBNWC00-B/DS_RVT43HLBNWC00-B_Rev.1.7.pdf
# https://github.com/riverdi/riverdi-eve-lib/blob/main/riverdi_modules/modules.h
PanelTiming = namedtuple("PanelTiming", (
    "width", "height", "hcycle", "hoffset", "hsync1", "vcycle", "voffset",
    "vsync1", "pclk_freq", "pclk_2x", "pclk",
))


class RiverdiEVE4:
    model = 817
    system_frequency = 72000000

    def __init__(self, panel=None, oscillator="external"):
        if oscillator not in ("internal", "external"):
            raise ValueError("Riverdi oscillator must be 'internal' or 'external'")
        self.panel = panel
        self.oscillator = oscillator

    def with_oscillator(self, oscillator):
        return type(self)(self.panel, oscillator)

    def wake(self, device):
        # CLKSEL requires a stopped PLL, even when the host is restarting a
        # running display. BRT_AN_033 section 2.4 specifies reset then ACTIVE.
        device.host_cmd(0x42)  # SLEEP
        device.host_cmd(0x44 if self.oscillator == "external" else 0x48)
        device.host_cmd(0x61, 0x46)  # CLKSEL, 72 MHz
        device.host_cmd(0x68)  # RST_PULSE, retains host command settings
        device.host_cmd(0x00)  # ACTIVE
        time.sleep(0.04)

    def configure_display(self, device):
        panel = self.panel
        if panel is None:
            raise ValueError(
                "Select the Riverdi panel profile matching the module's part number "
                "(riverdi-ips35, riverdi-ips43, riverdi-ips50, riverdi-ips70 or "
                "riverdi-ips101), or use minimal initialization to identify the chip."
            )

        device.wr8(reg.REG_PWM_DUTY, 0)
        device.wr8(reg.REG_PCLK, 0)
        device.wr16(reg.REG_PCLK_FREQ, panel.pclk_freq)
        device.wr8(reg.REG_PCLK_2X, panel.pclk_2x)
        device.wr16(reg.REG_HSIZE, panel.width)
        device.wr16(reg.REG_HCYCLE, panel.hcycle)
        device.wr16(reg.REG_HOFFSET, panel.hoffset)
        device.wr16(reg.REG_HSYNC0, 0)
        device.wr16(reg.REG_HSYNC1, panel.hsync1)
        device.wr16(reg.REG_VSIZE, panel.height)
        device.wr16(reg.REG_VCYCLE, panel.vcycle)
        device.wr16(reg.REG_VOFFSET, panel.voffset)
        device.wr16(reg.REG_VSYNC0, 0)
        device.wr16(reg.REG_VSYNC1, panel.vsync1)
        device.wr8(reg.REG_SWIZZLE, 0)
        device.wr8(reg.REG_PCLK_POL, 1)
        device.wr8(reg.REG_CSPREAD, 0)
        device.wr8(reg.REG_DITHER, 0)

        # Set a black first frame directly. A coprocessor swap could stall
        # with PCLK disabled. BRT_AN_033 section 2.4 also calls for zeroing
        # the upper layout/size bits of the user bitmap handles after reset.
        first_frame = bytearray(struct.pack("<II", 0x02000000, 0x26000007))
        for handle in range(16):
            # BITMAP_HANDLE, BITMAP_LAYOUT_H(0,0), BITMAP_SIZE_H(0,0)
            first_frame.extend(struct.pack("<III", 0x05000000 | handle, 0x28000000, 0x29000000))
        first_frame.extend(struct.pack("<I", 0))  # DISPLAY
        device.wr(reg.RAM_DL, first_frame)
        device.wr8(reg.REG_DLSWAP, reg.DLSWAP_FRAME)

        device.wr16(reg.REG_PWM_HZ, 10000)
        self.start_panel(device)
        device.cmd_dlstart()
        device.cmd_loadidentity()

    def start_panel(self, device):
        device.wr16(reg.REG_GPIOX_DIR, device.rd16(reg.REG_GPIOX_DIR) | 0x8000)
        device.wr16(reg.REG_GPIOX, device.rd16(reg.REG_GPIOX) | 0x8000)
        device.wr8(reg.REG_PCLK, self.panel.pclk)
        device.wr8(reg.REG_PWM_DUTY, 128)


class RiverdiIPS50(RiverdiEVE4):
    def start_panel(self, device):
        # Use the higher RGB pad drive and keep DISP low while starting the
        # 24 MHz pixel clock. Preserve all RiBUS GPIO directions and levels.
        gpio = (device.rd16(reg.REG_GPIOX) & ~0x8000) | 0x1000
        device.wr16(reg.REG_GPIOX, gpio)
        device.wr16(reg.REG_GPIOX_DIR, device.rd16(reg.REG_GPIOX_DIR) | 0x8000)
        device.wr8(reg.REG_PCLK, self.panel.pclk)
        time.sleep(0.12)
        device.wr16(reg.REG_GPIOX, gpio | 0x8000)
        # RVT50HQTNWC00 section 12.4 specifies 250 ms of valid RGB before light.
        time.sleep(0.25)
        device.wr8(reg.REG_PWM_DUTY, 128)


RIVERDI_PROFILES = {
    "riverdi": RiverdiEVE4(),  # Controller diagnostics before panel selection.
    "riverdi-ips35": RiverdiEVE4(PanelTiming(320, 240, 371, 43, 4, 260, 12, 4, 0x022, 0, 1)),
    "riverdi-ips43": RiverdiEVE4(PanelTiming(480, 272, 531, 43, 4, 292, 12, 4, 0x032, 0, 1)),
    "riverdi-ips50": RiverdiIPS50(PanelTiming(800, 480, 816, 8, 4, 496, 8, 4, 0xD14, 0, 3)),
    "riverdi-ips70": RiverdiEVE4(PanelTiming(1024, 600, 1344, 160, 70, 635, 23, 10, 0xD12, 0, 1)),
    "riverdi-ips101": RiverdiEVE4(PanelTiming(1280, 800, 1440, 88, 20, 838, 23, 10, 0x8C1, 1, 1)),
}
