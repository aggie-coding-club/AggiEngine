import pytmx
import Box2D
import importlib
from .gameobject import GameObject


class TileMap:

    def __init__(self, tmxFile, gameObjectHandler, gameScreen):
        tiled_map = pytmx.TiledMap(tmxFile, image_loader=gameScreen.image_loader)
        hitboxes = {}
        objects = tiled_map.objects

        #Looks for objects and gets its vertices
        for obj in objects:
            pairPoints = []
            for pair in obj.points:
                pairPoints.append((-(pair[0]-obj.x)/gameObjectHandler.scale,-(pair[1]-obj.y)/gameObjectHandler.scale))
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
                    gm.width = image[1] / gameObjectHandler.scale ** 2
                    gm.height = image[2] / gameObjectHandler.scale ** 2

                    # Sets up Body Type
                    bodyDef = Box2D.b2BodyDef()
                    bodyType = layer.properties.get('bodyType', 'static')
                    if bodyType=='dynamic':
                        bodyDef.type = Box2D.b2_dynamicBody
                    elif bodyType=='static':
                        bodyDef.type = Box2D.b2_staticBody
                    else:
                        bodyDef.type = Box2D.b2_kinematicBody
                    bodyDef.linearDamping = layer.properties.get('linearDamping',0)
                    bodyDef.angularDamping = layer.properties.get('angularDamping',0.01)
                    
                    # Linear Vel (Broken)
                    linearVel = layer.properties.get('linearVel',None)
                    if linearVel:
                        linearVel=linearVel.split(',')
                        linearVel =  [float(x) for x in linearVel]
                        bodyDef.linearVelocity = (linearVel[0],bodyDef.linearVelocity.x)
                        bodyDef.linearVelocity = (linearVel[1],bodyDef.linearVelocity.y)
            
                    # Sets up body Fixture
                    verticesName = layer.properties.get('hitboxName',0)
                    if verticesName:
                        vertices = hitboxes[verticesName]
                        bodyFixtureDef = Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(vertices=vertices))
                        gm.textureID = -1 # Temporary
                    else:
                        bodyFixtureDef = Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(
                            box=((image[1] / gameObjectHandler.scale) / 2,
                                (image[2] / gameObjectHandler.scale) / 2)))
                    bodyFixtureDef.density = layer.properties.get('density', 1)
                    bodyFixtureDef.friction = layer.properties.get('friction',0)
                    bodyFixtureDef.restitution = layer.properties.get('restitution',0)
                    # Sets up Position
                    bodyDef.position = (
                        -(x*tiled_map.tilewidth) / gameObjectHandler.scale,
                        -(y*tiled_map.tileheight) / gameObjectHandler.scale)
                    # adds box
                    gameObjectHandler.add(gm, bodyDef, bodyFixtureDef)
                    