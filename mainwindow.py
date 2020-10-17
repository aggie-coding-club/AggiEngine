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

        self.updateTimer = QTimer(self)  # Used to create update calls
        self.updateTimer.setTimerType(Qt.PreciseTimer)
        self.updateTimer.timeout.connect(self.__updateHandler)

        self.updateFPSTimer = QTimer(self)  # Used to manage frame timings
        self.updateFPSTimer.timeout.connect(self.__calculateFPS)

        self.lastScreen = 0  # Last frame time
        self.lastFixed = 0

        self.fixedFps = 0  # Calculated FPS
        self.screenFps = 0

        self.fixedTime = 0  # Accumulated Time
        self.screenTime = 0

        self.fixedFrames = 1  # Accumulated Frames
        self.screenFrames = 1

        self.targetfixedFPS = fixedFPS
        self.targetscreenFPS = screenFPS
        self.fixedTiming = 1 / fixedFPS  # seconds / frames per second
        self.screenTiming = 1 / screenFPS
        self.avgscreenTime = 0  # Average amount of time it takes the screen to update includes state update

    def start(self):
        """
        Called to start the window
        :return: None
        """
        self.stateManager.start()  # start the state

        self.updateTimer.start(0)  # start game loops
        self.updateFPSTimer.start(100)  # start frame timing management

    def __updateHandler(self):
        """
        In here fixed and scene updates are made based on timing
        :return: None
        """
        start = time.perf_counter()  # start time of the update call
        if time.perf_counter() - self.lastFixed > self.fixedTiming:  # Has enough time passed for next call
            self.__fixedUpdate()
            self.fixedFrames += 1

        now = time.perf_counter()  # Time after physics has been calculated
        if (now - start) < (self.fixedTiming - self.avgscreenTime):  # Is there enough time left to call update
            if (now - self.lastScreen) >= self.screenTiming:  # Has enough time passed for next call
                if self.gameScreen is not None:
                    self.gameScreen.update()
                self.__stateUpdate()
                self.screenFrames += 1

        self.avgscreenTime = (self.avgscreenTime + (time.perf_counter() - now)) / 2  # How long the state update took

    def __stateUpdate(self):
        self.screenTime += 1 / (time.perf_counter() - self.lastScreen)
        self.lastScreen = time.perf_counter()
        self.stateManager.update()

    def __fixedUpdate(self):
        self.fixedTime += 1 / (time.perf_counter() - self.lastFixed)
        self.lastFixed = time.perf_counter()
        self.stateManager.fixedUpdate()

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent):
        """
        Called when the window its closed
        :return: None
        """
        print("Window closed.")
        self.updateTimer.stop()
        self.updateFPSTimer.stop()
        self.stateManager.exit()

    def __calculateFPS(self):
        """
        Averages FPS and adjust frame timings
        :return: None
        """
        self.fixedFps = self.fixedTime / self.fixedFrames
        self.fixedTime = 0
        self.fixedFrames = 1

        self.screenFps = self.screenTime / self.screenFrames
        self.screenTime = 0
        self.screenFrames = 1

        self.fixedTiming += 0.001 * ((self.fixedFps - self.targetfixedFPS) / self.targetfixedFPS)
        self.screenTiming += 0.001 * ((self.screenFps - self.targetscreenFPS) / self.targetscreenFPS)

    def resizeEvent(self, event:PySide2.QtGui.QResizeEvent):
        self.gameScreen: GameScreen
        if self.gameScreen is not None:
            self.gameScreen.setGeometry(0, 0, self.width(), self.height())

    def keyPressEvent(self, event:PySide2.QtGui.QKeyEvent):
        self.stateManager.keyPressed(event)

    def keyReleaseEvent(self, event:PySide2.QtGui.QKeyEvent):
        self.stateManager.keyReleased(event)

