import ctypes
from gl_constants import *

_gl = ctypes.CDLL('libGLESv2.so')


GLboolean = ctypes.c_ubyte
GLint = ctypes.c_int
GLshort = ctypes.c_short
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


def glVertexPointer(size, data_type, stride, pointer):
	_gl.glVertexPointer(size, data_type, stride, ctypes.byref(pointer))


def glClearDepthf(depth):
	_gl.glDepthRangef(GLfloat(depth))


def glFrustumf(left, right, bottom, top, zNear, zFar):
	_gl.glFrustumf(GLfloat(left), GLfloat(right), GLfloat(bottom), GLfloat(top), GLfloat(zNear), GLfloat(zFar))


def glClearColor(r, g, b, a):
	_gl.glClearColor(GLfloat(r), GLfloat(g), GLfloat(b), GLfloat(a))


def glTranslatef(x, y, z):
	_gl.glTranslatef(GLfloat(x), GLfloat(y), GLfloat(z))


glDepthFunc = _gl.glDepthFunc
glEnable = _gl.glEnable
glEnableClientState = _gl.glEnableClientState
glShadeModel = _gl.glShadeModel
glMatrixMode = _gl.glMatrixMode
glLoadMatrixf = _gl.glLoadMatrixf
glClear = _gl.glClear
glDrawArrays = _gl.glDrawArrays
