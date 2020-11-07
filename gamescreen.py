import OpenGL.GL as gl
import numpy
from PIL import Image
from PIL import ImageOps
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
        self.cameraScale = 1
        self.renderInfoList = []

    def initializeGL(self):
        """
        Here we will override in order to setup OpenGL how we want
        :return: None
        """
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        """
        This is the function we'll override to draw to screen
        :return: None
        """

        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glScalef(self.cameraScale, self.cameraScale, 0)
        gl.glTranslatef(-self.cameraPosition[0], -self.cameraPosition[1], 0)
        for renderInfo in self.renderInfoList:

            if renderInfo[0] == -1:
                gl.glPushMatrix()
                gl.glTranslatef(renderInfo[3][0], renderInfo[3][1], 0)
                gl.glRotatef(renderInfo[4], 0, 0, 1)
                gl.glColor3f(renderInfo[2][0], renderInfo[2][1], renderInfo[2][2])
                gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)
                gl.glBegin(gl.GL_POLYGON)
                for vertex in renderInfo[1]:
                    gl.glVertex3f(vertex[0], vertex[1], 0)
                gl.glEnd()
                gl.glFlush()
                gl.glPopMatrix()
            else:
                gl.glEnable(gl.GL_TEXTURE_2D)
                gl.glBindTexture(gl.GL_TEXTURE_2D, renderInfo[0])
                gl.glPushMatrix()
                gl.glTranslatef(renderInfo[3][0], renderInfo[3][1], 0)
                gl.glRotatef(renderInfo[4], 0, 0, 1)
                w = renderInfo[1] / 2.0
                h = renderInfo[2] / 2.0
                gl.glBegin(gl.GL_QUADS)
                gl.glTexCoord2f(0, 0)
                gl.glVertex2f(-w, -h)
                gl.glTexCoord2f(0, 1)
                gl.glVertex2f(w, -h)
                gl.glTexCoord2f(1, 1)
                gl.glVertex2f(w, h)
                gl.glTexCoord2f(1, 0)
                gl.glVertex2f(-w, h)
                gl.glEnd()
                gl.glFlush()
                gl.glPopMatrix()
                gl.glDisable(gl.GL_TEXTURE_2D)

    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = w / h
        gl.glOrtho(aspect, -aspect, -1.0, 1.0, 1.0, -1.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        print(w, h)

    def loadTexture(self, imageData, width, height):
        textureID = gl.glGenTextures(1)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 4)
        gl.glBindTexture(gl.GL_TEXTURE_2D, textureID)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BASE_LEVEL, 0)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAX_LEVEL, 0)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, imageData)
        return textureID

    def image_loader(self, filename, colorkey, **kwargs):
        image = Image.open(filename)

        def extract_image(rect, flags):
            # Cropping the image to the necessary size
            crop = image.crop((rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]))
            # Handling the flags
            if flags.flipped_horizontally:
                crop = ImageOps.mirror(crop)
            if flags.flipped_vertically:
                crop = ImageOps.flip(crop)
            
            # Making sure the images face the right direction
            crop = ImageOps.flip(crop)
            crop = crop.rotate(90)
            # Making image data for OpenGL
            imageData = numpy.array(list(crop.getdata()), numpy.uint8)
            return self.loadTexture(imageData, crop.width, crop.height)

        return extract_image

