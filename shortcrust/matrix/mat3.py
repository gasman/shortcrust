import math
from shortcrust.gl2 import GLfloat

Mat3 = GLfloat * 9


def create(mat=None):
	"""
		Creates a new instance of a mat3 using the default array type
		Any array-like object containing at least 9 numeric elements can serve as a mat3

		@param {mat3} [mat] mat3 containing values to initialize with

		@returns {mat3} New mat3
	"""
	dest = Mat3()

	if mat:
		dest[0] = mat[0]
		dest[1] = mat[1]
		dest[2] = mat[2]
		dest[3] = mat[3]
		dest[4] = mat[4]
		dest[5] = mat[5]
		dest[6] = mat[6]
		dest[7] = mat[7]
		dest[8] = mat[8]

	return dest


def transpose(mat, dest=None):
	"""
		Transposes a mat3 (flips the values over the diagonal)

		Params:
		@param {mat3} mat mat3 to transpose
		@param {mat3} [dest] mat3 receiving transposed values. If not specified result is written to mat

		@returns {mat3} dest is specified, mat otherwise
	"""
	# If we are transposing ourselves we can skip a few steps but have to cache some values
	if (not dest) or (mat == dest):
		a01 = mat[1]
		a02 = mat[2]
		a12 = mat[5]

		mat[1] = mat[3]
		mat[2] = mat[6]
		mat[3] = a01
		mat[5] = mat[7]
		mat[6] = a02
		mat[7] = a12
		return mat

	dest[0] = mat[0]
	dest[1] = mat[3]
	dest[2] = mat[6]
	dest[3] = mat[1]
	dest[4] = mat[4]
	dest[5] = mat[7]
	dest[6] = mat[2]
	dest[7] = mat[5]
	dest[8] = mat[8]
	return dest
