class GameObject:

    def __init__(self, gameObjectHandler=None):
        self.body = None
        self.active = True
        self.window = None
        self.vertices = [[0, 0], [0.1, 0], [0.1, 0.1], [0, 0.1]]
        self.color = [1, 1, 1]
        self.position = [0, 0]
        self.rotation = 0
        self.gameObjectHandler = gameObjectHandler
        self.textureID = -1
        self.height = 0
        self.width = 0

    def start(self):
        pass

    def update(self):
        pass

    def fixedUpdate(self):
        pass

    def exit(self):
        pass

    def keyPressed(self, event):
        pass

    def keyReleased(self, event):
        pass

    def BeginContact(self, body):
        pass

    def EndContact(self, body):
        pass
    
    def PreSolve(self, contact, manifold):
        pass

    def PostSolve(self, contact, impulse):
        pass
    