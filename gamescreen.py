import OpenGL.GL as gl
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

    def paintGL(self):
        """
        This is the function we'll override to draw to screen
        :return: None
        """
        # Currently just draws random quad
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslatef(0, 0, -5.0)
        gl.glColor3f(0, 1, 1)
        gl.glPolygonMode(gl.GL_BACK, gl.GL_LINE)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex3f(1.0, -1.2, 0.0)
        gl.glVertex3f(1.0, 0.0, 0.0)
        gl.glVertex3f(1.6, 0.0, 0.0)
        gl.glVertex3f(1.9, -1.2, 0.0)
        gl.glEnd()
        gl.glFlush()

    def initializeGL(self):
        """
        Here we will override in order to setup OpenGL how we want
        :return: None
        """
        gl.glClearDepth(1.0)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gluPerspective(45.0, 1.33, 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
