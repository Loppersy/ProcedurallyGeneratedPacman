import pygame

import utilities


class ScorePopup(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, window_width, window_height, fps, score, color, time):
        super().__init__()

        self.score = score
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.image = utilities.get_text_image(str(score), int(scale*0.5), color)
        # blit a rectangle around the image
        # pygame.draw.rect(self.image, color, (0, 0, self.image.get_width(), self.image.get_height()), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.image.get_width() / 2
        self.rect.y = y - self.image.get_height() / 2
        self.time = time
        self.clock = 0
        self.fps = fps

    def update(self):
        self.clock += 1
        if self.clock >= self.time * self.fps:
            self.kill()
