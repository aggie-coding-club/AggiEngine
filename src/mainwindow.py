import time

import PySide2
from PySide2.QtCore import QTimer, Qt
from PySide2.QtWidgets import QMainWindow

from .uimanager import UiManager
from .statemanager import StateManager
from .state import State
from .gamescreen import GameScreen


class MainWindow(QMainWindow):

    def __init__(self, app, state: State, screenFPS, fixedFPS, parent=None):
        """
        The MainWindow is created by the application, here we handle ui/scenes and send out updates.
        :param state: The current state we want to start with.
        :param parent: The widget this held under, None by default because this is top widget
        """
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

    def start(self):
        """
        Called to start the window
        :return: None
        """
        self.stateManager.initializeState()  # start the state
        self.updateFPSTimer.start(100)

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent):
        """
        Called when the window its closed
        :return: None
        """
        print("Window closed.")
        self.updateFPSTimer.stop()
        self.stateManager.exit()

    def __calculateFPS(self):
        """
        Averages FPS and adjust frame timings
        :return: None
        """

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

    def resizeEvent(self, event: PySide2.QtGui.QResizeEvent):
        if self.gameScreen:
            self.gameScreen.setGeometry(0, 0, self.width(), self.height())

    def keyPressEvent(self, event: PySide2.QtGui.QKeyEvent):
        self.stateManager.keyPressed(event)

    def keyReleaseEvent(self, event: PySide2.QtGui.QKeyEvent):
        self.stateManager.keyReleased(event)

    def mouseMoveEvent(self, event: PySide2.QtGui.QMouseEvent):
        self.stateManager.mouseMoved(event)

    def mousePressEvent(self, event: PySide2.QtGui.QMouseEvent):
        self.stateManager.mousePressed(event)

    def mouseReleaseEvent(self, event: PySide2.QtGui.QMouseEvent):
        self.stateManager.mouseReleased(event)

    def waitForLoad(self):
        QTimer(self).singleShot(0, self.stateManager.start)
