import sys
if sys.implementation.name != "circuitpython":
    def const(x): return x

NEVER                  = const(0)
LESS                   = const(1)
LEQUAL                 = const(2)
GREATER                = const(3)
GEQUAL                 = const(4)
EQUAL                  = const(5)
NOTEQUAL               = const(6)
ALWAYS                 = const(7)

ARGB1555               = const(0)
L1                     = const(1)
L4                     = const(2)
L8                     = const(3)
RGB332                 = const(4)
ARGB2                  = const(5)
ARGB4                  = const(6)
RGB565                 = const(7)
PALETTED               = const(8)
TEXT8X8                = const(9)
TEXTVGA                = const(10)
BARGRAPH               = const(11)
PALETTED565            = const(14)       # FT810
PALETTED4444           = const(15)       # FT810
PALETTED8              = const(16)       # FT810
L2                     = const(17)       # FT810

GLFORMAT               = const(31)       # FT815
ASTC_4x4               = const(0x93B0)   # BT815
ASTC_5x4               = const(0x93B1)   # BT815
ASTC_5x5               = const(0x93B2)   # BT815
ASTC_6x5               = const(0x93B3)   # BT815
ASTC_6x6               = const(0x93B4)   # BT815
ASTC_8x5               = const(0x93B5)   # BT815
ASTC_8x6               = const(0x93B6)   # BT815
ASTC_8x8               = const(0x93B7)   # BT815
ASTC_10x5              = const(0x93B8)   # BT815
ASTC_10x6              = const(0x93B9)   # BT815
ASTC_10x8              = const(0x93BA)   # BT815
ASTC_10x10             = const(0x93BB)   # BT815
ASTC_12x10             = const(0x93BC)   # BT815
ASTC_12x12             = const(0x93BD)   # BT815


NEAREST                = const(0)
BILINEAR               = const(1)

BORDER                 = const(0)
REPEAT                 = const(1)

KEEP                   = const(1)
REPLACE                = const(2)
INCR                   = const(3)
DECR                   = const(4)
INVERT                 = const(5)

DLSWAP_DONE            = const(0)
DLSWAP_LINE            = const(1)
DLSWAP_FRAME           = const(2)

INT_SWAP               = const(1)
INT_TOUCH              = const(2)
INT_TAG                = const(4)
INT_SOUND              = const(8)
INT_PLAYBACK           = const(16)
INT_CMDEMPTY           = const(32)
INT_CMDFLAG            = const(64)
INT_CONVCOMPLETE       = const(128)

TOUCHMODE_OFF          = const(0)
TOUCHMODE_ONESHOT      = const(1)
TOUCHMODE_FRAME        = const(2)
TOUCHMODE_CONTINUOUS   = const(3)

ZERO                   = const(0)
ONE                    = const(1)
SRC_ALPHA              = const(2)
DST_ALPHA              = const(3)
ONE_MINUS_SRC_ALPHA    = const(4)
ONE_MINUS_DST_ALPHA    = const(5)

BITMAPS                = const(1)
POINTS                 = const(2)
LINES                  = const(3)
LINE_STRIP             = const(4)
EDGE_STRIP_R           = const(5)
EDGE_STRIP_L           = const(6)
EDGE_STRIP_A           = const(7)
EDGE_STRIP_B           = const(8)
RECTS                  = const(9)

OPT_MONO               = const(1)
OPT_NODL               = const(2)
OPT_FLAT               = const(256)
OPT_CENTERX            = const(512)
OPT_CENTERY            = const(1024)
OPT_CENTER             = const(OPT_CENTERX | OPT_CENTERY)
OPT_NOBACK             = const(4096)
OPT_NOTICKS            = const(8192)
OPT_NOHM               = const(16384)
OPT_NOPOINTER          = const(16384)
OPT_NOSECS             = const(32768)
OPT_NOHANDS            = const(49152)
OPT_RIGHTX             = const(2048)
OPT_SIGNED             = const(256)

OPT_NOTEAR             = const(4)
OPT_FULLSCREEN         = const(8)
OPT_MEDIAFIFO          = const(16)
OPT_FORMAT             = const(4096)     # For 815
OPT_FILL               = const(8192)     # For 815

LINEAR_SAMPLES         = const(0)
ULAW_SAMPLES           = const(1)
ADPCM_SAMPLES          = const(2)

# The built-in audio samples
HARP                   = const(0x40)     # Instruments
XYLOPHONE              = const(0x41)
TUBA                   = const(0x42)
GLOCKENSPIEL           = const(0x43)
ORGAN                  = const(0x44)
TRUMPET                = const(0x45)
PIANO                  = const(0x46)
CHIMES                 = const(0x47)
MUSICBOX               = const(0x48)
BELL                   = const(0x49)
CLICK                  = const(0x50)     # Percussive
SWITCH                 = const(0x51)
COWBELL                = const(0x52)
NOTCH                  = const(0x53)
HIHAT                  = const(0x54)
KICKDRUM               = const(0x55)
POP                    = const(0x56)
CLACK                  = const(0x57)
CHACK                  = const(0x58)
MUTE                   = const(0x60)     # Management
UNMUTE                 = const(0x61)

