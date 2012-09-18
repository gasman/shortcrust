import math
from shortcrust.gl2 import GLfloat
from shortcrust.matrix import mat3

Mat4 = GLfloat * 16


def create(mat=None):
	"""
		Creates a new instance of a mat4 using the default array type
		Any array-like object containing at least 16 numeric elements can serve as a mat4

		@param {mat4} [mat] mat4 containing values to initialize with

		@returns {mat4} New mat4
	"""
	dest = Mat4()

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
		dest[9] = mat[9]
		dest[10] = mat[10]
		dest[11] = mat[11]
		dest[12] = mat[12]
		dest[13] = mat[13]
		dest[14] = mat[14]
		dest[15] = mat[15]

	return dest


def identity(dest=None):
	"""
		Sets a mat4 to an identity matrix

		@param {mat4} dest mat4 to set

		@returns {mat4} dest
	"""
	if not dest:
		dest = create()

	dest[0] = 1
	dest[1] = 0
	dest[2] = 0
	dest[3] = 0
	dest[4] = 0
	dest[5] = 1
	dest[6] = 0
	dest[7] = 0
	dest[8] = 0
	dest[9] = 0
	dest[10] = 1
	dest[11] = 0
	dest[12] = 0
	dest[13] = 0
	dest[14] = 0
	dest[15] = 1
	return dest


def translate(mat, vec, dest=None):
	"""
		Translates a matrix by the given vector

		@param {mat4} mat mat4 to translate
		@param {vec3} vec vec3 specifying the translation
		@param {mat4} [dest] mat4 receiving operation result. If not specified result is written to mat

		@returns {mat4} dest if specified, mat otherwise
	"""
	x = vec[0]
	y = vec[1]
	z = vec[2]

	if (not dest) or (mat == dest):
		mat[12] = mat[0] * x + mat[4] * y + mat[8] * z + mat[12]
		mat[13] = mat[1] * x + mat[5] * y + mat[9] * z + mat[13]
		mat[14] = mat[2] * x + mat[6] * y + mat[10] * z + mat[14]
		mat[15] = mat[3] * x + mat[7] * y + mat[11] * z + mat[15]
		return mat

	a00 = mat[0]
	a01 = mat[1]
	a02 = mat[2]
	a03 = mat[3]

	a10 = mat[4]
	a11 = mat[5]
	a12 = mat[6]
	a13 = mat[7]

	a20 = mat[8]
	a21 = mat[9]
	a22 = mat[10]
	a23 = mat[11]

	dest[0] = a00
	dest[1] = a01
	dest[2] = a02
	dest[3] = a03

	dest[4] = a10
	dest[5] = a11
	dest[6] = a12
	dest[7] = a13

	dest[8] = a20
	dest[9] = a21
	dest[10] = a22
	dest[11] = a23

	dest[12] = a00 * x + a10 * y + a20 * z + mat[12]
	dest[13] = a01 * x + a11 * y + a21 * z + mat[13]
	dest[14] = a02 * x + a12 * y + a22 * z + mat[14]
	dest[15] = a03 * x + a13 * y + a23 * z + mat[15]

	return dest


