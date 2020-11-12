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
            gameScreen.bgColor = [color[0] / 256, color[1] / 256, color[2] / 256]
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
                    gm.setWidth(image[1] / gameObjectHandler.scale ** 2)
                    gm.setHeight(image[2] / gameObjectHandler.scale ** 2)
                    # create box
                    bodyDef = Box2D.b2BodyDef()
                    dynamic = layer.properties.get('dynamic', 0)
                    if dynamic == 1 or dynamic == 0:
                        if dynamic == 0:
                            bodyDef.type = Box2D.b2_staticBody
                        else:
                            bodyDef.type = Box2D.b2_dynamicBody

                        bodyFixtureDef = Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(
                            box=((image[1] / gameObjectHandler.scale) / 2,
                                 (image[2] / gameObjectHandler.scale) / 2)))
                        bodyFixtureDef.density = layer.properties.get('density', 1)

                        bodyDef.position = (
                            -(x * tiled_map.tilewidth) / gameObjectHandler.scale,
                            -(y * tiled_map.tileheight) / gameObjectHandler.scale)

                        # adds box
                        gameObjectHandler.add(gm, bodyDef, bodyFixtureDef)
                    else:
                        gm.position = (-x / gameObjectHandler.scale, -y / gameObjectHandler.scale)
                        gameObjectHandler.add(gm)
