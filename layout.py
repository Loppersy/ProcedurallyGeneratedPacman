"""
Loppersy: File taken from the UC Berkeley AI materials and used (unmodified) by Tycho van der Ouderaa.

This file contains the code to generate layouts from files.
The original implementation used text files, but this version uses
an image scanner to generate layouts from images, because it is
easier to create new layouts this way.

layouts use the bottom left corner as the origin while images and the new display use the top left corner as the origin.

the code for the image scanner is based on the code from:
https://github.com/Loppersy/ProcedurallyGeneratedPacman
"""


# layout.py
# ---------
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


import os

from PIL import Image

from game import Grid

VISIBILITY_MATRIX_CACHE = {}


class Layout:
    """
    A Layout manages the static information about the game board.
    """

    def __init__(self, layoutText):
        self.width = len(layoutText[0])
        self.height = len(layoutText)
        self.walls = Grid(self.width, self.height, False)
        self.food = Grid(self.width, self.height, False)
        self.capsules = []
        self.agentPositions = []
        self.numGhosts = 0
        self.processLayoutText(layoutText)
        self.layoutText = layoutText
        self.totalFood = len(self.food.asList())

    def getNumGhosts(self):
        return self.numGhosts

    def deepCopy(self):
        return Layout(self.layoutText[:])

    def processLayoutText(self, layoutText):
        """
        Coordinates are flipped from the input format to the (x,y) convention here

        The shape of the maze.  Each character
        represents a different type of object.
         % - Wall
         . - Food
         o - Capsule
         G - Ghost
         P - Pacman
        Other characters are ignored.
        """
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[maxY - y][x]
                self.processLayoutChar(x, y, layoutChar)
        self.agentPositions.sort()
        self.agentPositions = [(i == 0, pos, ghost_h) for i, pos, ghost_h in self.agentPositions]

    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == '%':
            self.walls[x][y] = True
        elif layoutChar == '.':
            self.food[x][y] = True
        elif layoutChar == 'o':
            self.capsules.append((x, y))
        elif layoutChar == 'P':
            self.agentPositions.append((0, (x, y), None))
        elif layoutChar in ['G']:
            self.agentPositions.append((1, (x, y), None))
            self.numGhosts += 1
        elif layoutChar in ['1', '2', '3', '4']:
            self.agentPositions.append((int(layoutChar), (x, y), None))
            self.numGhosts += 1
        elif layoutChar == 'H':
            self.walls[x][y] = True
            self.numGhosts += 4
            self.agentPositions.append((1, (x + 5, y - 2), (x + 3, y + 1)))  # Ghost, starting position, Ghost house entrance
            self.agentPositions.append((1, (x + 1, y - 2), (x + 3, y + 1)))
            self.agentPositions.append((1, (x + 3, y - 2), (x + 3, y + 1)))
            self.agentPositions.append((1, (x + 3, y + 1), (x + 3, y + 1)))






def getLayout(name, back=2):
    if name.endswith('.lay'):
        layout = tryToLoad('layouts/' + name)
        if layout == None:
            layout = tryToLoad(name)
    elif name.endswith('.png'):
        layout = tryToLoadImage('assets/' + name)
        if layout == None:
            layout = tryToLoadImage(name)
    else:
        layout = tryToLoad('layouts/' + name + '.lay')
        if layout == None:
            layout = tryToLoad(name + '.lay')
    if layout == None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = getLayout(name, back - 1)
        os.chdir(curdir)
    return layout


def tryToLoad(fullname):
    if (not os.path.exists(fullname)):
        return None
    f = open(fullname)
    try:
        return Layout([line.strip() for line in f])
    finally:
        f.close()


def tryToLoadImage(fullname):
    if (not os.path.exists(fullname)):
        return None
    MAZE1 = Image.open(fullname, 'r')

    maze_data = []

    for y in range(32):
        maze_data.append([])
        for x in range(32):
            # If the pixel is black, add a 0 to the maze_data list (representing empty space)
            if MAZE1.getpixel((x, y)) == (0, 0, 0):
                maze_data[y].append(0)
            # If the pixel is yellow, add a 2 to the maze_data list (representing a pellet)
            elif MAZE1.getpixel((x, y)) == (255, 255, 0):
                maze_data[y].append(2)
            # If the pixel is green, add a 3 to the maze_data list (representing a power pellet)
            elif MAZE1.getpixel((x, y)) == (0, 255, 0):
                maze_data[y].append(3)
            # If the pixel is red, add a 4 to the maze_data list (representing a ghost house)
            elif MAZE1.getpixel((x, y)) == (255, 0, 0):
                maze_data[y].append(4)
            # If the pixel is blue, add a 5 to the maze_data list (representing the player's starting position)
            elif MAZE1.getpixel((x, y)) == (0, 0, 255):
                maze_data[y].append(5)
            # If the pixel is orange, add a 6 to the maze_data list (representing a bonus fruit spawning position)
            elif MAZE1.getpixel((x, y)) == (255, 128, 0):
                maze_data[y].append(6)
            # If the pixel is purple, add a 7 to the maze_data list (representing an orphan ghost starting position)
            elif MAZE1.getpixel((x, y)) == (255, 0, 255):
                maze_data[y].append(7)
            # If the pixel is any other color, add a 1 to the maze_data list (representing a wall)
            else:
                maze_data[y].append(1)

    # conver maze_data to layoutText by concatenating the maze_data list into a string per row
    characters = []
    for y in range(32):
        characters.append([])
        for x in range(32):
            if maze_data[y][x] == 0:
                characters[y].append(' ')
            elif maze_data[y][x] == 1:
                characters[y].append('%')
            elif maze_data[y][x] == 2:
                characters[y].append('.')
            elif maze_data[y][x] == 3:
                characters[y].append('o')
            elif maze_data[y][x] == 4:
                characters[y].append('H')
            elif maze_data[y][x] == 5:
                characters[y].append('P')
            elif maze_data[y][x] == 7:
                characters[y].append('G')
            else:
                characters[y].append(' ')



    layoutText = []
    for y in range(32):
        layoutText.append(''.join(characters[y]))

    return Layout(layoutText)
