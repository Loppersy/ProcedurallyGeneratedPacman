"""
Loppersy: File taken from the UC Berkeley AI materials and used (unmodified) by Tycho van der Ouderaa.

This file was heavily modified by Loppersy to completely change the way the game is displayed.
It no loger uses tkinter and instead uses pygame. It also uses a new UI and SFX modules to
handle a new UI and extra sound effects.

layouts use the bottom left corner as the origin while the new display use the top left corner as the origin.
"""


import os

import pygame

import game
import utilities
from SFXHandler import SFXHandler
from UIHandler import UIHandler
from game import FPS

# graphicsDisplay.py
# ------------------
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


class PacmanGraphics:
    WIDTH, HEIGHT = 1080, 720
    BLACK = (0, 0, 0)
    SCALE = 22
    MAZE_SIZE = (32, 32)
    FPS = 60

    screen = pygame.display.set_mode((1080, 720))
    pygame.display.set_caption("Procedurally Generated Pacman")

    def checkNullDisplay(self):
        return False

    def __init__(self):
        self.INKY_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "inky.png")).convert_alpha()
        self.PINKY_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "pinky.png")).convert_alpha()
        self.BLINKY_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "blinky.png")).convert_alpha()
        self.CLYDE_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "clyde.png")).convert_alpha()
        self.PACMAN_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "pacman.png")).convert_alpha()
        self.EYES_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "eyes.png")).convert_alpha()
        self.PELLETS_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "pallets.png")).convert_alpha()
        self.FRIGHTENED_GHOST_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "frightened_ghost.png")).convert_alpha()
        self.BONUS_FRUIT_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "bonus_fruit.png")).convert_alpha()
        self.WALLS_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "walls.png")).convert_alpha()
        self.WALLS_WHITE_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "walls_white.png")).convert_alpha()
        self.sprite_groups = []

        self.REGENERATE_BUTTON = pygame.image.load(os.path.join("assets", "UI", "regen_button.png")).convert_alpha()
        self.REGENERATE_BUTTON_HOVER = pygame.image.load(os.path.join("assets", "UI", "regen_button_hover.png")).convert_alpha()
        self.GHOST_BUTTON = pygame.image.load(os.path.join("assets", "UI", "ghost_button.png")).convert_alpha()
        self.GHOST_BUTTON_HOVER = pygame.image.load(os.path.join("assets", "UI", "ghost_button_hover.png")).convert_alpha()
        self.BLINKY_BUTTON = pygame.image.load(os.path.join("assets", "UI", "blinky_button.png")).convert_alpha()
        self.PINKY_BUTTON = pygame.image.load(os.path.join("assets", "UI", "pinky_button.png")).convert_alpha()
        self.INKY_BUTTON = pygame.image.load(os.path.join("assets", "UI", "inky_button.png")).convert_alpha()
        self.CLYDE_BUTTON = pygame.image.load(os.path.join("assets", "UI", "clyde_button.png")).convert_alpha()
        self.PATH_BUTTON = pygame.image.load(os.path.join("assets", "UI", "path_button.png")).convert_alpha()
        self.PATH_BUTTON_HOVER = pygame.image.load(os.path.join("assets", "UI", "path_button_hover.png")).convert_alpha()
        self.PATHFINDER_BUTTON = pygame.image.load(os.path.join("assets", "UI", "pathfinder_button.png")).convert_alpha()
        self.PATHFINDER_BUTTON_HOVER = pygame.image.load(os.path.join("assets", "UI", "pathfinder_button_hover.png")).convert_alpha()
        self.A_STAR_TEXT = pygame.image.load(os.path.join("assets", "UI", "a_star.png")).convert_alpha()
        self.CLASSIC_TEXT = pygame.image.load(os.path.join("assets", "UI", "classic.png")).convert_alpha()
        self.NO_DMG_BUTTON = pygame.image.load(os.path.join("assets", "UI", "no_dmg.png")).convert_alpha()
        self.NO_DMG_BUTTON_HOVER = pygame.image.load(os.path.join("assets", "UI", "no_dmg_hover.png")).convert_alpha()
        self.ON = pygame.image.load(os.path.join("assets", "UI", "on.png")).convert_alpha()
        self.OFF = pygame.image.load(os.path.join("assets", "UI", "off.png")).convert_alpha()
        self.DISABLED_BUTTON = pygame.image.load(os.path.join("assets", "UI", "disabled_button.png")).convert_alpha()
        self.SOUND_BUTTON = pygame.image.load(os.path.join("assets", "UI", "sound_button.png")).convert_alpha()
        self.SOUND_BUTTON_HOVER = pygame.image.load(os.path.join("assets", "UI", "sound_button_hover.png")).convert_alpha()
        self.SOUND_ON = pygame.image.load(os.path.join("assets", "UI", "sound_on.png")).convert_alpha()
        self.SOUND_OFF = pygame.image.load(os.path.join("assets", "UI", "sound_off.png")).convert_alpha()
        self.CLASSIC_BUTTON = pygame.image.load(os.path.join("assets", "UI", "classic_button.png")).convert_alpha()
        self.CLASSIC_BUTTON_HOVER = pygame.image.load(os.path.join("assets", "UI", "classic_button_hover.png")).convert_alpha()

        self.UI_IMAGES = [self.REGENERATE_BUTTON, self.REGENERATE_BUTTON_HOVER,
                          self.GHOST_BUTTON, self.GHOST_BUTTON_HOVER, self.BLINKY_BUTTON, self.PINKY_BUTTON, self.INKY_BUTTON, self.CLYDE_BUTTON,
                          self.PATH_BUTTON, self.PATH_BUTTON_HOVER,
                          self.PATHFINDER_BUTTON, self.PATHFINDER_BUTTON_HOVER, self.A_STAR_TEXT, self.CLASSIC_TEXT,
                          self.NO_DMG_BUTTON, self.NO_DMG_BUTTON_HOVER, self.ON, self.OFF,
                          self.DISABLED_BUTTON,
                          self.SOUND_BUTTON, self.SOUND_BUTTON_HOVER, self.SOUND_ON, self.SOUND_OFF,
                          utilities.load_sheet(self.BONUS_FRUIT_SHEET_IMAGE, 1, 9, 16, 16),
                          utilities.load_sheet(self.PACMAN_SHEET_IMAGE, 1, 5, 16, 16)[4],
                          self.CLASSIC_BUTTON, self.CLASSIC_BUTTON_HOVER]

        self.BONUS_FRUIT = [["cherry", "cherry"],  # level 1
                       ["strawberry", "strawberry"],  # level 2
                       ["peach", "peach"],  # level 3
                       ["peach", "peach"],  # level 4
                       ["apple", "apple"],  # level 5
                       ["apple", "apple"],  # level 6
                       ["melon", "melon"],  # level 7
                       ["melon", "melon"],  # level 8
                       ["galaxian", "galaxian"],  # level 9
                       ["galaxian", "galaxian"],  # level 10
                       ["bell", "bell"],  # level 11
                       ["bell", "bell"],  # level 12
                       ["key", "key"]]  # level 13

        SFX_NAMES = ["credit.wav", "death_1.wav", "death_2.wav", "eat_fruit.wav", "eat_ghost.wav", "extend.wav",
                     "game_start.wav",
                     "intermission.wav", "munch_1.wav", "munch_2.wav"]

        MUSIC_NAMES = ["power_pellet.wav", "retreating.wav", "siren_1.wav",
                       "siren_2.wav", "siren_3.wav", "siren_4.wav", "siren_5.wav"]

        self.sfx_handler = SFXHandler(SFX_NAMES, MUSIC_NAMES, FPS)

        self.lives = 5
        self.current_level = 6

    def initialize(self, state):
        self.startGraphics(state)

        # Information
        self.previousState = state

    def draw_my_objects(self, sprite_groups, maze_data):
        if len(sprite_groups) == 0:
            return

        self.screen.fill((0, 0, 0))

        for sprite in sprite_groups:
            sprite.draw(self.screen)

        if utilities.draw_ghosts[0]:
            for ghost in sprite_groups[4]:
                if not ghost.is_enabled():
                    continue
                if utilities.AStarMode[0] and utilities.draw_paths[0]:
                    ghost.draw_astar_path(self.screen, maze_data)
                elif utilities.draw_paths[0]:
                    ghost.draw_classic_path(self.screen, maze_data)
                ghost.my_draw(self.screen)

        for pacman in sprite_groups[5]:
            pacman.my_draw(self.screen)


        if utilities.draw_highlighted_tiles[0]:
            size = 5
            last_color = None
            for int_pos in utilities.highlighted_tiles:
                window_pos = utilities.get_position_in_window(int_pos[0][0], int_pos[0][1], game.SCALE, game.WIDTH, game.HEIGHT)
                pygame.draw.rect(self.screen, int_pos[1],
                                 (window_pos[0] + game.SCALE / 2 - size / 2, window_pos[1] + game.SCALE / 2 - size / 2, size, size),
                                 2)
                if last_color is not None and last_color != int_pos[1] or size > game.SCALE:
                    size = 5
                last_color = int_pos[1]
                size += 1


    def startGraphics(self, state):

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.sfx_handler.initialize()

        self.ui_handler = UIHandler(self.SCALE, self.WIDTH, self.HEIGHT, self.FPS, self.lives, 0, self.sfx_handler, self.UI_IMAGES, self.BONUS_FRUIT)


        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height

        self.currentState = layout
        self.maze_data = utilities.layout_to_maze_data(layout)
        self.og_pellet_count = len(utilities.get_occurrences_in_maze(self.maze_data, 2))

    def update(self, newState, sprite_groups=None, agentIndex=None):

        self.sprite_groups = sprite_groups

        agentIndex = newState._agentMoved if newState._agentMoved is not None else agentIndex
        agentState = newState.agentStates[agentIndex]

        if len(self.sprite_groups) > 0 and newState is not None and agentIndex == 0:
            for pac in self.sprite_groups[5]:
                pac.my_update([self.sprite_groups[1], self.sprite_groups[2]])

        i = 1
        for ghost_object in self.sprite_groups[4]:
            if i == agentIndex:
                ghost_object.my_update(utilities.invert_coords([self.getPosition(agentState)], newState.layout.width, newState.layout.height)[0])
                break
            i += 1

        cursor_click_pos = None
        cursor_hover_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor_click_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEMOTION:
                cursor_hover_pos = pygame.mouse.get_pos()
        self.draw_my_objects(self.sprite_groups, utilities.layout_to_maze_data(newState.layout))
        self.ui_handler.update(cursor_click_pos, cursor_hover_pos, self.lives, utilities.high_score[0],utilities.current_score[0], self.current_level)
        self.ui_handler.draw(self.screen)

        self.update_music(self.sfx_handler, self.maze_data, self.og_pellet_count, self.sprite_groups[4], (newState._win or newState._lose))

        pygame.display.update()

    def update_music(self, sfx_handler, maze_data, og_pellets_count, ghosts, game_over):
        if not utilities.SFX_and_Music[0]:
            sfx_handler.stop_music()
            return
        sfx_handler.play_sfx(utilities.get_next_sfx())
        if game_over:
            sfx_handler.stop_music()
            return

        current_state = None
        for ghost in ghosts:
            if ghost.get_state() == "dead" and ghost.is_enabled():
                current_state = "dead"

            if ghost.get_state() == "frightened" and current_state != "dead" and ghost.is_enabled():
                current_state = "frightened"

        if current_state == "dead":
            sfx_handler.play_music("retreating.wav")
            return
        elif current_state == "frightened":
            sfx_handler.play_music("power_pellet.wav")
            return

        pellets_left = len(utilities.get_occurrences_in_maze(maze_data, 2))
        if pellets_left / og_pellets_count > 0.8:
            sfx_handler.play_music("siren_1.wav")
        elif pellets_left / og_pellets_count > 0.6:
            sfx_handler.play_music("siren_2.wav")
        elif pellets_left / og_pellets_count > 0.4:
            sfx_handler.play_music("siren_3.wav")
        elif pellets_left / og_pellets_count > 0.2:
            sfx_handler.play_music("siren_4.wav")
        else:
            sfx_handler.play_music("siren_5.wav")

    def getPosition(self, agentState):
        if agentState.configuration == None:
            return (-1000, -1000)
        return agentState.getPosition()

    def finish(self):
        pygame.display.quit()
        pygame.quit()