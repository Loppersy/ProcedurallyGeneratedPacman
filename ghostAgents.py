"""
Loppersy: File taken from the UC Berkeley AI materials and used (unmodified) by Tycho van der Ouderaa.

This file was modified by Loppersy to allow ghosts to use A* search to find the shortest path to their goal.
(Yes, the original game did not use A* search, but this way crazier maps can be used)
"""



import utilities
from AStar import AStar, Node
# ghostAgents.py
# --------------
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

from game import Agent
from game import Actions
from game import Directions
import random

from util import manhattanDistance
import util


class GhostAgent(Agent):

    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()


class RandomGhost(GhostAgent):
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, state):
        dist = util.Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist


class AStarGhost(GhostAgent):
    """A ghost that uses A* search to find the shortest path to Pacman."""

    def __init__(self, index, prob_attack=0.8, prob_scaredFlee=0.8):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee
        self.path_finder = AStar()

    def getDistribution(self, state):
        direction = Directions.STOP
        maze_data = utilities.layout_to_maze_data(state.data.layout)
        start = utilities.invert_coords([state.getGhostPosition(self.index)], state.data.layout.width, state.data.layout.height)[0]
        # transform to int
        start = (int(start[0]), int(start[1]))

        # get pacman direction and convert it to relative directions (to use with my code)
        # North = up, South = down, East = right, West = left

        goal = state.getGhostState(self.index).get_goal()
        node_start = Node(start)
        node_goal = Node(goal)
        if state.getGhostState(self.index).force_goal is not None:
            # when goal is forced, maze_data is filled with 0s
            path = self.path_finder.get_path(node_start, node_goal, [[0 for _ in range(32)] for _ in range(32)])
        elif state.getGhostState(self.index).goal is not None:
            path = self.path_finder.get_path(node_start, node_goal, maze_data, blocked_positions=[state.getGhostState(self.index).previous_node])
        else:  # if no goal is set, pick a valid direction randomly
            legal = state.getLegalActions(self.index)
            choice = random.choice(legal)
            next_node = None
            if choice == Directions.NORTH:
                next_node = (start[0], start[1] - 1)
            elif choice == Directions.SOUTH:
                next_node = (start[0], start[1] + 1)
            elif choice == Directions.EAST:
                next_node = (start[0] + 1, start[1])
            elif choice == Directions.WEST:
                next_node = (start[0] - 1, start[1])

            path = [start, next_node]

        # if the ghost is at the goal, but there are other possible paths, pick one of them randomly
        if len(path) == 1 or path[0] == path[1]:
            legal = state.getLegalActions(self.index)
            if len(legal) > 0:
                choice = random.choice(legal)
                next_node = None
                if choice == Directions.NORTH:
                    next_node = (start[0], start[1] - 1)
                elif choice == Directions.SOUTH:
                    next_node = (start[0], start[1] + 1)
                elif choice == Directions.EAST:
                    next_node = (start[0] + 1, start[1])
                elif choice == Directions.WEST:
                    next_node = (start[0] - 1, start[1])
                path = [start, next_node]

        if len(path) > 1:
            state.getGhostState(self.index).set_path(path)

            next_step = path[1]
            # get the direction of the next step, taking into account that ghost can teleport to the other side of the maze if it is at the edge
            if next_step[0] == start[0] - 1 or (next_step[0] == state.data.layout.width - 1 and start[0] == 0):
                direction = Directions.WEST
            elif next_step[0] == start[0] + 1 or (next_step[0] == 0 and start[0] == state.data.layout.width - 1):
                direction = Directions.EAST
            elif next_step[1] == start[1] - 1 or (next_step[1] == state.data.layout.height - 1 and start[1] == 0):
                direction = Directions.NORTH
            elif next_step[1] == start[1] + 1 or (next_step[1] == 0 and start[1] == state.data.layout.height - 1):
                direction = Directions.SOUTH
            else:
                direction = Directions.STOP

        # Construct distribution and update "previous_node" in ghost state
        # state.getGhostState(self.index).previous_node = start
        # utilities.add_highlighted_tile(start, (255, 0, 0)) if utilities.invisibility_debug[0] else None
        dist = util.Counter()
        dist[direction] = 1.0
        return dist


class DirectionalGhost(GhostAgent):
    "A ghost that prefers to rush Pacman, or flee when scared."

    def __init__(self, index, prob_attack=0.8, prob_scaredFlee=0.8):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution(self, state):
        # Read variables from state
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        pos = state.getGhostPosition(self.index)
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared:
            speed = 0.5

        actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
        newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance(
            pos, pacmanPosition) for pos in newPositions]
        if isScared:
            bestScore = max(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip(
            legalActions, distancesToPacman) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        for a in legalActions:
            dist[a] += (1 - bestProb) / len(legalActions)
        dist.normalize()
        return dist
