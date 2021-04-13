# AggiEngine

AggiEngine is a 2D game engine, designed for making game development easier. AggiEngine provides GUI, physics, state management and more...

## Installation

```bash
pip install AggiEngine
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

app = ag.Application(ExampleState("example.ui"))
app.run()
```

## Issues
Feel free to report any [issues](https://github.com/aggie-coding-club/AggiEngine/issues) you may find.
If there is a feature you would like added we'll do our best to implement it.
