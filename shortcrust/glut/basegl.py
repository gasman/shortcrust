import sys
import time
from OpenGL.GLUT import *


class BaseGLApp():
	# Some api in the chain is translating the keystrokes to this octal string
	# so instead of saying: ESCAPE = 27, we use the following.
	ESCAPE = '\033'

	title = "Shortcrust OpenGL framework - Gasman 2012"
	fullscreen = False

	def __init__(self):
		# Number of the glut window.
		self.window = 0
		self.width = 1024
		self.height = 768
		self.aspect_ratio = float(self.width) / float(self.height)

	def setup(self):
		pass

	def draw(self, time_ms):
		pass

	def on_exit(self):
		pass

	def run(self):
		# For now we just pass glutInit one empty argument. I wasn't sure what should or could be passed in (tuple, list, ...)
		# Once I find out the right stuff based on reading the PyOpenGL source, I'll address this.
		glutInit(sys.argv)

		# Select type of Display mode:
		#  Double buffer
		#  RGBA color
		# Alpha components supported
		# Depth buffer
		glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

		if self.fullscreen:
			glutGameModeString("%dx%d:32@75" % (self.width, self.height))
			glutEnterGameMode()
			glutSetCursor(GLUT_CURSOR_NONE)
		else:
			# get a window of the requested size
			glutInitWindowSize(self.width, self.height)

			# the window starts at the upper left corner of the screen
			glutInitWindowPosition(0, 0)

			# Okay, like the C version we retain the window id to use when closing, but for those of you new
			# to Python (like myself), remember this assignment would make the variable local and not global
			# if it weren't for the global declaration at the start of main.
			self.window = glutCreateWindow(self.title)

		def draw():
			self.draw(time.time() - start_time)
			#  since this is double buffered, swap the buffers to display what just got drawn.
			glutSwapBuffers()

		# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
		# set the function pointer and invoke a function to actually register the callback, otherwise it
		# would be very much like the C version of the code.
		glutDisplayFunc(draw)

		# When we are doing nothing, redraw the scene.
		glutIdleFunc(draw)

		# Register the function called when our window is resized.
		# glutReshapeFunc(ReSizeGLScene)

		# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
		def keyPressed(*args):
			# If escape is pressed, kill everything.
			if args[0] == BaseGLApp.ESCAPE:
				self.exit()
		# Register the function called when the keyboard is pressed.
		glutKeyboardFunc(keyPressed)

		# Initialize our window.
		self.setup()

		# Start Event Processing Engine
		start_time = time.time()
		glutMainLoop()

	def exit(self):
		self.on_exit()
		sys.exit()
