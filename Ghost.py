import pygame

import utilities
from AStar import AStar, Node


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, images, fright_images, ghost_type, window_width, window_height, scale, fps, level, speed):
        super().__init__()

        self.timer_on_hold = 0
        self.frightened_speed = speed * 0.7
        self.frightened_time = 5
        self.type = ghost_type
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
        self.current_speed = speed
        self.speed = speed
        self.direction = "stay"
        self.fps = fps
        self.level = level
        self.goal = (0, 0)
        self.next_node = None
        self.previous_node = None

        # Variables for the different modes of the ghosts
        self.state = "scatter"
        self.state_timer = 0  # in frames
        # times of the different modes for each level. In seconds
        self.state_times = [
            [("scatter", 7), ("chase", 20), ("scatter", 7), ("chase", 20), ("scatter", 5), ("chase", 20),
             ("scatter", 5), ("chase", -1)],  # level 1
            [("scatter", 7), ("chase", 20), ("scatter", 7), ("chase", 20), ("scatter", 5), ("chase", 1033),
             ("scatter", 1), ("chase", -1)],  # level 2 - 4
            [("scatter", 5), ("chase", 20), ("scatter", 5), ("chase", 20), ("scatter", 5), ("chase", 1037),
             ("scatter", 1), ("chase", -1)]]  # level 5+

        # frightened animation variables
        self.frightened_images = fright_images
        self.flash_last_update = None
        self.flash_timer = None
        self.flash_white = False
        self.flash_cooldown = 5 * self.fps  # in frames
        self.flash_start = 2000

    is_permanent_state = False

    # Update method. It handles the animation of the ghost, the movement of the ghost, the pathfinding and the hurtbox
    # It also handles the different modes of the ghosts (chase, scatter, frightened, dead), that change depending on the
    # game time.
    def update(self, pacmans, maze_data):

        self.check_collision(pacmans)

        # update the state of the ghost

        self.state_timer += 1
        if self.state == "frightened" and self.state_timer > self.frightened_time * self.fps:
            self.state = self.state_times[self.level - 1][0][0]
            self.state_timer = self.timer_on_hold
            # revert speed to normal
            self.current_speed = self.speed
            self.turn_around()

        elif self.state_timer > self.state_times[self.level - 1][0][1] * self.fps and not self.is_permanent_state:
            self.state_times[self.level - 1].pop(0)
            self.state = self.state_times[self.level - 1][0][0]
            self.state_timer = 0
            if self.state_times[self.level - 1][0][1] == -1:
                self.is_permanent_state = True

            if self.state == "scatter" or self.state == "chase":
                # reverse ghosts current direction
                self.turn_around()

        # change ghosts goal depending on the state
        if self.state == "scatter":

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

            # fix A* bug eventually
            # self.current_path = self.pathfinder.get_path(Node(
            #     utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width,
            #                                        self.window_height)), Node(
            #     (self.goal[0], self.goal[1])), maze_data)
        elif self.state == "chase":
            # self.current_path, self.goal = self.update_path_to_pacman(pacmans, maze_data)

            if self.type == "blinky":  # get the closest pacman and set its position as the goal
                closest_pacman = None
                for pacman in pacmans:
                    if not closest_pacman or utilities.get_distance(self.rect.x, self.rect.y, pacman.rect.x,
                                                                    pacman.rect.y) < utilities.get_distance(self.rect.x,
                                                                                                            self.rect.y,
                                                                                                            closest_pacman.rect.x,
                                                                                                            closest_pacman.rect.y):
                        closest_pacman = pacman
                if closest_pacman is not None:
                    self.goal = utilities.get_position_in_maze_int(closest_pacman.rect.x, closest_pacman.rect.y,
                                                                   self.scale,
                                                                   self.window_width, self.window_height)
                else:
                    self.state = "scatter"

            elif self.type == "pinky":  # get the closest pacman and set its position + 4 tiles in the direction it is
                # moving as the goal
                closest_pacman = None
                for pacman in pacmans:
                    if not closest_pacman or utilities.get_distance(self.rect.x, self.rect.y, pacman.rect.x,
                                                                    pacman.rect.y) < utilities.get_distance(self.rect.x,
                                                                                                            self.rect.y,
                                                                                                            closest_pacman.rect.x,
                                                                                                            closest_pacman.rect.y):
                        closest_pacman = pacman
                if closest_pacman is not None:
                    self.goal = utilities.get_position_in_maze_int(closest_pacman.rect.x, closest_pacman.rect.y,
                                                                   self.scale,
                                                                   self.window_width, self.window_height)
                    if closest_pacman.direction == "up":
                        self.goal = (self.goal[0], self.goal[1] - 4)
                    elif closest_pacman.direction == "down":
                        self.goal = (self.goal[0], self.goal[1] + 4)
                    elif closest_pacman.direction == "left":
                        self.goal = (self.goal[0] - 4, self.goal[1])
                    elif closest_pacman.direction == "right":
                        self.goal = (self.goal[0] + 4, self.goal[1])
                else:
                    self.state = "scatter"

        elif self.state == "frightened":
            self.goal = (0, 0)
            # TODO: implement frightened mode
        elif self.state == "dead":
            print("dead")
            # TODO: implement dead mode

        # self.change_direction(self.current_path)
        # self.move()

        self.move_ghost_classic(self.goal, maze_data)
        self.draw_ghost()

    #

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
            # finally, draw a circle at current goal
            (x, y) = utilities.get_position_in_window(self.goal[0], self.goal[1], self.scale, self.window_width,
                                                      self.window_height)
            pygame.draw.circle(screen, (255, 0, 0), (x + self.scale / 2, y + self.scale / 2), 5)

        # draw the path using the classic greedy algorithm

    # Check collision with pacman. If collision, that pacman dies
    def check_collision(self, pacmans):
        for pacman in pacmans:
            if self.rect.colliderect(pacman.rect):
                pacman.die()

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

    def update_path_to_pacman(self, pacmans, maze_data):

        if self.type == "blinky":
            # take the shortest path to any pacman
            shortest_path = []
            goal = None
            for pacman in pacmans:
                path = self.pathfinder.get_path(Node(
                    utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                       self.window_height)), Node(
                    utilities.get_position_in_maze_int(pacman.rect.x, pacman.rect.y, self.scale, self.window_width,
                                                       self.window_height)), maze_data)
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    goal = (
                        utilities.get_position_in_maze_int(pacman.rect.x, pacman.rect.y, self.scale, self.window_width,
                                                           self.window_height))
            return shortest_path, goal

    def draw_ghost(self):
        now = pygame.time.get_ticks()
        if self.state == "chase" or self.state == "scatter":
            if now - self.last_update > self.animation_cooldown:
                self.last_update = now
                self.current_image = (self.current_image + 1) % 2
                self.image = self.images[self.current_image]
            # add image[4] (eyes) on top of image
            self.image.blit(self.images[4], (0, 0))
            # TODO: scale image to be 1.5 times bigger than the tile and center it to the middle of the tile
            self.image = pygame.transform.scale(self.images[self.current_image], (self.scale * 1, self.scale * 1))
        elif self.state == "frightened":
            if now - self.flash_last_update > self.flash_cooldown:
                self.flash_last_update = now
                self.flash_white = not self.flash_white
            if now - self.last_update > self.animation_cooldown:
                self.last_update = now
                self.current_image = (self.current_image + 1) % 2
                if now - self.flash_timer > self.flash_start and self.flash_white:
                    self.image = pygame.transform.scale(self.frightened_images[self.current_image + 2],
                                                        (self.scale * 1, self.scale * 1))
                else:
                    self.image = pygame.transform.scale(self.frightened_images[self.current_image],
                                                        (self.scale * 1, self.scale * 1))

    # Move the ghost towards the goal the way it worked in the original game
    def move_ghost_classic(self, goal, maze_data):

        use_wrap_around = False

        int_position = utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                          self.window_height)
        float_position = utilities.get_position_in_maze_float(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                              self.window_height)

        # if the ghost is in the middle of the tile, it takes the decision of which tile to move next
        # and float_position[1] == int_position[1]:
        if self.next_node is None or (
                abs(float_position[0] - float(self.next_node[0])) <= 0.02 and abs(
            float_position[1] - float(self.next_node[1])) <= 0.02):

            # get the available tiles around the ghost. If the tile is not a wall, add it to the list of available
            # tiles. The ghost can't move to the tile it came from. If the tile to be checked would be out of bounds,
            # check the tile on the opposite side of the maze to account for the wrap around effect.
            available_tiles = []
            if int_position[1] - 1 >= 0:
                if maze_data[int_position[1] - 1][int_position[0]] != 1:
                    if self.direction != "down":
                        available_tiles.append("up")
            else:
                if maze_data[len(maze_data) - 1][int_position[0]] != 1:
                    if self.direction != "down":
                        available_tiles.append("up")

            if int_position[0] + 1 < len(maze_data[0]):
                if maze_data[int_position[1]][int_position[0] + 1] != 1:
                    if self.direction != "left":
                        available_tiles.append("right")
            else:
                if maze_data[int_position[1]][0] != 1:
                    if self.direction != "left":
                        available_tiles.append("right")

            if int_position[1] + 1 < len(maze_data):
                if maze_data[int_position[1] + 1][int_position[0]] != 1:
                    if self.direction != "up":
                        available_tiles.append("down")
            else:
                if maze_data[0][int_position[0]] != 1:
                    if self.direction != "up":
                        available_tiles.append("down")

            if int_position[0] - 1 >= 0:
                if maze_data[int_position[1]][int_position[0] - 1] != 1:
                    if self.direction != "right":
                        available_tiles.append("left")

            else:
                if maze_data[int_position[1]][len(maze_data[0]) - 1] != 1:
                    if self.direction != "right":
                        available_tiles.append("left")

            # Now get the distance to the goal from each available tile taking into account the wrap around effect.
            # The tile with the shortest distance to the goal is the one the ghost will move to.
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

                if not shortest_distance or distance < shortest_distance \
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

        # move the ghost in the direction it decided to move
        position_of_next_node = utilities.get_position_in_window(self.next_node[0], self.next_node[1], self.scale,
                                                                 self.window_width, self.window_height)
        if self.direction == "right":
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

    def draw_classic_path(self, screen, maze_data):
        # draw a red line that predicts the path that the ghost is going to take.
        current_tile = utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                          self.window_height)
        temp_direction = self.direction

        # draw circle at goal
        color = (255, 255, 255)
        if self.type == "blinky":
            color = (255, 0, 0)
        elif self.type == "pinky":
            color = (255, 0, 255)

        pygame.draw.circle(screen, color, (
            utilities.get_position_in_window(self.goal[0], self.goal[1], self.scale, self.window_width,
                                             self.window_height)[
                0] + self.scale // 2,
            utilities.get_position_in_window(self.goal[0], self.goal[1], self.scale, self.window_width,
                                             self.window_height)[
                1] + self.scale // 2), 5)

        # draw line from current tile to goal

    def trigger_frightening_state(self):
        # change the ghost's state to frightened
        self.state = "frightened"
        self.timer_on_hold = self.state_timer
        self.state_timer = 0
        self.current_speed = self.frightened_speed

        # reverse ghosts current direction
        self.turn_around()

        # if self.direction == "up":
        #     self.direction = "down"
        # elif self.direction == "down":
        #     self.direction = "up"
        # elif self.direction == "left":
        #     self.direction = "right"
        # elif self.direction == "right":
        #     self.direction = "left"

        self.current_image = 0
        self.image = pygame.transform.scale(self.frightened_images[self.current_image],
                                            (self.scale * 1, self.scale * 1))
        self.flash_timer = pygame.time.get_ticks()
        self.flash_last_update = pygame.time.get_ticks()

    def turn_around(self):
        int_position = utilities.get_position_in_maze_int(self.rect.x, self.rect.y, self.scale, self.window_width,
                                                          self.window_height)

        # Reverse the direction the ghost is facing. Change the next node to the node behind the ghost if the ghost is
        # not past the center of the tile. Change the next node to the current node if the ghost is  past the center of
        # the tile.
        if self.direction == "up":
            self.direction = "down"
            # if self.rect.y > utilities.get_position_in_window(int_position[0], int_position[1], self.scale,
            #                                                   self.window_width, self.window_height)[
            #     1] + self.scale / 2:
            #     self.next_node = int_position
            # else:
            #     self.next_node = (int_position[0], int_position[1] + 1)
        elif self.direction == "down":
            self.direction = "up"
            # if self.rect.y < utilities.get_position_in_window(int_position[0], int_position[1], self.scale,
            #                                                   self.window_width, self.window_height)[
            #     1] + self.scale / 2:
            #     self.next_node = int_position
            # else:
            #     self.next_node = (int_position[0], int_position[1] - 1)
        elif self.direction == "left":
            self.direction = "right"
            # if self.rect.x > utilities.get_position_in_window(int_position[0], int_position[1], self.scale,
            #                                                   self.window_width, self.window_height)[
            #     0] + self.scale / 2:
            #     self.next_node = int_position
            # else:
            #     self.next_node = (int_position[0] + 1, int_position[1])
        elif self.direction == "right":
            self.direction = "left"
            # if self.rect.x < utilities.get_position_in_window(int_position[0], int_position[1], self.scale,
            #                                                   self.window_width, self.window_height)[
            #     0] + self.scale / 2:
            #     self.next_node = int_position
            # else:
            #     self.next_node = (int_position[0] - 1, int_position[1])

        self.next_node = self.previous_node
