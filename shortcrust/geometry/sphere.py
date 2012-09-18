from shortcrust.geometry.base import BaseGeometry
import math


class Sphere(BaseGeometry):
	def __init__(self, r=1.0, c=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0],
		min_lat_deg=-90, max_lat_deg=90, min_lng_deg=-180, max_lng_deg=180,
		lat_divisions=20, lng_divisions=20):

		positions = []
		normals = []
		texture_positions = []
		indices = []

		min_lat = min_lat_deg * math.pi / 180.0
		max_lat = max_lat_deg * math.pi / 180.0
		min_lng = min_lng_deg * math.pi / 180.0
		max_lng = max_lng_deg * math.pi / 180.0

		lng_step = (max_lng - min_lng) / lng_divisions
		lat_step = (max_lat - min_lat) / lat_divisions

		current_lat_index = 0  # index of first point at the current latitude
		prev_lat_index = None  # index of first point at the previous latitude
		for y in range(lat_divisions + 1):
			lat = min_lat + y * lat_step

			# plot a ring of points
			radius = r * math.cos(lat)
			for x in range(lng_divisions + 1):
				lng = min_lng + x * lng_step
				positions += [(radius * scale[0] * math.sin(lng) + c[0], r * scale[1] * math.sin(lat) + c[1], radius * scale[2] * math.cos(lng) + c[2])]
				normals += [(math.cos(lat) * math.sin(lng), math.sin(lat), math.cos(lat) * math.cos(lng))]
				texture_positions += [(float(x) / lng_divisions, float(y) / lat_divisions)]

			if y == 0:
				# no polys to plot this time
				pass
			else:
				# plot a ring from previous latitude to this one
				for x0 in range(lng_divisions):
					x1 = x0 + 1
					indices += [
						prev_lat_index + x0, prev_lat_index + x1, current_lat_index + x0,
						prev_lat_index + x1, current_lat_index + x1, current_lat_index + x0
					]

			prev_lat_index = current_lat_index
			current_lat_index += lng_divisions + 1

		self.positions = positions
		self.normals = normals
		self.texture_positions = texture_positions
		self.indices = indices
