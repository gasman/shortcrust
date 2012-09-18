* Shortcrust *

Shortcrust is a Python wrapper library for OpenGL, intended for building
applications that are portable to the Raspberry Pi.

On machines where PyOpenGL is available (hereafter referred to as
'grown-up machines'), the standard PyOpenGL API methods will be accessible
to the application, with GLUT used to handle housekeeping tasks such as opening
viewport windows. When running on Raspberry Pi, the binary OpenGL ES driver is
wrapped to provide a subset of the PyOpenGL API. PyGame (shipped with the
default Raspbian install) is used for additional functions such as texture
loading.

The primary motivation for Shortcrust is creating demoscene productions
<http://www.demoscene.info/the-demoscene/> - however, it is hoped that it will
find wider use for 3D applications in general.


** BaseGLApp **

Applications in Shortcrust are implemented as subclasses of
shortcrust.BaseGLApp. Generally you will override the following methods:

* setup(self) - called once after the GL viewport has been created
* draw(self, time) - called repeatedly to render video frames. 'time' is the
  number of seconds since the application was started.
* on_exit(self) - called immediately before exiting the application. On
  grown-up machines, pressing escape causes an exit; you can also initiate one
  within your application by calling self.exit().

You can also set the following properties on your BaseGLApp subclass to
customise behaviour:

* fullscreen (default=False): If true, the application opens in a full-screen
  viewport on grown-up machines. On Raspberry Pi, applications are always
  full-screen.
* title: Specifies the title text for the viewport window on grown-up machines.
  No effect on Raspberry Pi (or when fullscreen=True).
* depthbuffer (default=True): Creates a GL viewport with depth buffer support
  enabled (pretty much essential for rendering any kind of 3D scenes).

Additionally, the properties 'width', 'height' and 'aspect_ratio' are defined,
to give information about the viewport dimensions.

** GL functions **

The following functions are available within the shortcrust.gl2 module,
following the PyOpenGL API
<http://pyopengl.sourceforge.net/documentation/manual-3.0/index.xhtml#GL>:

glActiveTexture
glAttachShader
glBindAttribLocation
glBindBuffer
glBindFramebuffer
glBindTexture
glBlendFunc
glBlendFuncSeparate
glBufferData
glClear
glClearColor
glCompileShader
glCreateProgram
glCreateShader
glCullFace
glDepthRangef
glDrawArrays
glDrawElements
glEnable
glEnableVertexAttribArray
glFinish
glFrontFace
glGenBuffers (does not currently support returning more than 1 buffer)
glGenTextures (does not currently support returning more than 1 texture)
glGetProgramInfoLog
glGetShaderInfoLog
glGetShaderiv
glGetString
glGetUniformLocation
glLinkProgram
glPixelStorei
glShaderSource
glTexImage2D
glTexParameteri
glUniform1f
glUniform2f
glUniform3f
glUniform4f
glUniform1i
glUniform2i
glUniform3i
glUniform4i
glUniform1fv
glUniform2fv
glUniform3fv
glUniform4fv
glUniform1iv
glUniform2iv
glUniform3iv
glUniform4iv
glUniformMatrix2fv
glUniformMatrix3fv
glUniformMatrix4fv
glUseProgram
glValidateProgram
glVertexAttribPointer
glViewport

As with PyOpenGL, error checking takes place after every GL operation, and
any errors are thrown as exceptions (of type GLError).

** Other batteries included **

* shortcrust.matrix is a library for performing matrix / vector operations,
  ported from gl-matrix by Brandon Jones: https://github.com/toji/gl-matrix
  The data structures it works with (as created by mat3.create(), mat4.create()
  and vec3.create()) are arrays of type GLfloat, suitable for passing as
  parameters to GL functions such as glUniformMatrix4fv.
* shortcrust.shader provides ShaderProgram, an abstract class that encapsulates
  a vertex shader / fragment shader pair, taking care of the details of
  compiling and linking them. It's intended that you should query the attribute
  and uniform locations within your shader using the provided get_attrib and
  get_uniform methods, and expose them as methods of your ShaderProgram object.
* shortcrust.buffer provides wrappers for various types of buffer, allowing you
  to push data in the form of arrays onto the graphics card.
* shortcrust.texture handles the uploading of texture data into GPU memory,
  using any image file format supported by PyGame as a starting point.
* shortcrust.geometry provides a number of primitive shape classes which can be
  combined and converted to a polygon mesh for rendering with a shader.

  Take a look at the example projects to see how it all fits together.

** Acknowledgements **

* Ben O'Steen - for the documentation and example code for framebuffer-based
  access to OpenGL ES on the RasPi:
  http://benosteen.wordpress.com/2012/04/27/using-opengl-es-2-0-on-the-raspberry-pi-without-x-windows/
* Peter de Rivaz - for the initial work on Python EGL / OpenGL ES bindings for
  the RasPi, which served as the starting point for this project:
  https://github.com/peterderivaz/pyopengles
* Sir Garbagetruck - for pointing me at the above and planting the idea of
  using Python for RasPi demos
* Giles Thomas - for the WebGL tutorials that steered me in the right direction
  with OpenGL ES and indirectly informed the API design
* Brandon Jones - for the glMatrix Javascript library, various sections of
  which I've ported to Python with minimal changes:
  https://github.com/toji/gl-matrix
* mnstrmnch - for troubleshooting thorny problems with alpha channels

** Author **

Matt Westcott <http://matt.west.co.tt/> - gasman@raww.org
twitter.com/gasmanic
