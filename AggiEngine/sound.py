import simpleaudio as sa

class Sound():
    def __init__(self) -> None:
        self.sounds = dict()
    
    def load(self, key, filestr):
        """
        Loads a wav file for future playback
        :param key: A key you will use to access the audio playback
        :param filestr: The file path for a wav file to play
        """
        self.sounds[key] = sa.WaveObject.from_wave_file(filestr)
    
    def play(self, key):
        """
        Plays your sound
        :param key: The key used when loading the sound
        """
        self.sounds[key].play()
    
    def stop_all(self):
        """
        Stops all sounds from playing
        """
        sa.stop_all()
    
    def stop(self, key):
        """
        Stops the selected sound from playing
        :param key: The key you used when loading the sound
        """
        self.sounds[key].stop()