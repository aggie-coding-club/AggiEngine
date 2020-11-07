import pytmx
import Box2D
import importlib
from .gameobject import GameObject


class TileMap:

    def __init__(self, tmxFile, gameObjectHandler, gameScreen):
        tiled_map = pytmx.TiledMap(tmxFile, image_loader=gameScreen.image_loader)
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

                    gm = className()
                    gm.textureID = image[0]
                    gm.width = image[1] / gameObjectHandler.scale ** 2
                    gm.height = image[2] / gameObjectHandler.scale ** 2
                    # create box
                    bodyDef = Box2D.b2BodyDef()
                    dynamic = layer.properties.get('dynamic', 0)
                    if dynamic:
                        bodyDef.type = Box2D.b2_dynamicBody
                    else:
                        bodyDef.type = Box2D.b2_staticBody
              
                    bodyFixtureDef = Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(
                        box=((image[1] / gameObjectHandler.scale) / 2,
                             (image[2] / gameObjectHandler.scale) / 2)))
                    bodyFixtureDef.density = layer.properties.get('density', 1)

                    bodyDef.position = (
                        -(x*tiled_map.tilewidth) / gameObjectHandler.scale,
                        -(y*tiled_map.tileheight) / gameObjectHandler.scale)
                    # adds box
                    gameObjectHandler.add(gm, bodyDef, bodyFixtureDef)
