bteve documentation
===================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

``bteve`` is a Python driver for BridgeTek's EVE series GPUs.
In particular it supports the Gameduino 3X series of display devices.

It supports:

* Python running on a PC, connected via a `SPIDriver <https://spidriver.com>`_ to the Gameduino or BT81x
* CircuitPython on an embedded board, including Adafruit M4 boards, Teensy 4.x, and Raspberry Pi Pico

Module classes
--------------

.. class:: Gameduino
  
  The Gameduino class is a specialization of the base class :class:`EVE`.

  .. method:: init()

      Initialize the EVE hardware, calling method
      Calls method :meth:`coldstart`.
      Confirm that it is running.

  .. method:: coldstart()

      Restarts the EVE core.

The class :class:`EVE` contains all the methods for acting on the EVE hardware.

.. class:: EVE

  The following methods are simple drawing operations, and simple graphics state.

  .. method:: Begin(prim) 

      Begin drawing a graphics primitive

      :param int prim: graphics primitive.

      Valid primitives are :data:`BITMAPS`, ``POINTS``, ``LINES``, ``LINE_STRIP``, ``EDGE_STRIP_R``, ``EDGE_STRIP_L``, ``EDGE_STRIP_A``, ``EDGE_STRIP_B`` and ``RECTS``.

  .. method:: BitmapHandle(handle) 

      Set the bitmap handle

      :param int handle: bitmap handle. Range 0-31. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: Vertex2ii(x, y, handle, cell) 

      :param int x: x-coordinate in pixels. Range 0-511
      :param int y: y-coordinate in pixels. Range 0-511
      :param int handle: bitmap handle. Range 0-31
      :param int cell: cell number. Range 0-127

      This method is an alternative to :meth:`Vertex2f`.

  .. method:: Vertex2f(x, y) 

      Draw a point.

      :param float x: pixel x-coordinate
      :param float y: pixel y-coordinate

  .. method:: LineWidth(width) 

      Set the width of rasterized lines

      :param float width: line width in pixels. Range 0-511. The initial value is 1

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: PointSize(size) 

      Set the diameter of rasterized points

      :param float size: point diameter in pixels. Range 0-1023. The initial value is 1

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: Cell(cell) 

      Set the bitmap cell number used for :meth:`Vertex2f` when drawing ``BITMAPS``.

      :param int cell: bitmap cell number. Range 0-127. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: ClearColorA(alpha) 

      Set clear value for the alpha channel

      :param int alpha: alpha value used when the color buffer is cleared. Range 0-255. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: ClearColorRGB(red, green, blue) 

      Set clear values for red, green and blue channels

      :param int red: red value used when the color buffer is cleared. Range 0-255. The initial value is 0
      :param int green: green value used when the color buffer is cleared. Range 0-255. The initial value is 0
      :param int blue: blue value used when the color buffer is cleared. Range 0-255. The initial value is 0

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: Clear(c, s, t) 

      Clear buffers to preset values

      :param int c: clear color buffer. Range 0-1
      :param int s: clear stencil buffer. Range 0-1
      :param int t: clear tag buffer. Range 0-1


  .. method:: End() 

      End drawing a graphics primitive

      :meth:`Vertex2ii` and :meth:`Vertex2f` calls are ignored until the next :meth:`Begin`.

  These methods control the alpha blending state, allowing advanced blending and transparency effects.

  .. method:: AlphaFunc(func, ref) 

      Set the alpha test function

      :param int func: specifies the test function, one of ``NEVER``, ``LESS``, ``LEQUAL``, ``GREATER``, ``GEQUAL``, ``EQUAL``, ``NOTEQUAL``, or ``ALWAYS``. Range 0-7. The initial value is ALWAYS(7)
      :param int ref: specifies the reference value for the alpha test. Range 0-255. The initial value is 0

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  These low-level methods set the bitmap format.
  :meth:`cmd_setbitmap` is a higher-level alternative.

  .. method:: BitmapExtFormat(format) 

      Set the bitmap format

      :param int format: bitmap pixel format.

  .. method:: BitmapLayoutH(linestride, height) 

      Set the source bitmap memory format and layout for the current handle. high bits for large bitmaps

      :param int linestride: high part of bitmap line stride, in bytes. Range 0-7
      :param int height: high part of bitmap height, in lines. Range 0-3

  .. method:: BitmapLayout(format, linestride, height) 

      Set the source bitmap memory format and layout for the current handle

      :param int format: bitmap pixel format, or GLFORMAT to use BITMAP_EXT_FORMAT instead. Range 0-31
      :param int linestride: bitmap line stride, in bytes. Range 0-1023
      :param int height: bitmap height, in lines. Range 0-511

  .. method:: BitmapSizeH(width, height) 

      Set the screen drawing of bitmaps for the current handle. high bits for large bitmaps

      :param int width: high part of drawn bitmap width, in pixels. Range 0-3
      :param int height: high part of drawn bitmap height, in pixels. Range 0-3

  .. method:: BitmapSize(filter, wrapx, wrapy, width, height) 

      Set the screen drawing of bitmaps for the current handle

      :param int filter: bitmap filtering mode, one of ``NEAREST`` or ``BILINEAR``. Range 0-1
      :param int wrapx: bitmap :math:`x` wrap mode, one of ``REPEAT`` or ``BORDER``. Range 0-1
      :param int wrapy: bitmap :math:`y` wrap mode, one of ``REPEAT`` or ``BORDER``. Range 0-1
      :param int width: drawn bitmap width, in pixels. Range 0-511
      :param int height: drawn bitmap height, in pixels. Range 0-511

  .. method:: BitmapSource(addr) 

      Set the source address for bitmap graphics

      :param int addr: Bitmap start address, pixel-aligned. May be in SRAM or flash. Range 0-16777215

  .. method:: BitmapSwizzle(r, g, b, a) 

      Set the source for the r,g,b and a channels of a bitmap

      :param int r: red component source channel. Range 0-7
      :param int g: green component source channel. Range 0-7
      :param int b: blue component source channel. Range 0-7
      :param int a: alpha component source channel. Range 0-7

  .. method:: BitmapTransformA(p, v) 

      Set the :math:`a` component of the bitmap transform matrix

      :param int p: precision control: 0 is 8.8, 1 is 1.15. Range 0-1. The initial value is 0
      :param int v: The :math:`a` component of the bitmap transform matrix, in signed 8.8 or 1.15 bit fixed-point form. Range 0-131071. The initial value is 256

      The initial value is **p** = 0, **v** = 256. This represents the value 1.0.

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: BitmapTransformB(p, v) 

      Set the :math:`b` component of the bitmap transform matrix

      :param int p: precision control: 0 is 8.8, 1 is 1.15. Range 0-1. The initial value is 0
      :param int v: The :math:`b` component of the bitmap transform matrix, in signed 8.8 or 1.15 bit fixed-point form. Range 0-131071. The initial value is 0

      The initial value is **p** = 0, **v** = 0. This represents the value 0.0.

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: BitmapTransformC(v) 

      Set the :math:`c` component of the bitmap transform matrix

      :param int v: The :math:`c` component of the bitmap transform matrix, in signed 15.8 bit fixed-point form. Range 0-16777215. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: BitmapTransformD(p, v) 

      Set the :math:`d` component of the bitmap transform matrix

      :param int p: precision control: 0 is 8.8, 1 is 1.15. Range 0-1. The initial value is 0
      :param int v: The :math:`d` component of the bitmap transform matrix, in signed 8.8 or 1.15 bit fixed-point form. Range 0-131071. The initial value is 0

      The initial value is **p** = 0, **v** = 0. This represents the value 0.0.

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: BitmapTransformE(p, v) 

      Set the :math:`e` component of the bitmap transform matrix

      :param int p: precision control: 0 is 8.8, 1 is 1.15. Range 0-1. The initial value is 0
      :param int v: The :math:`e` component of the bitmap transform matrix, in signed 8.8 or 1.15 bit fixed-point form. Range 0-131071. The initial value is 256

      The initial value is **p** = 0, **v** = 256. This represents the value 1.0.

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: BitmapTransformF(v) 

      Set the :math:`f` component of the bitmap transform matrix

      :param int v: The :math:`f` component of the bitmap transform matrix, in signed 15.8 bit fixed-point form. Range 0-16777215. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: BlendFunc(src, dst) 

      Set pixel arithmetic

      :param int src: specifies how the source blending factor is computed.  One of ``ZERO``, ``ONE``, ``SRC_ALPHA``, ``DST_ALPHA``, ``ONE_MINUS_SRC_ALPHA`` or ``ONE_MINUS_DST_ALPHA``. Range 0-7. The initial value is SRC_ALPHA(2)
      :param int dst: specifies how the destination blending factor is computed, one of the same constants as **src**. Range 0-7. The initial value is ONE_MINUS_SRC_ALPHA(4)

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: ClearStencil(s) 

      Set clear value for the stencil buffer

      :param int s: value used when the stencil buffer is cleared. Range 0-255. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: ClearTag(s) 

      Set clear value for the tag buffer

      :param int s: value used when the tag buffer is cleared. Range 0-255. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: ColorA(alpha) 

      Set the current color alpha

      :param int alpha: alpha for the current color. Range 0-255. The initial value is 255

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: ColorMask(r, g, b, a) 

      Enable and disable writing of frame buffer color components

      :param int r: allow updates to the frame buffer red component. Range 0-1. The initial value is 1
      :param int g: allow updates to the frame buffer green component. Range 0-1. The initial value is 1
      :param int b: allow updates to the frame buffer blue component. Range 0-1. The initial value is 1
      :param int a: allow updates to the frame buffer alpha component. Range 0-1. The initial value is 1

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: ColorRGB(red, green, blue) 

      Set the drawing color

      :param int red: red value for the current color. Range 0-255. The initial value is 255
      :param int green: green for the current color. Range 0-255. The initial value is 255
      :param int blue: blue for the current color. Range 0-255. The initial value is 255

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: swap() 

      End the display list, dispatch it to the graphics hardware, start compiling the display list for the next frame.

  .. method:: Macro(m) 

      Execute a single command from a macro register

      :param int m: macro register to read. Range 0-1

  .. method:: Nop() 

      No operation

  .. method:: PaletteSource(addr) 

      Set the base address of the palette

      :param int addr: Address in graphics SRAM, 2-byte aligned. Range 0-4194303. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: RestoreContext() 

      Restore the current graphics context from the context stack

  .. method:: SaveContext() 

      Push the current graphics context on the context stack.
      The hardware's graphics context stack is 4 levels deep.

  .. method:: ScissorSize(width, height) 

      Set the size of the scissor clip rectangle

      :param int width: The width of the scissor clip rectangle, in pixels. Range 0-4095. The initial value is hsize
      :param int height: The height of the scissor clip rectangle, in pixels. Range 0-4095. The initial value is 2048

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: ScissorXY(x, y) 

      Set the top left corner of the scissor clip rectangle

      :param int x: The :math:`x` coordinate of the scissor clip rectangle, in pixels. Range 0-2047. The initial value is 0
      :param int y: The :math:`y` coordinate of the scissor clip rectangle, in pixels. Range 0-2047. The initial value is 0

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: StencilFunc(func, ref, mask) 

      Set function and reference value for stencil testing

      :param int func: specifies the test function, one of ``NEVER``, ``LESS``, ``LEQUAL``, ``GREATER``, ``GEQUAL``, ``EQUAL``, ``NOTEQUAL``, or ``ALWAYS``. Range 0-7. The initial value is ALWAYS(7)
      :param int ref: specifies the reference value for the stencil test. Range 0-255. The initial value is 0
      :param int mask: specifies a mask that is ANDed with the reference value and the stored stencil value. Range 0-255. The initial value is 255

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: StencilMask(mask) 

      Control the writing of individual bits in the stencil planes

      :param int mask: the mask used to enable writing stencil bits. Range 0-255. The initial value is 255

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: StencilOp(sfail, spass) 
      Set stencil test actions

      :param int sfail: specifies the action to take when the stencil test fails, one of ``KEEP``, ``ZERO``, ``REPLACE``, ``INCR``, ``INCR_WRAP``, ``DECR``, ``DECR_WRAP``, and ``INVERT``. Range 0-7. The initial value is KEEP(1)
      :param int spass: specifies the action to take when the stencil test passes, one of the same constants as **sfail**. Range 0-7. The initial value is KEEP(1)

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: TagMask(mask) 
      Control the writing of the tag buffer

      :param int mask: allow updates to the tag buffer. Range 0-1. The initial value is 1

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: Tag(s) 
      Set the current tag value

      :param int s: tag value. Range 0-255. The initial value is 255

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: VertexTranslateX(x) 

      Set the vertex transformation's x translation component

      :param float x: signed x-coordinate in pixels. Range ±4095. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: VertexTranslateY(y) 

      Set the vertex transformation's y translation component

      :param float y: signed y-coordinate in pixels. Range ±4095. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: VertexFormat(frac) 

      Set the precision of coordinates used for :meth:`Vertex2f`

      :param int frac: Number of fractional bits in X,Y coordinates. Range 0-7. The initial value is 4

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: flush() 

      Send any queued drawing commands directly to the hardware.

  .. method:: cc(b) 

      Append bytes to the command FIFO.

      :param bytes b: The bytes to add. The length of the bytes must be a multiple of 4.


