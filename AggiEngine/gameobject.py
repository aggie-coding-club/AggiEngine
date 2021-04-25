class GameObject:

    def __init__(self, gameObjectHandler=None):
        self.body = None
        self.active = True
        self.window = None
        self.vertices = [[0, 0], [0.1, 0], [0.1, 0.1], [0, 0.1]]
        self.color = [1, 1, 1, 1]
        self.position = [0, 0]
        self.rotation = 0
        self.gameObjectHandler = gameObjectHandler
        self.textureID = -1
        self.height = 1
        self.width = 1

    def getWidth(self):
        return self.width * 2

    def getHeight(self):
        return self.height * 2

    def setWidth(self, width):
        self.width = width / 2

    def setHeight(self, height):
        self.height = height / 2

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

    def mouseMoved(self, event):
        pass

    def mousePressed(self, event):
        pass

    def mouseReleased(self, event):
        pass

    def beginContact(self, body):
        pass

    def endContact(self, body):
        pass
    
    def preSolve(self, contact, manifold):
        pass

    def postSolve(self, contact, impulse):
        pass
