import os

import pygame

from Consumable import Consumable
from utilities import load_sheet

POWER_PELLET_SCORE = 50

class PowerPellet(Consumable):
    def __init__(self, x, y, width, height, pellets_sheet_image):
        super().__init__(x, y, width, height, POWER_PELLET_SCORE)
        self.image = pygame.transform.scale(load_sheet(pellets_sheet_image, 2, 2, 16, 16)[1], (width, height))
        self.type = "power_pellet"

    def update(self, maze_data):
        pass

    def my_draw(self, surface):
        pass