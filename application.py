from collections import namedtuple
from PySide2.QtWidgets import QApplication
from .mainwindow import MainWindow


class Application(QApplication):
    Config = namedtuple('Config', ['screenFPS', 'fixedFPS'])

    def __init__(self, state, args=None, config: Config = None):
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

        self.__config = config
        if self.__config is None:
            self.__config = self.Config(screenFPS=120, fixedFPS=50)

        self.window = MainWindow(self, state, self.__config.screenFPS, self.__config.fixedFPS)

    def run(self):
        """
        Execute the application, this will start the state
        :return: None
        """
        self.window.start()
        self.window.show()
        self.exec_()
