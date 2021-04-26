from typing import Optional
import PySide2
from Box2D import b2Contact, b2Vec2, b2Manifold


class GameObject:

    def __init__(self, gameObjectHandler: Optional[object] = None):
        self.body = None
        self.active = True
        self.window = None
        self.vertices = [[0, 0], [0.1, 0], [0.1, 0.1], [0, 0.1]]
        self.color = [1, 1, 1, 1]
        self.position = [0, 0]
        self.rotation = 0
        self.gameObjectHandler = gameObjectHandler
        self.textureID = -1
        self.height = 1
        self.width = 1

    def getWidth(self) -> int:
        """
        Returns the width of the GameObject
        :return: Returns a float of the width of the game object
        """
        return self.width * 2

    def getHeight(self) -> int:
        """
        Returns the height
        :return: float height of the game object
        """
        return self.height * 2

    def setWidth(self, width: int) -> None:
        self.width = width / 2

    def setHeight(self, height: int) -> None:
        self.height = height / 2

    def start(self) -> None:
        pass

    def update(self) -> None:
        pass

    def fixedUpdate(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def keyPressed(self, event: PySide2.QtGui.QKeyEvent) -> None:
        pass

    def keyReleased(self, event: PySide2.QtGui.QKeyEvent) -> None:
        pass

    def mouseMoved(self, event: PySide2.QtGui.QMouseEvent) -> None:
        pass

    def mousePressed(self, event: PySide2.QtGui.QMouseEvent) -> None:
        pass

    def mouseReleased(self, event: PySide2.QtGui.QMouseEvent) -> None:
        pass

    def beginContact(self, body: object) -> None:
        pass

    def endContact(self, body: object) -> None:
        pass
    
    def preSolve(self, contact: b2Contact, manifold: b2Manifold) -> None:
        pass

    def postSolve(self, contact: b2Contact, impulse: b2Vec2) -> None:
        pass
