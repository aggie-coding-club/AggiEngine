from OpenGL.GL import *
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
        self.bgColor = [0, 0, 0]

    def initializeGL(self):
        """
        Here we will override in order to setup OpenGL how we want
        :return: None
        """
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(self.bgColor[0], self.bgColor[1], self.bgColor[2], 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)
        print('OpenGL widget ready')

    def paintGL(self):
        """
        This is the function we'll override to draw to screen
        :return: None
        """

        glClearColor(self.bgColor[0], self.bgColor[1], self.bgColor[2], 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1, 1, 1)
        glLoadIdentity()
        glScalef(self.cameraScale, self.cameraScale, 0)
        glTranslatef(-self.cameraPosition[0], -self.cameraPosition[1], 0)
        for renderInfo in self.renderInfoList:

            if renderInfo[0] == -1:
                glPushMatrix()
                glTranslatef(renderInfo[3][0], renderInfo[3][1], 0)
                glRotatef(renderInfo[4], 0, 0, 1)
                glColor4f(renderInfo[2][0], renderInfo[2][1], renderInfo[2][2], renderInfo[2][3])
                glPolygonMode(GL_FRONT, GL_FILL)
                glBegin(GL_POLYGON)
                for vertex in renderInfo[1]:
                    glVertex2f(vertex[0], vertex[1])
                glEnd()
                glPopMatrix()
            else:
                glPushMatrix()
                glTranslatef(renderInfo[3][0], renderInfo[3][1], 0)
                glRotatef(renderInfo[4], 0, 0, 1)
                glBindTexture(GL_TEXTURE_2D, renderInfo[0])
                glBegin(GL_QUADS)
                glTexCoord2f(0, 0)
                glVertex2f(renderInfo[1], renderInfo[2])
                glTexCoord2f(1, 0)
                glVertex2f(-renderInfo[1], renderInfo[2])
                glTexCoord2f(1, 1)
                glVertex2f(-renderInfo[1], -renderInfo[2])
                glTexCoord2f(0, 1)
                glVertex2f(renderInfo[1], -renderInfo[2])
                glEnd()
                glBindTexture(GL_TEXTURE_2D, 0)
                glPopMatrix()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h
        glOrtho(aspect, -aspect, -1.0, 1.0, 1.0, -1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def loadTexture(self, imageData, width, height):
        textureID = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        glBindTexture(GL_TEXTURE_2D, textureID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
        return textureID

    def loadImageTexture(self, fileName):
        image = Image.open(fileName)

        # Add alpha if the base image doesn't have one
        if not (fileName.split(".")[-1] == "png"):
            image.putalpha(256)

        # Making image data for OpenGL
        imageData = numpy.array(list(image.getdata()), numpy.uint8)
        return self.loadTexture(imageData, image.width, image.height)

    def image_loader(self, filename, colorkey, **kwargs):
        image = Image.open(filename)
        transparent = filename.split(".")[-1] == "png"

        def extract_image(rect=None, flags=None):
            # Cropping the image to the necessary size
            if rect:
                crop = image.crop((rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]))
            else:
                crop = image

            if flags:
                # Handling the flags
                if flags.flipped_horizontally:
                    crop = ImageOps.mirror(crop)
                if flags.flipped_vertically:
                    crop = ImageOps.flip(crop)
            
            # Add alpha if the base image doesn't have one
            if not transparent:
                crop.putalpha(256)
            # Making image data for OpenGL
            imageData = numpy.array(list(crop.getdata()), numpy.uint8)
            return self.loadTexture(imageData, crop.width, crop.height), crop.width, crop.height

        return extract_image

