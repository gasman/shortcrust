from .gl2 import *

TYPE_CONSTRUCTORS = {
	GL_UNSIGNED_BYTE: GLubyte,
	GL_UNSIGNED_SHORT: GLushort,
	GL_UNSIGNED_INT: GLuint,
	GL_FLOAT: GLfloat,
}


class Buffer(object):
	def __init__(self, items, data_type=None):
		if data_type:
			self.data_type = data_type

		self.element_count = len(items)

		# examine first element to find out whether it's a vector type,
		# in which case the array needs flattening
		try:
			self.element_size = len(items[0])
			is_flat = False
		except TypeError:
			# elements are scalar
			self.element_size = 1
			is_flat = True

		if is_flat:
			items_flat = items
		else:
			# need to flatten array
			items_flat = []
			for item in items:
				items_flat += item

		constructor = TYPE_CONSTRUCTORS[self.data_type]
		gl_items = (constructor * len(items_flat))(*items_flat)
		self.name = glGenBuffers(1)
		glBindBuffer(self.target, self.name)
		glBufferData(self.target, gl_items, GL_STATIC_DRAW)


class ElementArrayBuffer(Buffer):
	data_type = GL_UNSIGNED_SHORT
	target = GL_ELEMENT_ARRAY_BUFFER


class AttributeBuffer(Buffer):
	data_type = GL_FLOAT
	target = GL_ARRAY_BUFFER

	def attach(self, attr_location):
		glBindBuffer(self.target, self.name)
		glVertexAttribPointer(attr_location, self.element_size, self.data_type, GL_FALSE, 0, None)
