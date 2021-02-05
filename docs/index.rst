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

      Valid primitives are ``BITMAPS``, ``POINTS``, ``LINES``, ``LINE_STRIP``, ``EDGE_STRIP_R``, ``EDGE_STRIP_L``, ``EDGE_STRIP_A``, ``EDGE_STRIP_B`` and ``RECTS``.

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


.. autofunction:: bteve.align4

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
