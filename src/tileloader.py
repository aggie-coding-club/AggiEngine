import pytmx
import Box2D
import importlib
from PIL import ImageColor
from .gameobject import GameObject


class TileMap:

    def __init__(self, tmxFile, gameObjectHandler, gameScreen):
        tiled_map = pytmx.TiledMap(tmxFile, image_loader=gameScreen.image_loader)
        if tiled_map.background_color:
            color = ImageColor.getcolor(tiled_map.background_color, 'RGB')
            gameScreen.bgColor = [color[0] / 255, color[1] / 255, color[2] / 255]

        hitboxes = {}
        objects = tiled_map.objects

        # Looks for objects and gets its vertices
        for obj in objects:
            pairPoints = []
            for pair in obj.points:
                pairPoints.append(
                    (-(pair[0] - obj.x) / gameObjectHandler.scale, -(pair[1] - obj.y) / gameObjectHandler.scale))
            hitboxes[obj.name] = pairPoints

        for layer in tiled_map:
            # Checks for layers with tiles
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    # Gets class name and gets class name definition
                    className = layer.properties.get('class', 'GameObject')

                    if className != 'GameObject':
                        className = getattr(importlib.import_module('__main__'), className)
                    else:
                        className = GameObject
                    # Sets up Texture
                    gm = className()
                    gm.textureID = image[0]

                    gm.setWidth(image[1] / gameObjectHandler.scale ** 2)
                    gm.setHeight(image[2] / gameObjectHandler.scale ** 2)

                    # Sets up Color
                    color = layer.properties.get('color', None)
                    if color:
                        color = ImageColor.getcolor(color, 'RGBA')
                        color = [color[2] / 255, color[1] / 255, color[0] / 255, color[3] / 255]
                        print(color)

                    # Sets up Hitbox
                    verticesName = layer.properties.get('hitboxName', None)

                    # Sets up Body Type
                    bodyType = layer.properties.get('bodyType', 'none')
                    if bodyType != 'none':
                        bodyDef = Box2D.b2BodyDef()
                        if bodyType == 'dynamic':
                            bodyDef.type = Box2D.b2_dynamicBody
                        elif bodyType == 'static':
                            bodyDef.type = Box2D.b2_staticBody
                        else:
                            bodyDef.type = Box2D.b2_kinematicBody
                        bodyDef.linearDamping = layer.properties.get('linearDamping', 0)
                        bodyDef.angularDamping = layer.properties.get('angularDamping', 0)
                        bodyDef.fixedRotation = layer.properties.get('fixedRotation', False)

                        # Linear Vel (Broken)
                        linearVel = layer.properties.get('linearVel', None)
                        if linearVel:
                            linearVel = [float(x) for x in linearVel.split(',')]
                            bodyDef.linearVelocity = (linearVel[0], linearVel[1])

                        # Sets up body Fixture
                        if verticesName:
                            bodyFixtureDef = Box2D.b2FixtureDef(
                                shape=Box2D.b2PolygonShape(vertices=hitboxes[verticesName]))
                        else:
                            bodyFixtureDef = Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(
                                box=((image[1] / gameObjectHandler.scale) / 2,
                                     (image[2] / gameObjectHandler.scale) / 2)))
                        bodyFixtureDef.density = layer.properties.get('density', 1)
                        bodyFixtureDef.friction = layer.properties.get('friction', 0)
                        bodyFixtureDef.restitution = layer.properties.get('restitution', 0)
                        # Sets up Position
                        bodyDef.position = (
                            -(x * tiled_map.tilewidth) / gameObjectHandler.scale,
                            -(y * tiled_map.tileheight) / gameObjectHandler.scale)
                        # adds box
                        if color:
                            gm.textureID = -1
                            gameObjectHandler.add(gm, bodyDef, bodyFixtureDef, color)
                        else:
                            gameObjectHandler.add(gm, bodyDef, bodyFixtureDef)
                    else:
                        gm.position = (-x / gameObjectHandler.scale, -y / gameObjectHandler.scale)
                        if color:
                            gm.textureID = -1
                            vertices = hitboxes[verticesName]
                            gm.vertices = [
                                (v[0] / gameObjectHandler.scale, v[1] / gameObjectHandler.scale) for v in vertices]
                            gameObjectHandler.add(gm, color=color)
                        else:
                            gameObjectHandler.add(gm)
