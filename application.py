from PySide2.QtWidgets import QApplication
from .mainwindow import MainWindow


class Application(QApplication):

    def __init__(self, state, args=None, screenFps=-1, fixedFps=60):
        """
        Creates and starts the application.
        :param state: The initial state to launch the Application with
        :param args: System arguments passed in
        :param config: Set application parameters
        """
        if args is not None:
            super(Application, self).__init__(args)
        else:
            super(Application, self).__init__()

        self.window = MainWindow(self, state, screenFps, fixedFps)

    def run(self):
        """
        Execute the application, this will start the state
        :return: None
        """
        self.window.start()
        self.window.show()
        self.exec_()