def rotate(mat, angle, axis, dest=None):
	"""
		Rotates a matrix by the given angle around the specified axis
		If rotating around a primary axis (X,Y,Z) one of the specialized rotation functions should be used instead for performance

		@param {mat4} mat mat4 to rotate
		@param {number} angle Angle (in radians) to rotate
		@param {vec3} axis vec3 representing the axis to rotate around
		@param {mat4} [dest] mat4 receiving operation result. If not specified result is written to mat

		@returns {mat4} dest if specified, mat otherwise
	"""
	x = axis[0]
	y = axis[1]
	z = axis[2]
	length = math.sqrt(x * x + y * y + z * z)

	if not len:
		return None

	if length != 1:
		length = 1 / length
		x *= length
		y *= length
		z *= length

	s = math.sin(angle)
	c = math.cos(angle)
	t = 1 - c

	a00 = mat[0]
	a01 = mat[1]
	a02 = mat[2]
	a03 = mat[3]

	a10 = mat[4]
	a11 = mat[5]
	a12 = mat[6]
	a13 = mat[7]

	a20 = mat[8]
	a21 = mat[9]
	a22 = mat[10]
	a23 = mat[11]

	# Construct the elements of the rotation matrix
	b00 = x * x * t + c
	b01 = y * x * t + z * s
	b02 = z * x * t - y * s

	b10 = x * y * t - z * s
	b11 = y * y * t + c
	b12 = z * y * t + x * s

	b20 = x * z * t + y * s
	b21 = y * z * t - x * s
	b22 = z * z * t + c

	if not dest:
		dest = mat
	elif mat != dest:  # If the source and destination differ, copy the unchanged last row
		dest[12] = mat[12]
		dest[13] = mat[13]
		dest[14] = mat[14]
		dest[15] = mat[15]

	# Perform rotation-specific matrix multiplication
	dest[0] = a00 * b00 + a10 * b01 + a20 * b02
	dest[1] = a01 * b00 + a11 * b01 + a21 * b02
	dest[2] = a02 * b00 + a12 * b01 + a22 * b02
	dest[3] = a03 * b00 + a13 * b01 + a23 * b02

	dest[4] = a00 * b10 + a10 * b11 + a20 * b12
	dest[5] = a01 * b10 + a11 * b11 + a21 * b12
	dest[6] = a02 * b10 + a12 * b11 + a22 * b12
	dest[7] = a03 * b10 + a13 * b11 + a23 * b12

	dest[8] = a00 * b20 + a10 * b21 + a20 * b22
	dest[9] = a01 * b20 + a11 * b21 + a21 * b22
	dest[10] = a02 * b20 + a12 * b21 + a22 * b22
	dest[11] = a03 * b20 + a13 * b21 + a23 * b22
	return dest


def rotateX(mat, angle, dest=None):
	"""
		Rotates a matrix by the given angle around the X axis

		@param {mat4} mat mat4 to rotate
		@param {number} angle Angle (in radians) to rotate
		@param {mat4} [dest] mat4 receiving operation result. If not specified result is written to mat

		@returns {mat4} dest if specified, mat otherwise
	"""

	s = math.sin(angle)
	c = math.cos(angle)
	a10 = mat[4]
	a11 = mat[5]
	a12 = mat[6]
	a13 = mat[7]
	a20 = mat[8]
	a21 = mat[9]
	a22 = mat[10]
	a23 = mat[11]

	if not dest:
		dest = mat
	elif mat != dest:  # If the source and destination differ, copy the unchanged rows
		dest[0] = mat[0]
		dest[1] = mat[1]
		dest[2] = mat[2]
		dest[3] = mat[3]

		dest[12] = mat[12]
		dest[13] = mat[13]
		dest[14] = mat[14]
		dest[15] = mat[15]

	# Perform axis-specific matrix multiplication
	dest[4] = a10 * c + a20 * s
	dest[5] = a11 * c + a21 * s
	dest[6] = a12 * c + a22 * s
	dest[7] = a13 * c + a23 * s

	dest[8] = a10 * -s + a20 * c
	dest[9] = a11 * -s + a21 * c
	dest[10] = a12 * -s + a22 * c
	dest[11] = a13 * -s + a23 * c
	return dest


def rotateY(mat, angle, dest=None):
	"""
		Rotates a matrix by the given angle around the Y axis

		@param {mat4} mat mat4 to rotate
		@param {number} angle Angle (in radians) to rotate
		@param {mat4} [dest] mat4 receiving operation result. If not specified result is written to mat

		@returns {mat4} dest if specified, mat otherwise
	"""
	s = math.sin(angle)
	c = math.cos(angle)
	a00 = mat[0]
	a01 = mat[1]
	a02 = mat[2]
	a03 = mat[3]
	a20 = mat[8]
	a21 = mat[9]
	a22 = mat[10]
	a23 = mat[11]

	if not dest:
		dest = mat
	elif mat != dest:  # If the source and destination differ, copy the unchanged rows
		dest[4] = mat[4]
		dest[5] = mat[5]
		dest[6] = mat[6]
		dest[7] = mat[7]

		dest[12] = mat[12]
		dest[13] = mat[13]
		dest[14] = mat[14]
		dest[15] = mat[15]

	# Perform axis-specific matrix multiplication
	dest[0] = a00 * c + a20 * -s
	dest[1] = a01 * c + a21 * -s
	dest[2] = a02 * c + a22 * -s
	dest[3] = a03 * c + a23 * -s

	dest[8] = a00 * s + a20 * c
	dest[9] = a01 * s + a21 * c
	dest[10] = a02 * s + a22 * c
	dest[11] = a03 * s + a23 * c
	return dest


