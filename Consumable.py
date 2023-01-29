import pygame


class Consumable(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, score):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score = score

    def get_score(self):
        return self.score
