import ctypes
from gl2_constants import *

_gl = ctypes.CDLL('libGLESv2.so')


GLboolean = ctypes.c_ubyte
GLubyte = ctypes.c_ubyte
GLint = ctypes.c_int
GLuint = ctypes.c_uint
GLsizei = ctypes.c_int
GLenum = ctypes.c_uint
GLshort = ctypes.c_short
GLushort = ctypes.c_ushort
GLfloat = ctypes.c_float
GLdouble = ctypes.c_double

GL_FALSE = GLboolean(0)
GL_TRUE = GLboolean(1)


def GLints(L):
	"""Converts a tuple to an array of GLints (would a pointer return be better?)"""
	return (GLint * len(L))(*L)


def GLshorts(L):
	"""Converts a tuple to an array of GLshorts (would a pointer return be better?)"""
	return (GLshort * len(L))(*L)


def GLfloats(L):
	return (GLfloat * len(L))(*L)


class GLError(Exception):
	ERROR_STRINGS = {
		GL_INVALID_ENUM: 'GL_INVALID_ENUM',
		GL_INVALID_FRAMEBUFFER_OPERATION: 'GL_INVALID_FRAMEBUFFER_OPERATION',
		GL_INVALID_VALUE: 'GL_INVALID_VALUE',
		GL_INVALID_OPERATION: 'GL_INVALID_OPERATION',
		GL_OUT_OF_MEMORY: 'GL_OUT_OF_MEMORY',
	}

	def __init__(self, value):
		self.value = value

	def __str__(self):
		error_string = GLError.ERROR_STRINGS.get(self.value, "Unknown error")
		return "%s (0x%04x)" % (error_string, self.value)


def gl_check_error(func):
	def wrapped_func(*args, **kwargs):
		result = func(*args, **kwargs)
		err = _gl.glGetError()
		if err:
			raise GLError(err)
		return result
	return wrapped_func


glActiveTexture = (_gl.glActiveTexture)


glAttachShader = gl_check_error(_gl.glAttachShader)


@gl_check_error
def glBindAttribLocation(program, index, name):
	_gl.glBindAttribLocation(program, index, ctypes.byref(ctypes.c_char_p(name)))


_gl.glBindBuffer.argtypes = [GLenum, GLuint]
glBindBuffer = gl_check_error(_gl.glBindBuffer)


glBindFramebuffer = gl_check_error(_gl.glBindFramebuffer)


_gl.glBindTexture.argtypes = [GLenum, GLuint]
glBindTexture = gl_check_error(_gl.glBindTexture)


_gl.glBlendFunc.argtypes = [GLenum, GLenum]
glBlendFunc = gl_check_error(_gl.glBlendFunc)


_gl.glBlendFuncSeparate.argtypes = [GLenum, GLenum, GLenum, GLenum]
glBlendFuncSeparate = gl_check_error(_gl.glBlendFuncSeparate)


@gl_check_error
def glBufferData(target, data, usage):
	_gl.glBufferData(target, ctypes.sizeof(data), ctypes.byref(data), usage)


glClear = gl_check_error(_gl.glClear)


_gl.glClearColor.argtypes = [GLfloat, GLfloat, GLfloat, GLfloat]
glClearColor = gl_check_error(_gl.glClearColor)


glCompileShader = gl_check_error(_gl.glCompileShader)


_gl.glCreateProgram.restype = GLuint
glCreateProgram = gl_check_error(_gl.glCreateProgram)


glCreateShader = gl_check_error(_gl.glCreateShader)


glCullFace = gl_check_error(_gl.glCullFace)


_gl.glDepthRangef.argtypes = [GLfloat, GLfloat]
glDepthRangef = gl_check_error(_gl.glDepthRangef)


_gl.glDrawArrays.argtypes = [GLenum, GLint, GLsizei]
glDrawArrays = gl_check_error(_gl.glDrawArrays)


_gl.glDrawElements.argtypes = [GLenum, GLsizei, GLenum, ctypes.c_void_p]
glDrawElements = gl_check_error(_gl.glDrawElements)


_gl.glEnable.argtypes = [GLenum]
glEnable = gl_check_error(_gl.glEnable)


glEnableVertexAttribArray = gl_check_error(_gl.glEnableVertexAttribArray)


glFinish = gl_check_error(_gl.glFinish)


glFrontFace = gl_check_error(_gl.glFrontFace)


@gl_check_error
def glGenBuffers(n):
	buffers = ctypes.c_uint()
	_gl.glGenBuffers(n, ctypes.byref(buffers))
	if n == 1:
		return buffers.value
	else:
		raise Exception("glGenBuffers with n > 1 not implemented yet")


@gl_check_error
def glGenTextures(n):
	textures = ctypes.c_uint()
	_gl.glGenTextures(n, ctypes.byref(textures))
	if n == 1:
		return textures.value
	else:
		raise Exception("glGenTextures with n > 1 not implemented yet")


glGetAttribLocation = gl_check_error(_gl.glGetAttribLocation)


@gl_check_error
def glGetProgramInfoLog(program):
	N = 1024
	log = (ctypes.c_char * N)()
	loglen = ctypes.c_int()
	_gl.glGetProgramInfoLog(program, N, ctypes.byref(loglen), ctypes.byref(log))
	return log.value


