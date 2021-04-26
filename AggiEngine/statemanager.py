from typing import Callable

from PySide2.QtCore import QRunnable, Slot, QThreadPool
import PySide2
from .state import State
from .gamescreen import GameScreen

import time


class Physics(QRunnable):

    def __init__(self, fixedUpdate: Callable, state: State):
        QRunnable.__init__(self)
        self.fixedUpdate = fixedUpdate
        self.window = state.window
        self.state = state
        self.setAutoDelete(False)

    @Slot()  # QtCore.Slot
    def run(self) -> None:
        while self.state.active:
            start = time.perf_counter()
            self.fixedUpdate()
            self.window.fixedFrames += 1
            wait = self.window.fixedTiming - (time.perf_counter() - start)
            time.sleep(wait if wait > 0 else 0)


class Rendering(QRunnable):

    def __init__(self, update: Callable, state: State):
        QRunnable.__init__(self)
        self.update = update
        self.window = state.window
        self.state = state
        self.setAutoDelete(False)

    @Slot()  # QtCore.Slot
    def run(self) -> None:
        while self.state.active:
            start = time.perf_counter()
            self.update()
            if self.window.gameScreen:
                self.window.gameScreen.update()
            self.window.screenFrames += 1
            wait = self.window.screenTiming - (time.perf_counter() - start)
            time.sleep(wait if wait > 0 else 0)


class StateManager:

    def __init__(self, window: object, state: State):
        self.window = window
        self.currentState = state
        self.threadPool = QThreadPool()

    def changeState(self, state: State) -> None:
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

    def update(self) -> None:
        self.currentState.updateGOH()
        self.currentState.update()

    def fixedUpdate(self) -> None:
        self.currentState.fixedUpdateGOH()
        self.currentState.fixedUpdate()

    def initializeState(self) -> None:
        self.currentState.window = self.window  # Give the state a reference to the window
        self.currentState.loadUi()  # Load the states UI
        self.window.waitForLoad()

    def start(self) -> None:
        self.window.gameScreen = self.window.findChild(GameScreen)
        self.currentState.startGOH()
        self.currentState.start()  # Start the state
        self.threadPool.start(Physics(self.fixedUpdate, self.currentState))
        self.threadPool.start(Rendering(self.update, self.currentState))

    def exit(self) -> None:
        self.currentState.active = False
        self.currentState.exitGOH()
        self.currentState.exit()

    def keyPressed(self, event: PySide2.QtGui.QKeyEvent) -> None:
        self.currentState.keyPressed(event)
        self.currentState.gameObjectHandler.keyPressed(event)

    def keyReleased(self, event: PySide2.QtGui.QKeyEvent) -> None:
        self.currentState.keyReleased(event)
        self.currentState.gameObjectHandler.keyReleased(event)

    def mouseMoved(self, event: PySide2.QtGui.QMouseEvent) -> None:
        self.currentState.mouseMoved(event)
        self.currentState.gameObjectHandler.mouseMoved(event)

    def mousePressed(self, event: PySide2.QtGui.QMouseEvent) -> None:
        self.currentState.mousePressed(event)
        self.currentState.gameObjectHandler.mousePressed(event)

    def mouseReleased(self, event: PySide2.QtGui.QMouseEvent) -> None:
        self.currentState.mouseReleased(event)
        self.currentState.gameObjectHandler.mouseReleased(event)
