from shortcrust.gl2 import *
from shortcrust.buffer import AttributeBuffer, ElementArrayBuffer
from shortcrust.matrix import vec3


class Mesh(object):
	mode = GL_TRIANGLES

	def __init__(self, geometry, material_color=[1.0, 1.0, 1.0], texture=None):
		self.positions = AttributeBuffer(geometry.positions)
		self.normals = AttributeBuffer(geometry.normals)
		self.texture_positions = AttributeBuffer(geometry.texture_positions)
		self.indices = ElementArrayBuffer(geometry.indices)
		self.index_count = self.indices.element_count

		self.material_color = vec3.create(material_color)
		self.texture = texture

	def draw(self):
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices.name)
		glDrawElements(self.mode, self.index_count, self.indices.data_type, None)


class BaseGeometry(object):
	def to_mesh(self, **kwargs):
		return Mesh(self, **kwargs)
