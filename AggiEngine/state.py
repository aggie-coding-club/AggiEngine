from typing import Optional

import PySide2
from .gameobjecthandler import GameObjectHandler
from .tileloader import TileMap


class State:

    def __init__(self, ui_path: Optional[str] = None, window: Optional[object] = None):
        self.ui_path = ui_path
        self.window = window
        self.gameObjectHandler = None
        self.active = True

    def loadMap(self, filePath: str) -> None:
        TileMap(filePath, self.gameObjectHandler, self.window.gameScreen)

    def loadUi(self) -> None:
        if self.ui_path is not None:
            self.window.uiManager.loadWidgets(self.ui_path, True)

    def startGOH(self) -> None:
        self.gameObjectHandler = GameObjectHandler(self.window)

    def updateGOH(self) -> None:
        self.gameObjectHandler.update()

    def fixedUpdateGOH(self) -> None:
        self.gameObjectHandler.fixedUpdate()

    def exitGOH(self) -> None:
        self.gameObjectHandler.exit()

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
