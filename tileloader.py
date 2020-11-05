import pytmx
import Box2D
import importlib

class TileMap():

    def __init__(self,tmxFile, gameobjecthandler):
        tiled_map = pytmx.TiledMap(tmxFile)
        for layer in tiled_map:
            #Checks for layers with tiles
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer.tiles():
                    #Gets class name and gets class name definition
                    className = layer.properties['class-name']
                    className = getattr(importlib.import_module('__main__'),className)
                    #create box
                    bodyDef = Box2D.b2BodyDef()
                    if layer.properties['dynamic']:
                        bodyDef.type = Box2D.b2_dynamicBody
                    else:
                        bodyDef.type = Box2D.b2_staticBody
                    bodyFixtureDef =  Box2D.b2FixtureDef(shape=Box2D.b2PolygonShape(box=(10,10)))
                    bodyFixtureDef.density = layer.properties['density']
                    bodyDef.position=(x*10,-y*10)
                    #adds box
                    gameobjecthandler.add(className(),bodyDef, bodyFixtureDef)