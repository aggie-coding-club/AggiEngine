import simpleaudio as sa


class Sound:

    def __init__(self) -> None:
        self.sounds = dict()
    
    def load(self, key: Any, filestr: str) -> None:
        """
        Loads a wav file for future playback
        :param key: A key you will use to access the audio playback
        :param filestr: The file path for a wav file to play
        """
        self.sounds[key] = sa.WaveObject.from_wave_file(filestr)
    
    def play(self, key: Any) -> sa.PlayObject:
        """
        Plays your sound
        :param key: The key used when loading the sound
        :return: a PlayObject from the simpleaudio library
        """
        return self.sounds[key].play()
    
    def stop_all(self) -> None:
        """
        Stops all sounds from playing
        """
        sa.stop_all()
