from OpenGL.GL import *


def GLints(L):
	"""Converts a tuple to an array of GLints (would a pointer return be better?)"""
	return (GLint * len(L))(*L)


def GLshorts(L):
	"""Converts a tuple to an array of GLshorts (would a pointer return be better?)"""
	return (GLshort * len(L))(*L)


def GLfloats(L):
	return (GLfloat * len(L))(*L)


if not bool(glClearDepthf):
	glClearDepthf = glClearDepth

glFrustumf = glFrustum
