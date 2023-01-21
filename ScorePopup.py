import pygame

import utilities


class ScorePopup(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, window_width, window_height, fps, score, color, time):
        super().__init__()
        self.x = x
        self.y = y
        self.score = score
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.image = utilities.get_text_image(str(score), 200, color)
        self.rect = self.image.get_rect()
        self.time = time
        self.clock = 0
        self.fps = fps

    def update(self):
        self.clock += 1
        if self.clock >= self.time * self.fps:
            self.kill()
