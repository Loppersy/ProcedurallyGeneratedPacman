import pygame

import utilities
from Ghost import Ghost


class GhostHouse(pygame.sprite.Sprite):
    def __init__(self, x, y, window_width, window_height, scale,
                 fps):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.image.fill((0, 0, 0, 0))
        self.ghosts = []
        self.rect = pygame.Rect(x, y, 1, 1)
        self.int_pos = (int(utilities.get_position_in_maze_int(x, y, scale, window_width, window_height)[0]),
                        int(utilities.get_position_in_maze_int(x, y, scale, window_width, window_height)[1]))
        self.rect.x = x
        self.rect.y = y
        self.window_width = window_width
        self.window_height = window_height
        self.scale = scale
        self.fps = fps

        self.speed = 1.9

    def get_entrance(self):
        return self.int_pos[0] + 3, self.int_pos[1] - 1

    def get_ghosts(self):
        return self.ghosts

    def add_ghost(self, ghost):
        self.ghosts.append(ghost)

    def clear_ghosts(self):
        self.ghosts = []