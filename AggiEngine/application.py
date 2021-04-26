from typing import Optional

from PySide2.QtWidgets import QApplication

from . import State
from .mainwindow import MainWindow


class Application(QApplication):
    """
    This is the core class of an AggiEngine application.
    """

    def __init__(self, state: State, screenFps: Optional[float] = 120, fixedFps: Optional[float] = 60,
                 args: Optional[list] = None) -> None:
        """
        Creates and initializes QWidgets for the application to start.
        ``state:`` The initial state to launch the Application with    
        ``args:`` System arguments passed in    
        ``config:`` Set application parameters    
        """
        if args:
            super(Application, self).__init__(args)
        else:
            super(Application, self).__init__()

        self.window = MainWindow(self, state, screenFps, fixedFps)

    def run(self) -> None:
        """
        Execute the application, this will start the passed State
        """
        self.window.start()
        self.window.show()
        self.exec_()
