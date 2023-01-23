import pygame

import utilities
from utilities import load_sheet


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, window_width, window_height, pacman_sheet_image, scale, speed):
        super().__init__()
        self.consumed_power_pellet = False
        self.images = load_sheet(pacman_sheet_image, 2, 11, 16, 16)
        self.current_image = 0
        self.image = pygame.Surface((scale * 1, scale * 1), pygame.SRCALPHA)  # Do not update this surface
        self.rect = pygame.transform.scale(self.image, (scale * 0.5, scale * 0.5)).get_rect()
        self.image_scale = 1.5
        self.my_image = pygame.transform.scale(self.images[self.current_image],
                                               (scale * self.image_scale, scale * self.image_scale))

        self.last_update = pygame.time.get_ticks()

        self.current_speed = speed
        self.direction = "stay"
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.moving = False

        self.move(x, y)
        self.logic_pos = round(x), round(y)
        self.int_pos = utilities.get_position_in_maze_int(x, y, scale, window_width, window_height)

        self.animation_cooldown = 50
        self.dying_animation_cooldown = 150
        self.dying_animation_start_cooldown = 1300
        self.dying_animation_end_cooldown = 75
        self.start_animation_completed = False
        self.dead_animation_completed = False

    def move(self, x, y):
        # print("Pacman move: ", x, y)
        self.logic_pos = x, y
        self.int_pos = utilities.get_position_in_maze_int(x, y, self.scale, self.window_width, self.window_height)
        # self.rect.x = int(x + self.scale * 0.25)
        # self.rect.y = int(y + self.scale * 0.25)
        self.rect.topleft = round(x + self.scale * 0.25), round(y + self.scale * 0.25)

    def get_pos(self):
        return self.logic_pos

    def update(self, maze_data, consumables):
        if self.direction == "dead":
            self.kill()

        # consume any consumable in the current position
        maze_data = self.check_consumables(maze_data, consumables)

        return maze_data

    def my_draw(self, screen, animated=True):
        now = pygame.time.get_ticks()
        if self.direction == "dying" and animated:
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

            self.my_image = pygame.transform.scale(self.images[self.current_image],
                                                   (self.scale * self.image_scale, self.scale * self.image_scale))

        elif now - self.last_update > self.animation_cooldown and self.moving and animated:
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

            self.my_image = pygame.transform.scale(self.images[self.current_image],
                                                   (self.scale * self.image_scale, self.scale * self.image_scale))

        screen.blit(self.my_image, (self.rect.x - self.scale * 0.5, self.rect.y - self.scale * 0.5))

        # visualize rect boundaries
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)

    # check collision with walls in a given direction
    def can_change_direction(self, maze_data, direction, ignore_centerness=False):
        if self.direction == "dying" or self.direction == "dead":
            return False

        position = utilities.get_position_in_maze_int(self.get_pos()[0], self.get_pos()[1], self.scale,
                                                      self.window_width,
                                                      self.window_height)

        min_threshold = (.07, .07)
        if ignore_centerness:
            centerness = (0, 0)
        else:
            centerness = (
                abs(position[0] - (self.get_pos()[0] - (self.window_width - self.scale * 32) / 2) / self.scale),
                abs(position[1] - (self.get_pos()[1] - (self.window_height - self.scale * 32) / 2) / self.scale))
        # print(position, ((self.rect.x - (window_width - self.scale * 32) / 2)/ self.scale,(self.rect.y - (
        # window_height - self.scale * 32) / 2)/ self.scale), centerness)

        # if the pacman is not in the center of the tile, it can't change direction. if pacman is in the edge of the
        # maze, check if it can change direction by looking at the other side of the maze to account for the wrapping
        # / teleporting
        if direction == "left":
            if position[0] == 0:
                return maze_data[position[1]][31] != 1 and centerness[1] < min_threshold[1]
            else:
                return maze_data[position[1]][position[0] - 1] != 1 and centerness[1] < min_threshold[1]
        elif direction == "right":
            if position[0] == 31:
                return maze_data[position[1]][0] != 1 and centerness[1] < min_threshold[1]
            else:
                return maze_data[position[1]][position[0] + 1] != 1 and centerness[1] < min_threshold[1]
        elif direction == "up":
            if position[1] == 0:
                return maze_data[31][position[0]] != 1 and centerness[0] < min_threshold[0]
            else:
                return maze_data[position[1] - 1][position[0]] != 1 and centerness[0] < min_threshold[0]
        elif direction == "down":
            if position[1] == 31:
                return maze_data[0][position[0]] != 1 and centerness[0] < min_threshold[0]
            else:
                return maze_data[position[1] + 1][position[0]] != 1 and centerness[0] < min_threshold[0]

    def check_open_path(self, maze_data, direction):
        temp_pos = self.get_pos()
        position_int = utilities.get_position_in_maze_int(temp_pos[0], temp_pos[1], self.scale, self.window_width,
                                                          self.window_height)
        position_float = utilities.get_position_in_maze_float(temp_pos[0], temp_pos[1], self.scale, self.window_width,
                                                              self.window_height)
        min_threshold = (.07, .07)
        centerness = (abs(position_int[0] - position_float[0]), abs(position_int[1] - position_float[1]))
        # check if the pacman is in the middle of the tile and if there is a wall in the direction of the movement
        # if it is the end of the maze, check the tile in the other side of the maze.
        if direction == "left":
            if direction == "left":
                if position_int[0] <= 0:
                    return maze_data[position_int[1]][31] != 1 or centerness[0] > min_threshold[0]
                else:
                    return maze_data[position_int[1]][position_int[0] - 1] != 1 or centerness[0] > min_threshold[0]
        elif direction == "right":
            if position_int[0] >= 31:
                return maze_data[position_int[1]][0] != 1 or centerness[0] > min_threshold[0]
            else:
                return maze_data[position_int[1]][position_int[0] + 1] != 1 or centerness[0] > min_threshold[0]
        elif direction == "up":
            if position_int[1] <= 0:
                return maze_data[31][position_int[0]] != 1 or centerness[1] > min_threshold[1]
            else:
                return maze_data[position_int[1] - 1][position_int[0]] != 1 or centerness[1] > min_threshold[1]
        elif direction == "down":
            if position_int[1] >= 31:
                return maze_data[0][position_int[0]] != 1 or centerness[1] > min_threshold[1]
            else:
                return maze_data[position_int[1] + 1][position_int[0]] != 1 or centerness[1] > min_threshold[1]

    def check_consumables(self, maze_data, consumables):
        for i in range(len(consumables)):
            for consumable in consumables[i]:
                position_int = utilities.get_position_in_maze_int(consumable.rect.x, consumable.rect.y, self.scale,
                                                                  self.window_width,
                                                                  self.window_height)
                position_float = utilities.get_position_in_maze_float(self.logic_pos[0], self.logic_pos[1], self.scale,
                                                                      self.window_width,
                                                                      self.window_height)
                min_threshold = (.2, .2)
                centerness = (abs(position_int[0] - position_float[0]), abs(position_int[1] - position_float[1]))
                if centerness[0] < min_threshold[0] and centerness[1] < min_threshold[1]:
                    # print(consumable.type)
                    if consumable.type == "pellet":
                        consumable.kill()
                        maze_data[position_int[1]][position_int[0]] = 0
                        # TODO: add score
                    elif consumable.type == "power_pellet":
                        consumable.kill()
                        maze_data[position_int[1]][position_int[0]] = 0
                        # TODO: add score
                        self.consumed_power_pellet = True

                # check collision with bonus fruit and pacman
                if consumable.type == "bonus_fruit" and consumable.rect.colliderect(self.rect):
                    if consumable.consume():
                        utilities.queued_popups.append(
                            (consumable.rect.x + consumable.rect.width/2, consumable.rect.y + consumable.rect.height/2, consumable.score,
                             (217, 104, 200), 1,11))

        return maze_data

    def die(self):
        if self.direction != "dead":
            self.direction = "dying"
