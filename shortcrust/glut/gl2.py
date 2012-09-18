from OpenGL.GL import *


def GLints(L):
	"""Converts a tuple to an array of GLints (would a pointer return be better?)"""
	return (GLint * len(L))(*L)


def GLshorts(L):
	"""Converts a tuple to an array of GLshorts (would a pointer return be better?)"""
	return (GLshort * len(L))(*L)


def GLfloats(L):
	return (GLfloat * len(L))(*L)


if not bool(glDepthRangef):
	# need to define glDepthRangef in terms of glDepthRange
	def glDepthRangef(n, f):
		glDepthRange(ctypes.c_double(n), ctypes.c_double(f))
