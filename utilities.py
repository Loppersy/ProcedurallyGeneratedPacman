import os

import pygame

queued_popups = []  # list of popups to be displayed, each element is a tuple (x,y,text, color RGB, time in seconds)
ghost_eaten_score = [200]
highlighted_tiles = []  # list of tiles to be highlighted, each element is a tuple (x,y, color RGB, time in seconds)


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
