bteve documentation
===================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. highlight:: python

``bteve`` is a Python driver for BridgeTek's EVE series GPUs.
In particular it supports the `Gameduino 3X <https://gameduino.com>`_ series of display adapters.

It supports:

* Python running on Windows/MacOS/Linux, connected via a :class:`~spi:spidriver.SPIDriver` to the Gameduino or BT81x
* CircuitPython on an embedded board, including

    * Adafruit M4 Metro and Feather
    * Adafruit Metro M4
    * Teensy 4.x
    * Raspberry Pi Pico

.. literalinclude:: ../examples/helloworld.py

.. image:: /images/helloworld.png

.. literalinclude:: ../examples/fizz.py

.. image:: /images/fizz.png

Module classes
==============

Gameduino
---------

The Gameduino class is a specialization of the base class :class:`EVE`.

.. class:: Gameduino([d])

  :param spidriver d: when running on a PC, a SPIDriver object for communicating with the EVE hardware
  
  .. method:: init()

      Initialize the EVE hardware.
      Confirm that the BT81x is running, configure it for the attached screen, and render a blank frame.

      On CircuitPython this method uses :mod:`cpy:sdcardio` to attach to the GD3X microSD card as
      ``"/sd/"``, so any files on the card can be accessed with the prefix ``"/sd/"``.

  .. data:: w

      Width of the display, in pixels. Available after calling :meth:`init`.

  .. data:: h

      Height of the display, in pixels. Available after calling :meth:`init`.

  .. method:: rd(a, n)

      Read directly from EVE memory
 
      :param int a: address in EVE memory
      :param int n: number of bytes to read
      :return bytes: memory contents

  .. method:: wr(a, bb)

      Write directly to EVE memory
 
      :param int a: address in EVE memory
      :param bytes bb: bytes to write

  .. method:: rd32(a)

      Read a 32-bit value from EVE memory
      :param int a: address in EVE memory
      :returns int: memory contents

  .. method:: wr32(a, v)

      Write a 32-bit value to EVE memory
 
      :param int a: address in EVE memory
      :param int v: value to write

  .. method:: is_finished()

      Returns True if the EVE command FIFO is empty

      :returns bool: True if the EVE command FIFO is empty

      This method is the non-blocking equivalent of
      :meth:`EVE.finish`.

  .. method:: result(n = 1)

      :returns int: result field

      Return the result field of the most recent command, if any.

EVE
---

This class provides all graphics drawing operations,
graphics state operations, and graphics commands.

Methods for simple drawing and drawing state:

 * :meth:`~EVE.Begin`
 * :meth:`~EVE.Vertex2f`
 * :meth:`~EVE.LineWidth`
 * :meth:`~EVE.PointSize`
 * :meth:`~EVE.BitmapHandle`
 * :meth:`~EVE.Cell`
 * :meth:`~EVE.ColorRGB`
 * :meth:`~EVE.ColorA`
 * :meth:`~EVE.End`
 * :meth:`~EVE.Vertex2ii`

Methods for clearing the screen:

 * :meth:`~EVE.ClearColorA`
 * :meth:`~EVE.ClearColorRGB`
 * :meth:`~EVE.Clear`

Methods to set the 2D scissor clipping rectangle:

 * :meth:`~EVE.ScissorSize`
 * :meth:`~EVE.ScissorXY`

Methods to set the tag state, so that touch events can be attached to screen objects:

 * :meth:`~EVE.ClearTag`
 * :meth:`~EVE.TagMask`
 * :meth:`~EVE.Tag`

Methods to preserve and restore the graphics state:

 * :meth:`~EVE.RestoreContext`
 * :meth:`~EVE.SaveContext`

Methods to control rendering and display:

 * :meth:`~EVE.swap`
 * :meth:`~EVE.flush`
 * :meth:`~EVE.finish`

Methods to set the alpha blend state, allowing more advanced transparency and compositing operations:

 * :meth:`~EVE.AlphaFunc`
 * :meth:`~EVE.BlendFunc`
 * :meth:`~EVE.ColorMask`

Methods to set the stencil state, allowing conditional drawing and other logial operations:

 * :meth:`~EVE.ClearStencil`
 * :meth:`~EVE.StencilFunc`
 * :meth:`~EVE.StencilMask`
 * :meth:`~EVE.StencilOp`

Low-level methods to set the bitmap format
(See :meth:`~EVE.cmd_setbitmap` for a higher-level alternative.):

 * :meth:`~EVE.BitmapExtFormat`
 * :meth:`~EVE.BitmapLayoutH`
 * :meth:`~EVE.BitmapLayout`
 * :meth:`~EVE.BitmapSizeH`
 * :meth:`~EVE.BitmapSize`
 * :meth:`~EVE.BitmapSource`
 * :meth:`~EVE.BitmapSwizzle`
 * :meth:`~EVE.PaletteSource`

