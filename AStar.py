import numpy as np

"""
Loppersy: This file defines a class AStar that implements the A* algorithm for finding the shortest path between two points in a maze.
The class has methods for calculating the heuristic, updating the surrounding nodes, checking if a node is reachable, and getting a path or a tunnel.
The class uses a grid of 0s and 1s to represent the maze, where 0 is a walkable tile and 1 is a wall.
The class also supports wrap-around movement, where the edges of the grid are connected.

File taking from my original implementation of Pacman in Python, which can be found here:
https://github.com/Loppersy/ProcedurallyGeneratedPacman
"""

WALL_ID = 1
GRID_SIZE = 32

class AStar(object):
    def __init__(self):
        """
        Initializes an AStar object with empty attributes for the start, goal, grid, open, closed, path, and current nodes.
        Call get_path to get a path from the start to the goal.
        """
        self.start_node = None
        self.goal_node = None
        self.grid = None
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.current = None

    def get_path(self, start, goal, maze_data, use_wrap_around=True, blocked_positions=None):
        """
        The get_path method returns a list of tuples as a path from the given start to the given end in the given maze.
        The path is the shortest path from the start to the end, using the A* algorithm.
        The path can take any direction as long as there is not a wall in the way (id 1 in grid).
        The method also takes an optional argument use_wrap_around, which determines if the path can wrap around the edges of the grid.
        The method also takes an optional argument blocked_positions, which is a list of tuples of positions that are not walkable,
        even if they are walkable in maze_data.
        :param start: a Node object that represents the starting point of the path
        :param goal: a Node object that represents the ending point of the path
        :param maze_data: a list of lists of integers that represents the maze, where any non-1 is a walkable tile and 1 is a wall
        :param use_wrap_around: a boolean value that determines if the path can wrap around the edges of the grid (default is True)
        :param blocked_positions: a list of tuples of integers that are not walkable, even if they are walkable in the maze_data (default is None)
        :return: a list of tuples of integers that represents the path from the start to the goal (including the start and goal)
        """

        self.start_node = start
        self.goal_node = goal
        self.grid = maze_data
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.current = None

        # If the goal is not walkable (i.e, inside a wall or outside the maze), find the closest walkable tile to the goal
        if maze_data[self.goal_node.position[1]][self.goal_node.position[0]] == WALL_ID or\
                self.goal_node.position[0] < 0 or self.goal_node.position[0] >= len(maze_data[0]) or \
                self.goal_node.position[1] < 0 or self.goal_node.position[1] >= len(maze_data):
            self.goal_node.position = get_closest_walkable_tile(self.goal_node.position[0], self.goal_node.position[1], maze_data)

        # Add the start node to the open list
        # and update its values as well as the surrounding nodes
        if blocked_positions is not None:
            for blocked_position in blocked_positions:
                if blocked_position is not None:
                    blocked_node = Node((blocked_position[0], blocked_position[1]), 0, 0, 100000, None)
                    self.closed_list.append(blocked_node)
        self.calculate_values(self.start_node.position[0], self.start_node.position[1], Node(None, 0, 0, 0, None), use_wrap_around)
        self.update_surrounding_nodes(self.start_node, use_wrap_around)
        self.open_list.remove(self.start_node)
        self.closed_list.append(self.start_node)

        while len(self.open_list) > 0:
            # Get the open node with smallest f value
            self.current = self.open_list[0]
            for node in self.open_list:
                if self.current is None or node.f <= self.current.f:
                    self.current = node

            # Create a list of nodes that are not walls and are not in the closed list
            # for the nodes around the current node (up, down, left, right)
            # calculate the g, h, and f values for each node and add it to the open list
            # if the node to be checked is out of bounds, assume it is a wall
            self.update_surrounding_nodes(self.current, use_wrap_around)

            # Remove the current node from the open list and add it to the closed list
            self.open_list.remove(self.current)
            self.closed_list.append(self.current)

            # Found the goal.
            if self.current == self.goal_node:
                path = []
                current = self.current
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                return path[::-1]

        closest_node = self.closed_list[0]
        for node in self.closed_list:
            if self.heuristic(node.position, self.goal_node.position, use_wrap_around) < \
                    self.heuristic(closest_node.position, self.goal_node.position, use_wrap_around):
                closest_node = node

        # Then, make a path to that node
        path = []
        current = closest_node
        while current is not None:
            path.append(current.position)
            current = current.parent
        return path[::-1]

    def is_reachable(self, start, goal, maze_data):
        """
        Returns a boolean value that indicates if the given goal node can be reached from the given start node in the given maze.
        The method uses a simplified version of the A* algorithm that does not store the path or use wrap-around movement.
        :param start: a Node object that represents the starting point of the path
        :param goal: a Node object that represents the ending point of the path
        :param maze_data: a list of lists of integers that represents the maze, where any non-1 is a walkable tile and 1 is a wall
        :return: a boolean value that indicates if the given goal node can be reached from the given start node in the given maze
        """

        self.start_node = start
        self.goal_node = goal
        self.grid = maze_data
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.current = None

        # Add the start node to the open list
        # and update its values as well as the surrounding nodes
        self.calculate_values(self.start_node.position[0], self.start_node.position[1], Node(None, 0, 0, 0, None))
        self.update_surrounding_nodes(self.start_node)
        self.open_list.remove(self.start_node)
        self.closed_list.append(self.start_node)

        while len(self.open_list) > 0:
            # Get the open node with smallest f value
            self.current = self.open_list[0]
            for node in self.open_list:
                if self.current is None or node.f <= self.current.f:
                    self.current = node

            # Create a list of nodes that are not walls and are not in the closed list
            # for the nodes around the current node (up, down, left, right)
            # calculate the g, h, and f values for each node and add it to the open list
            # if the node to be checked is out of bounds, assume it is a wall

            self.update_surrounding_nodes(self.current)

            # Remove the current node from the open list and add it to the closed list
            self.open_list.remove(self.current)
            self.closed_list.append(self.current)

            # Found the goal.
            if self.current == self.goal_node:
                return True

        return False

    def update_surrounding_nodes(self, node, use_wrap_around=True):
        """
        This method updates the values of the nodes that are adjacent to the given node
        and adds them to the open list if they are not walls or in the closed list.
        It also takes into account wrapping around the maze if the use_wrap_around parameter is True.
        :param node: a Node object that represents the node whose surrounding nodes are to be updated
        :param use_wrap_around: a boolean value that indicates if wrap-around movement is allowed
        :return: None
        """
        # Checking "up" node
        if node.position[1] - 1 >= 0:
            if not self.grid[node.position[1] - 1][node.position[0]] == 1 and not self.is_in_closed(
                    (node.position[0], node.position[1] - 1)):
                self.calculate_values(node.position[0], node.position[1] - 1, node, use_wrap_around)
        # checking "up" node if it is out of bounds (i.e., wrap around)
        elif use_wrap_around:
            if not self.grid[GRID_SIZE-1][node.position[0]] == 1 and not self.is_in_closed((node.position[0], GRID_SIZE-1)):
                self.calculate_values(node.position[0], GRID_SIZE-1, node, use_wrap_around)
        # Checking "down" node
        if node.position[1] + 1 <= GRID_SIZE-1:
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
            if not self.grid[node.position[1]][GRID_SIZE-1] == 1 and not self.is_in_closed((GRID_SIZE-1, node.position[1])):
                self.calculate_values(GRID_SIZE-1, node.position[1], node, use_wrap_around)
        # Checking "right" node
        if node.position[0] + 1 <= GRID_SIZE-1:
            if not self.grid[node.position[1]][node.position[0] + 1] == 1 and not self.is_in_closed(
                    (node.position[0] + 1, node.position[1])):
                self.calculate_values(node.position[0] + 1, node.position[1], node, use_wrap_around)
        # checking "right" node if it is out of bounds (i.e., wrap around)
        elif use_wrap_around:
            if not self.grid[node.position[1]][0] == 1 and not self.is_in_closed((0, node.position[1])):
                self.calculate_values(0, node.position[1], node, use_wrap_around)

    def calculate_values(self, x, y, parent, wrap_around=True):
        """
        This method calculates the g, h, and f values for a node at the given x and y coordinates
        based on its parent node and the goal node. It also creates a new node object with these values
        and checks if it is already in the open list or not. If it is, it replaces the old node with the new one
        if the new one has a lower f value. If it is not, it adds the new node to the open list
        :param x: x coordinate of the node
        :param y: y coordinate of the node
        :param parent: the parent node of the node to be created
        :param wrap_around: a boolean value that indicates if wrap-around movement is allowed
        :return: None
        """
        g = parent.g + 1
        h = self.heuristic((x, y), self.goal_node.position, wrap_around)
        f = g + h
        node = Node((x, y), g, h, f, parent)

        # Check if node is already in open list and if it is, check if the new node has a lower f value
        # if it does, replace the old node with the new node
        # if it is not in the open list, add it to the open list
        for open_node in self.open_list:
            if open_node.position == node.position:
                if open_node.f > node.f:
                    self.open_list.remove(open_node)
                    self.open_list.append(node)
                return
        self.open_list.append(node)


    def heuristic(self, position, goal, wrap_around=True):
        """
        This method calculates the distance between two points (position and goal) using the Manhattan distance formula
        It also takes into account the wrap around if the wrap_around parameter is True, meaning that the distance
        is the shortest possible distance on a torus-shaped grid.
        :param position: a tuple of integers representing the x and y coordinates of the current node
        :param goal: a tuple of integers representing the x and y coordinates of the goal node
        :param wrap_around: a boolean value indicating whether to use wrap around the maze or not
        :return:
        """
        x1, y1 = position
        x2, y2 = goal
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        if wrap_around:
            if dx > 15:
                dx = GRID_SIZE-1 - dx
            if dy > 15:
                dy = GRID_SIZE-1 - dy

        return dx + dy

    def is_in_closed(self, param):
        for node in self.closed_list:
            if node.position == param:
                return True
        return False


def get_closest_walkable_tile(x, y, maze_data):
    """
    This method returns the closest walkable tile to the given position, even if outside the maze
    :param x: x coordinate of the position
    :param y: y coordinate of the position
    :param maze_data: a 2D array of integers representing the maze
    :return: a tuple of integers representing the x and y coordinates of the closest walkable tile
    """
    # get the closest walkable tile to the given position, even if outside the maze
    walkable_tiles = []
    for i in range(len(maze_data)):
        for j in range(len(maze_data[i])):
            if maze_data[i][j] != 1:
                walkable_tiles.append((j, i))

    np.array(walkable_tiles)
    # get the closest tile using numpy and the euclidean distance
    closest_tile = walkable_tiles[np.argmin(np.sqrt((np.array(walkable_tiles)[:, 0] - x) ** 2 + (
            np.array(walkable_tiles)[:, 1] - y) ** 2))]
    return closest_tile


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
