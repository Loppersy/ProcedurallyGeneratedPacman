import pygame

import utilities
from utilities import load_sheet


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, pacman_sheet_image, scale, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.images = load_sheet(pacman_sheet_image, 1, 2, 16, 16)
        self.current_image = 0
        self.image = pygame.transform.scale(self.images[self.current_image], (scale * 1, scale * 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.speed = speed
        self.direction = "stay"
        self.scale = scale

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            self.current_image = (self.current_image + 1) % 2
            # scale image to be 1.5 times bigger than the tile and center it to the middle of the tile
            self.image = pygame.transform.scale(self.images[self.current_image], (self.scale * 1, self.scale * 1))

    # check collision with walls in a given direction
    def can_change_direction(self, maze_data, direction, window_width, window_height):
        position = utilities.get_position_in_maze(self.rect.x, self.rect.y, self.scale, window_width, window_height)
        min_threshold = (.07, .07)
        centerness = (abs(position[0] - (self.rect.x - (window_width - self.scale * 32) / 2) / self.scale),
                            abs(position[1] - (self.rect.y - (window_height - self.scale * 32) / 2) / self.scale))
        print(position, ((self.rect.x - (window_width - self.scale * 32) / 2)/ self.scale,(self.rect.y - (window_height - self.scale * 32) / 2)/ self.scale), centerness)
        if direction == "left":
            return maze_data[position[1]][position[0] - 1] != 1 and centerness[0] < min_threshold[0] and centerness[1] < min_threshold[1]
        elif direction == "right":
            return maze_data[position[1]][position[0] + 1] != 1 and centerness[0] < min_threshold[0] and centerness[1] < min_threshold[1]
        elif direction == "up":
            return maze_data[position[1] - 1][position[0]] != 1 and centerness[1] < min_threshold[1] and centerness[0] < min_threshold[0]
        elif direction == "down":
            return maze_data[position[1] + 1][position[0]] != 1 and centerness[1] < min_threshold[1] and centerness[0] < min_threshold[0]
        return False

    def check_open_path(self, maze_data, direction, window_width, window_height):
        position = utilities.get_position_in_maze(self.rect.x, self.rect.y, self.scale, window_width, window_height)
        min_threshold = (.07, .07)
        centerness = (abs(position[0] - (self.rect.x - (window_width - self.scale * 32) / 2) / self.scale),
                            abs(position[1] - (self.rect.y - (window_height - self.scale * 32) / 2) / self.scale))
        if direction == "left":
            return maze_data[position[1]][position[0] - 1] != 1 or centerness[0] > min_threshold[0]
        elif direction == "right":
            return maze_data[position[1]][position[0] + 1] != 1 or centerness[0] > min_threshold[0]
        elif direction == "up":
            return maze_data[position[1] - 1][position[0]] != 1 or centerness[1] > min_threshold[1]
        elif direction == "down":
            return maze_data[position[1] + 1][position[0]] != 1 or centerness[1] > min_threshold[1]
        return True