Module constants
----------------

Constants for :meth:`EVE.StencilFunc` and :meth:`AlphaFunc`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: NEVER
  :value: 0

.. data:: LESS
  :value: 1

.. data:: LEQUAL
  :value: 2

.. data:: GREATER
  :value: 3

.. data:: GEQUAL
  :value: 4

.. data:: EQUAL
  :value: 5

.. data:: NOTEQUAL
  :value: 6

.. data:: ALWAYS
  :value: 7

Constants for :meth:`BitmapSwizzle`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: RED
  :value: 2

.. data:: GREEN
  :value: 3

.. data:: BLUE
  :value: 4

.. data:: ALPHA
  :value: 5

Bitmap Formats used by :meth:`BitmapLayout`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: ARGB1555
  :value: 0

.. data:: L1
  :value: 1

.. data:: L4
  :value: 2

.. data:: L8
  :value: 3

.. data:: RGB332
  :value: 4

.. data:: ARGB2
  :value: 5

.. data:: ARGB4
  :value: 6

.. data:: RGB565
  :value: 7

.. data:: PALETTED
  :value: 8

.. data:: TEXT8X8
  :value: 9

.. data:: TEXTVGA
  :value: 10

.. data:: BARGRAPH
  :value: 11

.. data:: PALETTED565
  :value: 14      