Low-level methods set the bitmap transform matrix
(See :meth:`~EVE.cmd_scale`, :meth:`cmd_translate`, :meth:`cmd_setmatrix` etc. for a higher-level alternative.):

 * :meth:`~EVE.BitmapTransformA`
 * :meth:`~EVE.BitmapTransformB`
 * :meth:`~EVE.BitmapTransformC`
 * :meth:`~EVE.BitmapTransformD`
 * :meth:`~EVE.BitmapTransformE`
 * :meth:`~EVE.BitmapTransformF`
 * :meth:`~EVE.Macro`

Methods to set the precision and offset used by :meth:`Vertex2f`:

 * :meth:`VertexTranslateX`
 * :meth:`VertexTranslateY`
 * :meth:`VertexFormat`

.. class:: EVE

  .. method:: AlphaFunc(func, ref) 

      Set the alpha test function

      :param int func: specifies the test function, one of :data:`NEVER`, :data:`LESS`, :data:`LEQUAL`, :data:`GREATER`, :data:`GEQUAL`, :data:`EQUAL`, :data:`NOTEQUAL`, or :data:`ALWAYS`. Range 0-7. The initial value is ALWAYS(7)
      :param int ref: specifies the reference value for the alpha test. Range 0-255. The initial value is 0

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: Begin(prim) 

      Begin drawing a graphics primitive

      :param int prim: graphics primitive.

      Valid primitives are :data:`BITMAPS`, :data:`POINTS`, :data:`LINES`, :data:`LINE_STRIP`, :data:`EDGE_STRIP_R`, :data:`EDGE_STRIP_L`, :data:`EDGE_STRIP_A`, :data:`EDGE_STRIP_B` and :data:`RECTS`.

      .. include:: gen/example-Begin.rst

  .. method:: BitmapExtFormat(format) 

      Set the bitmap format

      :param int format: bitmap pixel format.

  .. method:: BitmapHandle(handle) 

      Set the bitmap handle

      :param int handle: bitmap handle. Range 0-31. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: BitmapLayout(format, linestride, height) 

      Set the source bitmap memory format and layout for the current handle

      :param int format: bitmap pixel format, or GLFORMAT to use BITMAP_EXT_FORMAT instead. Range 0-31
      :param int linestride: bitmap line stride, in bytes. Range 0-1023
      :param int height: bitmap height, in lines. Range 0-511

  .. method:: BitmapLayoutH(linestride, height) 

      Set the source bitmap memory format and layout for the current handle. high bits for large bitmaps

      :param int linestride: high part of bitmap line stride, in bytes. Range 0-7
      :param int height: high part of bitmap height, in lines. Range 0-3

  .. method:: BitmapSize(filter, wrapx, wrapy, width, height) 

      Set the screen drawing of bitmaps for the current handle

      :param int filter: bitmap filtering mode, one of :data:`NEAREST` or :data:`BILINEAR`.
      :param int wrapx: bitmap :math:`x` wrap mode, one of :data:`REPEAT` or :data:`BORDER`.
      :param int wrapy: bitmap :math:`y` wrap mode, one of :data:`REPEAT` or :data:`BORDER`.
      :param int width: drawn bitmap width, in pixels. Range 0-511
      :param int height: drawn bitmap height, in pixels. Range 0-511

  .. method:: BitmapSizeH(width, height) 

      Set the screen drawing of bitmaps for the current handle. high bits for large bitmaps

      :param int width: high part of drawn bitmap width, in pixels. Range 0-3
      :param int height: high part of drawn bitmap height, in pixels. Range 0-3

  .. method:: BitmapSource(addr) 

      Set the source address for bitmap graphics

      :param int addr: Bitmap start address, pixel-aligned. May be in SRAM or flash. Range 0-16777215

  .. method:: BitmapSwizzle(r, g, b, a) 

      Set the source for the r,g,b and a channels of a bitmap

      :param int r: red component source
      :param int g: green component source
      :param int b: blue component source
      :param int a: alpha component source

      The source parameter may be one of:

      * :data:`ZERO` constant zero
      * :data:`ONE` constant one
      * :data:`RED` source bitmap red
      * :data:`GREEN` source bitmap green
      * :data:`BLUE` source bitmap blue
      * :data:`ALPHA` source bitmap alpha

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

      :param int src: specifies how the source blending factor is computed.  One of :data:`ZERO`, :data:`ONE`, :data:`SRC_ALPHA`, :data:`DST_ALPHA`, :data:`ONE_MINUS_SRC_ALPHA` or :data:`ONE_MINUS_DST_ALPHA`. The initial value is SRC_ALPHA
      :param int dst: specifies how the destination blending factor is computed, one of the same constants as **src**. The initial value is ONE_MINUS_SRC_ALPHA

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

      .. include:: gen/example-BlendFunc.rst

  .. method:: Cell(cell) 

      Set the bitmap cell number used by :meth:`Vertex2f` when drawing :data:`BITMAPS`.

      :param int cell: bitmap cell number. Range 0-127. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

      .. include:: gen/example-Cell.rst

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

      .. include:: gen/example-ClearColorRGB.rst

  .. method:: Clear(c = 1, s = 1, t = 1) 

      Clear buffers to preset values

      :param int c: clear color buffer. Range 0-1
      :param int s: clear stencil buffer. Range 0-1
      :param int t: clear tag buffer. Range 0-1

      .. include:: gen/example-Clear.rst

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

      .. include:: gen/example-ColorA.rst

  .. method:: ColorMask(r, g, b, a) 

      Enable and disable writing of frame buffer color components

      :param int r: allow updates to the frame buffer red component. Range 0-1. The initial value is 1
      :param int g: allow updates to the frame buffer green component. Range 0-1. The initial value is 1
      :param int b: allow updates to the frame buffer blue component. Range 0-1. The initial value is 1
      :param int a: allow updates to the frame buffer alpha component. Range 0-1. The initial value is 1

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

      .. include:: gen/example-ColorMask.rst

  .. method:: ColorRGB(red, green, blue) 

      Set the drawing color

      :param int red: red value for the current color. Range 0-255. The initial value is 255
      :param int green: green for the current color. Range 0-255. The initial value is 255
      :param int blue: blue for the current color. Range 0-255. The initial value is 255

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

      .. include:: gen/example-ColorRGB.rst

  .. method:: End() 

      End drawing a graphics primitive

      :meth:`Vertex2ii` and :meth:`Vertex2f` calls are ignored until the next :meth:`Begin`.

  .. method:: LineWidth(width) 

      Set the width of rasterized lines

      :param float width: line width in pixels. Range 0-511. The initial value is 1

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

      .. include:: gen/example-LineWidth.rst

  .. method:: Macro(m) 

      Execute a single command from a macro register

      :param int m: macro register to read. Range 0-1

  .. method:: Nop() 

      No operation

  .. method:: PaletteSource(addr) 

      Set the base address of the palette

      :param int addr: Address in graphics SRAM, 2-byte aligned. Range 0-4194303. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: PointSize(size) 

      Set the diameter of rasterized points

      :param float size: point diameter in pixels. Range 0-1023. The initial value is 1

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

      .. include:: gen/example-PointSize.rst

  .. method:: RestoreContext() 

      Restore the current graphics context from the context stack

  .. method:: SaveContext() 

      Push the current graphics context on the context stack.
      The hardware's graphics context stack is 4 levels deep.

      .. include:: gen/example-SaveContext.rst

  .. method:: ScissorSize(width, height) 

      Set the size of the scissor clip rectangle

      :param int width: The width of the scissor clip rectangle, in pixels. Range 0-4095. The initial value is hsize
      :param int height: The height of the scissor clip rectangle, in pixels. Range 0-4095. The initial value is 2048

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

      .. include:: gen/example-ScissorSize.rst

  .. method:: ScissorXY(x, y) 

      Set the top left corner of the scissor clip rectangle

      :param int x: The :math:`x` coordinate of the scissor clip rectangle, in pixels. Range 0-2047. The initial value is 0
      :param int y: The :math:`y` coordinate of the scissor clip rectangle, in pixels. Range 0-2047. The initial value is 0

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: StencilFunc(func, ref, mask) 

      Set function and reference value for stencil testing

      :param int func: specifies the test function, one of :data:`NEVER`, :data:`LESS`, :data:`LEQUAL`, :data:`GREATER`, :data:`GEQUAL`, :data:`EQUAL`, :data:`NOTEQUAL`, or :data:`ALWAYS`. The initial value is ALWAYS
      :param int ref: specifies the reference value for the stencil test. Range 0-255. The initial value is 0
      :param int mask: specifies a mask that is ANDed with the reference value and the stored stencil value. Range 0-255. The initial value is 255

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: StencilMask(mask) 

      Control the writing of individual bits in the stencil planes

      :param int mask: the mask used to enable writing stencil bits. Range 0-255. The initial value is 255

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: StencilOp(sfail, spass) 

      Set stencil test actions

      :param int sfail: specifies the action to take when the stencil test fails, one of :data:`KEEP`, :data:`ZERO`, :data:`REPLACE`, :data:`INCR`, :data:`INCR_WRAP`, :data:`DECR`, :data:`DECR_WRAP`, and :data:`INVERT`. The initial value is KEEP
      :param int spass: specifies the action to take when the stencil test passes, one of the same constants as **sfail**. The initial value is KEEP

      These values are part of the graphics context and are saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

      .. include:: gen/example-StencilOp.rst

  .. method:: TagMask(mask) 

      Control the writing of the tag buffer

      :param int mask: allow updates to the tag buffer. Range 0-1. The initial value is 1

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: Tag(s) 

      Set the current tag value

      :param int s: tag value. Range 0-255. The initial value is 255

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: Vertex2f(x, y) 

      Draw a vertex.
      This operation draws a graphics primitive, depending on the primitive set by :meth:`Begin`.

      :param float x: pixel x-coordinate
      :param float y: pixel y-coordinate

  .. method:: Vertex2ii(x, y, handle, cell) 

      Draw a vertex.

      :param int x: x-coordinate in pixels. Range 0-511
      :param int y: y-coordinate in pixels. Range 0-511
      :param int handle: bitmap handle. Range 0-31
      :param int cell: cell number. Range 0-127

      This method is an alternative to :meth:`BitmapHandle`, :meth:`Cell` and :meth:`Vertex2f`.

  .. method:: VertexFormat(frac) 

      Set the precision of coordinates used by :meth:`Vertex2f`

      :param int frac: Number of fractional bits in X,Y coordinates. Range 0-7. The initial value is 4

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: VertexTranslateX(x) 

      Set the vertex transformation's x translation component

      :param float x: signed x-coordinate in pixels. Range ±4095. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  .. method:: VertexTranslateY(y) 

      Set the vertex transformation's y translation component

      :param float y: signed y-coordinate in pixels. Range ±4095. The initial value is 0

      This value is part of the graphics context and is saved and restored by :meth:`SaveContext` and :meth:`RestoreContext`.

  |

  .. method:: cmd_animdraw(ch)

      Draw an animation

      :param int ch: animation channel

  .. method:: cmd_animframe(x, y, aoptr, frame)

      Draw one animation frame

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int aoptr: animation object pointer
      :param int frame: description

  .. method:: cmd_animframeram(x, y, aoptr, frame)

      Draw one animation frame from RAM

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int aoptr: animation object pointer
      :param int frame: description

  .. method:: cmd_animstart(ch, aoptr, loop)

      Start an animation

      :param int ch: animation channel
      :param int aoptr: animation object pointer
      :param int loop: description

  .. method:: cmd_animstartram(ch, aoptr, loop)

      Start an animation from RAM

      :param int ch: animation channel
      :param int aoptr: animation object pointer
      :param int loop: description

  .. method:: cmd_animstop(ch)

      Stop playing an animation

      :param int ch: animation channel

  .. method:: cmd_animxy(ch, x, y)

      Play an animation

      :param int ch: animation channel
      :param int x: x-coordinate
      :param int y: y-coordinate

  .. method:: cmd_apilevel(level)

      Set the API level

      :param int level: API level, 0 or 1.

      API levelel. 0 is strict BT815 compatible, 1 is BT817.

      .. note:: 817 only

  .. method:: cmd_append(ptr, num)

      Append main memory to the current display list

      :param int ptr: address in EVE memory, 32-bit aligned
      :param int num: byte count, 32-bit aligned

      Executes **num** bytes of drawing commands from graphics memory at
      **ptr**.  This can be useful for using graphics memory as a cache
      for frequently used drawing sequences, much like OpenGL's display lists.

  .. method:: cmd_appendf(ptr, num)

      Append from flash to the current display list

      :param int ptr: description
      :param int num: description

  .. method:: cmd_bgcolor(c)

      Sets the widget background color

      :param int c: RGB color

  .. method:: cmd_bitmap_transform(x0, y0, x1, y1, x2, y2, tx0, ty0, tx1, ty1, tx2, ty2, result)

      Computes an arbitrary bitmap transform

      :param x0 int:  point 0 screen x-coordinate
      :param y0 int:  point 0 screen y-coordinate
      :param x1 int:  point 1 screen x-coordinate
      :param y1 int:  point 1 screen y-coordinate
      :param x2 int:  point 2 screen x-coordinate
      :param y2 int:  point 2 screen y-coordinate
      :param tx0 int: point 0 bitmap x-coordinate
      :param ty0 int: point 0 bitmap y-coordinate
      :param tx1 int: point 1 bitmap x-coordinate
      :param ty1 int: point 1 bitmap y-coordinate
      :param tx2 int: point 2 bitmap x-coordinate
      :param ty2 int: point 2 bitmap y-coordinate
      :param int result: return code. Set to -1 on success.

  .. method:: cmd_button(x, y, w, h, font, options, s)

      Draw a button with a text label

      :param int x: button top left x
      :param int y: button top left y
      :param int w: button width in pixels
      :param int h: button height in pixels
      :param int font: font for label, 0-31
      :param int options: rendering options, see below
      :param str s: label text

      The ``button`` command
      draws a button widget at screen (``x``, ``y``) with pixel size ``w`` x ``h``.
      ``label`` gives the text label.

      The label is drawn centered within the button rectangle. It may cross multiple lines, separated by newline characters.

      The following options may be logically-ored together:

      * :data:`OPT_FLAT` render the element without 3D decorations
      * :data:`OPT_FORMAT` use a printf-style format string
      * :data:`OPT_FILL` apply multi-line text fill, see :meth:`cmd_fillwidth`

      .. include:: gen/example-cmd_button.rst

  .. method:: cmd_calibrate(result)

      Start the touch-screen calibration process

      :param int result: result code. Set to -1 on success.

  .. method:: cmd_calibratesub(x, y, w, h, result)

      Start the touch-screen calibration process

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int w: width
      :param int h: height
      :param int result: result code. Set to -1 on success.

      .. note:: 817 only

  .. method:: cmd_calllist(a)

      Invoke a call list

      :param int a: call list pointer

      .. note:: 817 only

  .. method:: cmd_clearcache()

      Clear the bitmap cache

  .. method:: cmd_clock(x, y, r, options, h, m, s, ms)

      Draw a clock

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int r: description
      :param int options: see below
      :param int h: height
      :param int m: description
      :param int s: description
      :param int ms: description

      The following options may be logically-ored together:

      * :data:`OPT_FLAT` render the element without 3D decorations
      * :data:`OPT_NOBACK` do not draw the dial back
      * :data:`OPT_NOTICKS` do not draw tick marks
      * :data:`OPT_NOSECS` do not draw seconds hand
      * :data:`OPT_NOHM` do not draw hours and minutes hands

      .. include:: gen/example-cmd_clock.rst

  .. method:: cmd_coldstart()

      Reset all coprocessor state to its default values

  .. method:: cmd_crc(ptr)

      Compute a CRC-32 for the currently displayed image

      :param int ptr: address in EVE memory

      The 32-bit CRC is written to the given address.

  .. method:: cmd_dial(x, y, r, options, val)

      Draws a dial, a circular widget with a single mark

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int r: description
      :param int options: see below
      :param int val: value, 0-65535

      The following options may be logically-ored together:

      * :data:`OPT_FLAT` render the element without 3D decorations

      .. include:: gen/example-cmd_dial.rst

  .. method:: cmd_dlstart()

      Low-level command to start a new display list

  .. method:: cmd_endlist()

      End a call list

      .. note:: 817 only

  .. method:: cmd_fgcolor(c)

      Set the widget foreground color

      :param int c: 24-bit color

  .. method:: cmd_fillwidth(s)

      Set the fill width used for multi-line text widgets

      :param int s: fill width in pixels

  .. method:: cmd_flashattach()

      Attach to the flash

  .. method:: cmd_flashdetach()

      Detach from flash

  .. method:: cmd_flasherase()

      Perform a full-chip erase on the flash

  .. method:: cmd_flashfast(result)

      Enter fast mode

      :param int result: result code. 0 on success.

  .. method:: cmd_flashprogram(dest, src, num)

      Program flash from EVE memory

      :param int dest: destination address in flash memory
      :param int src: source address in EVE memory
      :param int num: number of bytes to program

  .. method:: cmd_flashread(dest, src, num)

      Read from flash

      :param int dest: destination address in EVE memory
      :param int src: source address in flash memory
      :param int num: number of bytes to read

  .. method:: cmd_flashsource(ptr)

      Set the flash source address for :meth:`cmd_videostartf`.

      :param int ptr: source address in flash memory

  .. method:: cmd_flashspidesel()

      Deselect the flash

  .. method:: cmd_flashspirx(ptr, num)

      Perform a raw SPI read from flash

      :param int ptr: destination address in EVE memory
      :param int num: number of bytes to read

  .. method:: cmd_flashspitx(num!)

      Perform a raw SPI write to flash

      :param num int: number of bytes to write

      This command is followed by the ``num`` bytes of inline data.

  .. method:: cmd_flashupdate(dest, src, num)

      Program flash from EVE memory

      :param int dest: destination address in flash memory
      :param int src: source address in EVE memory
      :param int num: number of bytes to program

  .. method:: cmd_flashwrite(ptr, num)

      Program flash from inline data

      :param int ptr: destination address in flash memory
      :param num int: number of bytes to program

      This command is followed by the ``num`` bytes of inline data.

  .. method:: cmd_fontcache(font, ptr, num)

      Set up a font cache

      :param int font: font number 0-31
      :param int ptr: start of font cache area
      :param int num: number of bytes to use for font cache

      .. note:: 817 only

  .. method:: cmd_fontcachequery(total, used)

      Return statistics on font cache usage

      :param int total:  Total number of available bitmaps in the cache
      :param int used: Number of used bitmaps in the cache

  .. method:: cmd_gauge(x, y, r, options, major, minor, val, range)

      Draw an indicator gauge

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int r: radius
      :param int options: see below
      :param int major: number of major tick marks
      :param int minor: number of minor tick marks
      :param int val: gauge value
      :param int range: range of gauge

      .. include:: gen/example-cmd_gauge.rst

  .. method:: cmd_getimage(source, fmt, w, h, palette)

       Returns all the attributes of the bitmap made by the previous
       :meth:`cmd_loadimage`,
       :meth:`cmd_playvideo`,
       :meth:`cmd_videostart` or
       :meth:`cmd_videostartf`.

      :param int source: description
      :param int fmt: description
      :param int w: width
      :param int h: height
      :param int palette: description

  .. method:: cmd_getmatrix(a, b, c, d, e, f)

      Returns the current bitmap transform matrix

      :param int a: matrix coefficient
      :param int b: matrix coefficient
      :param int c: matrix coefficient
      :param int d: matrix coefficient
      :param int e: matrix coefficient
      :param int f: matrix coefficient

      The matrix is returned as:

         \begin{bmatrix}
         a & b & c \\
         d & e & f \\
         \end{bmatrix}

  .. method:: cmd_getprops(ptr, w, h)

      Returns the parameters of the last loaded image

      :param int ptr: bitmap source address
      :param int w: width
      :param int h: height

  .. method:: cmd_getptr(result)

      Returns the first unallocated memory location

      :param int result: first unused address in EVE memory

  .. method:: cmd_gradcolor(c)

      set the 3D widget highlight color

      :param int c: a 24-bit color

  .. method:: cmd_gradient(x0, y0, rgb0, x1, y1, rgb1)

      Draw a smooth color gradient between two points

      :param x0 int: point 0 x-coordinate
      :param y0 int: point 0 y-coordinate
      :param rgb0 int: a 24-bit color for point 0
      :param x1 int: point 1 x-coordinate
      :param y1 int: point 1 y-coordinate
      :param rgb1 int: a 24-bit color for point 1

      .. include:: gen/example-cmd_gradient.rst

  .. method:: cmd_gradienta(x0, y0, argb0, x1, y1, argb1)

      Draw a smooth color gradient between two points with alpha transparency

      :param x0 int: point 0 x-coordinate
      :param y0 int: point 0 y-coordinate
      :param argb0 int: a 32-bit color for point 0
      :param x1 int: point 1 x-coordinate
      :param y1 int: point 1 y-coordinate
      :param argb1 int: a 32-bit color for point 1

  .. method:: cmd_hsf(w)

      Configure the horizontal scanout filter

      :param int w: width in pixels

      .. note:: 817 only

  .. method:: cmd_inflate(ptr)

      Decompress data into EVE memory

      :param ptr int: destination pointer in EVE memory

  .. method:: cmd_inflate2(ptr, options!)

      Decompress data into EVE memory

      :param int ptr: destination pointer in EVE memory
      :param options! int: options

  .. method:: cmd_interrupt(ms)

      Trigger an interrupt

      :param int ms: delay before triggering interrupt in milliseconds

  .. method:: cmd_keys(x, y, w, h, font, options, s)

      Draw a row of keys

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int w: width
      :param int h: height
      :param int font: font number 0-31
      :param int options: see below
      :param str s: key labels

      .. include:: gen/example-cmd_keys.rst

  .. method:: cmd_loadidentity()

      Set the current bitmap transform matrix to the identity:

      .. math::

         \begin{bmatrix}
         1 & 0 & 0 \\
         0 & 1 & 0 \\
         \end{bmatrix}


  .. method:: cmd_loadimage(ptr, options!)

      Load an image into a bitmap

      :param int ptr: destination address in EVE memory
      :param options int: options

      This command is followed by the image data itself.
      Images may be in JPG or PNG format.

      .. include:: gen/example-cmd_loadimage.rst

  .. method:: cmd_logo()

      Display the BridgeTek logo.

  .. method:: cmd_mediafifo(ptr, size)

      Set the memory region used for the media FIFO

      :param int ptr: start address in EVE memory
      :param int size: size of the media FIFO in bytes

  .. method:: cmd_memcpy(dest, src, num)

      Copy EVE memory

      :param int dest: destination address in EVE memory
      :param int src: source address in EVE memory
      :param int num: number of bytes to copy

  .. method:: cmd_memcrc(ptr, num, result)

      Compute the CRC-32 of a region of EVE memory

      :param int ptr: start address in EVE memory
      :param int num: size of region in bytes
      :param int result: address to write destination CRC in EVE memory

  .. method:: cmd_memset(ptr, value, num)

      Set a region of EVE memory to a byte value

      :param int ptr: destination address in EVE memory
      :param int value: byte value
      :param int num: size of region in bytes

  .. method:: cmd_memwrite(ptr, num)

      Write the following inline data into EVE memory

      :param int ptr: destination address in EVE memory
      :param num int: number of bytes to write

      This command is followed by the inline data, and is padded to a 4-byte boundary.
      See :meth:`cc` and :func:`align4`.

  .. method:: cmd_memzero(ptr, num)

      Set a region of EVE memory to zero

      :param int ptr: destination address in EVE memory
      :param int num: size of region in bytes

  .. method:: cmd_newlist(a)

      Start compiling a call list

      :param int a: call list pointer

      .. note:: 817 only

  .. method:: cmd_nop()

      No operation.

  .. method:: cmd_number(x, y, font, options, n)

      Draw a number

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int font: font number 0-31
      :param int options: see below
      :param int n: number

      renders a number ``n`` in font ``font``
      at screen (``x``, ``y``).
      If an integer :math:`n` is supplied as an option,
      then leading zeroes are added so that :math:`n` digits are always drawn.

      The following options may be logically-ored together:

      * :data:`OPT_CENTER` shorthand for (:data:`OPT_CENTERX` | :data:`OPT_CENTERY`)
      * :data:`OPT_CENTERX` center element in the x direction
      * :data:`OPT_CENTERY` center element in the y direction
      * :data:`OPT_SIGNED` treat paramter ``n`` as signed. The default is unsigned
      * 0-32 draw the number so that :math:`n` digits are always drawn

      See also :meth:`cmd_setbase`

      .. include:: gen/example-cmd_number.rst

  .. method:: cmd_pclkfreq(ftarget, rounding, factual)

      Set the PCLK frequency

      :param int ftarget: target frequency, in Hz
      :param int rounding: rounding mode
      :param int factual: return value, actual frequency

      .. note:: 817 only

  .. method:: cmd_playvideo(options!)

      Play a video from inline video data

      :param options int: playback options

  .. method:: cmd_progress(x, y, w, h, options, val, range)

      Draw a progress bar

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int w: width
      :param int h: height
      :param int options: see below
      :param int val: progress bar value
      :param int range: progress bar range

      .. include:: gen/example-cmd_progress.rst

      The following options may be logically-ored together:

      * :data:`OPT_FLAT` render the element without 3D decorations

  .. method:: cmd_regread(ptr, result)

      Reads a 32-bit value from EVE memory

      :param int ptr: source address in EVE memory
      :param int result: register value

  .. method:: cmd_regwrite(ptr, val)

      Writes a 32-bit value to EVE memory

      :param int ptr: address in EVE memory
      :param int val: 32-bit value

  .. method:: cmd_resetfonts()

      Reset all ROM fonts (numbers 16-31) to their default settings

  .. method:: cmd_return()

      Return from a Call List

      .. note:: 817 only

  .. method:: cmd_romfont(font, romslot)

      Load a ROM font into a font handle

      :param int font: font number 0-31
      :param int romslot: ROM font number 16-34

  .. method:: cmd_rotate(a)

      Apply a rotation to the bitmap transform matrix

      :param float a: clockwise rotation angle, in degrees

  .. method:: cmd_rotatearound(x, y, a, s)

      Apply a rotation and scale to the bitmap transform matrix around a given point

      :param int x: center of rotation x-coordinate
      :param int y: center of rotation y-coordinate
      :param float a: clockwise rotation angle, in degrees
      :param float s: scale factor

  .. method:: cmd_runanim(waitmask, play)

      Run all active animations

      :param int waitmask: description
      :param int play: y-coordinate

      .. note:: 817 only

  .. method:: cmd_scale(sx, sy)

      Apply a scale to the bitmap transform matrix

      :param float sx: x-axis scale factor
      :param float sy: y-axis scale factor

  .. method:: cmd_screensaver()

      Run the screen-saver function. Use :meth:`cmd_stop` to stop it.

  .. method:: cmd_scrollbar(x, y, w, h, options, val, size, range)

      Draw a scroll bar

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int w: width
      :param int h: height
      :param int options: see below
      :param int val: bar starting position
      :param int size: bar size
      :param int range: range of entire bar

      The following options may be logically-ored together:

      * :data:`OPT_FLAT` render the element without 3D decorations

      .. include:: gen/example-cmd_scrollbar.rst

  .. method:: cmd_setbase(b)

      Set the base used by :math:`cmd_number`. The default base is 10 (decimal)

      :param int b: base, 1-36

  .. method:: cmd_setbitmap(source, fmt, w, h)

      Set all the parameters for a bitmap.

      :param int source: bitmap source address in EVE memory
      :param int fmt: bitmap format, see :ref:`formats`
      :param int w: width
      :param int h: height

  .. method:: cmd_setfont(font, ptr)

      Load a font slot from a font in RAM

      :param int font: font number 0-31
      :param int ptr: address to the font register value

  .. method:: cmd_setfont2(font, ptr, firstchar)

      Load a font slot from a font in RAM

      :param int font: font number 0-31
      :param int ptr: address of the font descriptor block in EVE memory
      :param int firstchar: first valid character in font

  .. method:: cmd_setmatrix()

      Append the current transform matrix to the display list.

  .. method:: cmd_setrotate(r)

      Change screen orientation by setting
      :data:`REG_ROTATE` and adjusting the touch transform matrix.

      :param int r: new orientation

  .. method:: cmd_setscratch(handle)

      Set the bitmap handle used for widget drawing.
      The default handle is 15.

      :param int handle: bitmap handle

  .. method:: cmd_sketch(x, y, w, h, ptr, format)

      Begin sketching.
      Use :meth:`cmd_stop` to stop it.

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int w: width
      :param int h: height
      :param int ptr: bitmap start address
      :param int format: either :data:`L1` or :data:`L8`

  .. method:: cmd_slider(x, y, w, h, options, val, range)

      Draw a slider

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int w: width
      :param int h: height
      :param int options: see below
      :param int val: position of slider knob
      :param int range: range of entire slider

      The following options may be logically-ored together:

      * :data:`OPT_FLAT` render the element without 3D decorations

      .. include:: gen/example-cmd_slider.rst

  .. method:: cmd_snapshot(ptr)

      Write a snapshot of the current screen as a bitmap

      :param int ptr: destination bitmap address in EVE memory

  .. method:: cmd_snapshot2(fmt, ptr, x, y, w, h)

      Write a snapshot of the current screen as a bitmap

      :param int fmt: bitmap format
      :param int ptr: destination bitmap address in EVE memory
      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int w: width of snapshot rectangle
      :param int h: height of snapshot rectangle

  .. method:: cmd_spinner(x, y, style, scale)

      Display a "waiting" spinner
      Use :meth:`cmd_stop` to stop it.

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int style: see below
      :param int scale: element size. 0 is small, 1 medium, 2 huge.

      There are four spinner styles available:

      * ``0`` circular
      * ``1`` linear
      * ``2`` clock
      * ``3`` rotating disks

      .. include:: gen/example-cmd_spinner.rst

  .. method:: cmd_stop()

      Stop any currently running background tasks.


  .. method:: cmd_swap()

      Low-level command to swap the display lists

  .. method:: cmd_sync()

      Delay execution until the next vertical blanking interval

  .. method:: cmd_testcard()

      Draw a diagnostic test-card

      .. note:: 817 only

  .. method:: cmd_text(x, y, font, options, s)

      Draws text

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int font: font number 0-31
      :param int options: see below
      :param str s: text

      renders a number ``n`` in font ``font``
      at screen (``x``, ``y``).

      The following options may be logically-ored together:

      * :data:`OPT_CENTER` shorthand for (:data:`OPT_CENTERX` | :data:`OPT_CENTERY`)
      * :data:`OPT_CENTERX` center element in the x direction
      * :data:`OPT_CENTERY` center element in the y direction
      * :data:`OPT_RIGHTX` right-justify the element
      * :data:`OPT_FILL` apply multi-line text fill, see :meth:`cmd_fillwidth`
      * :data:`OPT_FORMAT` use a printf-style format string

      .. include:: gen/example-cmd_text.rst

  .. method:: cmd_toggle(x, y, w, font, options, state, s1, s0)

      Draws a toggle widget

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int w: width
      :param int font: font number 0-31
      :param int options: see below
      :param int state: toggle position 0-65535
      :param str s1: label for right side
      :param str s0: label for left side

      .. include:: gen/example-cmd_toggle.rst

      The following options may be logically-ored together:

      * :data:`OPT_FLAT` render the element without 3D decorations
      * :data:`OPT_FORMAT` use a printf-style format string

  .. method:: cmd_track(x, y, w, h, tag)

      Start tracking touches for a graphical object

      :param int x: x-coordinate
      :param int y: y-coordinate
      :param int w: width
      :param int h: height
      :param int tag: object tag number 0-255

      Up to 255 objects may be tracked.
      Each object may be either linear (if either ``width`` or ``height`` is 1)
      or rotary (if both ``width`` and ``height`` are 1).

  .. method:: cmd_translate(tx, ty)

      Apply a translation to the bitmap transform matrix

      :param int tx: translation in x-axis
      :param int ty: translation in y-axis

  .. method:: cmd_videoframe(dst, ptr)

      Decode a single video frame

      :param int dst: bitmap destination in EVE memory
      :param int ptr: completion flag address in EVE memory

  .. method:: cmd_videostart()

      Start video playback

  .. method:: cmd_videostartf()

      Start video playback


  .. method:: cmd_wait(us)

      Wait

      :param int us: wait duration in microseconds

      .. note:: 817 only

  |

  .. method:: cc(b) 

      Append bytes to the command FIFO.

      :param bytes b: The bytes to add. Its length must be a multiple of 4.

  .. method:: finish()

      Send any queued drawing commands directly to the hardware,
      and return after they have all completed execution.

  .. method:: flush() 

      Send any queued drawing commands directly to the hardware.

  .. method:: swap() 

      End the current display list and dispatch it to the graphics hardware.
      Start compiling the display list for the next frame.

  .. method:: screenshot_im()

      Return the current screen contents as an image

      :returns image: Image of the current screen

      The returned image is a PIL :mod:`~pil:PIL.Image` with mode ``RGB`` and size (:data:`w`, :data:`h`).

      It can be saved to a file with::

          gd.screenshot_im().save("screenshot.png")

      .. note:: available on PC only


