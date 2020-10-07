class GameObject:

    def __init__(self):
        self.body = None
        self.active = True
        self.vertices = [[0, 0], [0.1, 0], [0.1, 0.1], [0, 0.1]]
        self.color = [1, 1, 1]
        self.position = [0, 0]
        self.rotation = 0

    def start(self):
        pass

    def update(self):
        pass

    def fixedUpdate(self):
        pass

    def exit(self):
        pass