def rotateZ(mat, angle, dest=None):
	"""
		Rotates a matrix by the given angle around the Z axis

		@param {mat4} mat mat4 to rotate
		@param {number} angle Angle (in radians) to rotate
		@param {mat4} [dest] mat4 receiving operation result. If not specified result is written to mat

		@returns {mat4} dest if specified, mat otherwise
	"""
	s = math.sin(angle)
	c = math.cos(angle)
	a00 = mat[0]
	a01 = mat[1]
	a02 = mat[2]
	a03 = mat[3]
	a10 = mat[4]
	a11 = mat[5]
	a12 = mat[6]
	a13 = mat[7]

	if not dest:
		dest = mat
	elif mat != dest:  # If the source and destination differ, copy the unchanged last row
		dest[8] = mat[8]
		dest[9] = mat[9]
		dest[10] = mat[10]
		dest[11] = mat[11]

		dest[12] = mat[12]
		dest[13] = mat[13]
		dest[14] = mat[14]
		dest[15] = mat[15]

	# Perform axis-specific matrix multiplication
	dest[0] = a00 * c + a10 * s
	dest[1] = a01 * c + a11 * s
	dest[2] = a02 * c + a12 * s
	dest[3] = a03 * c + a13 * s

	dest[4] = a00 * -s + a10 * c
	dest[5] = a01 * -s + a11 * c
	dest[6] = a02 * -s + a12 * c
	dest[7] = a03 * -s + a13 * c

	return dest


def frustum(left, right, bottom, top, near, far, dest=None):
	"""
		Generates a frustum matrix with the given bounds

		@param {number} left Left bound of the frustum
		@param {number} right Right bound of the frustum
		@param {number} bottom Bottom bound of the frustum
		@param {number} top Top bound of the frustum
		@param {number} near Near bound of the frustum
		@param {number} far Far bound of the frustum
		@param {mat4} [dest] mat4 frustum matrix will be written into

		@returns {mat4} dest if specified, a new mat4 otherwise
	"""

	if not dest:
		dest = create()

	rl = (right - left)
	tb = (top - bottom)
	fn = (far - near)
	dest[0] = (near * 2) / rl
	dest[1] = 0
	dest[2] = 0
	dest[3] = 0
	dest[4] = 0
	dest[5] = (near * 2) / tb
	dest[6] = 0
	dest[7] = 0
	dest[8] = (right + left) / rl
	dest[9] = (top + bottom) / tb
	dest[10] = -(far + near) / fn
	dest[11] = -1
	dest[12] = 0
	dest[13] = 0
	dest[14] = -(far * near * 2) / fn
	dest[15] = 0
	return dest


def perspective(fovy, aspect, near, far, dest=None):
	"""
		Generates a perspective projection matrix with the given bounds

		@param {number} fovy Vertical field of view
		@param {number} aspect Aspect ratio. typically viewport width/height
		@param {number} near Near bound of the frustum
		@param {number} far Far bound of the frustum
		@param {mat4} [dest] mat4 frustum matrix will be written into

		@returns {mat4} dest if specified, a new mat4 otherwise
	"""
	top = near * math.tan(fovy * math.pi / 360.0)
	right = top * aspect
	return frustum(-right, right, -top, top, near, far, dest)


