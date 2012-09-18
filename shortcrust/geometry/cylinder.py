from shortcrust.geometry.base import BaseGeometry
import math


class Cylinder(BaseGeometry):
	def __init__(self, c=[0.0, 0.0, 0.0], h=1.0, r=1.0, divisions=20,
		min_lng_deg=0, max_lng_deg=360):
		positions = []
		normals = []
		texture_positions = []
		indices = []

		min_lng = min_lng_deg * math.pi / 180
		max_lng = max_lng_deg * math.pi / 180
		lng_step = (max_lng - min_lng) / divisions

		for i in range(divisions):
			a = min_lng + i * lng_step
			positions += [(r * math.sin(a) + c[0], c[1], r * math.cos(a) + c[2])]
			normals += [(math.sin(a), 0, math.cos(a))]
			texture_positions += [(float(i) / divisions, 0.0)]
		for i in range(divisions):
			a = min_lng + i * lng_step
			positions += [(r * math.sin(a) + c[0], h + c[1], r * math.cos(a) + c[2])]
			normals += [(math.sin(a), 0, math.cos(a))]
			texture_positions += [(float(i) / divisions, 1.0)]

		for x0 in range(divisions):
			x1 = (x0 + 1) % divisions
			indices += [
				x0, x1, x0 + divisions,
				x1, x1 + divisions, x0 + divisions
			]

		self.positions = positions
		self.normals = normals
		self.texture_positions = texture_positions
		self.indices = indices
