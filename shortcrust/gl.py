from shortcrust import has_glut

if has_glut:
	from shortcrust.glut.gl import *
else:
	from shortcrust.raspi.gl import *
