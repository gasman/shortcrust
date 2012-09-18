from .egl import EGL
import time


class BaseGLApp():
	depthbuffer = True

	def setup(self):
		pass

	def draw(self):
		pass

	def exit(self):
		self.exit_requested = True

	def on_exit(self):
		pass

	def run(self):
		self.exit_requested = False

		egl = EGL(depthbuffer=self.depthbuffer)
		self.width = egl.width
		self.height = egl.height
		self.aspect_ratio = float(self.width) / float(self.height)
		self.setup()

		start_time = time.time()
		while not self.exit_requested:
			self.draw(time.time() - start_time)
			egl.swap_buffers()
			# time.sleep(0.02)

		self.on_exit()