.. data:: PALETTED4444
  :value: 15      

.. data:: PALETTED8
  :value: 16      

.. data:: L2
  :value: 17      

.. data:: GLFORMAT
  :value: 31      

.. data:: ASTC_4x4
  :value: 0x93B0  

.. data:: ASTC_5x4
  :value: 0x93B1  

.. data:: ASTC_5x5
  :value: 0x93B2  

.. data:: ASTC_6x5
  :value: 0x93B3  

.. data:: ASTC_6x6
  :value: 0x93B4  

.. data:: ASTC_8x5
  :value: 0x93B5  

.. data:: ASTC_8x6
  :value: 0x93B6  

.. data:: ASTC_8x8
  :value: 0x93B7  

.. data:: ASTC_10x5
  :value: 0x93B8  

.. data:: ASTC_10x6
  :value: 0x93B9  

.. data:: ASTC_10x8
  :value: 0x93BA  

.. data:: ASTC_10x10
  :value: 0x93BB  

.. data:: ASTC_12x10
  :value: 0x93BC  

.. data:: ASTC_12x12
  :value: 0x93BD  

.. data:: NEAREST
  :value: 0

.. data:: BILINEAR
  :value: 1

.. data:: BORDER
  :value: 0

.. data:: REPEAT
  :value: 1

