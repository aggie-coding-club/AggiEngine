class State:

    def __init__(self, ui_path=None, window=None):
        self.ui_path = ui_path
        self.window = window

    def loadUi(self):
        if self.ui_path is not None:
            self.window.uiManager.loadWidgets(self.ui_path, True)

    def start(self):
        pass

    def update(self):
        pass

    def fixedUpdate(self):
        pass

    def exit(self):
        pass
