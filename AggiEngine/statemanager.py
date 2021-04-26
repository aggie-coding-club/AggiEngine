from typing import Callable

from PySide2.QtCore import QRunnable, Slot, QThreadPool
import PySide2
from .state import State
from .gamescreen import GameScreen

import time


class Physics(QRunnable):

    def __init__(self, fixedUpdate: Callable, state: State):
        '''
        Runs all physics related events on a separate loop and thread.
        ``fixedUpdate:`` State Managers fixedUpdate function
        ``state:`` The current state loaded
        '''
        QRunnable.__init__(self)
        self.fixedUpdate = fixedUpdate
        self.window = state.window
        self.state = state
        self.setAutoDelete(False)

    @Slot()  # QtCore.Slot
    def run(self) -> None:
        '''
        Starts the physics loop
        '''
        while self.state.active:
            start = time.perf_counter()
            self.fixedUpdate()
            self.window.fixedFrames += 1
            wait = self.window.fixedTiming - (time.perf_counter() - start)
            time.sleep(wait if wait > 0 else 0)


class Rendering(QRunnable):

    def __init__(self, update: Callable, state: State):
        '''
        Runs all rendering related events on a separate loop and thread.
        ``update:`` State Managers update function
        ``state:`` The current state loaded
        '''
        QRunnable.__init__(self)
        self.update = update
        self.window = state.window
        self.state = state
        self.setAutoDelete(False)

    @Slot()  # QtCore.Slot
    def run(self) -> None:
        '''
        Starts the rendering loop
        '''
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
        '''
        ``window:`` The main window class on the application
        ``state:`` The initial state to be displayed
        '''
        self.window = window
        self.currentState = state
        self.threadPool = QThreadPool()

    def changeState(self, state: State) -> None:
        '''
        Switch states
        ``state:`` The next state to show  
        '''
        self.currentState.active = False
        self.currentState.exitGOH()
        self.currentState.exit()
        self.currentState = state
        self.initializeState()

    def update(self) -> None:
        '''
        Triggered after a frame draw
        '''
        self.currentState.updateGOH()
        self.currentState.update()

    def fixedUpdate(self) -> None:
        '''
        Triggered after a physics update
        '''
        self.currentState.fixedUpdateGOH()
        self.currentState.fixedUpdate()

    def initializeState(self) -> None:
        '''
        Prepares State for execution
        '''
        self.currentState.window = self.window  # Give the state a reference to the window
        self.currentState.loadUi()  # Load the states UI
        self.window.waitForLoad()

    def start(self) -> None:
        '''
        Starts game loops and starts the State
        '''
        self.window.gameScreen = self.window.findChild(GameScreen)
        self.currentState.startGOH()
        self.currentState.start()  # Start the state
        self.threadPool.start(Physics(self.fixedUpdate, self.currentState))
        self.threadPool.start(Rendering(self.update, self.currentState))

    def exit(self) -> None:
        '''
        Stops the State
        '''
        self.currentState.active = False
        self.currentState.exitGOH()
        self.currentState.exit()

    def keyPressed(self, event: PySide2.QtGui.QKeyEvent) -> None:
        '''
        Triggered when a key is pressed down
        ``event:`` The key event contains the key(s) pressed
        '''
        self.currentState.keyPressed(event)
        self.currentState.gameObjectHandler.keyPressed(event)

    def keyReleased(self, event: PySide2.QtGui.QKeyEvent) -> None:
        '''
        Triggered when a key is released
        ``event:`` The key event contains the key(s) released
        '''
        self.currentState.keyReleased(event)
        self.currentState.gameObjectHandler.keyReleased(event)

    def mouseMoved(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Triggered when the mouse is moved
        ``event:`` The mouse event contains the new mouse positions
        '''
        self.currentState.mouseMoved(event)
        self.currentState.gameObjectHandler.mouseMoved(event)

    def mousePressed(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Triggered when mouse buttons are pressed
        ``event:`` The mouse event contains the mouse buttons pressed
        '''
        self.currentState.mousePressed(event)
        self.currentState.gameObjectHandler.mousePressed(event)

    def mouseReleased(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Triggered when mouse buttons are released
        ``event:`` The mouse event contains the mouse buttons released
        '''
        self.currentState.mouseReleased(event)
        self.currentState.gameObjectHandler.mouseReleased(event)
