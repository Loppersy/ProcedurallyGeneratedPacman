import pygame

import utilities
from AStar import AStar, Node


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, images, type, window_width, window_height, scale, speed):
        super().__init__()
        self.type = type
        self.images = images
        self.current_image = 0
        self.image = pygame.transform.scale(self.images[self.current_image], (scale * 1, scale * 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 150
        self.window_width = window_width
        self.window_height = window_height
        self.scale = scale
        self.pathfinder = AStar()
        self.current_path = []
        self.speed = speed
        self.direction = "stay"

    def update(self, pacmans, maze_data):

        self.check_collision(pacmans)
        self.current_path = self.update_path(pacmans, maze_data)
        self.change_direction(self.current_path)
        self.move()
        self.draw_ghost()

    def move(self):
        if self.direction == "right":
            self.position = (self.position[0] + self.speed, self.position[1])
        elif self.direction == "left":
            self.position = (self.position[0] - self.speed, self.position[1])
        elif self.direction == "down":
            self.position = (self.position[0], self.position[1] + self.speed)
        elif self.direction == "up":
            self.position = (self.position[0], self.position[1] - self.speed)

        # if the position is out of the maze, move it to the other side
        if utilities.get_position_in_maze_float(self.position[0], self.position[1], self.scale, self.window_width,
                                                self.window_height)[0] < 0:
            self.position = (
                utilities.get_position_in_window(31, self.position[1], self.scale, self.window_width,
                                                 self.window_height)[
                    0], self.position[1])
        elif utilities.get_position_in_maze_float(self.position[0], self.position[1], self.scale, self.window_width,
                                                    self.window_height)[0] > 31:
                self.position = (
                    utilities.get_position_in_window(0, self.position[1], self.scale, self.window_width,
                                                     self.window_height)[
                        0], self.position[1])
        elif utilities.get_position_in_maze_float(self.position[0], self.position[1], self.scale, self.window_width,
                                                  self.window_height)[1] < 0:
            self.position = (
                self.position[0],
                utilities.get_position_in_window(self.position[0], 31, self.scale, self.window_width,
                                                 self.window_height)[
                    1])
        elif utilities.get_position_in_maze_float(self.position[0], self.position[1], self.scale, self.window_width,
                                                    self.window_height)[1] > 31:
                self.position = (
                    self.position[0],
                    utilities.get_position_in_window(self.position[0], 0, self.scale, self.window_width,
                                                     self.window_height)[
                        1])

        self.rect.topleft = round(self.position[0]), round(self.position[1])

    # draw the path to the objective on the screen, taking into account the scale of the maze and the position of the
    # maze in the window. Drawn with a thin red line
    def draw_path(self, screen):
        if self.current_path:
            for node in self.current_path:
                (x, y) = utilities.get_position_in_window(node[0], node[1], self.scale, self.window_width,
                                                          self.window_height)
                # check if next node is in the same direction as the current node and draw a line to it if it is.
                # if not, draw a line to the middle of the tile and then draw a line to the next node
                if self.current_path.index(node) + 1 < len(self.current_path):
                    (next_x, next_y) = utilities.get_position_in_window(
                        self.current_path[self.current_path.index(node) + 1][0],
                        self.current_path[self.current_path.index(node) + 1][1],
                        self.scale, self.window_width,
                        self.window_height)
                    if node[0] == self.current_path[self.current_path.index(node) + 1][0]:
                        pygame.draw.line(screen, (255, 0, 0), (x + self.scale / 2, y + self.scale / 2),
                                         (x + self.scale / 2, next_y + self.scale / 2), 3)
                    elif node[1] == self.current_path[self.current_path.index(node) + 1][1]:
                        pygame.draw.line(screen, (255, 0, 0), (x + self.scale / 2, y + self.scale / 2),
                                         (next_x + self.scale / 2, y + self.scale / 2), 3)
                    else:
                        pygame.draw.line(screen, (255, 0, 0), (x + self.scale / 2, y + self.scale / 2),
                                         (x + self.scale / 2, y + self.scale / 2), 3)
                        pygame.draw.line(screen, (255, 0, 0), (x + self.scale / 2, y + self.scale / 2),
                                         (next_x + self.scale / 2, next_y + self.scale / 2), 3)

    # Check collision with pacman. If collision, that pacman dies
    def check_collision(self, pacmans):
        for pacman in pacmans:
            if self.rect.colliderect(pacman.rect):
                pacman.die()

    # TODO: Make an option to use the classic pathfinding found in pacman
    def change_direction(self, path):
        # find in what direction is the next node in the path by comparing path[0] with path[1]
        # only change direction if the ghost is in the middle of a tile
        min_threshold = (0.2, 0.2)
        position = utilities.get_position_in_maze_float(self.position[0], self.position[1], self.scale,
                                                        self.window_width,
                                                        self.window_height)
        centerness = (position[0] - int(position[0]), position[1] - int(position[1]))
        if path and len(path) > 1:
            if centerness[0] < min_threshold[0] and centerness[1] < min_threshold[1]:
                # First, check if next node is wrapped around the map
                if path[0][0] == 0 and path[1][0] == 31:
                    self.direction = "left"
                    self.position = (self.position[0], utilities.get_position_in_window(
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[0],
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[1], self.scale,
                        self.window_width, self.window_height)[1])
                elif path[0][0] == 31 and path[1][0] == 0:
                    self.direction = "right"
                    self.position = (self.position[0], utilities.get_position_in_window(
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[0],
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[1], self.scale,
                        self.window_width, self.window_height)[1])
                elif path[0][1] == 0 and path[1][1] == 31:
                    self.direction = "up"
                    self.position = (utilities.get_position_in_window(
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[0],
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[1], self.scale,
                        self.window_width, self.window_height)[0], self.position[1])
                elif path[0][1] == 31 and path[1][1] == 0:
                    self.direction = "down"
                    self.position = (utilities.get_position_in_window(
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[0],
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[1], self.scale,
                        self.window_width, self.window_height)[0], self.position[1])

                elif path[0][0] < path[1][0]:
                    self.direction = "right"
                    # center ghost in the middle of the tile
                    self.position = (self.position[0], utilities.get_position_in_window(
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[0],
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[1], self.scale,
                        self.window_width, self.window_height)[1])
                elif path[0][0] > path[1][0]:
                    self.direction = "left"
                    self.position = (self.position[0], utilities.get_position_in_window(
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[0],
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[1], self.scale,
                        self.window_width, self.window_height)[1])
                elif path[0][1] < path[1][1]:
                    self.direction = "down"
                    self.position = (utilities.get_position_in_window(
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[0],
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[1], self.scale,
                        self.window_width, self.window_height)[0], self.position[1])
                elif path[0][1] > path[1][1]:
                    self.direction = "up"
                    self.position = (utilities.get_position_in_window(
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[0],
                        utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                                                           self.window_width, self.window_height)[1], self.scale,
                        self.window_width, self.window_height)[0], self.position[1])
        else:
            self.direction = "stay"

    def update_path(self, pacmans, maze_data):

        if self.type == "blinky":
            # take the shortest path to any pacman
            shortest_path = []
            for pacman in pacmans:
                path = self.pathfinder.get_path(Node(
                    utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                       self.window_height)), Node(
                    utilities.get_position_in_maze_int(pacman.rect.x, pacman.rect.y, self.scale, self.window_width,
                                                       self.window_height)), maze_data)
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
            return shortest_path

    def draw_ghost(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            self.current_image = (self.current_image + 1) % 2
            self.image = self.images[self.current_image]
        # add image[4] (eyes) on top of image
        self.image.blit(self.images[4], (0, 0))
        # TODO: scale image to be 1.5 times bigger than the tile and center it to the middle of the tile
        self.image = pygame.transform.scale(self.images[self.current_image], (self.scale * 1, self.scale * 1))
