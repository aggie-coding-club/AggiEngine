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
                    # className = layer.properties.get('class-name', 'GameObject')
                    # print(className)
                    # className = getattr(importlib.import_module('__main__'), className)
                    className = GameObject
                    gm = GameObject()
                    gm.textureID = image
                    gm.width = tiled_map.tilewidth / gameObjectHandler.scale
                    gm.height = tiled_map.tileheight / gameObjectHandler.scale
                    # create box
                    bodyDef = Box2D.b2BodyDef()
                    if layer.properties['dynamic']:
                        bodyDef.type = Box2D.b2_dynamicBody
                    else:
                        bodyDef.type = Box2D.b2_staticBody
              
                    bodyFixtureDef = Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(tiled_map.tilewidth / gameObjectHandler.scale, tiled_map.tilewidth / gameObjectHandler.scale)))
                    bodyFixtureDef.density = layer.properties['density']
                    bodyDef.position = (x*tiled_map.tilewidth, -y*tiled_map.tileheight)
                    # adds box
                    gameObjectHandler.add(gm, bodyDef, bodyFixtureDef)
