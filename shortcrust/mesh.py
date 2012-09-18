from .gl2 import *


class Mesh(object):
    def __init__(self):
        self.vertex_count = len(self.vertices)
        self.vertex_size = len(self.vertices[0])

        vertices_flat = []
        for vertex in self.vertices:
            vertices_flat += vertex
        self.gl_vertices = GLfloats(vertices_flat)
        self.vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.gl_vertices, GL_STATIC_DRAW)

    def draw(self, vertex_position_attr):
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glVertexAttribPointer(vertex_position_attr, self.vertex_size, GL_FLOAT, GL_FALSE, 0, None)
        glDrawArrays(self.mode, 0, self.vertex_count)
