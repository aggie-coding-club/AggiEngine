import random

import OpenGL.arrays.vbo as glvbo
import OpenGL.GL as gl
import numpy as np
from OpenGL.GLU import *
from PySide2.QtWidgets import QOpenGLWidget


class GameScreen(QOpenGLWidget):

    def __init__(self, parent):
        """
        Subclass of the QOpenGLWidget, this is promoted in Qt Designer so that
        we can draw to the widget.
        :param parent: The widget that the this held under usually MainWindow
        """
        super(GameScreen, self).__init__(parent=parent)
        print("OpenGL widget created")

    def initializeGL(self):
        """
        Here we will override in order to setup OpenGL how we want
        :return: None
        """
        self.vertices = np.array([
            # <- x,y,z ----->  <- r,g,b -->
            -0.5, -0.2, 0.0, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
             0.5, 0.5,  0.0, 1.0, 0.0, 0.0,
             0.4, -0.2, 0.0, 0.0, 1.0, 0.0,
             1.4, -0.5, 0.0, 0.0, 1.0, 0.0,
             1.4, 0.5,  0.0, 0.0, 1.0, 0.0,
        ], 'f')

        self.vbo = glvbo.VBO(self.vertices)
        self.vbo.bind()

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        buffer_offset = ctypes.c_void_p
        stride = (3+3)*self.vertices.itemsize
        gl.glVertexPointer(3, gl.GL_FLOAT, stride, None)
        gl.glColorPointer(3, gl.GL_FLOAT, stride, buffer_offset(12))

        gl.glBindVertexArray(0)
        self.position = [0, 0, 0]

    def paintGL(self):
        """
        This is the function we'll override to draw to screen
        :return: None
        """
        self.position[0] -= 0.001
        print(self.position)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glLoadIdentity()
        gl.glTranslatef(self.position[0], 0, 0)
        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
        gl.glBindVertexArray(0)
