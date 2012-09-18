#!/usr/bin/env python

# Globe example for Shortcrust

from shortcrust import BaseGLApp
from shortcrust.shader import ShaderProgram
from shortcrust.geometry import Sphere
from shortcrust.texture import Texture
from shortcrust.gl2 import *
from shortcrust.matrix import mat4, mat3, vec3

class PhongTextureShader(ShaderProgram):
	vertex_shader = """
		attribute vec3 aVertexPosition;
		attribute vec3 aVertexNormal;
		attribute vec2 aTexturePosition;

		uniform mat4 uMVMatrix;
		uniform mat4 uPMatrix;
		uniform mat3 uNMatrix;

		varying vec3 vNormal;
		varying vec4 vPosition;
		varying vec2 vTextureCoord;

		void main(void) {
			/* apply MVMatrix to move vertex into correct position within the scene */
			vPosition = uMVMatrix * vec4(aVertexPosition, 1.0);
			/* perform equivalent transform on normal */
			vNormal = uNMatrix * aVertexNormal;

			/* project vertex into screen space */
			gl_Position = uPMatrix * vPosition;

			/* pass texture coordinates through to fragment shader for interpolation */
			vTextureCoord = aTexturePosition;
		}
	"""

	fragment_shader = """
#ifdef GLES2
		precision mediump float;
#endif

		varying vec3 vNormal;
		varying vec4 vPosition;
		varying vec2 vTextureCoord;

		uniform vec3 uLightLocation;
		uniform sampler2D uSampler;

		const vec3 cAmbientColor = vec3(0.1, 0.1, 0.1);
		const vec3 cDiffuseColor = vec3(0.8, 0.8, 0.8);
		const vec3 cSpecularColor = vec3(0.0, 0.0, 0.0);
		const float cMaterialShininess = 3.0;

		void main(void) {
			/* calculate diffuse light intensity - angle between light and surface normal */
			vec3 lightDirection = normalize(uLightLocation - vPosition.xyz);
			float diffuseLightIntensity = max(dot(vNormal, lightDirection), 0.0);

			/* calculate specular light intensity - angle between eye and reflected light */
			vec3 eyeDirection = normalize(-vPosition.xyz);
			vec3 reflectionDirection = reflect(-lightDirection, vNormal);
			float specularLightIntensity = pow(max(dot(reflectionDirection, eyeDirection), 0.0), cMaterialShininess);

			/* add ambient, diffuse and specular components to give final light colour */
			vec3 lightWeighting = cAmbientColor + cDiffuseColor * diffuseLightIntensity + cSpecularColor + specularLightIntensity;

			vec3 materialColor = texture2D(uSampler, vec2(vTextureCoord.s, vTextureCoord.t)).rgb;

			gl_FragColor = vec4(materialColor * lightWeighting, 1.0);
		}
	"""

	def __init__(self):
		super(PhongTextureShader, self).__init__()
		self.use()

		self.aVertexPosition = self.get_attrib('aVertexPosition')
		self.aVertexNormal = self.get_attrib('aVertexNormal')
		self.aTexturePosition = self.get_attrib('aTexturePosition')

		self.uPMatrix = self.get_uniform('uPMatrix')
		self.uMVMatrix = self.get_uniform('uMVMatrix')
		self.uNMatrix = self.get_uniform('uNMatrix')
		self.uLightLocation = self.get_uniform('uLightLocation')
		self.uSampler = self.get_uniform('uSampler')

	# define accessor functions for the uniforms in the shader

	def set_pmatrix(self, pMatrix):
		glUniformMatrix4fv(self.uPMatrix, 1, GL_FALSE, pMatrix)

	def set_mvmatrix(self, mvMatrix):
		glUniformMatrix4fv(self.uMVMatrix, 1, GL_FALSE, mvMatrix)

	def set_nmatrix(self, nMatrix):
		glUniformMatrix3fv(self.uNMatrix, 1, GL_FALSE, nMatrix)

	def set_light_location(self, lightLocation):
		glUniform3fv(self.uLightLocation, 1, lightLocation)

	def draw(self, model):
		# set the model's texture to be the active texture in slot 0
		model.texture.activate(GL_TEXTURE0)
		# specify texture slot 0 as the one the sampler should use
		glUniform1i(self.uSampler, 0)

		# associate the model's vertex position, normal and texture coordinate buffers
		# with the relevant attributes of the shader
		model.positions.attach(self.aVertexPosition)
		model.normals.attach(self.aVertexNormal)
		model.texture_positions.attach(self.aTexturePosition)

		# Get the model to push its polygon data to the shader.
		# (This is the responsibility of the model, rather than the shader, as different
		# models may use different vertex addressing schemes)
		model.draw()


class GlobeDemo(BaseGLApp):
	title = "Shortcrust globe example"

	def setup(self):
		""" Called once to set up resources, once the GL viewport has been initialised """

		glEnable(GL_DEPTH_TEST)
		self.shader = PhongTextureShader()

		self.shader.use()

		# Create a perspective projection matrix and pass it to the shader's pMatrix uniform
		self.shader.set_pmatrix(mat4.perspective(45, self.aspect_ratio, 0.1, 100.0))

		# Define model-view matrix and normal matrices as attributes of the GlobeDemo object;
		# this avoids the overhead of creating fresh mat3/mat4 objects on every frame
		self.mv_matrix = mat4.create()
		self.n_matrix = mat3.create()

		self.light_location = vec3.create([2, 5, -3])
		self.transformed_light_location = vec3.create()

		# define model to be a sphere geometry object with default parameters
		# (unit radius centred on origin) converted to a mesh.
		# (Sphere itself is a pure python object; calling to_mesh converts it to a form
		# suitable for rendering with a shader, with the point data written to GL buffers)
		self.model = Sphere().to_mesh()
		# attach a texture (stored in RGB format, no alpha) taken from the image file world.jpg
		self.model.texture = Texture("world.jpg", format=GL_RGB, flipped=True)

	def draw(self, time):
		""" Called repeatedly to render successive video frames """

		glClearColor(0, 0, 0, 1.0)  # solid black background
		glViewport(0, 0, self.width, self.height)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# Generate model-view matrix for a camera at (0, 0, -4) and write it to our
		# mv_matrix attribute
		mat4.lookAt(
			[0, 0, -4],  # eye
			[0, 0, 0],  # lookat
			[0, 1, 0],  # up
			self.mv_matrix)

		self.shader.use()  # select the active GL shader

		# transform the initial light location using our model-view matrix,
		# and pass the transformed location to the shader
		mat4.multiplyVec3(self.mv_matrix, self.light_location, self.transformed_light_location)
		self.shader.set_light_location(self.transformed_light_location)

		# rotate the model-view matrix by (time/2) radians about the Y axis,
		# to cause the globe to spin
		mat4.rotateY(self.mv_matrix, time / 2)
		self.shader.set_mvmatrix(self.mv_matrix)  # pass the rotated model-view matrix to the shader

		# form a normal matrix from the model-view matrix, and pass this to the shader
		mat4.toInverseMat3(self.mv_matrix, self.n_matrix)
		mat3.transpose(self.n_matrix)
		self.shader.set_nmatrix(self.n_matrix)

		self.shader.draw(self.model)  # draw the globe


# Create an instance of GlobeDemo and kick things off...
GlobeDemo().run()