Module constants
================

Constants for :meth:`EVE.StencilFunc` and :meth:`AlphaFunc`
-----------------------------------------------------------

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
-----------------------------------

.. data:: RED
  :value: 2

.. data:: GREEN
  :value: 3

.. data:: BLUE
  :value: 4

.. data:: ALPHA
  :value: 5

.. _formats:

Bitmap Formats used by :meth:`EVE.BitmapLayout` and :meth:`EVE.cmd_setbitmap`
-----------------------------------------------------------------------------

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

Filter types for :meth:`BitmapSize`
-----------------------------------

.. data:: NEAREST
  :value: 0

.. data:: BILINEAR
  :value: 1

Wrap types for :meth:`BitmapSize`
---------------------------------

.. data:: BORDER
  :value: 0

.. data:: REPEAT
  :value: 1

Actions for :meth:`StencilFunc`
-------------------------------

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

Blend factors for :meth:`BlendFunc`
-----------------------------------

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

Primitive types for :meth:`Begin`
---------------------------------

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

Options bitfields
-----------------

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

Sample formats for use with :data:`REG_PLAYBACK_FORMAT`
-------------------------------------------------------

.. data:: LINEAR_SAMPLES
  :value: 0

.. data:: ULAW_SAMPLES
  :value: 1

.. data:: ADPCM_SAMPLES
  :value: 2

Instrument names for use with :data:`REG_SOUND`
-----------------------------------------------

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

Hardware register addresses
---------------------------

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
* :ref:`search`
