import random

import numpy as np
import pygame

import utilities
from AStar import AStar, Node


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, images, fright_images, ghost_type, window_width, window_height, scale, fps, speed,
                 ghost_house, ghost_number):
        super().__init__()

        self.is_dead = False
        self.path = None
        self.pathfinder = AStar()
        self.respawning = None
        self.image_scale = 1.5
        self.my_image = None
        self.closest_pacman = None
        self.exited_house = False
        self.time_to_spawn = None
        self.float_position = None
        self.exit_house = False
        self.ghost_number = ghost_number
        self.ghost_house = ghost_house
        self.starting_position = (x, y)  # in window coordinates
        if self.ghost_house:
            ghost_house_entrance = ghost_house.get_entrance()
            if self.ghost_number == 0:
                self.starting_position = utilities.get_position_in_window(ghost_house_entrance[0],
                                                                          ghost_house_entrance[1],
                                                                          scale, window_width, window_height)
                x = self.starting_position[0]
                y = self.starting_position[1]
            elif self.ghost_number == 1:
                self.starting_position = utilities.get_position_in_window(ghost_house_entrance[0],
                                                                          ghost_house_entrance[1] + 3,
                                                                          scale, window_width, window_height)
                x = self.starting_position[0]
                y = self.starting_position[1]
            elif self.ghost_number == 2:
                self.starting_position = utilities.get_position_in_window(ghost_house_entrance[0] - 2,
                                                                          ghost_house_entrance[1] + 3,
                                                                          scale, window_width, window_height)
                x = self.starting_position[0]
                y = self.starting_position[1]
            elif self.ghost_number == 3:
                self.starting_position = utilities.get_position_in_window(ghost_house_entrance[0] + 2,
                                                                          ghost_house_entrance[1] + 3,
                                                                          scale, window_width, window_height)
                x = self.starting_position[0]
                y = self.starting_position[1]

            self.ghost_house.add_ghost(self)

        self.is_permanent_overwrite = False
        self.force_goal = None
        self.overwrite_clock = 0
        self.overwrite_time = 0
        self.global_state = None
        self.level_state_clock = 0
        self.timer_on_hold = 0
        self.frightened_speed = speed * 0.7
        self.frightened_time = 5
        self.type = ghost_type
        self.images = images
        self.current_image = 0
        # self.image = pygame.transform.scale(self.images[self.current_image], (scale * 1, scale * 1))
        self.image = pygame.Surface((scale * 1, scale * 1), pygame.SRCALPHA)  # Do not update this surface
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = (x, y)
        self.int_position = utilities.get_position_in_maze_int(self.rect.x, self.rect.y, scale, window_width,
                                                               window_height)
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 150
        self.window_width = window_width
        self.window_height = window_height
        self.scale = scale
        self.current_path = []
        self.current_speed = speed
        self.speed = speed
        self.direction = "stay"
        self.fps = fps
        self.goal = (0, 0)
        self.next_node = None
        self.previous_node = None
        self.empty_maze_data = []

        self.clyde_fleeing = False

        # test var for dead state
        self.dead_time = 5
        self.dead_timer = 0
        self.resume_state_timer = True

        # Variables for the different modes of the ghosts
        self.state = "scatter"
        if self.ghost_number == 0:
            self.stay_in_house = False
        else:
            self.stay_in_house = True

        self.movement_inside_house = "up"
        if self.ghost_number == 1:
            self.movement_inside_house = "down"
        self.spawn_clock = 0
        self.level_state_timer = 0  # in frames
        self.state_overwrite = False
        self.current_level_state = None

        # frightened animation variables
        self.frightened_images = fright_images
        self.flash_last_update = None
        self.flash_timer = None
        self.flash_white = False
        self.flash_cooldown = 5 * self.fps  # in frames
        self.flash_start = 2000

        if self.stay_in_house:
            if self.ghost_number == 1:
                self.time_to_spawn = 5
            elif self.ghost_number == 2:
                self.time_to_spawn = 10
            elif self.ghost_number == 3:
                self.time_to_spawn = 15

            self.overwrite_global_state("spawn", -1)

        # Variables for inky's behaviour
        self.ghost_to_pivot = None
        self.pivot = None

    is_permanent_state = False

    # Update method. It handles the animation of the ghost, the movement of the ghost, the pathfinding and the hurtbox
    # It also handles the different modes of the ghosts (chase, scatter, frightened, dead), that change depending on the
    # game time.
    def update(self, maze_data, pacmans, ghosts):
        self.empty_maze_data = [[0] * len(maze_data[0]) for _ in range(len(maze_data))]
        self.int_position = utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                               self.window_height)
        self.float_position = utilities.get_position_in_maze_float(self.rect.x, self.rect.y, self.scale,
                                                                   self.window_width,
                                                                   self.window_height)
        self.pivot = None

        self.check_collision(pacmans)
        self.update_overwritten_state()

        if self.respawning and not self.force_goal:  # return to normal speed after respawning
            self.apply_speed(self.state)
            self.respawning = False

        # change ghosts goal depending on the state
        if self.state == "spawn":
            self.current_speed = self.speed * 0.7
            self.spawn_clock += 1
            ghost_house_entrance = self.ghost_house.get_entrance()
            if self.spawn_clock >= self.time_to_spawn * self.fps and self.exit_house is False:
                self.set_force_goal((ghost_house_entrance[0], ghost_house_entrance[1] + 3))
                self.spawn_clock = 0
                self.exit_house = True
            elif self.movement_inside_house == "up" and self.force_goal is None:
                if self.ghost_number == 1:
                    self.set_force_goal((ghost_house_entrance[0], ghost_house_entrance[1] + 2))
                elif self.ghost_number == 2:
                    self.set_force_goal((ghost_house_entrance[0] - 2, ghost_house_entrance[1] + 2))
                elif self.ghost_number == 3:
                    self.set_force_goal((ghost_house_entrance[0] + 2, ghost_house_entrance[1] + 2))

                self.movement_inside_house = "down"
            elif self.movement_inside_house == "down" and self.force_goal is None:
                if self.ghost_number == 1:
                    self.set_force_goal((ghost_house_entrance[0], ghost_house_entrance[1] + 4))
                elif self.ghost_number == 2:
                    self.set_force_goal((ghost_house_entrance[0] - 2, ghost_house_entrance[1] + 4))
                elif self.ghost_number == 3:
                    self.set_force_goal((ghost_house_entrance[0] + 2, ghost_house_entrance[1] + 4))
                self.movement_inside_house = "up"
            if utilities.is_centered(self.float_position, self.force_goal) and self.exit_house:
                self.set_force_goal(ghost_house_entrance)
                self.stay_in_house = False
                self.current_speed = self.speed * 0.5

            if self.stay_in_house is False and self.next_node == ghost_house_entrance:
                self.exit_house = False
                self.exited_house = True
                self.overwrite_global_state(self.global_state, 0)
        elif self.state == "scatter":

            if self.type == "blinky":
                self.goal = (31, 0)
            elif self.type == "pinky":
                self.goal = (0, 0)
            elif self.type == "inky":
                self.goal = (31, 31)
            elif self.type == "clyde":
                self.goal = (0, 31)
            else:
                print("Error: ghost type not found when trying to scatter: " + self.type)
                self.goal = (0, 0)

        elif self.state == "chase":
            # self.current_path, self.goal = self.update_path_to_pacman(pacmans, maze_data)
            self.closest_pacman = None
            for pacman in pacmans:
                if not self.closest_pacman or utilities.get_distance(self.rect.x, self.rect.y, pacman.rect.x,
                                                                     pacman.rect.y) < utilities.get_distance(
                    self.rect.x,
                    self.rect.y,
                    self.closest_pacman.rect.x,
                    self.closest_pacman.rect.y):
                    self.closest_pacman = pacman
            if self.type == "blinky":  # get the closest pacman and set its position as the goal

                if self.closest_pacman is not None:
                    self.goal = utilities.get_position_in_maze_int(self.closest_pacman.rect.x,
                                                                   self.closest_pacman.rect.y,
                                                                   self.scale,
                                                                   self.window_width, self.window_height)
                else:
                    self.goal = None

            elif self.type == "pinky":  # get the closest pacman and set its position + 4 tiles in the direction it is
                # moving as the goal

                if self.closest_pacman is not None:
                    self.goal = utilities.get_position_in_maze_int(self.closest_pacman.rect.x,
                                                                   self.closest_pacman.rect.y,
                                                                   self.scale,
                                                                   self.window_width, self.window_height)
                    if self.closest_pacman.direction == "up":
                        self.goal = (self.goal[0], self.goal[1] - 4)
                    elif self.closest_pacman.direction == "down":
                        self.goal = (self.goal[0], self.goal[1] + 4)
                    elif self.closest_pacman.direction == "left":
                        self.goal = (self.goal[0] - 4, self.goal[1])
                    elif self.closest_pacman.direction == "right":
                        self.goal = (self.goal[0] + 4, self.goal[1])
                else:
                    self.goal = None

            elif self.type == "inky":  # get the closest pacman and set its position

                if self.closest_pacman is not None:
                    self.pivot = utilities.get_position_in_maze_int(self.closest_pacman.rect.x,
                                                                    self.closest_pacman.rect.y,
                                                                    self.scale,
                                                                    self.window_width, self.window_height)
                    if self.closest_pacman.direction == "up":
                        self.pivot = (self.pivot[0], self.pivot[1] - 2)
                    elif self.closest_pacman.direction == "down":
                        self.pivot = (self.pivot[0], self.pivot[1] + 2)
                    elif self.closest_pacman.direction == "left":
                        self.pivot = (self.pivot[0] - 2, self.pivot[1])
                    elif self.closest_pacman.direction == "right":
                        self.pivot = (self.pivot[0] + 2, self.pivot[1])

                    # if no ghost to pivot is found, get a ghost's position from the same ghost house. If no ghost
                    # house is found, use a random ghost instead
                    if self.ghost_to_pivot is None:
                        if self.ghost_house is not None:
                            # Get the position of the ghost with number equal to this
                            # ghost_number - 2. If it goes below 0, wrap around to the last ghost

                            ghosts_in_ghost_house = self.ghost_house.get_ghosts()
                            index = self.ghost_number
                            for i in range(2):
                                index -= 1
                                if index < 0:
                                    index = len(ghosts_in_ghost_house) - 1

                            self.ghost_to_pivot = ghosts_in_ghost_house[index]
                        else:
                            self.ghost_to_pivot = random.choice(ghosts.sprites())

                    # Set the goal by getting the vector from the pivot to the ghost and rotating it by 180 degrees
                    ghost_to_pivot_position = utilities.get_position_in_maze_int(self.ghost_to_pivot.rect.x,
                                                                                 self.ghost_to_pivot.rect.y,
                                                                                 self.scale,
                                                                                 self.window_width, self.window_height)
                    vector = (ghost_to_pivot_position[0] - self.pivot[0], ghost_to_pivot_position[1] - self.pivot[1])
                    vector = (vector[0] * -1, vector[1] * -1)
                    self.goal = (self.pivot[0] + vector[0], self.pivot[1] + vector[1])
                else:
                    self.goal = None
            elif self.type == "clyde":
                if self.closest_pacman is not None and utilities.get_distance(self.rect.x, self.rect.y,
                                                                              self.closest_pacman.rect.x,
                                                                              self.closest_pacman.rect.y) > 8 * self.scale:
                    self.goal = utilities.get_position_in_maze_int(self.closest_pacman.rect.x,
                                                                   self.closest_pacman.rect.y,
                                                                   self.scale,
                                                                   self.window_width, self.window_height)
                    self.clyde_fleeing = False
                elif self.closest_pacman is not None:
                    self.goal = (0, 31)
                    self.clyde_fleeing = True
                else:
                    self.goal = None
        elif self.state == "frightened":
            self.goal = None
        elif self.state == "dead":
            if self.ghost_house is not None:
                self.goal = self.ghost_house.get_entrance()
                entrance_int_pos = self.goal
            else:
                self.goal = utilities.get_position_in_maze_int(self.starting_position[0],
                                                               self.starting_position[1],
                                                               self.scale,
                                                               self.window_width, self.window_height)
                entrance_int_pos = self.goal
            float_position = utilities.get_position_in_maze_float(self.rect.x, self.rect.y, self.scale,
                                                                  self.window_width,
                                                                  self.window_height)

            if self.force_goal is None \
                    and self.int_position[0] == entrance_int_pos[0] \
                    and self.int_position[1] == entrance_int_pos[1]:
                if self.ghost_house is not None:
                    self.set_force_goal((self.goal[0], self.goal[1] + 3))
                else:
                    self.set_force_goal((self.goal[0], self.goal[1]))

            elif utilities.is_centered(float_position, self.force_goal):
                self.is_permanent_overwrite = False
                self.set_force_goal(entrance_int_pos)
                self.switch_state(self.global_state)
                self.respawning = True
                self.current_speed = self.speed * 0.5

        # self.change_direction(self.current_path)
        # self.move()
        if self.force_goal is not None:
            self.move_ghost_classic(self.force_goal, self.empty_maze_data)
            if utilities.is_centered(self.float_position, self.force_goal):
                self.force_goal = None
        else:
            if utilities.AStarMode[0]:
                use_wrap_around = not (self.state == "scatter" or (self.type == "clyde" and self.clyde_fleeing))
                self.move_ghost_astar(self.goal, maze_data, use_wrap_around)
            else:
                self.move_ghost_classic(self.goal, maze_data)

    def move(self):

        if self.direction == "up":
            self.position = (self.position[0], self.position[1] - self.current_speed)
        elif self.direction == "down":
            self.position = (self.position[0], self.position[1] + self.current_speed)
        elif self.direction == "left":
            self.position = (self.position[0] - self.current_speed, self.position[1])
        elif self.direction == "right":
            self.position = (self.position[0] + self.current_speed, self.position[1])

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
    def draw_astar_path(self, screen, maze_data):
        if self.goal is None:
            return
        color = self.get_ghost_color()
        offset = 0
        if color == (255, 255, 0):
            offset = 3
        elif color == (255, 0, 255):
            offset = 6
        elif color == (255, 128, 0):
            offset = -3

        self.draw_lines_in_path(color, maze_data, offset, screen, self.current_path)
        self.draw_pivot(color, screen)
        self.draw_clyde_circle(color, screen)
        self.draw_goal(color, screen)
        self.draw_forced_goal(color, screen)

    def draw_lines_in_path(self, color, maze_data, offset, screen, path_to_draw):
        if path_to_draw is None or len(path_to_draw) < 0:
            return

        for node in path_to_draw:
            (x, y) = utilities.get_position_in_window(node[0], node[1], self.scale, self.window_width,
                                                      self.window_height)
            # check if next node is in the same direction as the current node and draw a line to it if it is.
            # if not, draw a line to the middle of the tile and then draw a line to the next node
            if path_to_draw.index(node) + 1 < len(path_to_draw):
                (next_x, next_y) = utilities.get_position_in_window(
                    path_to_draw[path_to_draw.index(node) + 1][0],
                    path_to_draw[path_to_draw.index(node) + 1][1],
                    self.scale, self.window_width,
                    self.window_height)
                if node[0] == path_to_draw[path_to_draw.index(node) + 1][0]:
                    # if the next_y wraps around the maze, skip the line
                    if abs(y - next_y) > len(maze_data) / 2 * self.scale:
                        continue
                    pygame.draw.line(screen, color,
                                     (x + self.scale / 2 + offset, y + self.scale / 2 + offset),
                                     (x + self.scale / 2 + offset, next_y + self.scale / 2 + offset),
                                     3)
                elif node[1] == path_to_draw[path_to_draw.index(node) + 1][1]:
                    # if the next_x wraps around the maze, skip the line
                    if abs(x - next_x) > len(maze_data[0]) / 2 * self.scale:
                        continue
                    pygame.draw.line(screen, color,
                                     (x + self.scale / 2 + offset, y + self.scale / 2 + offset),
                                     (next_x + self.scale / 2 + offset, y + self.scale / 2 + offset),
                                     3)
                else:
                    # if the next_x wraps around the maze, skip the line
                    if abs(x - next_x) > len(maze_data[0]) / 2 * self.scale:
                        continue
                    pygame.draw.line(screen, color,
                                     (x + self.scale / 2 + offset, y + self.scale / 2 + offset),
                                     (x + self.scale / 2 + offset, y + self.scale / 2 + offset),
                                     3)
                    # if the next_y wraps around the maze, skip the line
                    if abs(y - next_y) > len(maze_data) / 2 * self.scale:
                        continue
                    pygame.draw.line(screen, color,
                                     (x + self.scale / 2 + offset, y + self.scale / 2 + offset),
                                     (next_x + self.scale / 2 + offset, next_y + self.scale / 2 + offset),
                                     3)

    def draw_pivot(self, color, screen):
        if self.pivot is not None and self.goal is not None:
            # draw a circle at the pivot
            pygame.draw.circle(screen, color, (
                utilities.get_position_in_window(self.pivot[0], self.pivot[1], self.scale, self.window_width,
                                                 self.window_height)[
                    0] + self.scale // 2,
                utilities.get_position_in_window(self.pivot[0], self.pivot[1], self.scale, self.window_width,
                                                 self.window_height)[
                    1] + self.scale // 2), 2)

    def get_ghost_color(self):
        color = (255, 255, 255)
        if self.type == "blinky":
            color = (255, 0, 0)
        elif self.type == "pinky":
            color = (255, 0, 255)
        elif self.type == "inky":
            color = (0, 255, 255)
        elif self.type == "clyde":
            color = (255, 128, 0)
        return color

    # Check collision with pacman. If collision, that pacman dies
    def check_collision(self, pacmans):
        if (self.state == "chase" or self.state == "scatter") and not utilities.invisibility_debug[0]:
            for pacman in pacmans:
                if self.rect.colliderect(pacman.rect):
                    pacman.die()
        elif self.state == "frightened":
            for pacman in pacmans:
                if self.rect.colliderect(pacman.rect) and (pacman.direction != "dying" and pacman.direction != "dead"):
                    self.overwrite_global_state("dead", -1)
                    utilities.add_sfx_to_queue("ghost_eaten.wav")
                    utilities.queued_popups.append(
                        (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2,
                         utilities.ghost_eaten_score[0],
                         (65, 167, 200), 1, 11))
                    utilities.ghost_eaten_score[0] *= 2

    def change_direction(self, path):
        # find in what direction is the next node in the path by comparing path[0] with path[1]
        # only change direction if the ghost is in the middle of a tile
        min_threshold = (0.05, 0.05)
        position = utilities.get_position_in_maze_float(self.position[0], self.position[1], self.scale,
                                                        self.window_width,
                                                        self.window_height)
        centerness = (position[0] - int(position[0]), position[1] - int(position[1]))
        if path and len(path) > 1:
            if centerness[0] < min_threshold[0] and centerness[1] < min_threshold[1]:
                # First, check if next node is wrapped around the map
                if path[0][0] == 0 and path[1][0] == 31:
                    self.direction = "left"
                    # self.position = (self.position[0], utilities.get_position_in_window(
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[0],
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[1], self.scale,
                    #     self.window_width, self.window_height)[1])
                elif path[0][0] == 31 and path[1][0] == 0:
                    self.direction = "right"
                    # self.position = (self.position[0], utilities.get_position_in_window(
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[0],
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[1], self.scale,
                    #     self.window_width, self.window_height)[1])
                elif path[0][1] == 0 and path[1][1] == 31:
                    self.direction = "up"
                    # self.position = (utilities.get_position_in_window(
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[0],
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[1], self.scale,
                    #     self.window_width, self.window_height)[0], self.position[1])
                elif path[0][1] == 31 and path[1][1] == 0:
                    self.direction = "down"
                    # self.position = (utilities.get_position_in_window(
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[0],
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[1], self.scale,
                    #     self.window_width, self.window_height)[0], self.position[1])

                elif path[0][0] < path[1][0]:
                    self.direction = "right"
                    # center ghost in the middle of the tile
                    # self.position = (self.position[0], utilities.get_position_in_window(
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[0],
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[1], self.scale,
                    #     self.window_width, self.window_height)[1])
                elif path[0][0] > path[1][0]:
                    self.direction = "left"
                    # self.position = (self.position[0], utilities.get_position_in_window(
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[0],
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[1], self.scale,
                    #     self.window_width, self.window_height)[1])
                elif path[0][1] < path[1][1]:
                    self.direction = "down"
                    # self.position = (utilities.get_position_in_window(
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[0],
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[1], self.scale,
                    #     self.window_width, self.window_height)[0], self.position[1])
                elif path[0][1] > path[1][1]:
                    self.direction = "up"
                    # self.position = (utilities.get_position_in_window(
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[0],
                    #     utilities.get_position_in_maze_int(self.position[0], self.position[1], self.scale,
                    #                                        self.window_width, self.window_height)[1], self.scale,
                    #     self.window_width, self.window_height)[0], self.position[1])
        else:
            self.direction = "stay"

    def move_ghost_astar(self, goal, maze_data, use_wrap_around):
        # To optimize the pathfinding, we only check the path every time the ghost is in the middle of a tile
        if goal is None:
            self.move_ghost_classic(goal, maze_data)
            return

        if utilities.is_centered(self.float_position, self.int_position):
            start = Node((self.int_position[0], self.int_position[1]))
            goal = Node((goal[0], goal[1]))
            self.current_path = self.pathfinder.get_path(start, goal, maze_data, use_wrap_around, [self.previous_node])

        if len(self.current_path) > 1:
            self.move_ghost_classic(self.current_path[1], maze_data)
        elif len(self.current_path) == 1:
            self.move_ghost_classic(self.current_path[0], maze_data)
        else:
            self.move_ghost_classic(None, maze_data)

    def my_draw(self, screen):
        now = pygame.time.get_ticks()
        if self.state == "chase" or self.state == "scatter" or self.state == "spawn":
            if now - self.last_update > self.animation_cooldown:
                self.last_update = now
                self.current_image = (self.current_image + 1) % 2

            self.my_image = pygame.Surface.copy(self.images[self.current_image])

            # add eyes on top of image depending on which direction the ghost is facing.
            # if no direction is given, the eyes are removed
            if self.direction == "right" or self.direction == "stay":
                self.my_image.blit(self.images[4], (0, 0))
            elif self.direction == "left":
                self.my_image.blit(self.images[5], (0, 0))
            elif self.direction == "up":
                self.my_image.blit(self.images[6], (0, 0))
            elif self.direction == "down":
                self.my_image.blit(self.images[7], (0, 0))

            self.my_image = pygame.transform.scale(self.my_image,
                                                   (self.scale * self.image_scale, self.scale * self.image_scale))

        elif self.state == "frightened":
            if now - self.flash_last_update > self.flash_cooldown:
                self.flash_last_update = now
                self.flash_white = not self.flash_white
            if now - self.last_update > self.animation_cooldown:
                self.last_update = now
                self.current_image = (self.current_image + 1) % 2
                if now - self.flash_timer > self.flash_start and self.flash_white:
                    self.my_image = pygame.transform.scale(self.frightened_images[self.current_image + 2],
                                                           (self.scale * self.image_scale,
                                                            self.scale * self.image_scale))
                else:
                    self.my_image = pygame.transform.scale(self.frightened_images[self.current_image],
                                                           (self.scale * self.image_scale,
                                                            self.scale * self.image_scale))

        elif self.state == "dead":

            self.my_image = pygame.Surface.copy(
                self.images[self.current_image])  # changed to 3 in trigger_dead_state method

            # add eyes on top of image depending on which direction the ghost is facing.
            # if no direction is given, the eyes are removed
            if self.direction == "right":
                self.my_image.blit(self.images[4], (0, 0))
            elif self.direction == "left":
                self.my_image.blit(self.images[5], (0, 0))
            elif self.direction == "up":
                self.my_image.blit(self.images[6], (0, 0))
            elif self.direction == "down":
                self.my_image.blit(self.images[7], (0, 0))

            self.my_image = pygame.transform.scale(self.my_image,
                                                   (self.scale * self.image_scale, self.scale * self.image_scale))

        screen.blit(self.my_image, (self.rect.x - self.scale * 0.25, self.rect.y - self.scale * 0.25))

    # Move the ghost towards the goal the way it worked in the original game
    def move_ghost_classic(self, goal, maze_data):

        use_wrap_around = False

        int_position = utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                          self.window_height)
        float_position = utilities.get_position_in_maze_float(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                              self.window_height)

        # if the ghost is in the middle of the tile, it takes the decision of which tile to move next

        if self.next_node is None \
                or ((abs(float_position[0] - float(self.next_node[0])) <= 0.02 and abs(float_position[1] - float(
            self.next_node[
                1])) <= 0.02)) and not (self.next_node == goal and self.force_goal):  # Use to make ghost stay in goal

            # get the available tiles around the ghost. If the tile is not a wall, add it to the list of available
            # tiles. The ghost can't move to the tile it came from. If the tile to be checked would be out of bounds,
            # check the tile on the opposite side of the maze to account for the wrap around effect.
            available_tiles = []
            if int_position[1] - 1 >= 0:
                if maze_data[int_position[1] - 1][int_position[0]] != 1:
                    if self.direction != "down" or self.force_goal is not None:
                        available_tiles.append("up")
            else:
                if maze_data[len(maze_data) - 1][int_position[0]] != 1:
                    if self.direction != "down" or self.force_goal is not None:
                        available_tiles.append("up")

            if int_position[0] + 1 < len(maze_data[0]):
                if maze_data[int_position[1]][int_position[0] + 1] != 1:
                    if self.direction != "left" or self.force_goal is not None:
                        available_tiles.append("right")
            else:
                if maze_data[int_position[1]][0] != 1:
                    if self.direction != "left" or self.force_goal is not None:
                        available_tiles.append("right")

            if int_position[1] + 1 < len(maze_data):
                if maze_data[int_position[1] + 1][int_position[0]] != 1:
                    if self.direction != "up" or self.force_goal is not None:
                        available_tiles.append("down")
            else:
                if maze_data[0][int_position[0]] != 1:
                    if self.direction != "up" or self.force_goal is not None:
                        available_tiles.append("down")

            if int_position[0] - 1 >= 0:
                if maze_data[int_position[1]][int_position[0] - 1] != 1:
                    if self.direction != "right" or self.force_goal is not None:
                        available_tiles.append("left")

            else:
                if maze_data[int_position[1]][len(maze_data[0]) - 1] != 1:
                    if self.direction != "right" or self.force_goal is not None:
                        available_tiles.append("left")

            # if no available tiles are found, but the ghost can back track, it will do so
            if len(available_tiles) == 0:
                if ((int_position[1] + 1 < len(maze_data) and maze_data[int_position[1] + 1][int_position[0]] != 1) \
                    or (int_position[1] + 1 >= len(maze_data) and maze_data[0][
                            int_position[0]] != 1)) and self.direction == "up":
                    available_tiles.append("down")
                elif ((int_position[0] + 1 < len(maze_data[0]) and maze_data[int_position[1]][int_position[0] + 1] != 1) \
                      or (int_position[0] + 1 >= len(maze_data[0]) and maze_data[int_position[1]][
                            0] != 1)) and self.direction == "left":
                    available_tiles.append("right")
                elif ((int_position[1] - 1 >= 0 and maze_data[int_position[1] - 1][int_position[0]] != 1) \
                      or (int_position[1] - 1 < 0 and maze_data[len(maze_data) - 1][
                            int_position[0]] != 1)) and self.direction == "down":
                    available_tiles.append("up")
                elif ((int_position[0] - 1 >= 0 and maze_data[int_position[1]][int_position[0] - 1] != 1) \
                      or (int_position[0] - 1 < 0 and maze_data[int_position[1]][
                            len(maze_data[0]) - 1] != 1)) and self.direction == "right":
                    available_tiles.append("left")

            # if there is a goal to go to, calculate the shortest path. If there is no goal, choose a new direction
            # randomly
            if goal is not None:
                self.change_direction_to_closest_tile(available_tiles, goal, int_position, maze_data, use_wrap_around)
            else:
                self.change_direction_randomly(available_tiles, int_position, maze_data)

        # move the ghost in the direction it decided to move
        if self.next_node is not None:
            position_of_next_node = utilities.get_position_in_window(self.next_node[0], self.next_node[1], self.scale,
                                                                     self.window_width, self.window_height)
        else:
            position_of_next_node = utilities.get_position_in_window(int_position[0], int_position[1], self.scale,
                                                                     self.window_width, self.window_height)
        if self.direction == "stay":
            pass
        elif self.direction == "right":
            # if adding speed were to make the ghost overshoot the center of the tile, move it to the center
            if self.rect.x + self.current_speed > position_of_next_node[0]:
                self.position = position_of_next_node
            else:
                self.position = (self.position[0] + self.current_speed, self.position[1])
        elif self.direction == "left":
            if self.rect.x - self.current_speed < position_of_next_node[0]:
                self.position = position_of_next_node
            else:
                self.position = (self.position[0] - self.current_speed, self.position[1])
        elif self.direction == "down":
            if self.rect.y + self.current_speed > position_of_next_node[1]:
                self.position = position_of_next_node
            else:
                self.position = (self.position[0], self.position[1] + self.current_speed)
        elif self.direction == "up":
            if self.rect.y - self.current_speed < position_of_next_node[1]:
                self.position = position_of_next_node
            else:
                self.position = (self.position[0], self.position[1] - self.current_speed)

        # if the ghost is out of the bounds of the maze, move it to the opposite side of the maze, taking into account
        # the scale and position of the maze
        left_bound_in_window = self.window_width / 2 - self.scale * len(maze_data[0]) / 2
        right_bound_in_window = self.window_width / 2 + self.scale * len(maze_data[0]) / 2
        top_bound_in_window = self.window_height / 2 - self.scale * len(maze_data) / 2
        bottom_bound_in_window = self.window_height / 2 + self.scale * len(maze_data) / 2

        if self.rect.x < left_bound_in_window:
            self.position = (right_bound_in_window - self.scale, self.position[1])
        elif self.rect.x > right_bound_in_window - self.scale:
            self.position = (left_bound_in_window, self.position[1])
        if self.rect.y < top_bound_in_window:
            self.position = (self.position[0], bottom_bound_in_window - self.scale)
        elif self.rect.y > bottom_bound_in_window - self.scale:
            self.position = (self.position[0], top_bound_in_window)

        self.rect.topleft = round(self.position[0]), round(self.position[1])

    def change_direction_to_closest_tile(self, available_tiles, goal, int_position, maze_data, use_wrap_around):
        # Now get the distance to the goal from each available tile taking into account the wrap around effect (if
        # set to true). The tile with the shortest distance to the goal is the one the ghost will move to.
        shortest_distance = None
        distance = None
        for tile in available_tiles:
            if tile == "right":
                if int_position[0] + 1 < len(maze_data[0]):
                    distance = utilities.get_distance(int_position[0] + 1, int_position[1], goal[0], goal[1],
                                                      use_wrap_around)
                else:
                    distance = utilities.get_distance(0, int_position[1], goal[0], goal[1], use_wrap_around)

            elif tile == "left":
                if int_position[0] - 1 >= 0:
                    distance = utilities.get_distance(int_position[0] - 1, int_position[1], goal[0], goal[1],
                                                      use_wrap_around)
                else:
                    distance = utilities.get_distance(len(maze_data[0]) - 1, int_position[1], goal[0], goal[1],
                                                      use_wrap_around)

            elif tile == "down":
                if int_position[1] + 1 < len(maze_data):
                    distance = utilities.get_distance(int_position[0], int_position[1] + 1, goal[0], goal[1],
                                                      use_wrap_around)
                else:
                    distance = utilities.get_distance(int_position[0], 0, goal[0], goal[1], use_wrap_around)

            elif tile == "up":
                if int_position[1] - 1 >= 0:
                    distance = utilities.get_distance(int_position[0], int_position[1] - 1, goal[0], goal[1],
                                                      use_wrap_around)
                else:
                    distance = utilities.get_distance(int_position[0], len(maze_data) - 1, goal[0], goal[1],
                                                      use_wrap_around)

            if shortest_distance is None or distance < shortest_distance \
                    or (distance == shortest_distance and (
                    (tile == "up") or (tile == "left" and self.direction != "up") or (
                    tile == "down" and self.direction == "right"))):
                shortest_distance = distance
                self.direction = tile
                self.previous_node = int_position
                if tile == "right":
                    if int_position[0] + 1 < len(maze_data[0]):
                        self.next_node = (int_position[0] + 1, int_position[1])
                    else:
                        self.next_node = (0, int_position[1])
                elif tile == "left":
                    if int_position[0] - 1 >= 0:
                        self.next_node = (int_position[0] - 1, int_position[1])
                    else:
                        self.next_node = (len(maze_data[0]) - 1, int_position[1])
                elif tile == "down":
                    if int_position[1] + 1 < len(maze_data):
                        self.next_node = (int_position[0], int_position[1] + 1)
                    else:
                        self.next_node = (int_position[0], 0)
                elif tile == "up":
                    if int_position[1] - 1 >= 0:
                        self.next_node = (int_position[0], int_position[1] - 1)
                    else:
                        self.next_node = (int_position[0], len(maze_data) - 1)

    def draw_classic_path(self, screen, maze_data):
        if self.goal is None:
            return

        # Draw a line connecting all the tiles that the ghost would have blocked_positions if it was using the classic path
        path_to_draw = []
        if self.int_position is not None and self.direction != "stay":
            path_to_draw = [self.int_position]
            current_direction = self.direction
            for i in range(100):
                next_tile, current_direction = self.find_next_node_classic(path_to_draw[-1],
                                                                           self.goal, maze_data, current_direction)
                if next_tile not in path_to_draw:
                    path_to_draw.append(next_tile)
                else:
                    path_to_draw.append(next_tile)
                    break
                if path_to_draw[-1] == self.goal:
                    break

        color = self.get_ghost_color()
        offset = 0
        if color == (255, 255, 0):
            offset = 3
        elif color == (255, 0, 255):
            offset = 6
        elif color == (255, 128, 0):
            offset = -3

        self.draw_lines_in_path(color, maze_data, offset, screen, path_to_draw)
        self.draw_goal(color, screen)
        self.draw_forced_goal(color, screen)
        self.draw_pivot(color, screen)
        self.draw_clyde_circle(color, screen)

    def draw_forced_goal(self, color, screen):
        if self.force_goal is not None:
            # draw an X at the center of the forced goal
            pygame.draw.line(screen, color, (
                utilities.get_position_in_window(self.force_goal[0], self.force_goal[1], self.scale, self.window_width,
                                                 self.window_height)[
                    0] + self.scale // 2 - 5,
                utilities.get_position_in_window(self.force_goal[0], self.force_goal[1], self.scale, self.window_width,
                                                 self.window_height)[
                    1] + self.scale // 2 - 5), (
                                 utilities.get_position_in_window(self.force_goal[0], self.force_goal[1], self.scale,
                                                                  self.window_width, self.window_height)[
                                     0] + self.scale // 2 + 5,
                                 utilities.get_position_in_window(self.force_goal[0], self.force_goal[1], self.scale,
                                                                  self.window_width, self.window_height)[
                                     1] + self.scale // 2 + 5), 5)
            pygame.draw.line(screen, color, (
                utilities.get_position_in_window(self.force_goal[0], self.force_goal[1], self.scale, self.window_width,
                                                 self.window_height)[
                    0] + self.scale // 2 + 5,
                utilities.get_position_in_window(self.force_goal[0], self.force_goal[1], self.scale, self.window_width,
                                                 self.window_height)[
                    1] + self.scale // 2 - 5), (
                                 utilities.get_position_in_window(self.force_goal[0], self.force_goal[1], self.scale,
                                                                  self.window_width, self.window_height)[
                                     0] + self.scale // 2 - 5,
                                 utilities.get_position_in_window(self.force_goal[0], self.force_goal[1], self.scale,
                                                                  self.window_width, self.window_height)[
                                     1] + self.scale // 2 + 5), 5)

    def draw_clyde_circle(self, color, screen):
        # draw line from current tile to goal
        if self.type == "clyde" and self.closest_pacman is not None and self.state == "chase":
            # Draw circle around closest pacman to indicate where clyde is not chasing pacman

            pacman_position = (self.closest_pacman.rect.x + self.scale / 2, self.closest_pacman.rect.y + self.scale / 2)
            pygame.draw.circle(screen, color, pacman_position, 8 * self.scale, 1)

    def turn_around(self):
        if self.force_goal:
            return
        # Reverse the direction the ghost is facing. Change the next node to the node behind the ghost if the ghost is
        # not past the center of the tile. Change the next node to the current node if the ghost is  past the center of
        # the tile.
        if self.direction == "up":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "up"
        elif self.direction == "left":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "left"

        temp = self.next_node
        self.next_node = self.previous_node
        self.previous_node = temp

    def change_direction_randomly(self, available_tiles, int_position, maze_data):
        # change the ghost's direction randomly
        if len(available_tiles) < 1:
            self.direction = "stay"
            return

        self.direction = random.choice(available_tiles)
        self.previous_node = int_position
        if self.direction == "right":
            if int_position[0] + 1 < len(maze_data[0]):
                self.next_node = (int_position[0] + 1, int_position[1])
            else:
                self.next_node = (0, int_position[1])
        elif self.direction == "left":
            if int_position[0] - 1 >= 0:
                self.next_node = (int_position[0] - 1, int_position[1])
            else:
                self.next_node = (len(maze_data[0]) - 1, int_position[1])
        elif self.direction == "down":
            if int_position[1] + 1 < len(maze_data):
                self.next_node = (int_position[0], int_position[1] + 1)
            else:
                self.next_node = (int_position[0], 0)
        elif self.direction == "up":
            if int_position[1] - 1 >= 0:
                self.next_node = (int_position[0], int_position[1] - 1)
            else:
                self.next_node = (int_position[0], len(maze_data) - 1)

    def set_global_state(self, state):
        self.global_state = state

    def switch_state(self, state):
        if state is None or (state == "frightened" and self.state == "dead") or (
                self.exited_house is False and self.state == "spawn"):
            return False
        if state == self.state:  # reapply some state specific things
            self.apply_speed(state)
            if state == "frightened":
                self.flash_timer = pygame.time.get_ticks()
                self.flash_last_update = pygame.time.get_ticks()
            return False
        self.state = state
        # switch the ghost to a state
        if state == "dead":
            utilities.set_stop_time(0.5)
            self.current_image = 3
            self.my_image = pygame.transform.scale(self.images[self.current_image],
                                                   (self.scale * self.image_scale, self.scale * self.image_scale))
            utilities.add_sfx_to_queue("eat_ghost.wav")
        elif state == "frightened":
            # reverse ghosts current direction
            self.turn_around()

            self.current_image = 0
            self.my_image = pygame.transform.scale(self.frightened_images[self.current_image],
                                                   (self.scale * self.image_scale, self.scale * self.image_scale))
            self.flash_timer = pygame.time.get_ticks()
            self.flash_last_update = pygame.time.get_ticks()
        elif state == "chase" or state == "scatter":
            self.turn_around()

        self.apply_speed(state)
        return True

    def overwrite_global_state(self, state, time):
        self.switch_state(state)
        self.state_overwrite = True
        self.overwrite_clock = 0
        if time == -1:
            self.is_permanent_overwrite = True
        else:
            self.is_permanent_overwrite = False
            self.overwrite_time = time * self.fps

    def update_overwritten_state(self):
        if not self.state_overwrite:
            self.switch_state(self.global_state)
            return

        self.overwrite_clock += 1
        if self.overwrite_clock >= self.overwrite_time and not self.is_permanent_overwrite:
            self.state_overwrite = False
            self.switch_state(self.global_state)

    def set_force_goal(self, goal):
        self.force_goal = goal
        # self.change_direction_to_closest_tile(["right", "left", "up", "down"], self.force_goal,
        #                                       utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale,
        #                                                                          self.window_width,
        #                                                                          self.window_height),
        #                                       self.empty_maze_data,
        #                                       False)

    def apply_speed(self, state):
        if state == "frightened":
            self.current_speed = self.frightened_speed
        elif state == "dead":
            self.current_speed = self.speed * 1.5
        else:
            self.current_speed = self.speed

    def get_state(self):
        return self.state

    def find_next_node_classic(self, position, goal, maze_data, direction):
        next_node_to_draw = None

        use_wrap_around = False

        # get the available tiles around the ghost. If the tile is not a wall, add it to the list of available
        # tiles. The ghost can't move to the tile it came from. If the tile to be checked would be out of bounds,
        # check the tile on the opposite side of the maze to account for the wrap around effect.
        available_tiles = []
        if position[1] - 1 >= 0:
            if maze_data[position[1] - 1][position[0]] != 1:
                if direction != "down" or self.force_goal is not None:
                    available_tiles.append("up")
        else:
            if maze_data[len(maze_data) - 1][position[0]] != 1:
                if direction != "down" or self.force_goal is not None:
                    available_tiles.append("up")

        if position[0] + 1 < len(maze_data[0]):
            if maze_data[position[1]][position[0] + 1] != 1:
                if direction != "left" or self.force_goal is not None:
                    available_tiles.append("right")
        else:
            if maze_data[position[1]][0] != 1:
                if direction != "left" or self.force_goal is not None:
                    available_tiles.append("right")

        if position[1] + 1 < len(maze_data):
            if maze_data[position[1] + 1][position[0]] != 1:
                if direction != "up" or self.force_goal is not None:
                    available_tiles.append("down")
        else:
            if maze_data[0][position[0]] != 1:
                if direction != "up" or self.force_goal is not None:
                    available_tiles.append("down")

        if position[0] - 1 >= 0:
            if maze_data[position[1]][position[0] - 1] != 1:
                if direction != "right" or self.force_goal is not None:
                    available_tiles.append("left")

        else:
            if maze_data[position[1]][len(maze_data[0]) - 1] != 1:
                if direction != "right" or self.force_goal is not None:
                    available_tiles.append("left")

        # if no available tiles are found, but the ghost can back track, it will do so
        if len(available_tiles) == 0:
            if ((position[1] + 1 < len(maze_data) and maze_data[position[1] + 1][position[0]] != 1) \
                or (position[1] + 1 >= len(maze_data) and maze_data[0][
                        position[0]] != 1)) and direction == "up":
                available_tiles.append("down")
            elif ((position[0] + 1 < len(maze_data[0]) and maze_data[position[1]][position[0] + 1] != 1) \
                  or (position[0] + 1 >= len(maze_data[0]) and maze_data[position[1]][
                        0] != 1)) and direction == "left":
                available_tiles.append("right")
            elif ((position[1] - 1 >= 0 and maze_data[position[1] - 1][position[0]] != 1) \
                  or (position[1] - 1 < 0 and maze_data[len(maze_data) - 1][
                        position[0]] != 1)) and direction == "down":
                available_tiles.append("up")
            elif ((position[0] - 1 >= 0 and maze_data[position[1]][position[0] - 1] != 1) \
                  or (position[0] - 1 < 0 and maze_data[position[1]][
                        len(maze_data[0]) - 1] != 1)) and direction == "right":
                available_tiles.append("left")

        # if there is a goal to go to, calculate the shortest path. If there is no goal, choose a new direction
        # randomly
        shortest_distance = None
        distance = None
        for tile in available_tiles:
            if tile == "right":
                if position[0] + 1 < len(maze_data[0]):
                    distance = utilities.get_distance(position[0] + 1, position[1], goal[0], goal[1],
                                                      use_wrap_around)
                else:
                    distance = utilities.get_distance(0, position[1], goal[0], goal[1], use_wrap_around)

            elif tile == "left":
                if position[0] - 1 >= 0:
                    distance = utilities.get_distance(position[0] - 1, position[1], goal[0], goal[1],
                                                      use_wrap_around)
                else:
                    distance = utilities.get_distance(len(maze_data[0]) - 1, position[1], goal[0], goal[1],
                                                      use_wrap_around)

            elif tile == "down":
                if position[1] + 1 < len(maze_data):
                    distance = utilities.get_distance(position[0], position[1] + 1, goal[0], goal[1],
                                                      use_wrap_around)
                else:
                    distance = utilities.get_distance(position[0], 0, goal[0], goal[1], use_wrap_around)

            elif tile == "up":
                if position[1] - 1 >= 0:
                    distance = utilities.get_distance(position[0], position[1] - 1, goal[0], goal[1],
                                                      use_wrap_around)
                else:
                    distance = utilities.get_distance(position[0], len(maze_data) - 1, goal[0], goal[1],
                                                      use_wrap_around)

            if shortest_distance is None or distance < shortest_distance \
                    or (distance == shortest_distance and (
                    (tile == "up") or (tile == "left" and direction != "up") or (
                    tile == "down" and direction == "right"))):
                shortest_distance = distance
                direction = tile
                if tile == "right":
                    if position[0] + 1 < len(maze_data[0]):
                        next_node_to_draw = (position[0] + 1, position[1])
                    else:
                        next_node_to_draw = (0, position[1])
                elif tile == "left":
                    if position[0] - 1 >= 0:
                        next_node_to_draw = (position[0] - 1, position[1])
                    else:
                        next_node_to_draw = (len(maze_data[0]) - 1, position[1])
                elif tile == "down":
                    if position[1] + 1 < len(maze_data):
                        next_node_to_draw = (position[0], position[1] + 1)
                    else:
                        next_node_to_draw = (position[0], 0)
                elif tile == "up":
                    if position[1] - 1 >= 0:
                        next_node_to_draw = (position[0], position[1] - 1)
                    else:
                        next_node_to_draw = (position[0], len(maze_data) - 1)
        return next_node_to_draw, direction

    def draw_goal(self, color, screen):
        if self.state == "spawn":
            return
        pygame.draw.circle(screen, color, (
            utilities.get_position_in_window(self.goal[0], self.goal[1], self.scale, self.window_width,
                                             self.window_height)[
                0] + self.scale // 2,
            utilities.get_position_in_window(self.goal[0], self.goal[1], self.scale, self.window_width,
                                             self.window_height)[
                1] + self.scale // 2), 5)
