import math

from Box2D import *


class GameObjectHandler:

    def __init__(self, window, scale=128):
        self.timing = window.targetfixedFPS
        self.window = window
        self.world = Box2D.b2World(gravity=(0, -98))  # create instance of box 2d world
        self.scale = scale  # scaling parameter, is equal to pixels to meter
        self.gameObjects = []  # game object list

    def setScale(self, scale):
        self.scale = scale

    def update(self):
        for gameObject in self.gameObjects:
            if gameObject.active:
                gameObject.update()

    def fixedUpdate(self):
        self.world.Step(1 / self.timing, 6, 2)
        self.world.ClearForces()

        newRenderInfoList = []
        for gameObject in self.gameObjects:
            info = [gameObject.vertices, gameObject.color]
            if gameObject.active:
                gameObject.fixedUpdate()
                if gameObject.body is not None:
                    gameObject.position = gameObject.body.position / self.scale
                    gameObject.rotation = gameObject.body.angle
                info += [gameObject.position, math.degrees(gameObject.rotation)]
            newRenderInfoList.append(info)
        if self.window.gameScreen is not None:
            self.window.gameScreen.renderInfoList = newRenderInfoList

    def add(self, gameObject, bodyDef=None, bodyFixtureDef=None, color=None):
        self.gameObjects.append(gameObject)  # adds game object to list of game objects

        if bodyDef is not None:
            body = self.world.CreateBody(bodyDef)
            body.CreateFixture(bodyFixtureDef)
            gameObject.body = body

            if type(bodyFixtureDef.shape) is b2PolygonShape:
                gameObject.vertices.clear()
                for vertex in bodyFixtureDef.shape.vertices:
                    gameObject.vertices.append([vertex[0] / self.scale, vertex[1] / self.scale])

            if color is None:
                gameObject.color = [1, 1, 1]
            else:
                gameObject.color = color
            gameObject.position = body.position / self.scale

        gameObject.window = self.window
        gameObject.start()

    def exit(self):
        pass

    def keyPressed(self, event):
        for gameObject in self.gameObjects:
            gameObject.keyPressed(event)

    def keyReleased(self, event):
        for gameObject in self.gameObjects:
            gameObject.keyReleased(event)
