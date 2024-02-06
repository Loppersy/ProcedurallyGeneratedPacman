import pygame
import utilities  # Assuming utilities has SFX_and_Music flag

class SFXHandler:
    def __init__(self, resources, fps):
        """
        Initializes the sound effects handler with preloaded resources.

        :param resources: A dictionary containing all preloaded resources, including sounds and music paths.
        :param fps: The frames per second the game is running at, for timing purposes.
        """
        self.sfxs = resources["sounds"]
        self.music_paths = resources["music_paths"]
        self.current_music = None
        self.fps = fps

    def play_sfx(self, sfx_name):
        """
        Plays a sound effect by name.

        :param sfx_name: The name of the sound effect to play.
        """
        if not utilities.SFX_and_Music[0]:
            return

        if sfx_name in self.sfxs:
            self.sfxs[sfx_name].play()

    def play_music(self, music_name):
        """
        Plays a music track by name, stopping any currently playing track.

        :param music_name: The name of the music track to play.
        """
        if not utilities.SFX_and_Music[0] or self.current_music == music_name:
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        music_path = self.music_paths.get(music_name)
        if music_path:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            self.current_music = music_name
        else:
            print(f"Music not found: {music_name}")

    def stop_music(self):
        """
        Stops any currently playing music.
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.current_music = None
