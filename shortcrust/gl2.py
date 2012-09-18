from shortcrust import has_glut

if has_glut:
	from shortcrust.glut.gl2 import *
else:
	from shortcrust.raspi.gl2 import *
