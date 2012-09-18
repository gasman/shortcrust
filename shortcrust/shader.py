from .gl2 import *


class ShaderProgram(object):
	vertex_shader = None
	fragment_shader = None

	@staticmethod
	def load_shader(shader_type, shader_src):
		shader = glCreateShader(shader_type)
		# print "shader: %s" % repr(shader)

		glShaderSource(shader, shader_src)
		glCompileShader(shader)
		compiled = glGetShaderiv(shader, GL_COMPILE_STATUS)
		# print "compiled? %s" % repr(compiled)

		if not compiled:
			print "Error compiling shader: %s" % glGetShaderInfoLog(shader)
			raise ValueError

		return shader

	def __init__(self):
		self.program_object = glCreateProgram()
		# print "program_object: %s, %s" % (repr(self.program_object), type(self.program_object))

		if self.vertex_shader:
			vertex_shader_obj = self.load_shader(GL_VERTEX_SHADER, self.vertex_shader)
			glAttachShader(self.program_object, vertex_shader_obj)

		if self.fragment_shader:
			fragment_shader_obj = self.load_shader(GL_FRAGMENT_SHADER, self.fragment_shader)
			glAttachShader(self.program_object, fragment_shader_obj)

		glLinkProgram(self.program_object)
		#linked = glGetProgramiv(self.program_object, GL_LINK_STATUS)
		#print "linked: %s" % repr(linked)
		program_log = glGetProgramInfoLog(self.program_object)
		if program_log:
			print "linking notes: %s" % program_log

		glValidateProgram(self.program_object)
		#validated = glGetProgramiv(self.program_object, GL_VALIDATE_STATUS)
		#print "validated: %s" % repr(validated)
		program_log = glGetProgramInfoLog(self.program_object)
		if program_log:
			print "validation notes: %s" % program_log

	def get_attrib(self, name):
		attr_location = glGetAttribLocation(self.program_object, name)
		glEnableVertexAttribArray(attr_location)
		return attr_location

	def get_uniform(self, name):
		return glGetUniformLocation(self.program_object, name)

	def use(self):
		glUseProgram(self.program_object)
