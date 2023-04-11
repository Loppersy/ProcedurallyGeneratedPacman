import os

import pygame

import utilities
"""
Loppersy: This class is used for playing sound effects and music in the game.

File taken from: https://github.com/Loppersy/ProcedurallyGeneratedPacman and it is mostly the same as the original
"""

class SFXHandler:

    def __init__(self, sfxs, musics, fps):
        pygame.mixer.init()
        self.sfxs = dict()
        for i in range(len(sfxs)):
            self.sfxs.update({sfxs[i]: pygame.mixer.Sound(os.path.join("assets", "sound_effects", sfxs[i]))})

        self.musics = dict()
        for i in range(len(musics)):
            self.musics.update({musics[i]: os.path.join("assets", "sound_effects", musics[i])})

        self.current_music = None
        self.fps = fps

    def play_sfx(self, sfx):
        if not utilities.SFX_and_Music[0]:
            return

        if sfx in self.sfxs:
            self.sfxs[sfx].play()

    def play_music(self, music):
        if not utilities.SFX_and_Music[0]:
            return
        if self.current_music is None or self.current_music != music:
            if music in self.musics:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load(self.musics[music])
                pygame.mixer.music.play(-1)
                print("playing music: " + music)
                self.current_music = music
            else:
                print("music not found: " + music)

    def stop_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        self.current_music = None

    def initialize(self):
        utilities.sfx_queue = []
        pygame.mixer.init()



