import time
from typing import Optional

import PySide2
from PySide2.QtCore import QTimer, Qt
from PySide2.QtWidgets import QMainWindow, QWidget

from .uimanager import UiManager
from .statemanager import StateManager
from .state import State
from .gamescreen import GameScreen


class MainWindow(QMainWindow):

    def __init__(self, app, state: State, screenFPS: int, fixedFPS: int, parent: Optional[QWidget] = None):
        '''
        The MainWindow is created by the application, here we handle ui/scenes and send out updates.
        ``state:`` The current state we want to start with.  
        ``parent:`` The widget this held under, None by default because this is top widget  
        '''
        QMainWindow.__init__(self, parent)
        self.app = app  # the application created
        self.gameScreen = None  # where all graphics are drawn
        self.uiManager = UiManager(self, customWidgets=[GameScreen])  # Loads widgets into window from a file
        self.stateManager = StateManager(self, state)  # Manages state updates and transitions

        self.updateFPSTimer = QTimer(self)  # Used to manage frame timings
        self.updateFPSTimer.timeout.connect(self.__calculateFPS)

        self.fixedFps = 0  # Calculated FPS
        self.screenFps = 0

        self.fixedFrames = 0  # Accumulated Frames
        self.screenFrames = 0

        self.targetFixedFPS = fixedFPS
        self.targetUpdateFPS = screenFPS
        self.fixedTiming = 1 / self.targetFixedFPS
        self.screenTiming = 1 / self.targetUpdateFPS
        self.fixedNeeded = fixedFPS
        self.screenNeeded = screenFPS
        self.lastTime = 0
        self.setMouseTracking(True)

        self.uiManager.keepWidgets = self.children()

    def start(self) -> None:
        '''
        Called when application.run() is executed. Starts the actual engine.
        '''
        self.stateManager.initializeState()  # start the state
        self.updateFPSTimer.start(100)

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent) -> None:
        '''
        Called when the window is closed
        '''
        print("Window closed.")
        self.updateFPSTimer.stop()
        self.stateManager.exit()

    def __calculateFPS(self) -> None:
        '''
        Averages FPS and adjust frame timings to meet the targets
        '''

        self.fixedFps = self.fixedFrames / (time.perf_counter() - self.lastTime)
        self.fixedFrames = 0

        self.screenFps = self.screenFrames / (time.perf_counter() - self.lastTime)
        self.screenFrames = 0

        if -0.5 < (self.targetFixedFPS - self.fixedFps) / self.targetFixedFPS < 0.5 and self.fixedNeeded > 30:
            self.fixedNeeded += (self.targetFixedFPS - self.fixedFps) * 0.25
            self.fixedTiming = 1 / self.fixedNeeded

        if -0.5 < (self.screenNeeded - self.screenFps) / self.targetUpdateFPS < 0.5 and self.screenNeeded > 30:
            self.screenNeeded += (self.targetUpdateFPS - self.screenFps) * 0.15
            self.screenTiming = 1 / self.screenNeeded

        self.lastTime = time.perf_counter()

    def resizeEvent(self, event: PySide2.QtGui.QResizeEvent) -> None:
        '''
        Triggered when the screen is resized and passes down the event.
        '''
        if self.gameScreen:
            self.gameScreen.setGeometry(0, 0, self.width(), self.height())

    def keyPressEvent(self, event: PySide2.QtGui.QKeyEvent) -> None:
        '''
        Triggered when a key is pressed and passes down the event.
        '''
        self.stateManager.keyPressed(event)

    def keyReleaseEvent(self, event: PySide2.QtGui.QKeyEvent) -> None:
        '''
        Triggered when a key is released and passes down the event.
        '''
        self.stateManager.keyReleased(event)

    def mouseMoveEvent(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Triggered when the mouse is moved and passes down the event.
        '''
        self.stateManager.mouseMoved(event)

    def mousePressEvent(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Triggered when a mouse key is pressed and passes down the event.
        '''
        self.stateManager.mousePressed(event)

    def mouseReleaseEvent(self, event: PySide2.QtGui.QMouseEvent) -> None:
        '''
        Triggered when a mouse key is released and passes down the event.
        '''
        self.stateManager.mouseReleased(event)

    def waitForLoad(self) -> None:
        '''
        Makes state manager wait until the current state finishes loading widgets.
        '''
        QTimer(self).singleShot(0, self.stateManager.start)
