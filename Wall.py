import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = pygame.transform.scale(self.image, (width, height)).get_rect()
        self.rect.x = x
        self.rect.y = y