@gl_check_error
def glGetProgramiv(program, pname):
	raise Exception("FIXME: glGetProgramiv is broken")
	params = GLint()
	_gl.glGetShaderiv(GLuint(program), pname, ctypes.byref(params))
	return params.value


@gl_check_error
def glGetShaderInfoLog(shader):
	N = 1024
	log = (ctypes.c_char * N)()
	loglen = ctypes.c_int()
	_gl.glGetShaderInfoLog(shader, N, ctypes.byref(loglen), ctypes.byref(log))
	return log.value


@gl_check_error
def glGetShaderiv(shader, pname):
	status = GLint()
	_gl.glGetShaderiv(shader, pname, ctypes.byref(status))
	return status.value


@gl_check_error
def glGetString(name):
	_gl.glGetString.restype = ctypes.c_char_p
	return _gl.glGetString(name)


glGetUniformLocation = gl_check_error(_gl.glGetUniformLocation)


_gl.glLinkProgram.argtypes = [GLuint]
glLinkProgram = gl_check_error(_gl.glLinkProgram)


glPixelStorei = gl_check_error(_gl.glPixelStorei)


@gl_check_error
def glShaderSource(shader_obj, string):
	_gl.glShaderSource(shader_obj, 1, ctypes.byref(ctypes.c_char_p(string)), 0)


_gl.glTexImage2D.argtypes = [GLenum, GLint, GLint, GLsizei, GLsizei, GLint, GLenum, GLenum, ctypes.c_char_p]
glTexImage2D = gl_check_error(_gl.glTexImage2D)


glTexParameteri = gl_check_error(_gl.glTexParameteri)


_gl.glUniform1f.argtypes = [GLint, GLfloat]
glUniform1f = gl_check_error(_gl.glUniform1f)

_gl.glUniform2f.argtypes = [GLint, GLfloat, GLfloat]
glUniform2f = gl_check_error(_gl.glUniform2f)

_gl.glUniform3f.argtypes = [GLint, GLfloat, GLfloat, GLfloat]
glUniform3f = gl_check_error(_gl.glUniform3f)

_gl.glUniform4f.argtypes = [GLint, GLfloat, GLfloat, GLfloat, GLfloat]
glUniform4f = gl_check_error(_gl.glUniform4f)

_gl.glUniform1i.argtypes = [GLint, GLint]
glUniform1i = gl_check_error(_gl.glUniform1i)

_gl.glUniform2i.argtypes = [GLint, GLint, GLint]
glUniform2i = gl_check_error(_gl.glUniform2i)

_gl.glUniform3i.argtypes = [GLint, GLint, GLint, GLint]
glUniform3i = gl_check_error(_gl.glUniform3i)

_gl.glUniform4i.argtypes = [GLint, GLint, GLint, GLint, GLint]
glUniform4i = gl_check_error(_gl.glUniform4i)


_gl.glUniform1fv.argtypes = [GLint, GLsizei, ctypes.POINTER(GLfloat)]
glUniform1fv = gl_check_error(_gl.glUniform1fv)

_gl.glUniform2fv.argtypes = [GLint, GLsizei, ctypes.POINTER(GLfloat)]
glUniform2fv = gl_check_error(_gl.glUniform2fv)

_gl.glUniform3fv.argtypes = [GLint, GLsizei, ctypes.POINTER(GLfloat)]
glUniform3fv = gl_check_error(_gl.glUniform3fv)

_gl.glUniform4fv.argtypes = [GLint, GLsizei, ctypes.POINTER(GLfloat)]
glUniform4fv = gl_check_error(_gl.glUniform4fv)


_gl.glUniform1iv.argtypes = [GLint, GLsizei, ctypes.POINTER(GLint)]
glUniform1iv = gl_check_error(_gl.glUniform1iv)

_gl.glUniform2iv.argtypes = [GLint, GLsizei, ctypes.POINTER(GLint)]
glUniform2iv = gl_check_error(_gl.glUniform2iv)

_gl.glUniform3iv.argtypes = [GLint, GLsizei, ctypes.POINTER(GLint)]
glUniform3iv = gl_check_error(_gl.glUniform3iv)

_gl.glUniform4iv.argtypes = [GLint, GLsizei, ctypes.POINTER(GLint)]
glUniform4iv = gl_check_error(_gl.glUniform4iv)


_gl.glUniformMatrix2fv.argtypes = [GLint, GLsizei, GLboolean, ctypes.POINTER(GLfloat)]
glUniformMatrix2fv = gl_check_error(_gl.glUniformMatrix2fv)

_gl.glUniformMatrix3fv.argtypes = [GLint, GLsizei, GLboolean, ctypes.POINTER(GLfloat)]
glUniformMatrix3fv = gl_check_error(_gl.glUniformMatrix3fv)

_gl.glUniformMatrix4fv.argtypes = [GLint, GLsizei, GLboolean, ctypes.POINTER(GLfloat)]
glUniformMatrix4fv = gl_check_error(_gl.glUniformMatrix4fv)


glUseProgram = gl_check_error(_gl.glUseProgram)


_gl.glValidateProgram.argtypes = [GLuint]
glValidateProgram = gl_check_error(_gl.glValidateProgram)


glVertexAttribPointer = gl_check_error(_gl.glVertexAttribPointer)


glViewport = gl_check_error(_gl.glViewport)
