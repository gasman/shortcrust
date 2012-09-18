#!/usr/bin/env python

# Plasma example for Shortcrust -
# based on the default effect in GLSL Sandbox <http://glsl.heroku.com/> by @mrdoob

from shortcrust import BaseGLApp
from shortcrust.shader import ShaderProgram
from shortcrust.gl2 import *
from shortcrust.buffer import AttributeBuffer

class PlasmaShader(ShaderProgram):
	# A 'do nothing' vertex shader that simply passes vertex positions through to screen coordinates.
	vertex_shader = """
		attribute vec4 vPosition;
		void main()
		{
			gl_Position = vPosition;
		}
	"""

	# A fragment shader that colours pixels as a function of x/y coordinate, resolution and time.
	fragment_shader = """
#ifdef GLES2
		precision mediump float;
#endif

		uniform float time;
		uniform vec2 resolution;

		void main( void ) {

			vec2 position = ( gl_FragCoord.xy / resolution.xy );

			float color = 0.0;
			color += sin( position.x * cos( time / 15.0 ) * 80.0 ) + cos( position.y * cos( time / 15.0 ) * 10.0 );
			color += sin( position.y * sin( time / 10.0 ) * 40.0 ) + cos( position.x * sin( time / 25.0 ) * 40.0 );
			color += sin( position.x * sin( time / 5.0 ) * 10.0 ) + sin( position.y * sin( time / 35.0 ) * 80.0 );
			color *= sin( time / 10.0 ) * 0.5;

			gl_FragColor = vec4( vec3( color, color * 0.5, sin( color + time / 3.0 ) * 0.75 ), 1.0 );

		}
	"""

	def __init__(self):
		super(PlasmaShader, self).__init__()

		# Retrieve the locations of the position, time and resolution attributes / uniforms
		# so that we can push values to them later
		self.attr_vposition = self.get_attrib('vPosition')
		self.unif_time = self.get_uniform('time')
		self.unif_resolution = self.get_uniform('resolution')

	def set_time(self, value):
		"""
			Set the 'time' uniform within the shader
		"""
		glUniform1f(self.unif_time, value)

	def set_resolution(self, width, height):
		"""
			Set the 'resolution' uniform from the passed width and height
		"""
		glUniform2f(self.unif_resolution, width, height)

	def draw(self, model):
		"""
			Render the passed model (i.e. anything with a 'positions' buffer that can be bound
			to the vPosition attribute, and a 'draw' method that pushes the triangles to GL)
			via this shader.
		"""
		model.positions.attach(self.attr_vposition)
		model.draw()


class FullscreenQuad(object):

	# render as a triangle strip: i.e. triangles with vertex indices (0, 1, 2) and (1, 2, 3)
	mode = GL_TRIANGLE_STRIP

	def __init__(self):
		# Define a buffer of vertex positions, at the four corners of the screen
		self.positions = AttributeBuffer([
			(-1, -1, 0), (-1, 1, 0), (1, -1, 0), (1, 1, 0)
		])
		self.vertex_count = self.positions.element_count

	def draw(self):
		"""
			Called by the shader once the positions buffer has been attached to the
			appropriate attribute; sends polygons to GL in the form of a triangle strip
		"""
		glDrawArrays(self.mode, 0, self.vertex_count)


class PlasmaDemo(BaseGLApp):
	title = "Shortcrust plasma example"

	def setup(self):
		""" Called once to set up resources, once the GL viewport has been initialised """

		# Create an instance of our shader and model
		self.shader = PlasmaShader()
		self.model = FullscreenQuad()

		self.shader.use()
		self.shader.set_resolution(self.width, self.height)

	def draw(self, time):
		""" Called repeatedly to render successive video frames """
		self.shader.use()  # select our PlasmaShader as the active GL shader
		self.shader.set_time(time)  # Pass the current time elapsed (in seconds) to the shader
		self.shader.draw(self.model)  # draw our fullscreen quad


# Create an instance of PlasmaDemo and kick things off...
PlasmaDemo().run()
