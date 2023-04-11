
import os

import pygame
import numpy as np
"""
Loppersy: This class is used for storing global variables and functions that are used in multiple classes.

File taken from: https://github.com/Loppersy/ProcedurallyGeneratedPacman and it is mostly the same as the original with a few extra
methods to handle the different origins of the display and the maze
"""

queued_popups = []  # list of popups to be displayed, each element is a tuple (x,y,text, color RGB, time in seconds)
ghost_eaten_score = [200]
current_score = [0]
high_score = [0]
highlighted_tiles = []  # list of tiles to be highlighted, each element is a tuple (x,y, color RGB, time in seconds)
sfx_queue = []  # list of sfx to be played
munch = [False]

stop_time = [0]

regenerate_maze = [True]
AStarMode = [True]
draw_paths = [False]
power_pellet_debug = [False]
invisibility_debug = [False]
new_maze = [True]  # Hit R to load a new maze
classic_mode = [False]
draw_highlighted_tiles = [True]
update_blinky = [True]
update_pinky = [True]
update_inky = [True]
update_clyde = [True]
SFX_and_Music = [True]

draw_ghosts = [True]


def bool_to_maze_data(grid, number):
    return [[number if grid[x][y] else 0 for x in range(grid.width)] for y in range(grid.height)]


def bool_to_maze_data_inverted(grid):
    return [[int(grid[x][y]) for x in range(grid.width)] for y in range(grid.height - 1, -1, -1)]


def bool_to_coords(grid):
    return [(x, y) for x in range(grid.width) for y in range(grid.height) if grid[x][y]]


def bool_to_coords_inverted(grid):
    """
    (0,0) is bottom left corner for grid but top left for coords returned
    :param grid:
    :return:
    """
    return [(x, grid.height - y - 1) for x in range(grid.width) for y in range(grid.height) if grid[x][y]]


def coords_to_maze_data_inverted(coords, grid_width, grid_height):
    coords = invert_coords(coords, grid_width, grid_height)
    return [[int((x, y) in coords) for x in range(grid_width)] for y in range(grid_height)]


def invert_coords(coords, grid_width, grid_height):
    return [(x, grid_height - y - 1) for x, y in coords]


def add_sfx_to_queue(sfx):
    if SFX_and_Music[0] is False:
        return
    if sfx == "munch":
        if munch[0]:
            sfx = "munch_1.wav"
        else:
            sfx = "munch_2.wav"
        munch[0] = not munch[0]
    sfx_queue.append(sfx)


def get_next_sfx():
    if len(sfx_queue) > 0:
        return sfx_queue.pop(0)
    else:
        return None


def load_ghost_sheet(sheet, rows, cols, width, height, EYES_SHEET_IMAGE):
    images = load_sheet(sheet, rows, cols, width, height)
    for i in range(4):
        EYES_SHEET_IMAGE.set_clip(pygame.Rect(i * width, 0, width, height))
        images.append(pygame.transform.scale(EYES_SHEET_IMAGE.subsurface(EYES_SHEET_IMAGE.get_clip()), (100, 100)))
    return images


def load_sheet(sheet, rows, cols, width, height):
    sheet.set_clip(pygame.Rect(0, 0, width, height))
    images = []
    for j in range(rows):
        for i in range(cols):
            sheet.set_clip(pygame.Rect(i * width, j * height, width, height))
            images.append(pygame.transform.scale(sheet.subsurface(sheet.get_clip()), (100, 100)))
    return images


# get position of the player inside the maze taking into account the scale of the tiles and the offset of the maze
# rounded to the nearest integer
def get_position_in_maze_int(x, y, scale, window_width, window_height):
    return int((x - (window_width - scale * 32) // 2) // scale), int(((y - (window_height - scale * 32) // 2) // scale))


def get_position_in_maze_float(x, y, scale, window_width, window_height):
    return (x - (window_width - scale * 32) / 2) / scale, ((y - (window_height - scale * 32) / 2) / scale)


# get position in the window taking into account the scale of the tiles and the offset of the maze
def get_position_in_window(x, y, scale, window_width, window_height):
    return x * scale + (window_width - scale * 32) / 2, y * scale + (window_height - scale * 32) / 2


# get distance from one point to another taking into account the wrap around of the maze
def get_distance(x, y, x1, y1, use_wrap_around=False):
    if use_wrap_around:
        return ((min(abs(float(x) - float(x1)), 32.0 - abs(float(x) - float(x1)))) ** 2 + (
            min(abs(float(y) - float(y1)), 32.0 - abs(float(y) - float(y1)))) ** 2) ** 0.5
    else:
        return ((float(x) - float(x1)) ** 2 + (float(y) - float(y1)) ** 2) ** 0.5


# def get_distance(x, y, x1, y1):
#     return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5

def is_centered(float_pos, int_pos):
    if float_pos is None or int_pos is None:
        return False
    return abs(float_pos[0] - float(int_pos[0])) <= 0.02 and abs(float_pos[1] - float(int_pos[1])) <= 0.02


def get_occurrences_in_maze(maze_data, object_to_find):
    occurrences = []
    for i in range(len(maze_data)):
        for j in range(len(maze_data[i])):
            if maze_data[i][j] == object_to_find:
                occurrences.append((i, j))
    return occurrences




def set_stop_time(var):
    stop_time[0] = var


def get_stop_time():
    if stop_time[0] > 0:
        return stop_time[0]
    else:
        return False


def get_text_image(string, size, color):
    pygame.font.init()
    font = pygame.font.Font(os.path.join("assets", "fonts", "PressStart2P.ttf"), size)
    return font.render(string, False, color)


def add_highlighted_tile(int_pos, color):
    highlighted_tiles.append((int_pos, color))


def empty_highlighted_tiles():
    highlighted_tiles.clear()





def set_regenerate_new_maze(var):
    regenerate_maze[0] = var


def get_regenerate_new_maze():
    return regenerate_maze[0]


def add_score(score):
    current_score[0] += score
    if current_score[0] > high_score[0]:
        high_score[0] = current_score[0]


def get_movement_direction(old_pos, logic_pos):
    if old_pos[0] < logic_pos[0]:
        return "right"
    elif old_pos[0] > logic_pos[0]:
        return "left"
    elif old_pos[1] < logic_pos[1]:
        return "down"
    elif old_pos[1] > logic_pos[1]:
        return "up"
    elif old_pos[1] == logic_pos[1] and old_pos[0] == logic_pos[0]:
        return "stay"
    else:
        return None


def layout_to_maze_data(layout):

    width, height = layout.width, layout.height
    pellets = layout.food.data
    walls = layout.walls
    power_pellets = layout.capsules
    maze_data = [[0 for _ in range(width)] for _ in range(height)]
    for i in range(width):
        for j in range(height):
            if walls[i][j]:
                maze_data[height - j - 1][i] = 1
            elif pellets[i][j]:
                maze_data[height - j - 1][i] = 2
            elif (i, j) in power_pellets:
                maze_data[height - j - 1][i] = 3
    return maze_data

