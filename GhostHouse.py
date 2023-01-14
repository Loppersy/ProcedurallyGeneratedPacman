import pygame

import utilities
from Ghost import Ghost


class GhostHouse(pygame.sprite.Sprite):
    def __init__(self, x, y, ghosts_to_spawn, ghosts_images, frightened_images, window_width, window_height, scale,
                 fps):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.image.fill((0, 0, 0, 0))
        self.ghosts = pygame.sprite.Group()
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

        # for i in range(0, len(ghosts_to_spawn)):
        #     self.ghosts.add(
        #         Ghost(15 * scale + (window_width - 32 * scale) / 2, 12 * scale + (window_height - 32 * scale) / 2,
        #               ghosts_images[i], frightened_images, ghosts_to_spawn[i], self.window_width, self.window_height,
        #               self.scale, self.fps, self.speed, self))

    # def update(self, pacmans, maze_data):
    # for ghost in self.ghosts:
    #     ghost.update(pacmans, maze_data)
    #     if ghost.state == "dead" and ghost.position == (self.int_pos[0] + 3, self.int_pos[1] - 1):
    #         ghost.force_goal = (self.int_pos[0] + 3, self.int_pos[1] + 3)

    # def draw(self, screen):
    # for ghost in self.ghosts:
    #     ghost.draw(screen)

    # def overwrite_global_states(self, state, time):
    # for ghost in self.ghosts:
    #     ghost.overwrite_global_state(state, time)

    def get_entrance(self):
        return self.int_pos[0] + 3, self.int_pos[1] - 1