def toInverseMat3(mat, dest=None):
	"""
		Calculates the inverse of the upper 3x3 elements of a mat4 and copies the result into a mat3
		The resulting matrix is useful for calculating transformed normals

		Params:
		@param {mat4} mat mat4 containing values to invert and copy
		@param {mat3} [dest] mat3 receiving values

		@returns {mat3} dest is specified, a new mat3 otherwise, null if the matrix cannot be inverted
	"""
	# Cache the matrix values (makes for huge speed increases!)
	a00 = mat[0]
	a01 = mat[1]
	a02 = mat[2]

	a10 = mat[4]
	a11 = mat[5]
	a12 = mat[6]

	a20 = mat[8]
	a21 = mat[9]
	a22 = mat[10]

	b01 = a22 * a11 - a12 * a21
	b11 = -a22 * a10 + a12 * a20
	b21 = a21 * a10 - a11 * a20

	d = a00 * b01 + a01 * b11 + a02 * b21

	if not d:
		return None
	id = 1.0 / d

	if not dest:
		dest = mat3.create()

	dest[0] = b01 * id
	dest[1] = (-a22 * a01 + a02 * a21) * id
	dest[2] = (a12 * a01 - a02 * a11) * id
	dest[3] = b11 * id
	dest[4] = (a22 * a00 - a02 * a20) * id
	dest[5] = (-a12 * a00 + a02 * a10) * id
	dest[6] = b21 * id
	dest[7] = (-a21 * a00 + a01 * a20) * id
	dest[8] = (a11 * a00 - a01 * a10) * id

	return dest


def multiplyVec3(mat, vec, dest=None):
	"""
		Transforms a vec3 with the given matrix
		4th vector component is implicitly '1'

		@param {mat4} mat mat4 to transform the vector with
		@param {vec3} vec vec3 to transform
		@param {vec3} [dest] vec3 receiving operation result. If not specified result is written to vec

		@returns {vec3} dest if specified, vec otherwise
	"""
	if not dest:
		dest = vec

	x = vec[0]
	y = vec[1]
	z = vec[2]

	dest[0] = mat[0] * x + mat[4] * y + mat[8] * z + mat[12]
	dest[1] = mat[1] * x + mat[5] * y + mat[9] * z + mat[13]
	dest[2] = mat[2] * x + mat[6] * y + mat[10] * z + mat[14]

	return dest


def lookAt(eye, center, up, dest=None):
	"""
		Generates a look-at matrix with the given eye position, focal point, and up axis

		@param {vec3} eye Position of the viewer
		@param {vec3} center Point the viewer is looking at
		@param {vec3} up vec3 pointing "up"
		@param {mat4} [dest] mat4 matrix will be written into

		@returns {mat4} dest if specified, a new mat4 otherwise
	"""

	if not dest:
		dest = create()

	eyex = eye[0]
	eyey = eye[1]
	eyez = eye[2]
	upx = up[0]
	upy = up[1]
	upz = up[2]
	centerx = center[0]
	centery = center[1]
	centerz = center[2]

	if (eyex == centerx and eyey == centery and eyez == centerz):
		return identity(dest)

	# vec3.direction(eye, center, z)
	z0 = eyex - centerx
	z1 = eyey - centery
	z2 = eyez - centerz

	# normalize (no check needed for 0 because of early return)
	len = 1 / math.sqrt(z0 * z0 + z1 * z1 + z2 * z2)
	z0 *= len
	z1 *= len
	z2 *= len

	# vec3.normalize(vec3.cross(up, z, x))
	x0 = upy * z2 - upz * z1
	x1 = upz * z0 - upx * z2
	x2 = upx * z1 - upy * z0
	len = math.sqrt(x0 * x0 + x1 * x1 + x2 * x2)
	if not len:
		x0 = 0
		x1 = 0
		x2 = 0
	else:
		len = 1 / len
		x0 *= len
		x1 *= len
		x2 *= len

	# vec3.normalize(vec3.cross(z, x, y));
	y0 = z1 * x2 - z2 * x1
	y1 = z2 * x0 - z0 * x2
	y2 = z0 * x1 - z1 * x0

	len = math.sqrt(y0 * y0 + y1 * y1 + y2 * y2)
	if not len:
		y0 = 0
		y1 = 0
		y2 = 0
	else:
		len = 1 / len
		y0 *= len
		y1 *= len
		y2 *= len

	dest[0] = x0
	dest[1] = y0
	dest[2] = z0
	dest[3] = 0
	dest[4] = x1
	dest[5] = y1
	dest[6] = z1
	dest[7] = 0
	dest[8] = x2
	dest[9] = y2
	dest[10] = z2
	dest[11] = 0
	dest[12] = -(x0 * eyex + x1 * eyey + x2 * eyez)
	dest[13] = -(y0 * eyex + y1 * eyey + y2 * eyez)
	dest[14] = -(z0 * eyex + z1 * eyey + z2 * eyez)
	dest[15] = 1

	return dest