RAM_CMD                = const(0x308000)
RAM_DL                 = const(0x300000)
REG_CLOCK              = const(0x302008)
REG_CMDB_SPACE         = const(0x302574)
REG_CMDB_WRITE         = const(0x302578)
REG_CMD_DL             = const(0x302100)
REG_CMD_READ           = const(0x3020f8)
REG_CMD_WRITE          = const(0x3020fc)
REG_CPURESET           = const(0x302020)
REG_CSPREAD            = const(0x302068)
REG_DITHER             = const(0x302060)
REG_DLSWAP             = const(0x302054)
REG_FRAMES             = const(0x302004)
REG_FREQUENCY          = const(0x30200c)
REG_GPIO               = const(0x302094)
REG_GPIO_DIR           = const(0x302090)
REG_HCYCLE             = const(0x30202c)
REG_HOFFSET            = const(0x302030)
REG_HSIZE              = const(0x302034)
REG_HSYNC0             = const(0x302038)
REG_HSYNC1             = const(0x30203c)
REG_ID                 = const(0x302000)
REG_INT_EN             = const(0x3020ac)
REG_INT_FLAGS          = const(0x3020a8)
REG_INT_MASK           = const(0x3020b0)
REG_MACRO_0            = const(0x3020d8)
REG_MACRO_1            = const(0x3020dc)
REG_OUTBITS            = const(0x30205c)
REG_PCLK               = const(0x302070)
REG_PCLK_POL           = const(0x30206c)
REG_PLAY               = const(0x30208c)
REG_PLAYBACK_FORMAT    = const(0x3020c4)
REG_PLAYBACK_FREQ      = const(0x3020c0)
REG_PLAYBACK_LENGTH    = const(0x3020b8)
REG_PLAYBACK_LOOP      = const(0x3020c8)
REG_PLAYBACK_PLAY      = const(0x3020cc)
REG_PLAYBACK_READPTR   = const(0x3020bc)
REG_PLAYBACK_START     = const(0x3020b4)
REG_PWM_DUTY           = const(0x3020d4)
REG_PWM_HZ             = const(0x3020d0)
REG_ROTATE             = const(0x302058)
REG_SOUND              = const(0x302088)
REG_SWIZZLE            = const(0x302064)
REG_TAG                = const(0x30207c)
REG_TAG_X              = const(0x302074)
REG_TAG_Y              = const(0x302078)
REG_TAP_CRC            = const(0x302024)
REG_TOUCH_ADC_MODE     = const(0x302108)
REG_TOUCH_CHARGE       = const(0x30210c)
REG_TOUCH_DIRECT_XY    = const(0x30218c)
REG_TOUCH_DIRECT_Z1Z2  = const(0x302190)
REG_TOUCH_MODE         = const(0x302104)
REG_TOUCH_OVERSAMPLE   = const(0x302114)
REG_TOUCH_RAW_XY       = const(0x30211c)
REG_TOUCH_RZ           = const(0x302120)
REG_TOUCH_RZTHRESH     = const(0x302118)
REG_TOUCH_SCREEN_XY    = const(0x302124)
REG_TOUCH_SETTLE       = const(0x302110)
REG_TOUCH_TAG          = const(0x30212c)
REG_TOUCH_TAG_XY       = const(0x302128)
REG_TOUCH_TRANSFORM_A  = const(0x302150)
REG_TOUCH_TRANSFORM_B  = const(0x302154)
REG_TOUCH_TRANSFORM_C  = const(0x302158)
REG_TOUCH_TRANSFORM_D  = const(0x30215c)
REG_TOUCH_TRANSFORM_E  = const(0x302160)
REG_TOUCH_TRANSFORM_F  = const(0x302164)
REG_TRACKER            = const(0x309000)
REG_TRIM               = const(0x302180)
REG_VCYCLE             = const(0x302040)
REG_VOFFSET            = const(0x302044)
REG_VOL_PB             = const(0x302080)
REG_VOL_SOUND          = const(0x302084)
REG_VSIZE              = const(0x302048)
REG_VSYNC0             = const(0x30204c)
REG_VSYNC1             = const(0x302050)

RED                    = const(2)
GREEN                  = const(3)
BLUE                   = const(4)
ALPHA                  = const(5)

# 810 registers

REG_MEDIAFIFO_BASE     = const(0x30901c) 
REG_MEDIAFIFO_READ     = const(0x309014) 
REG_MEDIAFIFO_SIZE     = const(0x309020) 
REG_MEDIAFIFO_WRITE    = const(0x309018) 
REG_GPIOX              = const(0x30209c)
REG_GPIOX_DIR          = const(0x302098)


# 815 registers
REG_FLASH_SIZE         = const(0x00309024) 
REG_FLASH_STATUS       = const(0x003025f0) 
REG_ADAPTIVE_FRAMERATE = const(0x0030257c) 
