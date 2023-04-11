import pygame

"""
Loppersy: This is the base class for all consumables in the game. In this version of the Pac-man game,
there are only two types of consumables: pellets and power pellets. This class and its subclasses
are used for visualizing the consumables on the screen, rather than for the actual logic of the game.

File taken from: https://github.com/Loppersy/ProcedurallyGeneratedPacman (where the subclasses actually have
game logic in it)
"""


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
