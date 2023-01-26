import random

import pygame

import utilities


class AStar(object):
    def __init__(self):
        self.start = None
        self.goal = None
        self.grid = None
        self.open = []
        self.closed = []
        self.path = []
        self.current = None

    # Return a list of tuples as a path from the given start to the given end in the given maze.
    # The path is the shortest path from the start to the end.
    # The path can take any direction as long as there is not a wall in the way (id 1 in grid).
    def get_path(self, start, goal, maze_data, use_wrap_around=True, blocked_positions=None):

        self.start = start
        self.goal = goal

        new_x, new_y = utilities.get_closest_walkable_tile(self.goal.position[0], self.goal.position[1], maze_data)

        # utilities.add_highlighted_tile((new_x, new_y), (255, 0, 0))
        self.goal.position = (new_x, new_y)

        self.grid = maze_data
        self.open = []
        self.closed = []
        self.path = []
        self.current = None

        # Add the start node to the open list
        # and update its values as well as the surrounding nodes
        if blocked_positions is not None:
            for blocked_position in blocked_positions:
                if blocked_position is not None:
                    blocked_node = Node((blocked_position[0], blocked_position[1]), 0, 0, 100000, None)
                    self.closed.append(blocked_node)
        self.calculate_values(self.start.position[0], self.start.position[1], Node(None, 0, 0, 0, None),
                              use_wrap_around)
        self.update_surrounding_nodes(self.start, use_wrap_around)
        self.open.remove(self.start)
        self.closed.append(self.start)

        while len(self.open) > 0:
            # Get the open node with smallest f value
            self.current = self.open[0]
            for node in self.open:
                if self.current is None or node.f <= self.current.f:
                    self.current = node

            # Create a list of nodes that are not walls and are not in the closed list
            # for the nodes around the current node (up, down, left, right)
            # calculate the g, h, and f values for each node and add it to the open list
            # if the node to be checked is out of bounds, assume it is a wall

            self.update_surrounding_nodes(self.current, use_wrap_around)

            # Remove the current node from the open list and add it to the closed list
            self.open.remove(self.current)
            self.closed.append(self.current)

            # Found the goal.
            if self.current == self.goal:
                path = []
                current = self.current
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                return path[::-1]

        # If the goal cannot be reached, make a path to the closest node to the goal
        # First, find the closest node to the goal
        # get random color
        # color = (pygame.Color('white'))
        # color.hsva = (random.randint(0, 360), 100, 100, 100)
        # for node in self.closed:
        #     utilities.add_highlighted_tile((node.position[0], node.position[1]), color)

        closest_node = self.closed[0]
        for node in self.closed:
            if self.heuristic(node.position, self.goal.position, use_wrap_around) < self.heuristic(
                    closest_node.position,
                    self.goal.position, use_wrap_around):
                closest_node = node

        # Then, make a path to that node
        path = []
        current = closest_node
        while current is not None:
            path.append(current.position)
            current = current.parent
        return path[::-1]

    def is_reachable(self, start, goal, maze_data):
        self.start = start
        self.goal = goal
        self.grid = maze_data
        self.open = []
        self.closed = []
        self.path = []
        self.current = None

        # Add the start node to the open list
        # and update its values as well as the surrounding nodes
        self.calculate_values(self.start.position[0], self.start.position[1], Node(None, 0, 0, 0, None))
        self.update_surrounding_nodes(self.start)
        self.open.remove(self.start)
        self.closed.append(self.start)

        while len(self.open) > 0:
            # Get the open node with smallest f value
            self.current = self.open[0]
            for node in self.open:
                if self.current is None or node.f <= self.current.f:
                    self.current = node

            # Create a list of nodes that are not walls and are not in the closed list
            # for the nodes around the current node (up, down, left, right)
            # calculate the g, h, and f values for each node and add it to the open list
            # if the node to be checked is out of bounds, assume it is a wall

            self.update_surrounding_nodes(self.current)

            # Remove the current node from the open list and add it to the closed list
            self.open.remove(self.current)
            self.closed.append(self.current)

            # Found the goal.
            if self.current == self.goal:
                return True

        return False

    # Like get path but gets a valid path among walls for a tunnel to be placed
    def get_tunel(self, start, goal, maze_data):
        # get random color
        # color = (pygame.Color('white'))
        # color.hsva = (random.randint(0, 360), 100, 100, 100)
        # utilities.add_highlighted_tile(start.position, color)
        # utilities.add_highlighted_tile(goal.position, color)
        self.start = start
        self.goal = goal
        self.grid = maze_data
        self.open = []
        self.closed = []
        self.path = []
        self.current = None

        # Add the start node to the open list
        # and update its values as well as the surrounding nodes
        self.calculate_values(self.start.position[0], self.start.position[1], Node(None, 0, 0, 0, None), False)
        self.update_surrounding_nodes_tunel(self.start)
        self.open.remove(self.start)
        self.closed.append(self.start)

        while len(self.open) > 0:
            # Get the open node with smallest f value
            self.current = self.open[0]
            for node in self.open:
                if self.current is None or node.f <= self.current.f:
                    self.current = node

            # Create a list of nodes that are not walls and are not in the closed list
            # for the nodes around the current node (up, down, left, right)
            # calculate the g, h, and f values for each node and add it to the open list
            # if the node to be checked is out of bounds, assume it is a wall

            self.update_surrounding_nodes_tunel(self.current)

            # Remove the current node from the open list and add it to the closed list
            self.open.remove(self.current)
            self.closed.append(self.current)

            # Found the goal.
            if self.current == self.goal:
                path = []
                current = self.current
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                return path[::-1]

        # If the goal cannot be reached, print an error message
        print("Error: Tunel goal cannot be reached")
        print(" Start :", self.start.position)
        print(" Goal :", self.goal.position)
        print(" Closed list :", self.closed)
        # If the goal cannot be reached, make a path to the closest node to the goal
        # First, find the closest node to the goal
        closest_node = self.closed[0]
        for node in self.closed:
            if self.heuristic(node.position, self.goal.position) < self.heuristic(closest_node.position,
                                                                                  self.goal.position):
                closest_node = node

        # Then, make a path to that node
        path = []
        current = closest_node
        while current is not None:
            path.append(current.position)
            current = current.parent

        return path[::-1]

    def update_surrounding_nodes_tunel(self, node):
        # Checking "up" node
        if node.position[1] - 1 >= 0:
            if (not self.is_in_closed((node.position[0], node.position[1] - 1))
                and self.does_not_create_2x2(node.position[0], node.position[1] - 1)) \
                    or (node.position[0], node.position[1] - 1) == self.goal.position:
                self.calculate_values(node.position[0], node.position[1] - 1, node, False)

        # Checking "down" node
        if node.position[1] + 1 <= len(self.grid[0]):
            if (not self.is_in_closed(
                    (node.position[0], node.position[1] + 1)) and self.does_not_create_2x2(node.position[0],
                                                                                           node.position[1] + 1)) \
                    or (node.position[0], node.position[1] + 1) == self.goal.position:
                self.calculate_values(node.position[0], node.position[1] + 1, node, False)

        # Checking "left" node
        if node.position[0] - 1 >= 0:
            if (not self.is_in_closed(
                    (node.position[0] - 1, node.position[1])) and self.does_not_create_2x2(node.position[0] - 1,
                                                                                           node.position[1])) \
                    or (node.position[0] - 1, node.position[1]) == self.goal.position:
                self.calculate_values(node.position[0] - 1, node.position[1], node, False)

        # Checking "right" node
        if node.position[0] + 1 <= len(self.grid) // 2:
            if (not self.is_in_closed(
                    (node.position[0] + 1, node.position[1])) and self.does_not_create_2x2(node.position[0] + 1,
                                                                                           node.position[1])) \
                    or (node.position[0] + 1, node.position[1]) == self.goal.position:
                self.calculate_values(node.position[0] + 1, node.position[1], node, False)

    def does_not_create_2x2(self, current_x, current_y):

        new_x = current_x
        new_y = current_y

        height = len(self.grid[0])
        width = len(self.grid) // 2

        if new_x < 1 or new_x >= width - 1 or new_y < 1 or new_y >= height - 1:
            return False

        # check that the new position wont result in a 2x2 area of walkable tiles
        # [topleft, top, topright, left, middle, right, bottomleft, bottom, bottomright]
        walkable_tiles = [False] * 9
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= new_y + j < height and 0 <= new_x + i < width and self.grid[new_y + j][
                    new_x + i] != 1:
                    walkable_tiles[(j + 1) * 3 + i + 1] = True
                # else:
                #     utilities.add_highlighted_tile((new_x + i, new_y + j), (0, 0, 255))

        walkable_tiles[4] = True
        if walkable_tiles[0] and walkable_tiles[1] and walkable_tiles[3] and walkable_tiles[4] \
                or walkable_tiles[1] and walkable_tiles[2] and walkable_tiles[4] and walkable_tiles[5] \
                or walkable_tiles[3] and walkable_tiles[4] and walkable_tiles[6] and walkable_tiles[7] \
                or walkable_tiles[4] and walkable_tiles[5] and walkable_tiles[7] and walkable_tiles[8]:
            return False

        return True

    def update_surrounding_nodes(self, node, use_wrap_around=True):
        # Checking "up" node
        if node.position[1] - 1 >= 0:
            if not self.grid[node.position[1] - 1][node.position[0]] == 1 and not self.is_in_closed(
                    (node.position[0], node.position[1] - 1)):
                self.calculate_values(node.position[0], node.position[1] - 1, node, use_wrap_around)
        # checking "up" node if it is out of bounds (i.e., wrap around)
        elif use_wrap_around:
            if not self.grid[31][node.position[0]] == 1 and not self.is_in_closed((node.position[0], 31)):
                self.calculate_values(node.position[0], 31, node, use_wrap_around)
        # Checking "down" node
        if node.position[1] + 1 <= 31:
            if not self.grid[node.position[1] + 1][node.position[0]] == 1 and not self.is_in_closed(
                    (node.position[0], node.position[1] + 1)):
                self.calculate_values(node.position[0], node.position[1] + 1, node, use_wrap_around)
        # checking "down" node if it is out of bounds (i.e., wrap around)
        elif use_wrap_around:
            if not self.grid[0][node.position[0]] == 1 and not self.is_in_closed((node.position[0], 0)):
                self.calculate_values(node.position[0], 0, node, use_wrap_around)
        # Checking "left" node
        if node.position[0] - 1 >= 0:
            if not self.grid[node.position[1]][node.position[0] - 1] == 1 and not self.is_in_closed(
                    (node.position[0] - 1, node.position[1])):
                self.calculate_values(node.position[0] - 1, node.position[1], node, use_wrap_around)
        # checking "left" node if it is out of bounds (i.e., wrap around)
        elif use_wrap_around:
            if not self.grid[node.position[1]][31] == 1 and not self.is_in_closed((31, node.position[1])):
                self.calculate_values(31, node.position[1], node, use_wrap_around)
        # Checking "right" node
        if node.position[0] + 1 <= 31:
            if not self.grid[node.position[1]][node.position[0] + 1] == 1 and not self.is_in_closed(
                    (node.position[0] + 1, node.position[1])):
                self.calculate_values(node.position[0] + 1, node.position[1], node, use_wrap_around)
        # checking "right" node if it is out of bounds (i.e., wrap around)
        elif use_wrap_around:
            if not self.grid[node.position[1]][0] == 1 and not self.is_in_closed((0, node.position[1])):
                self.calculate_values(0, node.position[1], node, use_wrap_around)

    def calculate_values(self, x, y, parent, wrap_around=True):
        g = parent.g + 1
        h = self.heuristic((x, y), self.goal.position, wrap_around)
        f = g + h
        node = Node((x, y), g, h, f, parent)

        # Check if node is already in open list and if it is, check if the new node has a lower f value
        # if it does, replace the old node with the new node
        # if it is not in the open list, add it to the open list
        for open_node in self.open:
            if open_node.position == node.position:
                if open_node.f > node.f:
                    self.open.remove(open_node)
                    self.open.append(node)
                return
        self.open.append(node)

    # calculate the distance between two points taking into account wrap around
    def heuristic(self, position, goal, wrap_around=True):
        x1, y1 = position
        x2, y2 = goal
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        if wrap_around:
            if dx > 15:
                dx = 31 - dx
            if dy > 15:
                dy = 31 - dy

        return dx + dy

    def is_in_closed(self, param):
        for node in self.closed:
            if node.position == param:
                return True
        return False


class Node(object):
    def __init__(self, position, g=0, h=0, f=0, parent=None):
        self.position = position
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent
        self.neighbors = []

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return '({}, {})'.format(self.position, self.f)
