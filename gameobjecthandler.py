from AggiEngine.contactlistener import ContactListener
import math

from Box2D import *


class GameObjectHandler:

    def __init__(self, window, scale=16):
        self.timing = 1 / window.targetFixedFPS
        self.window = window
        
        self.world = Box2D.b2World(gravity=(0, -9.8))  # create instance of box 2d world
        self.world.contactListener = ContactListener()
        
        self.scale = scale  # scaling parameter, is equal to pixels to meter
        self.gameObjects = []  # game object list

    def setScale(self, scale):
        self.scale = scale

    def update(self):
        for gameObject in self.gameObjects:
            if gameObject.active:
                gameObject.update()

    def fixedUpdate(self):
        self.world.Step(self.timing, 6, 2)
        self.world.ClearForces()

        newRenderInfoList = []
        for gameObject in self.gameObjects:
            info = [gameObject.textureID]

            if gameObject.textureID == -1:
                info += [gameObject.vertices, gameObject.color]
            else:
                info += [gameObject.width, gameObject.height]

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
        gameObject.gameObjectHandler = self

        if bodyDef:
            body = self.world.CreateBody(bodyDef)
            body.CreateFixture(bodyFixtureDef)
            gameObject.body = body
            gameObject.body.userData = gameObject

            gameObject.body.userData = gameObject

            if type(bodyFixtureDef.shape) is b2PolygonShape:
                gameObject.vertices.clear()
                for vertex in bodyFixtureDef.shape.vertices:
                    gameObject.vertices.append([vertex[0] / self.scale, vertex[1] / self.scale])
            elif type(bodyFixtureDef.shape) is b2CircleShape:
                vertices = []
                for i in range(0, 30):
                    rad = (2 * math.pi * i) / 30
                    r = bodyFixtureDef.shape.radius / self.scale
                    vertices.append([(r * math.cos(rad) - (bodyFixtureDef.shape.pos[0] / self.scale)),
                                     (r * math.sin(rad) - (bodyFixtureDef.shape.pos[1] / self.scale))])
                gameObject.vertices = vertices

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