.. data:: KEEP
  :value: 1

.. data:: REPLACE
  :value: 2

.. data:: INCR
  :value: 3

.. data:: DECR
  :value: 4

.. data:: INVERT
  :value: 5

.. data:: ZERO
  :value: 0

.. data:: ONE
  :value: 1

.. data:: SRC_ALPHA
  :value: 2

.. data:: DST_ALPHA
  :value: 3

.. data:: ONE_MINUS_SRC_ALPHA
  :value: 4

.. data:: ONE_MINUS_DST_ALPHA
  :value: 5

.. data:: BITMAPS
  :value: 1

.. data:: POINTS
  :value: 2

.. data:: LINES
  :value: 3

.. data:: LINE_STRIP
  :value: 4

.. data:: EDGE_STRIP_R
  :value: 5

.. data:: EDGE_STRIP_L
  :value: 6

.. data:: EDGE_STRIP_A
  :value: 7

.. data:: EDGE_STRIP_B
  :value: 8

.. data:: RECTS
  :value: 9

.. data:: OPT_MONO
  :value: 1

.. data:: OPT_NODL
  :value: 2

.. data:: OPT_FLAT
  :value: 256

.. data:: OPT_CENTERX
  :value: 512

.. data:: OPT_CENTERY
  :value: 1024

