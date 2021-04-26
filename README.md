# AggiEngine

AggiEngine is a 2D game engine, designed for making game development easier. AggiEngine provides GUI, physics, state management and more...


## Easy Installation

```bash
pip install AggiEngine
```

## Manual Installation
```bash
pip install PySide2
pip install PyOpenGL
pip install Box2D
pip install pytmx
pip install pillow
pip install numpy
pip install simpleaudio
```

## Usage

```python
import AggiEngine as ag


class ExampleState(ag.State):

    def __init__(self, ui_path):
        ag.State.__init__(self, ui_path)
        
    def start(self):
        self.loadMap('example_map.tmx')
    
    def update(self):
        print("Updated!")

state = ExampleState("example.ui")
app = ag.Application(state)
app.run()
```

## Issues
Feel free to report any [issues](https://github.com/aggie-coding-club/AggiEngine/issues) you may find.
If there is a feature you would like added we'll do our best to implement it.
