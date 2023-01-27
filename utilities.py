import os

import pygame
import numpy as np

queued_popups = []  # list of popups to be displayed, each element is a tuple (x,y,text, color RGB, time in seconds)
ghost_eaten_score = [200]
highlighted_tiles = []  # list of tiles to be highlighted, each element is a tuple (x,y, color RGB, time in seconds)
sfx_queue = []  # list of sfx to be played
munch = [False]

regenerate_maze = [False]
AStarMode = [True]
draw_paths = [True]
power_pellet_debug = [False]
invisibility_debug = [False]
new_maze = [True]  # Hit R to load a new maze
classic_mode = [False]
draw_highlighted_tiles = [False]

def add_sfx_to_queue(sfx):
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


stop_time = [0]


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


def get_closest_walkable_tile(x, y, maze_data):
    # get the closest walkable tile to the given position, even if outside the maze
    walkable_tiles = []
    for i in range(len(maze_data)):
        for j in range(len(maze_data[i])):
            if maze_data[i][j] != 1:
                walkable_tiles.append((j, i))
                # add_highlighted_tile((j, i), (255, 255, 255))

    np.array(walkable_tiles)
    # get the closest tile using numpy and the euclidean distance
    closest_tile = walkable_tiles[np.argmin(np.sqrt((np.array(walkable_tiles)[:, 0] - x) ** 2 + (
            np.array(walkable_tiles)[:, 1] - y) ** 2))]
    return closest_tile


def set_regenerate_new_maze(var):
    regenerate_maze[0] = var


def get_regenerate_new_maze():
    return regenerate_maze[0]
