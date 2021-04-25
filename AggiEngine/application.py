from PySide2.QtWidgets import QApplication
from .mainwindow import MainWindow


class Application(QApplication):

    def __init__(self, state, screenFps=120, fixedFps=60, args=None):
        """
        Creates and starts the application.
        :param state: The initial state to launch the Application with
        :param args: System arguments passed in
        :param config: Set application parameters
        """
        if args:
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
