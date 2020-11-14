from .gameobjecthandler import GameObjectHandler
from .tileloader import TileMap


class State:

    def __init__(self, ui_path=None, window=None):
        self.ui_path = ui_path
        self.window = window
        self.gameObjectHandler = None
        self.active = True

    def loadMap(self, filePath):
        TileMap(filePath, self.gameObjectHandler, self.window.gameScreen)

    def loadUi(self):
        if self.ui_path is not None:
            self.window.uiManager.loadWidgets(self.ui_path, True)

    def startGOH(self):
        self.gameObjectHandler = GameObjectHandler(self.window)

    def updateGOH(self):
        self.gameObjectHandler.update()

    def fixedUpdateGOH(self):
        self.gameObjectHandler.fixedUpdate()

    def exitGOH(self):
        self.gameObjectHandler.exit()

    def start(self):
        pass

    def update(self):
        pass

    def fixedUpdate(self):
        pass

    def exit(self):
        pass

    def keyPressed(self, event):
        pass

    def keyReleased(self, event):
        pass

    def mouseMoved(self, event):
        pass

    def mousePressed(self, event):
        pass

    def mouseReleased(self, event):
        pass
