try:
	from OpenGL import GLUT
	has_glut = True
	from shortcrust.glut.basegl import BaseGLApp
except ImportError:
	has_glut = False
	try:
		from shortcrust.raspi.basegl import BaseGLApp
	except OSError:
		raise ImportError("*** No OpenGL support found. ***\nOn Raspberry Pi, ensure that the GL libraries are present in /opt/vc/lib;\nfor other platforms, you need to install PyOpenGL.")
