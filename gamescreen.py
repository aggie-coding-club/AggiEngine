import random
from collections import namedtuple

import OpenGL.arrays.vbo as glvbo
import OpenGL.GL as gl
import numpy as np
from OpenGL import GLU
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

        self.cameraPosition = [0, 0]
        self.renderInfoList = []

    def initializeGL(self):
        """
        Here we will override in order to setup OpenGL how we want
        :return: None
        """

    def paintGL(self):
        """
        This is the function we'll override to draw to screen
        :return: None
        """

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslatef(-self.cameraPosition[0], -self.cameraPosition[1], 0)
        for renderInfo in self.renderInfoList:
            gl.glPushMatrix()
            gl.glTranslatef(renderInfo[2][0], renderInfo[2][1], 0)
            gl.glRotatef(renderInfo[3], 0, 0, 1)
            gl.glColor3f(renderInfo[1][0], renderInfo[1][1], renderInfo[1][2])
            gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)
            gl.glBegin(gl.GL_POLYGON)
            for vertex in renderInfo[0]:
                gl.glVertex3f(vertex[0], vertex[1], 0)
            gl.glEnd()
            gl.glFlush()
            gl.glPopMatrix()

    def resizeGL(self, w:int, h:int):
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = w / h
        gl.glOrtho(aspect, -aspect, -1.0, 1.0, 1.0, -1.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

