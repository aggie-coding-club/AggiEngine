import sys

from gameobjecthandler import GameObjectHandler


class State:

    def __init__(self, ui_path=None, window=None):
        self.ui_path = ui_path
        self.window = window
        self.gameObjectHandler = None

    def loadUi(self):
        if self.ui_path is not None:
            self.window.uiManager.loadWidgets(self.ui_path, True)

    def startGOH(self):
        self.gameObjectHandler = GameObjectHandler(self.window)

    def updateGOH(self):
        self.gameObjectHandler.update()

    def fixedUpdateGOH(self):
        self.gameObjectHandler.updateFixed()

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
