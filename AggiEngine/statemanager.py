from PySide2.QtCore import QRunnable, Slot, QThreadPool

from .state import State
from .gamescreen import GameScreen

import time


class Physics(QRunnable):

    def __init__(self, fixedUpdate, state):
        QRunnable.__init__(self)
        self.fixedUpdate = fixedUpdate
        self.window = state.window
        self.state = state
        self.setAutoDelete(False)

    @Slot()  # QtCore.Slot
    def run(self):
        while self.state.active:
            start = time.perf_counter()
            self.fixedUpdate()
            self.window.fixedFrames += 1
            wait = self.window.fixedTiming - (time.perf_counter() - start)
            time.sleep(wait if wait > 0 else 0)


class Rendering(QRunnable):

    def __init__(self, update, state):
        QRunnable.__init__(self)
        self.update = update
        self.window = state.window
        self.state = state
        self.setAutoDelete(False)

    @Slot()  # QtCore.Slot
    def run(self):
        while self.state.active:
            start = time.perf_counter()
            self.update()
            if self.window.gameScreen:
                self.window.gameScreen.update()
            self.window.screenFrames += 1
            wait = self.window.screenTiming - (time.perf_counter() - start)
            time.sleep(wait if wait > 0 else 0)


class StateManager:

    def __init__(self, window, state: State):
        self.window = window
        self.currentState = state
        self.threadPool = QThreadPool()

    def changeState(self, state: State):
        """
        Switch states
        :param state: The next state to show
        :return: None
        """

        self.currentState.active = False
        self.currentState.exitGOH()
        self.currentState.exit()
        self.currentState = state
        self.initializeState()

    def update(self):
        self.currentState.updateGOH()
        self.currentState.update()

    def fixedUpdate(self):
        self.currentState.fixedUpdateGOH()
        self.currentState.fixedUpdate()

    def initializeState(self):
        self.currentState.window = self.window  # Give the state a reference to the window
        self.currentState.loadUi()  # Load the states UI
        self.window.waitForLoad()

    def start(self):
        self.window.gameScreen = self.window.findChild(GameScreen)
        self.currentState.startGOH()
        self.currentState.start()  # Start the state
        self.threadPool.start(Physics(self.fixedUpdate, self.currentState))
        self.threadPool.start(Rendering(self.update, self.currentState))

    def exit(self):
        self.currentState.active = False
        self.currentState.exitGOH()
        self.currentState.exit()

    def keyPressed(self, event):
        self.currentState.keyPressed(event)
        self.currentState.gameObjectHandler.keyPressed(event)

    def keyReleased(self, event):
        self.currentState.keyReleased(event)
        self.currentState.gameObjectHandler.keyReleased(event)

    def mouseMoved(self, event):
        self.currentState.mouseMoved(event)
        self.currentState.gameObjectHandler.mouseMoved(event)

    def mousePressed(self, event):
        self.currentState.mousePressed(event)
        self.currentState.gameObjectHandler.mousePressed(event)

    def mouseReleased(self, event):
        self.currentState.mouseReleased(event)
        self.currentState.gameObjectHandler.mouseReleased(event)
