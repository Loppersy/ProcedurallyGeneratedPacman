import os

import pygame


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
    return (x - (window_width - scale * 32) // 2) // scale, ((y - (window_height - scale * 32) // 2) // scale)


def get_position_in_maze_float(x, y, scale, window_width, window_height):
    return (x - (window_width - scale * 32) / 2) / scale, ((y - (window_height - scale * 32) / 2) / scale)


# get position in the window taking into account the scale of the tiles and the offset of the maze
def get_position_in_window(x, y, scale, window_width, window_height):
    return x * scale + (window_width - scale * 32) / 2, y * scale + (window_height - scale * 32) / 2
