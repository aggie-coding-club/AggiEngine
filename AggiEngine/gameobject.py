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
        '''
        Returns the width of the GameObject.
        '''
        return self.width * 2

    def getHeight(self) -> int:
        '''
        Returns the height.
        '''
        return self.height * 2

    def setWidth(self, width: int) -> None:
        '''
        Sets the GameObject's width.
        '''
        self.width = width / 2

    def setHeight(self, height: int) -> None:
        '''
        Sets the GameObject's height.
        '''
        self.height = height / 2

    def start(self) -> None:
        '''
        Called when the GameObject is created.
        '''
        pass

    def update(self) -> None:
        '''
        Called everytime the screen is rendered.
        '''
        pass

    def fixedUpdate(self) -> None:
        '''
        Called everytime Box2D finishes a physics update.
        '''
        pass

    def exit(self) -> None:
        '''
        Called when the GameObject is destroyed.
        '''
        pass

    def keyPressed(self, event: PySide2.QtGui.QKeyEvent) -> None:
        '''
        Called when a key is pushed down.
        '''
        pass

    def keyReleased(self, event: PySide2.QtGui.QKeyEvent) -> None:
        '''
        Called when a key is released.
        '''
        pass

    def mouseMoved(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Called when the cursor moves.
        '''
        pass

    def mousePressed(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Called when a mouse button is pressed.
        '''
        pass

    def mouseReleased(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Called when a mouse button is released.
        '''
        pass

    def beginContact(self, body: object) -> None:
        '''
        Called whenever a GameObject's object first makes contact with another body.
        '''
        pass

    def endContact(self, body: object) -> None:
        '''
        Called whenever a GameObject's object stops making contact with another.
        '''
        pass
    
    def preSolve(self, contact: b2Contact, manifold: b2Manifold) -> None:
        '''
        Called whenever a GameObject's body's shape is overlapping another.
        Gravity and other forces will trigger this even if the body hasn't stopped making contact.
        '''
        pass

    def postSolve(self, contact: b2Contact, impulse: b2Vec2) -> None:
        '''
        Called whenever a GameObject's body's shape is not longer overlapping another.
        Gravity and other forces will trigger this even if the body hasn't stopped making contact.
        '''
        pass