.. data:: OPT_CENTER
  :value: 1536

.. data:: OPT_NOBACK
  :value: 4096

.. data:: OPT_NOTICKS
  :value: 8192

.. data:: OPT_NOHM
  :value: 16384

.. data:: OPT_NOPOINTER
  :value: 16384

.. data:: OPT_NOSECS
  :value: 32768

.. data:: OPT_NOHANDS
  :value: 49152

.. data:: OPT_RIGHTX
  :value: 2048

.. data:: OPT_SIGNED
  :value: 256

.. data:: OPT_FULLSCREEN
  :value: 8

.. data:: OPT_MEDIAFIFO
  :value: 16

.. data:: OPT_FORMAT
  :value: 4096    

.. data:: OPT_FILL
  :value: 8192    

.. data:: LINEAR_SAMPLES
  :value: 0

.. data:: ULAW_SAMPLES
  :value: 1

.. data:: ADPCM_SAMPLES
  :value: 2

.. data:: HARP
  :value: 0x40    

.. data:: XYLOPHONE
  :value: 0x41

.. data:: TUBA
  :value: 0x42

.. data:: GLOCKENSPIEL
  :value: 0x43

.. data:: ORGAN
  :value: 0x44

.. data:: TRUMPET
  :value: 0x45

.. data:: PIANO
  :value: 0x46

.. data:: CHIMES
  :value: 0x47

.. data:: MUSICBOX
  :value: 0x48

.. data:: BELL
  :value: 0x49

.. data:: CLICK
  :value: 0x50    

.. data:: SWITCH
  :value: 0x51

.. data:: COWBELL
  :value: 0x52

.. data:: NOTCH
  :value: 0x53

.. data:: HIHAT
  :value: 0x54

.. data:: KICKDRUM
  :value: 0x55

.. data:: POP
  :value: 0x56

.. data:: CLACK
  :value: 0x57

.. data:: CHACK
  :value: 0x58

.. data:: MUTE
  :value: 0x60    

.. data:: UNMUTE
  :value: 0x61

.. data:: RAM_CMD
  :value: 0x308000

.. data:: RAM_DL
  :value: 0x300000

.. data:: REG_CLOCK
  :value: 0x302008

.. data:: REG_CMDB_SPACE
  :value: 0x302574

.. data:: REG_CMDB_WRITE
  :value: 0x302578

.. data:: REG_CMD_DL
  :value: 0x302100

.. data:: REG_CMD_READ
  :value: 0x3020f8

.. data:: REG_CMD_WRITE
  :value: 0x3020fc

.. data:: REG_CPURESET
  :value: 0x302020

.. data:: REG_CSPREAD
  :value: 0x302068

.. data:: REG_DITHER
  :value: 0x302060

.. data:: REG_DLSWAP
  :value: 0x302054

.. data:: REG_FRAMES
  :value: 0x302004

.. data:: REG_FREQUENCY
  :value: 0x30200c

.. data:: REG_GPIO
  :value: 0x302094

.. data:: REG_GPIO_DIR
  :value: 0x302090

.. data:: REG_HCYCLE
  :value: 0x30202c

.. data:: REG_HOFFSET
  :value: 0x302030

.. data:: REG_HSIZE
  :value: 0x302034

.. data:: REG_HSYNC0
  :value: 0x302038

.. data:: REG_HSYNC1
  :value: 0x30203c

.. data:: REG_ID
  :value: 0x302000

.. data:: REG_INT_EN
  :value: 0x3020ac

.. data:: REG_INT_FLAGS
  :value: 0x3020a8

.. data:: REG_INT_MASK
  :value: 0x3020b0

.. data:: REG_MACRO_0
  :value: 0x3020d8

.. data:: REG_MACRO_1
  :value: 0x3020dc

