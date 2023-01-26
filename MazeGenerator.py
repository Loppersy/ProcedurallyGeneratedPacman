import random

import pygame

import utilities
from AStar import AStar, Node

# TODO: Restore A* algorithm

BRANCH_LENGTH = 30
BRANCH_MIN_LENGTH = 2
BRANCH_CHANCE_PER_LENGTH = 20
BRANCH_CHANCE_PENALTY_PER_BRANCH = 10
BRANCH_DIRCHANGE_CHANCE = 40
BRANCH_CAN_WRAP_AROUND = False
POWER_PELLETS_PER_SIDE = 2


class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze_data = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.directions = ["up", "right", "down", "left"]

    # Generate left side of the maze_data (the right side will be generated by mirroring the left side)
    def generate(self):
        # First, a ghost house is placed in the maze_data at a random location in the vertical middle(keeping in mind that
        # the ghost house is 8x5 and that the surrounding tiles are empty, and that these empty tiles are not on the
        # edge of the maze_data)
        self.maze_data = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        ghost_house_pos = self.find_available_position(self.visited, self.width // 2 - 5, -1, 10, 7)
        # ghost_house_pos = (self.width // 2 - 5 , 2)

        # now we add the empty tiles around the ghost house (the walls will be added during the maze_data population)
        for i in range(ghost_house_pos[0], ghost_house_pos[0] + 10):
            for j in range(ghost_house_pos[1], ghost_house_pos[1] + 7):
                self.maze_data[j][i] = 0
                self.visited[j][i] = True

        self.maze_data[ghost_house_pos[1] + 1][ghost_house_pos[0] + 1] = 4

        # Now we select a random tile that has not been visited yet and place pacman there. (it must not be on the
        # edge of the maze_data)
        pacman_pos = self.find_available_position(self.visited, self.width // 2 - 1, -1, 2, 1)
        # pacman_pos = (self.width // 2 - 1, 10)
        self.maze_data[pacman_pos[1]][pacman_pos[0]] = 5
        self.maze_data[pacman_pos[1]][pacman_pos[0] + 1] = 0
        self.visited[pacman_pos[1]][pacman_pos[0]] = True
        self.visited[pacman_pos[1]][pacman_pos[0] + 1] = True
        self.visited[pacman_pos[1] + 1][pacman_pos[0]] = True
        self.visited[pacman_pos[1] + 1][pacman_pos[0] + 1] = True
        self.visited[pacman_pos[1] - 1][pacman_pos[0]] = True
        self.visited[pacman_pos[1] - 1][pacman_pos[0] + 1] = True

        # Now we select a random tile that has not been visited yet and place a bonus fruit. (it must not be on the
        # edge of the maze_data)
        bonus_pos = self.find_available_position(self.visited, self.width // 2 - 1, -1, 2, 1)
        # bonus_pos = (self.width // 2 - 8, 12)
        self.maze_data[bonus_pos[1]][bonus_pos[0]] = 6
        self.maze_data[bonus_pos[1]][bonus_pos[0] + 1] = 0
        self.visited[bonus_pos[1]][bonus_pos[0]] = True
        self.visited[bonus_pos[1]][bonus_pos[0] + 1] = True
        self.visited[bonus_pos[1] + 1][bonus_pos[0]] = True
        self.visited[bonus_pos[1] + 1][bonus_pos[0] + 1] = True
        self.visited[bonus_pos[1] - 1][bonus_pos[0]] = True
        self.visited[bonus_pos[1] - 1][bonus_pos[0] + 1] = True

        # Generate "branches" starting from the ghost house, bonus fruit and pacman positions
        # self.generate_branch(bonus_pos[0] - 6, bonus_pos[1]+1, "right", BRANCH_LENGTH, False, True)
        self.generate_branch(pacman_pos[0] - 1, pacman_pos[1], "left", BRANCH_LENGTH, False, True)
        self.generate_branch(bonus_pos[0] - 1, bonus_pos[1], "left", BRANCH_LENGTH, False, True)

        possible_ghost_house_branches = [(-1, 0, "left"), (-1, 1, "left"), (-1, 2, "left"), (-1, 3, "left"),
                                         (-1, 4, "left"), (-1, 5, "left"), (-1, 6, "left"),
                                         (0, -1, "up"), (1, -1, "up"), (2, -1, "up"), (3, -1, "up"),
                                         (0, 7, "down"), (1, 7, "down"), (2, 7, "down"), (3, 7, "down")]
        chosen_ghost_house_branches = []
        branches_count = random.randint(2, 3)
        for i in range(branches_count):
            index = random.randint(0, len(possible_ghost_house_branches) - 1)
            while (ghost_house_pos[0] + possible_ghost_house_branches[index][0] < 1 or \
                   ghost_house_pos[0] + possible_ghost_house_branches[index][0] >= self.width - 1 or \
                   ghost_house_pos[1] + possible_ghost_house_branches[index][1] < 1 or \
                   ghost_house_pos[1] + possible_ghost_house_branches[index][1] >= self.height - 1) \
                    and len(possible_ghost_house_branches) > 1:
                possible_ghost_house_branches.pop(index)
                index = random.randint(0, len(possible_ghost_house_branches) - 1)

            if len(possible_ghost_house_branches) < 1: print(" No possible branches left")
            chosen_ghost_house_branches.append(possible_ghost_house_branches[index])

            if (index == 0 or index == len(possible_ghost_house_branches) - 2) and len(
                    possible_ghost_house_branches) > 2:
                for j in range(2):
                    possible_ghost_house_branches.pop(index)
            elif index == len(possible_ghost_house_branches) - 1 and len(possible_ghost_house_branches) > 1:
                possible_ghost_house_branches.pop(index)
            elif len(possible_ghost_house_branches) > 3:
                for j in range(3):
                    possible_ghost_house_branches.pop(index - 1)

        for i in range(branches_count):
            self.generate_branch(ghost_house_pos[0] + chosen_ghost_house_branches[i][0],
                                 ghost_house_pos[1] + chosen_ghost_house_branches[i][1],
                                 chosen_ghost_house_branches[i][2], BRANCH_LENGTH, False)

        # for i in range(len(possible_ghost_house_branches)):
        #     self.generate_branch(ghost_house_pos[0] + possible_ghost_house_branches[i][0],
        #                          ghost_house_pos[1] + possible_ghost_house_branches[i][1],
        #                          possible_ghost_house_branches[i][2], 40, False)

        # Add two power pellets in the maze_data
        self.add_power_pellets(POWER_PELLETS_PER_SIDE)

        # Mirror the left side of the maze_data to the right side
        for i in range(self.height):
            for j in range(self.width // 2):
                if self.maze_data[i][j] == 0 or self.maze_data[i][j] == 1 or self.maze_data[i][j] == 2 or \
                        self.maze_data[i][j] == 3:
                    self.maze_data[i][self.width - j - 1] = self.maze_data[i][j]
                else:
                    self.maze_data[i][self.width - j - 1] = 0

        # ensure that all tiles are accessible. if not, create a tunnel between the ghost house and pacman and the bonus
        # fruit

        # find which object has the highest y value
        positions = [(pacman_pos[0] - 1, pacman_pos[1]), (bonus_pos[0] - 1, bonus_pos[1]), ghost_house_pos]
        lowest_y = min(positions, key=lambda x: x[1])[1]
        highest_y = max(positions, key=lambda x: x[1])[1]
        middle_y = 0
        lowest_pos = None
        middle_pos = None
        highest_pos = None
        for i in range(len(positions)):
            if positions[i][1] != lowest_y and positions[i][1] != highest_y:
                middle_y = positions[i][1]
                break

        for i in range(len(positions)):
            if positions[i][1] == lowest_y:
                lowest_pos = positions[i]
            elif positions[i][1] == middle_y:
                middle_pos = positions[i]
            elif positions[i][1] == highest_y:
                highest_pos = positions[i]

        # utilities.add_highlighted_tile(lowest_pos, (255, 0, 0))
        # utilities.add_highlighted_tile(middle_pos, (255, 255, 0))
        # utilities.add_highlighted_tile(highest_pos, (255, 255, 255))

        path_finder = AStar()
        # if path_finder.is_reachable(Node(lowest_pos), Node(middle_pos), self.maze_data):
        #     path = path_finder.get_path(Node(lowest_pos), Node(middle_pos), self.maze_data, True)
        #     for i in range(len(path)):
        #         utilities.add_highlighted_tile(path[i], (255, 0, 255))

        if not path_finder.is_reachable(Node(lowest_pos), Node(middle_pos), self.maze_data):
            closest_node_lowest_pos = path_finder.get_path(Node(lowest_pos), Node(middle_pos), self.maze_data, False)[
                -1]
            closest_node_middle_pos = \
                path_finder.get_path(Node(middle_pos), Node(closest_node_lowest_pos), self.maze_data, False)[-1]

            utilities.add_highlighted_tile(closest_node_lowest_pos, (255, 0, 0))
            utilities.add_highlighted_tile(closest_node_middle_pos, (0, 255, 0))

            # if closest_node_middle_pos == closest_node_lowest_pos:
            #     closest_node_middle_pos = middle_pos
            self.create_tunel(path_finder.get_tunel(Node(closest_node_lowest_pos),
                                                    Node(closest_node_middle_pos),
                                                    self.maze_data))

        # if path_finder.is_reachable(Node(middle_pos), Node(highest_pos), self.maze_data):
        #     path = path_finder.get_path(Node(middle_pos), Node(highest_pos), self.maze_data, True)
        #     for i in range(len(path)):
        #         utilities.add_highlighted_tile(path[i], (255, 255, 255))

        if not path_finder.is_reachable(Node(middle_pos), Node(highest_pos), self.maze_data):
            closest_node_middle_pos = path_finder.get_path(Node(middle_pos), Node(highest_pos), self.maze_data, False)[
                -1]

            closest_node_highest_pos = \
                path_finder.get_path(Node(highest_pos), Node(closest_node_middle_pos), self.maze_data, False)[-1]

            utilities.add_highlighted_tile(closest_node_middle_pos, (255, 255, 0))
            utilities.add_highlighted_tile(closest_node_highest_pos, (0, 255, 255))

            # if closest_node_middle_pos == closest_node_highest_pos:
            #     closest_node_highest_pos = highest_pos
            self.create_tunel(path_finder.get_tunel(Node(closest_node_middle_pos),
                                                    Node(closest_node_highest_pos),
                                                    self.maze_data))

        # mirror the changes once again
        # Mirror the left side of the maze_data to the right side
        for i in range(self.height):
            for j in range(self.width // 2):
                if self.maze_data[i][j] == 0 or self.maze_data[i][j] == 1 or self.maze_data[i][j] == 2 or \
                        self.maze_data[i][j] == 3:
                    self.maze_data[i][self.width - j - 1] = self.maze_data[i][j]

    def get_maze_data(self):
        # for i in range(self.height):
        #     for j in range(self.width):
        #         if self.visited[i][j]:
        #             utilities.add_highlighted_tile((j, i), (255, 255, 255))
        return self.maze_data

    def find_available_position(self, visited, x_lock, y_lock, width, height, object_spacing=1):

        x = random.randint(1, self.width - width)
        y = random.randint(1, self.height - height)

        if x_lock != -1:
            x = x_lock
            available_y = []
            for i in range(object_spacing, self.height - height):
                size_fit = True
                for j in range(-object_spacing, width + object_spacing):
                    for k in range(-object_spacing, height + object_spacing):
                        if visited[i + k][x + j]:
                            size_fit = False
                if not visited[i][x] and size_fit:
                    available_y.append(i)
            if len(available_y) > 0:
                y = available_y[random.randint(0, len(available_y) - 1)]
                return x, y
            else:
                print("No available position in x axis", x)
                return -1, -1
        if y_lock != -1:
            y = y_lock
            available_x = []
            for i in range(object_spacing, self.width - width):
                size_fit = True
                for j in range(-object_spacing, width + object_spacing):
                    for k in range(-object_spacing, height + object_spacing):
                        if visited[y + k][i + j]:
                            size_fit = False
                if not visited[y][i] and size_fit:
                    available_x.append(i)
            if len(available_x) > 0:
                x = available_x[random.randint(0, len(available_x) - 1)]
                return x, y
            else:
                print("No available position in y axis", y)
                return -1, -1

        available_x = []
        available_y = []
        for i in range(self.width // 2 - width):
            for j in range(self.height // 2 - height):
                size_fit = True
                for k in range(-object_spacing, width + object_spacing):
                    for l in range(-object_spacing, height + object_spacing):
                        if visited[j + l][i + k]:
                            size_fit = False
                if not visited[j][i] and size_fit:
                    available_x.append(i)
                    available_y.append(j)
        if len(available_x) > 0:
            x = available_x[random.randint(0, len(available_x) - 1)]
            y = available_y[random.randint(0, len(available_y) - 1)]

        return x, y

    def generate_branch(self, x, y, direction=None, branch_length=50, backtracking=True, force_first_tile=False, branch_number=1):
        current_x = x
        current_y = y
        og_length = branch_length
        if direction is None:
            my_direction = random.choice(self.directions)
        else:
            my_direction = direction

        if (not self.visited[current_y][current_x] and self.does_not_create_2x2(current_x, current_y,
                                                                                "stay", True)) or force_first_tile:
            self.visited[current_y][current_x] = True
            self.maze_data[current_y][current_x] = 2
            same_direction_count = 0
            while True:

                if self.does_not_create_2x2(current_x, current_y, my_direction, BRANCH_CAN_WRAP_AROUND):
                    current_x, current_y = self.add_direction(current_x, current_y, my_direction, True)
                    same_direction_count += 1
                else:
                    old_direction = my_direction
                    my_direction = self.change_direction(current_x, current_y, my_direction, backtracking)
                    same_direction_count = 0
                    if old_direction == my_direction:
                        self.continue_tunel_until_connection(current_x, current_y, my_direction)
                        break
                    current_x, current_y = self.add_direction(current_x, current_y, my_direction, True)

                self.maze_data[current_y][current_x] = 2
                self.visited[current_y][current_x] = True
                branch_length -= 1

                if branch_length <= 0:
                    self.continue_tunel_until_connection(current_x, current_y, my_direction)
                    break

                if random.randint(0,100) < BRANCH_CHANCE_PER_LENGTH * same_direction_count \
                        and same_direction_count > BRANCH_MIN_LENGTH \
                        and not (current_x == 0 or current_x == self.width - 1 or current_y == 0 or current_y == self.height - 1):
                    if random.randint(0, 100) < BRANCH_DIRCHANGE_CHANCE - BRANCH_CHANCE_PENALTY_PER_BRANCH * (branch_number - 1):
                        new_branch_direction = self.change_direction(current_x, current_y, my_direction, backtracking)
                        new_branch_x, new_branch_y = self.add_direction(current_x, current_y, new_branch_direction)
                        same_direction_count = 0
                        self.generate_branch(new_branch_x, new_branch_y, new_branch_direction, branch_length,
                                             True, False, branch_number + 1)
                    else:
                        same_direction_count = 0
                        my_direction = self.change_direction(current_x, current_y, my_direction, backtracking)

    def continue_tunel_until_connection(self, x, y, direction):
        current_x = x
        current_y = y
        my_direction = direction
        # utilities.add_highlighted_tile((current_x, current_y), (255, 0, 0))
        # utilities.add_highlighted_tile(self.add_direction(current_x, current_y, my_direction, True), (255, 0, 0))

        while self.no_empty_neighbors(current_x, current_y, my_direction):
            if (not self.does_not_create_2x2(current_x, current_y, my_direction, True) or \
                    self.visited[self.add_direction(current_x, current_y, my_direction, True)[1]][
                        self.add_direction(current_x, current_y, my_direction, True)[0]]) or \
                    my_direction == "up" or my_direction == "down":
                my_direction = self.change_direction(current_x, current_y, my_direction, False, True)
                print("change direction", my_direction)

            current_x, current_y = self.add_direction(current_x, current_y, my_direction, True)
            self.visited[current_y][current_x] = True
            self.maze_data[current_y][current_x] = 2

        # utilities.add_highlighted_tile((current_x, current_y), (255, 0, 0))

    def change_direction(self, current_x, current_y, direction, backtracking=True, wrap_around=False):
        old_direction = direction
        if direction == "up" or direction == "down":
            my_direction = random.choice(["left", "right"])
        else:
            my_direction = random.choice(["up", "down"])
        continue_prev_direction = True
        if not self.does_not_create_2x2(current_x, current_y, my_direction):
            if my_direction == "up":
                my_direction = "down"
            elif my_direction == "down":
                my_direction = "up"
            elif my_direction == "left":
                my_direction = "right"
            elif my_direction == "right":
                my_direction = "left"
        else:
            continue_prev_direction = False
        if not self.does_not_create_2x2(current_x, current_y, my_direction):
            if my_direction == "up":
                my_direction = "down"
            elif my_direction == "down":
                my_direction = "up"
            elif my_direction == "left":
                my_direction = "right"
            elif my_direction == "right":
                my_direction = "left"
        else:
            continue_prev_direction = False

        if not backtracking \
                and ((my_direction == "up" and old_direction == "down")
                     or (my_direction == "down" and old_direction == "up")
                     or (my_direction == "left" and old_direction == "right")
                     or (my_direction == "right" and old_direction == "left")):
            print("Backtracking not allowed, reverting to old direction")
            return old_direction

        new_x, new_y = self.add_direction(current_x, current_y, my_direction)
        if (new_x < 1 or new_x >= self.width // 2 - 1 or new_y < 1 or new_y >= self.height - 1) and not wrap_around:
            return old_direction

        if continue_prev_direction:
            return old_direction
        else:
            return my_direction

    def add_direction(self, current_x, current_y, my_direction, wrap_around=False):
        if my_direction == "up":
            current_y -= 1
        elif my_direction == "down":
            current_y += 1
        elif my_direction == "left":
            current_x -= 1
        elif my_direction == "right":
            current_x += 1

        if wrap_around:
            if current_x < 0:
                current_x = self.width - 1
            if current_x >= self.width:
                current_x = 0
            if current_y < 0:
                current_y = self.height - 1
            if current_y >= self.height:
                current_y = 0
        return current_x, current_y

    def does_not_create_2x2(self, current_x, current_y, my_direction, wrap_around=False):
        if my_direction != "stay":
            new_x, new_y = self.add_direction(current_x, current_y, my_direction, True)
        else:
            new_x = current_x
            new_y = current_y

        if (new_x < 1 or new_x >= self.width - 1 or new_y < 1 or new_y >= self.height - 1) and not wrap_around:
            return False
        if self.visited[new_y][new_x]:
            return False

        # check that the new position wont result in a 2x2 area of walkable tiles
        # [bottomleft, bottom, bottomright, left, middle, right, topleft, top, topright ]
        color = (pygame.Color('white'))
        color.hsva = (random.randint(0, 360), 100, 100, 100)

        walkable_tiles = [False] * 9
        for i in range(-1, 2):
            for j in range(-1, 2):
                if wrap_around:
                    temp_y = new_y + j
                    if temp_y < 0:
                        temp_y += self.height
                    elif temp_y >= self.height:
                        temp_y -= self.height
                    temp_x = new_x + i
                    if temp_x < 0:
                        temp_x += self.width
                    elif temp_x >= self.width:
                        temp_x -= self.width

                    if self.maze_data[temp_y][temp_x] != 1:
                        walkable_tiles[(j + 1) * 3 + i + 1] = True

                else:
                    if 0 <= new_y + j < self.height and 0 <= new_x + i < self.width and self.maze_data[new_y + j][
                        new_x + i] != 1:
                        walkable_tiles[(j + 1) * 3 + i + 1] = True

        walkable_tiles[4] = True
        if (walkable_tiles[0] and walkable_tiles[1] and walkable_tiles[3] and walkable_tiles[4]) \
                or (walkable_tiles[1] and walkable_tiles[2] and walkable_tiles[4] and walkable_tiles[5]) \
                or (walkable_tiles[3] and walkable_tiles[4] and walkable_tiles[6] and walkable_tiles[7]) \
                or (walkable_tiles[4] and walkable_tiles[5] and walkable_tiles[7] and walkable_tiles[8]):
            return False

        return True

    def no_empty_neighbors(self, current_x, current_y, my_direction, ignore_visited_walls=True):

        neighbors_to_check = []
        if my_direction == "up":
            if current_x - 1 < 0:
                neighbors_to_check = [(self.width - 1, current_y), (current_x, current_y - 1),
                                      (current_x + 1, current_y)]
            elif current_x + 1 >= self.width:
                neighbors_to_check = [(current_x - 1, current_y), (current_x, current_y - 1), (0, current_y)]
            elif current_y - 1 < 0:
                neighbors_to_check = [(current_x - 1, current_y), (current_x, self.height - 1),
                                      (current_x + 1, current_y)]
            else:
                neighbors_to_check = [(current_x - 1, current_y), (current_x, current_y - 1),
                                      (current_x + 1, current_y)]
        elif my_direction == "down":
            if current_x - 1 < 0:
                neighbors_to_check = [(self.width - 1, current_y), (current_x, current_y + 1),
                                      (current_x + 1, current_y)]
            elif current_x + 1 >= self.width:
                neighbors_to_check = [(current_x - 1, current_y), (current_x, current_y + 1), (0, current_y)]
            elif current_y + 1 >= self.height:
                neighbors_to_check = [(current_x - 1, current_y), (current_x, 0), (current_x + 1, current_y)]
            else:
                neighbors_to_check = [(current_x - 1, current_y), (current_x, current_y + 1),
                                      (current_x + 1, current_y)]
        elif my_direction == "left":
            if current_y - 1 < 0:
                neighbors_to_check = [(current_x, self.height - 1), (current_x - 1, current_y),
                                      (current_x, current_y + 1)]
            elif current_y + 1 >= self.height:
                neighbors_to_check = [(current_x, current_y - 1), (current_x - 1, current_y), (current_x, 0)]
            elif current_x - 1 < 0:
                neighbors_to_check = [(self.width - 1, current_y), (current_x, current_y - 1),
                                      (current_x, current_y + 1)]
            else:
                neighbors_to_check = [(current_x, current_y - 1), (current_x - 1, current_y),
                                      (current_x, current_y + 1)]
        elif my_direction == "right":
            if current_y - 1 < 0:
                neighbors_to_check = [(current_x, self.height - 1), (current_x + 1, current_y),
                                      (current_x, current_y + 1)]
            elif current_y + 1 >= self.height:
                neighbors_to_check = [(current_x, current_y - 1), (current_x + 1, current_y), (current_x, 0)]
            elif current_x + 1 >= self.width:
                neighbors_to_check = [(0, current_y), (current_x, current_y - 1), (current_x, current_y + 1)]
            else:
                neighbors_to_check = [(current_x, current_y - 1), (current_x + 1, current_y),
                                      (current_x, current_y + 1)]

        for x, y in neighbors_to_check:
            if ignore_visited_walls:
                if self.maze_data[y][x] != 1:
                    return False
            else:
                if self.visited[y][x]:
                    return False

        return True

    def ensure_all_tiles_accessible(self, pacman_pos):
        positions_to_check = []
        for y in range(self.height):
            for x in range(self.width):
                if self.maze_data[y][x] != 1 and self.visited[y][x]:
                    positions_to_check.append((x, y))

        path_finder = AStar()
        while len(positions_to_check) > 1:
            old_len = len(positions_to_check)
            path = path_finder.get_path(Node((pacman_pos[0], pacman_pos[1])),
                                        Node((positions_to_check[1][0], positions_to_check[1][1])), self.maze_data)
            for x, y in path:
                for i, j in positions_to_check:
                    if i == x and j == y:
                        positions_to_check.remove((i, j))
                        break

            if len(positions_to_check) == old_len:
                return False

        return True

    def create_tunel(self, path):
        if not path:
            return
        for x, y in path:
            # utilities.add_highlighted_tile((x, y), (0, 255, 0))
            if self.maze_data[y][x] == 1:
                self.maze_data[y][x] = 2

    def add_power_pellets(self, number_of_power_pellets):
        power_pellets_pos = []
        attempted_positions = []
        power_pellets_added = 0
        while power_pellets_added < number_of_power_pellets:
            x = random.randint(0, self.width // 3 - 1)
            y = random.randint(0, self.height - 1)
            attempted_positions.append((x, y))
            if len(attempted_positions) > self.get_number_of_pellets():
                print("Could not add all power pellets")
                return
            if self.maze_data[y][x] == 2:
                pick_new = False
                if len(power_pellets_pos) > 0:
                    for i, j in power_pellets_pos:
                        if abs(j - y) < self.get_diff_between_h_l_pellet() // (number_of_power_pellets + 1):
                            pick_new = True
                            break
                if pick_new:
                    continue
                power_pellets_pos.append((x, y))
                self.maze_data[y][x] = 3
                power_pellets_added += 1


    def get_number_of_pellets(self):
        number_of_pellets = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.maze_data[y][x] == 2:
                    number_of_pellets += 1

        return number_of_pellets
    def get_diff_between_h_l_pellet(self):
        lowest_y = self.height
        highest_y = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.maze_data[y][x] == 2:
                    if y < lowest_y:
                        lowest_y = y
                    if y > highest_y:
                        highest_y = y

        return highest_y - lowest_y
