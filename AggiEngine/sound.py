import simpleaudio as sa

class Sound():
    def __init__(self) -> None:
        self.sounds = dict()
    
    def load(self, key, filestr):
        self.sounds[key] = sa.WaveObject.from_wave_file(filestr)
    
    def play(self, key):
        self.sounds[key].play()
    
    def stop_all(self):
        sa.stop_all()
    
    def stop(self, key):
        self.sounds[key].stop()