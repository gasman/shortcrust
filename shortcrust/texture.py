from pygame import image
from shortcrust.gl2 import *

class Texture(object):
	def __init__(self, filename, format, flipped=True):
		# print "loading texture: %s" % filename
		texture_img = image.load(filename)
		if format == GL_ALPHA:
			# write as RGBA, then take character index 3 (A) from every quartet
			pixels = image.tostring(texture_img, 'RGBA', flipped)[3::4]
		elif format == GL_RGB:
			pixels = image.tostring(texture_img, 'RGB', flipped)
		elif format == GL_RGBA:
			pixels = image.tostring(texture_img, 'RGBA', flipped)
		elif format == GL_LUMINANCE:
			# write as RGB, then take character index 1 (G) from every triplet
			pixels = image.tostring(texture_img, 'RGB', flipped)[1::3]
		elif format == GL_LUMINANCE_ALPHA:
			# write as RGBA, then take every second character (G and A)
			pixels = image.tostring(texture_img, 'RGBA', flipped)[1::2]

		self.texture_id = glGenTextures(1)
		# print "texture ID: %s" % self.texture_id
		glBindTexture(GL_TEXTURE_2D, self.texture_id)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glTexImage2D(
			GL_TEXTURE_2D, 0, format, texture_img.get_width(), texture_img.get_height(), 0,
			format, GL_UNSIGNED_BYTE, pixels
		)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

	def activate(self, texture_index):
		glActiveTexture(texture_index)
		glBindTexture(GL_TEXTURE_2D, self.texture_id)
