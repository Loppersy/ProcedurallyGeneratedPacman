import pygame

import utilities
from utilities import load_sheet


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, window_width, window_height, pacman_sheet_image, scale, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.images = load_sheet(pacman_sheet_image, 2, 11, 16, 16)
        self.current_image = 0
        self.image = pygame.transform.scale(self.images[self.current_image], (scale * 1, scale * 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = pygame.time.get_ticks()

        self.speed = speed
        self.direction = "stay"
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.moving = False

        self.animation_cooldown = 50
        self.dying_animation_cooldown = 150
        self.dying_animation_start_cooldown = 1000
        self.dying_animation_end_cooldown = 75
        self.start_animation_completed = False
        self.dead_animation_completed = False

    def update(self, maze_data, consumables):
        if self.direction == "dead":
            self.kill()
        self.draw_pacman()

        # consume any consumable in the current position
        maze_data = self.check_consumables(maze_data, consumables)

        return maze_data

    def draw_pacman(self):
        now = pygame.time.get_ticks()
        if self.direction == "dying":
            if not self.start_animation_completed:
                self.current_image = 11

            if now - self.last_update > self.dying_animation_start_cooldown:
                self.start_animation_completed = True

            if now - self.last_update > self.dying_animation_end_cooldown and self.dead_animation_completed:
                self.last_update = now
                self.current_image = 10
                self.direction = "dead"

            if now - self.last_update > self.dying_animation_cooldown and self.start_animation_completed:
                self.last_update = now
                if self.current_image != 21:
                    self.current_image = (self.current_image + 1) % len(self.images)
                else:
                    self.dead_animation_completed = True

            self.image = pygame.transform.scale(self.images[self.current_image], (self.scale * 1, self.scale * 1))


        elif now - self.last_update > self.animation_cooldown and self.moving:
            self.last_update = now
            if self.direction == "right":
                if self.current_image >= 2:
                    self.current_image = 0
                elif self.current_image < 1:
                    self.current_image = 1
                else:
                    self.current_image = self.current_image + 1
            elif self.direction == "left":
                if self.current_image >= 4:
                    self.current_image = 0
                elif self.current_image < 3:
                    self.current_image = 3
                else:
                    self.current_image = self.current_image + 1
            elif self.direction == "up":
                if self.current_image >= 6:
                    self.current_image = 0
                elif self.current_image < 5:
                    self.current_image = 5
                else:
                    self.current_image = self.current_image + 1
            elif self.direction == "down":
                if self.current_image >= 8:
                    self.current_image = 0
                elif self.current_image < 7:
                    self.current_image = 7
                else:
                    self.current_image = self.current_image + 1

            # TODO: scale image to be 1.5 times bigger than the tile and center it to the middle of the tile
            self.image = pygame.transform.scale(self.images[self.current_image], (self.scale * 1, self.scale * 1))

    # check collision with walls in a given direction
    def can_change_direction(self, maze_data, direction):
        position = utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width, self.window_height)
        min_threshold = (.07, .07)
        centerness = (abs(position[0] - (self.rect.x - (self.window_width - self.scale * 32) / 2) / self.scale),
                      abs(position[1] - (self.rect.y - (self.window_height - self.scale * 32) / 2) / self.scale))
        # print(position, ((self.rect.x - (window_width - self.scale * 32) / 2)/ self.scale,(self.rect.y - (window_height - self.scale * 32) / 2)/ self.scale), centerness)

        # if the pacman is not in the center of the tile, it can't change direction. if pacman is in the edge of the
        # maze, check if it can change direction by looking at the other side of the maze to account for the wrapping
        # / teleporting
        if direction == "left":
            if position[0] == 0:
                return maze_data[position[1]][31] != 1 and centerness[0] < min_threshold[0] and centerness[1] < \
                    min_threshold[1]
            else:
                return maze_data[position[1]][position[0] - 1] != 1 and centerness[0] < min_threshold[0] and centerness[1] < \
                    min_threshold[1]
        elif direction == "right":
            if position[0] == 31:
                return maze_data[position[1]][0] != 1 and centerness[0] < min_threshold[0] and centerness[1] < \
                    min_threshold[1]
            else:
                return maze_data[position[1]][position[0] + 1] != 1 and centerness[0] < min_threshold[0] and centerness[1] < \
                    min_threshold[1]
        elif direction == "up":
            if position[1] == 0:
                return maze_data[31][position[0]] != 1 and centerness[0] < min_threshold[0] and centerness[1] < \
                    min_threshold[1]
            else:
                return maze_data[position[1] - 1][position[0]] != 1 and centerness[0] < min_threshold[0] and centerness[1] < \
                    min_threshold[1]
        elif direction == "down":
            if position[1] == 31:
                return maze_data[0][position[0]] != 1 and centerness[0] < min_threshold[0] and centerness[1] < \
                    min_threshold[1]
            else:
                return maze_data[position[1] + 1][position[0]] != 1 and centerness[0] < min_threshold[0] and centerness[1] < \
                    min_threshold[1]

        # elif direction == "right":
        #     return maze_data[position[1]][position[0] + 1] != 1 and centerness[0] < min_threshold[0] and centerness[1] < \
        #         min_threshold[1]
        # elif direction == "up":
        #     return maze_data[position[1] - 1][position[0]] != 1 and centerness[1] < min_threshold[1] and centerness[0] < \
        #         min_threshold[0]
        # elif direction == "down":
        #     return maze_data[position[1] + 1][position[0]] != 1 and centerness[1] < min_threshold[1] and centerness[0] < \
        #         min_threshold[0]
        # return False

    def check_open_path(self, maze_data, direction):
        position_int = utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                          self.window_height)
        position_float = utilities.get_position_in_maze_float(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                              self.window_height)
        min_threshold = (.07, .07)
        centerness = (abs(position_int[0] - position_float[0]), abs(position_int[1] - position_float[1]))
        # check if the pacman is in the middle of the tile and if there is a wall in the direction of the movement
        # if it is the end of the maze, check the tile in the other side of the maze.
        if direction == "left":
            if direction == "left":
                if position_int[0] == 0:
                    return maze_data[position_int[1]][position_int[0] + 31] != 1 or centerness[0] > min_threshold[0]
                else:
                    return maze_data[position_int[1]][position_int[0] - 1] != 1 or centerness[0] > min_threshold[0]
        elif direction == "right":
            if position_int[0] == 31:
                return maze_data[position_int[1]][position_int[0] - 31] != 1 or centerness[0] > min_threshold[0]
            else:
                return maze_data[position_int[1]][position_int[0] + 1] != 1 or centerness[0] > min_threshold[0]
        elif direction == "up":
            if position_int[1] == 0:
                return maze_data[position_int[1] + 31][position_int[0]] != 1 or centerness[1] > min_threshold[1]
            else:
                return maze_data[position_int[1] - 1][position_int[0]] != 1 or centerness[1] > min_threshold[1]
        elif direction == "down":
            if position_int[1] == 31:
                return maze_data[position_int[1] - 31][position_int[0]] != 1 or centerness[1] > min_threshold[1]
            else:
                return maze_data[position_int[1] + 1][position_int[0]] != 1 or centerness[1] > min_threshold[1]

    def check_consumables(self, maze_data, consumables):
        for i in range(len(consumables)):
            for consumable in consumables[i]:
                position_int = utilities.get_position_in_maze_int(consumable.rect.x, consumable.rect.y, self.scale,
                                                                  self.window_width,
                                                                  self.window_height)
                position_float = utilities.get_position_in_maze_float(self.rect.x, self.rect.y, self.scale,
                                                                      self.window_width,
                                                                      self.window_height)
                min_threshold = (.2, .2)
                centerness = (abs(position_int[0] - position_float[0]), abs(position_int[1] - position_float[1]))
                if centerness[0] < min_threshold[0] and centerness[1] < min_threshold[1]:
                    #print(consumable.type)
                    if consumable.type == "pellet":
                        consumable.kill()
                        maze_data[position_int[1]][position_int[0]] = 0
                        # TODO: add score
                    elif consumable.type == "power_pellet":
                        consumable.kill()
                        maze_data[position_int[1]][position_int[0]] = 0
                        # TODO: add score
                        # TODO: add power pellet effect

        return maze_data

    def die(self):
        if self.direction != "dead":
            self.direction = "dying"