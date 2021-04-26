from typing import Optional

import PySide2
from .gameobjecthandler import GameObjectHandler
from .tileloader import TileMap


class State:

    def __init__(self, ui_path: Optional[str] = None, window: Optional[object] = None):
        '''
        Initialized class variables.
        ``ui_path:`` The path to the .ui file for the State to display
        ``window:`` The main window class for the whole application
        '''
        self.ui_path = ui_path
        self.window = window
        self.gameObjectHandler = None
        self.active = True

    def loadMap(self, filePath: str) -> None:
        '''
        Loads the TMX file and creates the contained game objects
        ``filePath:`` The path to the .tmx file to load game objects
        '''
        TileMap(filePath, self.gameObjectHandler, self.window.gameScreen)

    def loadUi(self) -> None:
        '''
        Loads the widgets in the .ui file
        '''
        if self.ui_path is not None:
            self.window.uiManager.loadWidgets(self.ui_path, True)

    def startGOH(self) -> None:
        '''
        Starts the game object handler
        '''
        self.gameObjectHandler = GameObjectHandler(self.window)

    def updateGOH(self) -> None:
        '''
        Updates the game object handler after a screen draw
        '''
        self.gameObjectHandler.update()

    def fixedUpdateGOH(self) -> None:
        '''
        Updates the game object handler after a physics update
        '''
        self.gameObjectHandler.fixedUpdate()

    def exitGOH(self) -> None:
        '''
        Stops the game object handler
        '''
        self.gameObjectHandler.exit()

    def start(self) -> None:
        '''
        Triggered when the State is first activated
        '''
        pass

    def update(self) -> None:
        '''
        Triggered after a screen draw
        '''
        pass

    def fixedUpdate(self) -> None:
        '''
        Triggered after a physics update
        '''
        pass

    def exit(self) -> None:
        '''
        Triggered when the State stops
        '''
        pass

    def keyPressed(self, event: PySide2.QtGui.QKeyEvent) -> None:
        '''
        Triggered when a key is pressed down
        ``event:`` The key event contains the key(s) pressed
        '''
        pass

    def keyReleased(self, event: PySide2.QtGui.QKeyEvent) -> None:
        '''
        Triggered when a key is released
        ``event:`` The key event contains the key(s) released
        '''
        pass

    def mouseMoved(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Triggered when the mouse is moved
        ``event:`` The mouse event contains the new mouse positions
        '''
        pass

    def mousePressed(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Triggered when mouse buttons are pressed
        ``event:`` The mouse event contains the mouse buttons pressed
        '''
        pass

    def mouseReleased(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Triggered when mouse buttons are released
        ``event:`` The mouse event contains the mouse buttons released
        '''
        pass
