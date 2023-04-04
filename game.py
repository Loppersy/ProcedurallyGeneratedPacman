# TODO: explain this and give credits to authors

"""
NEURO 240: Based on Git history, Tycho van der Ouderaa did not edit this at all compared to the corresponding original Berkeley pacman file since the commit Tycho made was just pasting this code into the file.
"""
import pygame

import main
import utilities

from Ghost import Ghost
from PacmanOG import Pacman
from Pellet import Pellet
from PowerPellet import PowerPellet
from Wall import Wall
from main import global_state_stop_time, LEVEL_STATE_TIMES, FPS
# game.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# game.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import *
import time
import os
import traceback
import sys


#######################
# Parts worth reading #
#######################


class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """

    def __init__(self, index=0):
        self.index = index

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        raiseNotDefined()


class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {NORTH: WEST,
            SOUTH: EAST,
            EAST: NORTH,
            WEST: SOUTH,
            STOP: STOP}

    RIGHT = dict([(y, x) for x, y in list(LEFT.items())])

    REVERSE = {NORTH: SOUTH,
               SOUTH: NORTH,
               EAST: WEST,
               WEST: EAST,
               STOP: STOP}


class Configuration:
    """
    A Configuration holds the (x,y) coordinate of a character, along with its
    traveling direction.

    The convention for positions, like a graph, is that (0,0) is the lower left corner, x increases
    horizontally and y increases vertically.  Therefore, north is the direction of increasing y, or (0,1).
    """

    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def getPosition(self):
        return (self.pos)

    def getDirection(self):
        return self.direction

    def __eq__(self, other):
        if other == None:
            return False
        return (self.pos == other.pos and self.direction == other.direction)

    def __hash__(self):
        x = hash(self.pos)
        y = hash(self.direction)
        return hash(x + 13 * y)

    def generateSuccessor(self, vector):
        """
        Generates a new configuration reached by translating the current
        configuration by the action vector.  This is a low-level call and does
        not attempt to respect the legality of the movement.

        Actions are movement vectors.
        """
        x, y = self.pos
        dx, dy = vector
        direction = Actions.vectorToDirection(vector)
        # if direction == Directions.STOP:
        #     direction = self.direction  # There is no stop direction
        return Configuration((x + dx, y + dy), direction)


class AgentState:
    """
    AgentStates hold the state of an agent (configuration, speed, scared, etc).
    """
    GHOST_SPEED = 2.3
    FRIGHTENED_SPEED = GHOST_SPEED * 0.7
    DEAD_SPEED = GHOST_SPEED * 1.5

    def __init__(self, startConfiguration, isPacman):


        self.start = startConfiguration
        self.configuration = startConfiguration
        self.isPacman = isPacman
        self.scaredTimer = 0
        self.numCarrying = 0
        self.numReturned = 0

        # =====================
        self.game_object = None
        self.current_state = "scatter"  # scatter, chase, frightened, dead
        self.global_state = None  # normal state for ghost when not frightened/dead
        self.respawning = False
        self.force_goal = None
        self.goal = None
        self.type = None
        self.current_speed = 0
        self.state_overwrite = False
        self.overwrite_time = 0
        self.overwrite_clock = 0
        self.ghost_house = None
        self.starting_position = startConfiguration.getPosition()
        self.next_node = self.starting_position
        self.previous_node = self.starting_position
        self.reverse_direction = False
        self.pivot = None
        self.clyde_fleeing = False
        self.is_permanent_overwrite = None
        self.path = None

    def get_goal(self):
        if self.force_goal is not None:
            return self.force_goal
        else:
            return self.goal

    def set_path(self, path):
        self.path = path
        if self.game_object is not None:
            self.game_object.set_path(path)

    def set_force_goal(self, goal):
        self.force_goal = goal
        if self.game_object is not None:
            self.game_object.set_force_goal(goal)

    def set_goal(self, goal):
        if self.game_object is not None:
            self.game_object.set_goal(goal)
        self.goal = goal

    def update(self, pacman_configuration, blinky_position):
        self.update_overwritten_state()

        if self.respawning and not self.force_goal:
            self.apply_speed(self.current_state)
            self.respawning = False

        # change ghosts goal depending on the state
        if self.current_state == "spawnNOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO":
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
        elif self.current_state == "scatter":

            if self.type == "blinky":
                self.set_goal((31, 0))
            elif self.type == "pinky":
                self.set_goal((0, 0))
            elif self.type == "inky":
                self.set_goal((31, 31))
            elif self.type == "clyde":
                self.set_goal((0, 31))
            else:
                print("Error: ghost type not found when trying to scatter: " + self.type)
                self.set_goal((0, 0))

        elif self.current_state == "chase":
            closest_pacman = utilities.invert_coords([pacman_configuration.getPosition()], 32, 32)[0]
            pacman_direction = pacman_configuration.getDirection()
            if pacman_direction == Directions.NORTH:
                pacman_direction = "up"
            elif pacman_direction == Directions.SOUTH:
                pacman_direction = "down"
            elif pacman_direction == Directions.EAST:
                pacman_direction = "right"
            elif pacman_direction == Directions.WEST:
                pacman_direction = "left"
            if self.type == "blinky":
                self.set_goal(closest_pacman)

            elif self.type == "pinky":
                self.set_goal(closest_pacman)
                if pacman_direction == "up":
                    self.set_goal((self.goal[0], self.goal[1] - 4))
                elif pacman_direction == "down":
                    self.set_goal((self.goal[0], self.goal[1] + 4))
                elif pacman_direction == "left":
                    self.set_goal((self.goal[0] - 4, self.goal[1]))
                elif pacman_direction == "right":
                    self.set_goal((self.goal[0] + 4, self.goal[1]))
            elif self.type == "inky":
                self.pivot = closest_pacman
                if pacman_direction == "up":
                    self.pivot = (self.pivot[0], self.pivot[1] - 2)
                elif pacman_direction == "down":
                    self.pivot = (self.pivot[0], self.pivot[1] + 2)
                elif pacman_direction == "left":
                    self.pivot = (self.pivot[0] - 2, self.pivot[1])
                elif pacman_direction == "right":
                    self.pivot = (self.pivot[0] + 2, self.pivot[1])

                # if no ghost to pivot is found, get a ghost's position from the same ghost house. If no ghost
                # house is found, use a random ghost instead
                # Set the goal by getting the vector from the pivot to the ghost and rotating it by 180 degrees
                ghost_to_pivot_position = blinky_position
                vector = (ghost_to_pivot_position[0] - self.pivot[0], ghost_to_pivot_position[1] - self.pivot[1])
                vector = (vector[0] * -1, vector[1] * -1)
                self.set_goal((self.pivot[0] + vector[0], self.pivot[1] + vector[1]))

            elif self.type == "clyde":
                if utilities.get_distance(self.configuration.getPosition()[0], self.configuration.getPosition()[1], closest_pacman[0],
                                          closest_pacman[1], False) > 8:
                    self.set_goal(closest_pacman)
                    self.clyde_fleeing = False
                else:
                    self.set_goal((0, 31))
                    self.clyde_fleeing = True

        elif self.current_state == "frightened":
            self.set_goal(None)
        elif self.current_state == "dead":
            if self.ghost_house is not None:
                self.set_goal(self.ghost_house.get_entrance())
                # entrance_int_pos = self.set_goal()
            else:
                self.set_goal(self.starting_position)
                # entrance_int_pos = self.set_goal()

            # if self.force_goal is None \
            #         and self.int_pos[0] == entrance_int_pos[0] \
            #         and self.int_pos[1] == entrance_int_pos[1]:
            #     if self.ghost_house is not None:
            #         self.set_force_goal((self.goal[0], self.goal[1] + 3))
            #     else:
            #         self.set_force_goal((self.goal[0], self.goal[1]))
            #
            # elif utilities.is_centered(float_position, self.force_goal):
            #     self.is_permanent_overwrite = False
            #     self.set_force_goal(entrance_int_pos)
            #     self.switch_state(self.global_state)
            #     self.respawning = True
            #     self.current_speed = self.speed * 0.5

        if self.force_goal is not None:
            if utilities.is_centered(self.configuration.getPosition(), self.force_goal):
                self.force_goal = None

    def set_game_object(self, game_object):
        self.game_object = game_object

    def __eq__(self, other):
        if other == None:
            return False
        return self.configuration == other.configuration and self.scaredTimer == other.scaredTimer

    def __hash__(self):
        return hash(hash(self.configuration) + 13 * hash(self.scaredTimer))

    def copy(self):
        state = AgentState(self.start, self.isPacman)
        state.configuration = self.configuration
        state.scaredTimer = self.scaredTimer
        state.numCarrying = self.numCarrying
        state.numReturned = self.numReturned
        # =====================
        state.game_object = self.game_object
        state.current_state = self.current_state  # scatter, chase, frightened, dead
        state.global_state = self.global_state  # normal state for ghost when not frightened/dead
        state.respawning = self.respawning
        state.force_goal = self.force_goal
        state.goal = self.goal
        state.type = self.type
        state.current_speed = self.current_speed
        state.state_overwrite = self.state_overwrite
        state.overwrite_time = self.overwrite_time
        state.overwrite_clock = self.overwrite_clock
        state.ghost_house = self.ghost_house
        state.starting_position = self.starting_position
        state.next_node = self.next_node
        state.previous_node = self.previous_node
        state.starting_position = self.starting_position
        state.reverse_direction = self.reverse_direction
        state.pivot = self.pivot
        state.clyde_fleeing = self.clyde_fleeing
        return state

    def getPosition(self):
        if self.configuration == None:
            return None
        return self.configuration.getPosition()

    def apply_speed(self, current_state):
        if current_state == "frightened":
            self.current_speed = self.FRIGHTENED_SPEED
        elif current_state == "dead":
            self.current_speed = self.DEAD_SPEED
        else:
            self.current_speed = self.GHOST_SPEED

    def update_overwritten_state(self):
        if not self.state_overwrite:
            self.switch_state(self.global_state)
            return self.overwrite_time - self.overwrite_clock

        self.overwrite_clock += 1
        print(self.overwrite_clock, self.overwrite_time)
        if self.overwrite_clock >= self.overwrite_time and not self.is_permanent_overwrite:

            self.state_overwrite = False
            self.switch_state(self.global_state)
            return self.overwrite_time - self.overwrite_clock

        return self.overwrite_time - self.overwrite_clock

    def overwrite_global_state(self, state, state_time):
        self.switch_state(state)
        self.state_overwrite = True
        self.overwrite_clock = 0
        if state_time == -1:
            self.is_permanent_overwrite = True
        else:
            self.is_permanent_overwrite = False
            self.overwrite_time = state_time * main.FPS

    def switch_state(self, ghost_state):
        if ghost_state is None or (ghost_state == "frightened" and self.current_state == "dead"):
            # or (
            #     self.exited_house is False and self.current_state == "spawn"):
            return False
        if ghost_state == self.current_state:  # reapply some ghost_state specific things
            self.apply_speed(ghost_state)
            # if ghost_state == "frightened":
            #     self.flash_timer = pygame.time.get_ticks()
            #     self.flash_last_update = pygame.time.get_ticks()
            return False
        self.current_state = ghost_state
        # switch the ghost to a ghost_state
        if ghost_state == "dead":
            utilities.set_stop_time(0.5)
            self.game_object.overwrite_global_state("dead", -1) if self.game_object is not None else None
            # self.current_image = 3
            # self.my_image = pygame.transform.scale(self.images[self.current_image],
            #                                        (self.scale * self.image_scale, self.scale * self.image_scale))
            # utilities.add_sfx_to_queue("eat_ghost.wav")
        elif ghost_state == "frightened":
            # reverse ghosts current direction
            self.turn_around()
            self.game_object.overwrite_global_state("frightened", -1) if self.game_object is not None else None

            # self.current_image = 0
            # self.my_image = pygame.transform.scale(self.frightened_images[self.current_image],
            #                                        (self.scale * self.image_scale, self.scale * self.image_scale))
            # self.flash_timer = pygame.time.get_ticks()
            # self.flash_last_update = pygame.time.get_ticks()
        elif ghost_state == "chase" or ghost_state == "scatter":
            self.turn_around()
            self.game_object.overwrite_global_state("chase", -1) if self.game_object is not None else None

        self.apply_speed(ghost_state)
        return True

    def turn_around(self):
        if self.force_goal:
            return

        # self.configuration.direction = Directions.REVERSE[self.configuration.direction]
        # temp = self.next_node
        # self.next_node = self.previous_node
        # self.previous_node = temp
        # self.configuration.position = self.previous_node
        # self.reverse_direction = True


class Grid:
    """
    A 2-dimensional array of objects backed by a list of lists.  Data is accessed
    via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.

    The __str__ method constructs an output that is oriented like a pacman board.
    """

    def __init__(self, width, height, initialValue=False, bitRepresentation=None):
        if initialValue not in [False, True]:
            raise Exception('Grids can only contain booleans')
        self.CELLS_PER_INT = 30

        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(
            height)] for x in range(width)]
        if bitRepresentation:
            self._unpackBits(bitRepresentation)

    def __getitem__(self, i):
        return self.data[i]

    def __eq__(self, other):
        if other == None:
            return False
        return self.data == other.data

    def __hash__(self):
        # return hash(str(self))
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item=True):
        return sum([x.count(item) for x in self.data])

    def asList(self, key=True):
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key:
                    list.append((x, y))
        return list


####################################
# Parts you shouldn't have to read #
####################################


class Actions:
    """
    A collection of static methods for manipulating move actions.
    """
    # Directions
    _directions = {Directions.NORTH: (0, 1),
                   Directions.SOUTH: (0, -1),
                   Directions.EAST: (1, 0),
                   Directions.WEST: (-1, 0),
                   Directions.STOP: (0, 0)}

    _directionsAsList = list(_directions.items())

    TOLERANCE = .001

    def reverseDirection(action):
        if action == Directions.NORTH:
            return Directions.SOUTH
        if action == Directions.SOUTH:
            return Directions.NORTH
        if action == Directions.EAST:
            return Directions.WEST
        if action == Directions.WEST:
            return Directions.EAST
        return action

    reverseDirection = staticmethod(reverseDirection)

    def vectorToDirection(vector):
        dx, dy = vector
        if dy > 0:
            return Directions.NORTH
        if dy < 0:
            return Directions.SOUTH
        if dx < 0:
            return Directions.WEST
        if dx > 0:
            return Directions.EAST
        return Directions.STOP

    vectorToDirection = staticmethod(vectorToDirection)

    def directionToVector(direction, speed=1.0):
        dx, dy = Actions._directions[direction]
        return (dx * speed, dy * speed)

    directionToVector = staticmethod(directionToVector)

    def getPossibleActions(config, walls):
        possible = []
        x, y = config.pos
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int) > Actions.TOLERANCE):
            return [config.getDirection()]

        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]:
                possible.append(dir)

        return possible

    getPossibleActions = staticmethod(getPossibleActions)


class GameStateData:
    """

    """

    def __init__(self, prevState=None):
        """
        Generates a new data packet by copying information from its predecessor.
        """
        if prevState != None:
            self.food = prevState.food.shallowCopy()
            self.capsules = prevState.capsules[:]
            self.agentStates = self.copyAgentStates(prevState.agentStates)
            self.layout = prevState.layout
            self._eaten = prevState._eaten
            self.score = prevState.score

        self._foodEaten = None
        self._foodAdded = None
        self._capsuleEaten = None
        self._agentMoved = None
        self._lose = False
        self._win = False
        self.scoreChange = 0

    def deepCopy(self):
        state = GameStateData(self)
        state.food = self.food.deepCopy()
        state.layout = self.layout.deepCopy()
        state._agentMoved = self._agentMoved
        state._foodEaten = self._foodEaten
        state._foodAdded = self._foodAdded
        state._capsuleEaten = self._capsuleEaten
        return state

    def copyAgentStates(self, agentStates):
        copiedStates = []
        for agentState in agentStates:
            copiedStates.append(agentState.copy())
        return copiedStates

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        if other == None:
            return False
        # TODO Check for type of other
        if not self.agentStates == other.agentStates:
            return False
        if not self.food == other.food:
            return False
        if not self.capsules == other.capsules:
            return False
        if not self.score == other.score:
            return False
        return True

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        for i, state in enumerate(self.agentStates):
            try:
                int(hash(state))
            except TypeError(e):
                print(e)
                # hash(state)
        return int((hash(tuple(self.agentStates)) + 13 * hash(self.food) + 113 * hash(tuple(self.capsules)) + 7 * hash(self.score)) % 1048575)

    def initialize(self, layout, numGhostAgents):
        """
        Creates an initial game state from a layout array (see layout.py).
        """
        self.food = layout.food.copy()
        # self.capsules = []
        self.capsules = layout.capsules[:]
        self.layout = layout
        self.score = 0
        self.scoreChange = 0

        self.agentStates = []
        numGhosts = 0
        for isPacman, pos in layout.agentPositions:
            if not isPacman:
                if numGhosts == numGhostAgents:
                    continue  # Max ghosts reached already
                else:
                    numGhosts += 1
            self.agentStates.append(AgentState(
                Configuration(pos, Directions.STOP), isPacman))
            if not isPacman:
                if numGhosts % 4 + 1 == 1:
                    self.agentStates[numGhosts].type = "blinky"
                elif numGhosts % 4 + 1 == 2:
                    self.agentStates[numGhosts].type = "pinky"
                elif numGhosts % 4 + 1 == 3:
                    self.agentStates[numGhosts].type = "inky"
                elif numGhosts % 4 + 1 == 4:
                    self.agentStates[numGhosts].type = "clyde"
        self._eaten = [False for a in self.agentStates]


class Game:
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, agents, display, rules, startingIndex=0, muteAgents=False, catchExceptions=False):
        self.agentCrashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.startingIndex = startingIndex
        self.gameOver = False
        self.muteAgents = muteAgents
        self.catchExceptions = catchExceptions
        self.moveHistory = []
        self.totalAgentTimes = [0 for agent in agents]
        self.totalAgentTimeWarnings = [0 for agent in agents]
        self.agentTimeout = False
        import io
        self.agentOutput = [io.StringIO() for agent in agents]

    def _agentCrash(self, agentIndex, quiet=False):
        "Helper method for handling agent crashes"
        if not quiet:
            traceback.print_exc()
        self.gameOver = True
        self.agentCrashed = True
        self.rules.agentCrash(self, agentIndex)

    OLD_STDOUT = None
    OLD_STDERR = None

    def mute(self, agentIndex):
        if not self.muteAgents:
            return
        global OLD_STDOUT, OLD_STDERR
        import io
        OLD_STDOUT = sys.stdout
        OLD_STDERR = sys.stderr
        sys.stdout = self.agentOutput[agentIndex]
        sys.stderr = self.agentOutput[agentIndex]

    def unmute(self):
        if not self.muteAgents:
            return
        global OLD_STDOUT, OLD_STDERR
        # Revert stdout/stderr to originals
        sys.stdout = OLD_STDOUT
        sys.stderr = OLD_STDERR

    WIDTH, HEIGHT = 1080, 720
    BLACK = (0, 0, 0)
    SCALE = 22
    MAZE_SIZE = (32, 32)
    FPS = 60

    def create_my_objects(self, state):

        # create the walls
        wall_coords = utilities.bool_to_coords_inverted(state.layout.walls)
        for wall in wall_coords:
            self.walls.add(Wall(wall[0] * self.SCALE + (self.WIDTH - 32 * self.SCALE) / 2,
                                wall[1] * self.SCALE + (self.HEIGHT - 32 * self.SCALE) / 2,
                                self.SCALE, self.WIDTH, self.HEIGHT,
                                utilities.load_sheet(self.display.WALLS_SHEET_IMAGE, 12, 4, 16, 16),
                                utilities.load_sheet(self.display.WALLS_WHITE_SHEET_IMAGE, 12, 4, 16, 16)))

        # create the pellets
        pellet_coords = utilities.bool_to_coords_inverted(state.layout.food)
        for pellet in pellet_coords:
            self.pellets.add(Pellet(pellet[0] * self.SCALE + (self.WIDTH - 32 * self.SCALE) / 2,
                                    pellet[1] * self.SCALE + (self.HEIGHT - 32 * self.SCALE) / 2,
                                    self.SCALE, self.SCALE, self.display.PELLETS_SHEET_IMAGE))

        # create the power pellets
        power_pellet_coords = utilities.invert_coords(state.layout.capsules, state.layout.width, state.layout.height)
        for power_pellet in power_pellet_coords:
            self.power_pellets.add(PowerPellet(power_pellet[0] * self.SCALE + (self.WIDTH - 32 * self.SCALE) / 2,
                                               power_pellet[1] * self.SCALE + (self.HEIGHT - 32 * self.SCALE) / 2,
                                               self.SCALE, self.SCALE, self.display.PELLETS_SHEET_IMAGE))

        # create the ghost houses
        # TODO: implement ghost houses

        # create pacman
        pacman_x = state.agentStates[0].configuration.getPosition()[0]
        pacman_y = state.agentStates[0].configuration.getPosition()[1]
        pacman_y = state.layout.height - pacman_y - 1
        pacman = Pacman(pacman_x * self.SCALE + (self.WIDTH - 32 * self.SCALE) / 2,
                        pacman_y * self.SCALE + (self.HEIGHT - 32 * self.SCALE) / 2,
                        self.WIDTH, self.HEIGHT, self.display.PACMAN_SHEET_IMAGE, self.SCALE, 2.5)
        self.pacmans.add(pacman)
        state.agentStates[0].set_game_object(pacman)
        # create the bonus fruits
        # TODO: implement bonus fruits

        # create the ghosts
        ghostStates = []
        for i in range(1, len(state.agentStates)):
            ghostStates.append(state.agentStates[i])

        ghost_types = [("blinky", self.display.BLINKY_SHEET_IMAGE),
                       ("pinky", self.display.PINKY_SHEET_IMAGE),
                       ("inky", self.display.INKY_SHEET_IMAGE),
                       ("clyde", self.display.CLYDE_SHEET_IMAGE)]
        for ghostState in ghostStates:
            logic_pos = ghostState.configuration.getPosition()
            logic_pos = (logic_pos[0], state.layout.height - logic_pos[1] - 1)
            spawn_point = utilities.get_position_in_window(logic_pos[0], logic_pos[1], self.SCALE, self.WIDTH, self.HEIGHT)
            ghost = Ghost(spawn_point[0], spawn_point[1],
                          utilities.load_ghost_sheet(ghost_types[0][1], 1, 4, 16, 16, self.display.EYES_SHEET_IMAGE),
                          utilities.load_sheet(self.display.FRIGHTENED_GHOST_SHEET_IMAGE, 1, 4, 16, 16), ghost_types.pop(0)[0],
                          self.WIDTH, self.HEIGHT, self.SCALE, self.FPS, 2.3, None, 0)
            self.ghosts.add(ghost)
            ghostState.set_game_object(ghost)

    def run(self):
        """
        Main control loop for game play.
        """
        self.display.initialize(self.state.data)

        # ==================== MY CODE ====================

        self.walls = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.power_pellets = pygame.sprite.Group()
        self.ghost_houses = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.pacmans = pygame.sprite.Group()
        self.bonus_fruits = pygame.sprite.Group()
        self.score_popups = pygame.sprite.Group()

        self.sprite_groups = [self.walls, self.pellets, self.power_pellets, self.ghost_houses, self.ghosts, self.pacmans, self.bonus_fruits,
                              self.score_popups]
        if not self.display.checkNullDisplay():
            self.create_my_objects(self.state.data)

            self.walls.update(utilities.bool_to_maze_data_inverted(self.state.data.layout.walls))
        # ==================== END MY CODE =================

        # self.display.initialize(self.state.makeObservation(1).data)
        # inform learning agents of the game start
        for i in range(len(self.agents)):
            agent = self.agents[i]
            if not agent:
                self.mute(i)
                # this is a null agent, meaning it failed to load
                # the other team wins
                print("Agent %d failed to load" % i)
                self.unmute()
                self._agentCrash(i, quiet=True)
                return
            if ("registerInitialState" in dir(agent)):
                self.mute(i)
                if self.catchExceptions:
                    try:
                        timed_func = TimeoutFunction(
                            agent.registerInitialState, int(self.rules.getMaxStartupTime(i)))
                        try:
                            start_time = time.time()
                            timed_func(self.state.deepCopy())
                            time_taken = time.time() - start_time
                            self.totalAgentTimes[i] += time_taken
                        except TimeoutFunctionException:
                            print("Agent %d ran out of time on startup!" %
                                  i, file=sys.stderr)
                            self.unmute()
                            self.agentTimeout = True
                            self._agentCrash(i, quiet=True)
                            return
                    except Exception(data):
                        self._agentCrash(i, quiet=False)
                        self.unmute()
                        return
                else:
                    agent.registerInitialState(self.state.deepCopy())
                # TODO: could this exceed the total time
                self.unmute()

        numAgents = len(self.agents)
        clock = pygame.time.Clock()
        current_tim = 0
        current_level = 0
        stop_time_clock = 0  # To keep track of the time when the time is stopped
        while not self.gameOver:
            # ==================== MY CODE ====================
            clock.tick(self.FPS) if not self.display.checkNullDisplay() else None  # limit the game to 60 FPS if display is active

            if len(global_state_stop_time) > 0:
                global_state_stop_time[0] = (global_state_stop_time[0][0] + 1, global_state_stop_time[0][1])
                if global_state_stop_time[0][0] >= global_state_stop_time[0][1] * FPS:
                    global_state_stop_time.pop(0)
            else:
                current_tim += 1
            if current_level == 0:
                self.update_states(LEVEL_STATE_TIMES[current_level], current_tim / FPS, self.state.data.agentStates[1:])
            elif 0 < current_level < 4:
                self.update_states(LEVEL_STATE_TIMES[1], current_tim / FPS, self.state.data.agentStates[1:])
            else:
                self.update_states(LEVEL_STATE_TIMES[2], current_tim / FPS, self.state.data.agentStates[1:])

            for agentIndex in range(numAgents):
                if self.gameOver:
                    break
                # ==================== END MY CODE =================

                # Fetch the next agent
                agent = self.agents[agentIndex]
                move_time = 0
                skip_action = False
                if not utilities.get_stop_time() or self.display.checkNullDisplay():  # stop time for that nice effect
                    # ==================== MY CODE ====================
                    # Move agent to the direction it is facing
                    # State observations and actions happen once the agent reaches the center of the tile

                    if agentIndex > 0:  # update ghost specific things
                        self.state.data.agentStates[agentIndex].scaredTimer -= 1
                        self.state.data.agentStates[agentIndex].update(self.state.data.agentStates[0].configuration,
                                                                       self.state.data.agentStates[1].configuration.getPosition())
                    self.move_agent_forward(self.state.data.agentStates[agentIndex]) if not self.display.checkNullDisplay() else None

                    if self.display.checkNullDisplay() or (
                            self.isInCenter(self.state.data.agentStates[agentIndex].game_object) and self.isAgentAndObjectTogether(
                        self.state.data.agentStates[agentIndex], self.state.data.layout.width, self.state.data.layout.height)):
                        # Generate an observation of the state
                        if 'observationFunction' in dir(agent):
                            self.mute(agentIndex)
                            observation = agent.observationFunction(self.state.deepCopy())
                            self.unmute()
                        else:
                            observation = self.state.deepCopy()

                        # Solicit an action
                        self.mute(agentIndex)
                        action = agent.getAction(observation)
                        self.unmute()

                        # Execute the action
                        self.moveHistory.append((agentIndex, action))
                        self.state = self.state.generateSuccessor(agentIndex, action)

                        # Allow for game specific conditions (winning, losing, etc.)
                        self.rules.process(self.state, self)

                    # if game_over[0]:
                    #     draw_ghosts[0] = False
                    #     for bonus_fruit in bonus_fruits:
                    #         bonus_fruit.despawn_fruit()
                else:
                    stop_time_clock += 1
                    if stop_time_clock >= utilities.get_stop_time() * FPS:
                        utilities.set_stop_time(0)
                        stop_time_clock = 0

                # # Change the display
                self.display.update(self.state.data, self.sprite_groups)

        # inform a learning agent of the game result
        for agentIndex, agent in enumerate(self.agents):
            if "final" in dir(agent):
                try:
                    self.mute(agentIndex)
                    agent.final(self.state)
                    self.unmute()
                except Exception as e:
                    if not self.catchExceptions:
                        raise
                    self._agentCrash(agentIndex)
                    self.unmute()
                    return
        self.display.finish()

    def move_agent_forward(self, agentState, forceMovement=False):
        """Move the agent forward in the direction it is facing.
           Game_objects use top left corner as origin, while agents use bottom left corner as origin."""
        if agentState.game_object is None:
            return

        game_object = agentState.game_object
        old_pos = game_object.get_pos()
        direction = agentState.configuration.getDirection()
        if direction == Directions.STOP and not forceMovement:
            return
        elif direction == Directions.STOP and forceMovement:
            if game_object.direction == 'up':
                direction = Directions.NORTH
            elif game_object.direction == 'down':
                direction = Directions.SOUTH
            elif game_object.direction == 'left':
                direction = Directions.WEST
            elif game_object.direction == 'right':
                direction = Directions.EAST

        if direction == Directions.WEST:
            next_tile_pos = utilities.get_position_in_window(game_object.int_pos[0], game_object.int_pos[1], game_object.scale,
                                                             game_object.window_width, game_object.window_height)
            # If object were to overshoot the center of the next tile, move it to the center of the next tile
            if old_pos[0] - game_object.current_speed < next_tile_pos[0] and old_pos[0] != next_tile_pos[0]:
                game_object.move(next_tile_pos[0], old_pos[1])
            else:
                game_object.move(old_pos[0] - game_object.current_speed, old_pos[1])

        elif direction == Directions.EAST:
            next_tile_pos = utilities.get_position_in_window(game_object.int_pos[0] + 1, game_object.int_pos[1], game_object.scale,
                                                             game_object.window_width, game_object.window_height)
            # If object were to overshoot the center of the next tile, move it to the center of the next tile
            if old_pos[0] + game_object.current_speed > next_tile_pos[0]:
                game_object.move(next_tile_pos[0], old_pos[1])
            else:
                game_object.move(old_pos[0] + game_object.current_speed, old_pos[1])

        elif direction == Directions.SOUTH:
            # check down instead because diff origins
            next_tile_pos = utilities.get_position_in_window(game_object.int_pos[0], game_object.int_pos[1] + 1, game_object.scale,
                                                             game_object.window_width, game_object.window_height)
            # If object were to overshoot the center of the next tile, move it to the center of the next tile
            if old_pos[1] + game_object.current_speed > next_tile_pos[1]:
                game_object.move(old_pos[0], next_tile_pos[1])
            else:
                game_object.move(old_pos[0], old_pos[1] + game_object.current_speed)

        elif direction == Directions.NORTH:
            # check up instead because diff origins
            next_tile_pos = utilities.get_position_in_window(game_object.int_pos[0], game_object.int_pos[1], game_object.scale,
                                                             game_object.window_width, game_object.window_height)
            # If object were to overshoot the center of the next tile, move it to the center of the next tile
            if old_pos[1] - game_object.current_speed < next_tile_pos[1] and old_pos[1] != next_tile_pos[1]:
                game_object.move(old_pos[0], next_tile_pos[1])
            else:
                game_object.move(old_pos[0], old_pos[1] - game_object.current_speed)

    def isInCenter(self, game_object):
        """Returns true if the agent is in the center of a tile."""
        position_int = utilities.get_position_in_maze_int(game_object.get_pos()[0], game_object.get_pos()[1], game_object.scale,
                                                          game_object.window_width,
                                                          game_object.window_height)
        position_float = utilities.get_position_in_maze_float(game_object.get_pos()[0], game_object.get_pos()[1], game_object.scale,
                                                              game_object.window_width,
                                                              game_object.window_height)
        min_threshold = (.07, .07)
        centerness = (abs(position_int[0] - position_float[0]), abs(position_int[1] - position_float[1]))

        return centerness[0] < min_threshold[0] and centerness[1] < min_threshold[1]

    def allAgentsInCenter(self, agentStates):
        """Returns true if all agents are in the center of a tile."""
        for agentState in agentStates:
            if agentState.game_object is not None and not self.isInCenter(agentState.game_object):
                return False
        return True

    def areGhostAndPacmanTouching(self, agentStates):
        """Returns true if the ghost and pacman are touching."""
        pacman = agentStates[0].game_object
        ghosts = [agentState.game_object for agentState in agentStates[1:]]
        for ghost in ghosts:
            if utilities.get_distance(pacman.get_pos()[0], pacman.get_pos()[1], ghost.get_pos()[0], ghost.get_pos()[1]) < pacman.scale / 2:
                return True
        return False

    def isAgentAndObjectTogether(self, agentState, width, height):
        """Returns true if the agent and object are in the same tile to avoid multiple actions in the same tile."""
        game_object = agentState.game_object
        agentState_pos = utilities.invert_coords([agentState.configuration.getPosition()], width, height)[0]
        game_object_pos = game_object.get_int_pos()
        return agentState_pos[0] == game_object_pos[0] and agentState_pos[1] == game_object_pos[1]

    def update_states(self, level_times, current_time, ghost_states):
        state = "scatter"
        time = level_times[0][1]

        for i in range(len(level_times)):
            if current_time < time:
                state = level_times[i][0]
                break

            if i != len(level_times) - 1 or level_times[i][1] != -1:
                time += level_times[i + 1][1]
            else:
                state = level_times[i][0]
                break

        for ghost_state in ghost_states:
            ghost_state.global_state = state