.. data:: REG_OUTBITS
  :value: 0x30205c

.. data:: REG_PCLK
  :value: 0x302070

.. data:: REG_PCLK_POL
  :value: 0x30206c

.. data:: REG_PLAY
  :value: 0x30208c

.. data:: REG_PLAYBACK_FORMAT
  :value: 0x3020c4

.. data:: REG_PLAYBACK_FREQ
  :value: 0x3020c0

.. data:: REG_PLAYBACK_LENGTH
  :value: 0x3020b8

.. data:: REG_PLAYBACK_LOOP
  :value: 0x3020c8

.. data:: REG_PLAYBACK_PLAY
  :value: 0x3020cc

.. data:: REG_PLAYBACK_READPTR
  :value: 0x3020bc

.. data:: REG_PLAYBACK_START
  :value: 0x3020b4

.. data:: REG_PWM_DUTY
  :value: 0x3020d4

.. data:: REG_PWM_HZ
  :value: 0x3020d0

.. data:: REG_ROTATE
  :value: 0x302058

.. data:: REG_SOUND
  :value: 0x302088

.. data:: REG_SWIZZLE
  :value: 0x302064

.. data:: REG_TAG
  :value: 0x30207c

.. data:: REG_TAG_X
  :value: 0x302074

.. data:: REG_TAG_Y
  :value: 0x302078

.. data:: REG_TAP_CRC
  :value: 0x302024

.. data:: REG_TOUCH_ADC_MODE
  :value: 0x302108

.. data:: REG_TOUCH_CHARGE
  :value: 0x30210c

.. data:: REG_TOUCH_DIRECT_XY
  :value: 0x30218c

.. data:: REG_TOUCH_DIRECT_Z1Z2
  :value: 0x302190

.. data:: REG_TOUCH_MODE
  :value: 0x302104

.. data:: REG_TOUCH_OVERSAMPLE
  :value: 0x302114

.. data:: REG_TOUCH_RAW_XY
  :value: 0x30211c

.. data:: REG_TOUCH_RZ
  :value: 0x302120

.. data:: REG_TOUCH_RZTHRESH
  :value: 0x302118

.. data:: REG_TOUCH_SCREEN_XY
  :value: 0x302124

.. data:: REG_TOUCH_SETTLE
  :value: 0x302110

.. data:: REG_TOUCH_TAG
  :value: 0x30212c

.. data:: REG_TOUCH_TAG_XY
  :value: 0x302128

.. data:: REG_TOUCH_TRANSFORM_A
  :value: 0x302150

.. data:: REG_TOUCH_TRANSFORM_B
  :value: 0x302154

.. data:: REG_TOUCH_TRANSFORM_C
  :value: 0x302158

.. data:: REG_TOUCH_TRANSFORM_D
  :value: 0x30215c

.. data:: REG_TOUCH_TRANSFORM_E
  :value: 0x302160

.. data:: REG_TOUCH_TRANSFORM_F
  :value: 0x302164

.. data:: REG_TRACKER
  :value: 0x309000

.. data:: REG_TRIM
  :value: 0x302180

.. data:: REG_VCYCLE
  :value: 0x302040

.. data:: REG_VOFFSET
  :value: 0x302044

.. data:: REG_VOL_PB
  :value: 0x302080

.. data:: REG_VOL_SOUND
  :value: 0x302084

.. data:: REG_VSIZE
  :value: 0x302048

.. data:: REG_VSYNC0
  :value: 0x30204c

.. data:: REG_VSYNC1
  :value: 0x302050

.. data:: REG_MEDIAFIFO_BASE
  :value: 0x30901c 

.. data:: REG_MEDIAFIFO_READ
  :value: 0x309014 

.. data:: REG_MEDIAFIFO_SIZE
  :value: 0x309020 

.. data:: REG_MEDIAFIFO_WRITE
  :value: 0x309018 

.. data:: REG_GPIOX
  :value: 0x30209c

.. data:: REG_GPIOX_DIR
  :value: 0x302098

.. data:: REG_FLASH_SIZE
  :value: 0x309024 

.. data:: REG_FLASH_STATUS
  :value: 0x3025f0 

.. data:: REG_ADAPTIVE_FRAMERATE
  :value: 0x30257c 


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
