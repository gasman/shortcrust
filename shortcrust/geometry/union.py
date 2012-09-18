from shortcrust.geometry.base import BaseGeometry


class Union(BaseGeometry):
	def __init__(self, geometries):
		positions = []
		normals = []
		texture_positions = []
		indices = []

		next_index = 0

		for geometry in geometries:
			positions += geometry.positions
			normals += geometry.normals
			texture_positions += geometry.texture_positions
			indices += [(next_index + i) for i in geometry.indices]
			next_index += len(geometry.positions)

		self.positions = positions
		self.normals = normals
		self.texture_positions = texture_positions
		self.indices = indices
