import math
from shortcrust.gl2 import GLfloat

Vec3 = GLfloat * 3


def create(vec=None):
	"""
		Creates a new instance of a vec3 using the default array type
		Any javascript array-like objects containing at least 3 numeric elements can serve as a vec3

		@param {vec3} [vec] vec3 containing values to initialize with

		@returns {vec3} New vec3
	"""
	dest = Vec3()

	if vec:
		dest[0] = vec[0]
		dest[1] = vec[1]
		dest[2] = vec[2]
	else:
		dest[0] = dest[1] = dest[2] = 0

	return dest
