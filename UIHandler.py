import os

import pygame

import utilities


class UIHandler:

    def __init__(self, scale, window_width, window_height, fps, lives, current_level, sfx_handler, ui_images):
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.fps = fps
        self.lives = lives
        self.current_level = current_level
        self.sfx_handler = sfx_handler
        self.font_size = int(scale * 2)

        self.regenerate_button_image = ui_images[0]
        self.regenerate_button_rect = self.regenerate_button_image.get_rect()
        self.regenerate_button_rect.x = self.window_width - self.regenerate_button_rect.width - self.scale
        self.regenerate_button_rect.y = self.window_height - self.regenerate_button_rect.height - self.scale

        self.regenerate_button_hover_image = ui_images[1]
        self.regenerate_button_normal_image = ui_images[0]

        self.ghost_button_image_1 = ui_images[2]
        self.ghost_button_rect_1 = self.ghost_button_image_1.get_rect()
        self.ghost_button_rect_1.x = self.window_width - self.ghost_button_rect_1.width * 2 - self.scale
        self.ghost_button_rect_1.y = self.window_height - self.ghost_button_rect_1.height * 2 - self.regenerate_button_rect.height - self.scale * 2

        self.ghost_button_image_2 = ui_images[2]
        self.ghost_button_rect_2 = self.ghost_button_image_2.get_rect()
        self.ghost_button_rect_2.x = self.window_width - self.ghost_button_rect_2.width - self.scale
        self.ghost_button_rect_2.y = self.window_height - self.ghost_button_rect_2.height * 2 - self.regenerate_button_rect.height - self.scale * 2

        self.ghost_button_image_3 = ui_images[2]
        self.ghost_button_rect_3 = self.ghost_button_image_3.get_rect()
        self.ghost_button_rect_3.x = self.window_width - self.ghost_button_rect_3.width * 2 - self.scale
        self.ghost_button_rect_3.y = self.window_height - self.ghost_button_rect_3.height - self.regenerate_button_rect.height - self.scale * 2

        self.ghost_button_image_4 = ui_images[2]
        self.ghost_button_rect_4 = self.ghost_button_image_4.get_rect()
        self.ghost_button_rect_4.x = self.window_width - self.ghost_button_rect_4.width - self.scale
        self.ghost_button_rect_4.y = self.window_height - self.ghost_button_rect_4.height - self.regenerate_button_rect.height - self.scale * 2

        self.ghost_button_hover_image = ui_images[3]
        self.ghost_button_normal_image = ui_images[2]

        self.blinky_button_image = ui_images[4]
        self.blinky_button_rect = self.blinky_button_image.get_rect()
        self.blinky_button_rect.x = self.window_width - self.blinky_button_rect.width * 2 - self.scale
        self.blinky_button_rect.y = self.window_height - self.blinky_button_rect.height * 2 - self.regenerate_button_rect.height - self.scale * 2

        self.pinky_button_image = ui_images[5]
        self.pinky_button_rect = self.pinky_button_image.get_rect()
        self.pinky_button_rect.x = self.window_width - self.pinky_button_rect.width - self.scale
        self.pinky_button_rect.y = self.window_height - self.pinky_button_rect.height * 2 - self.regenerate_button_rect.height - self.scale * 2

        self.inky_button_image = ui_images[6]
        self.inky_button_rect = self.inky_button_image.get_rect()
        self.inky_button_rect.x = self.window_width - self.inky_button_rect.width * 2 - self.scale
        self.inky_button_rect.y = self.window_height - self.inky_button_rect.height - self.regenerate_button_rect.height - self.scale * 2

        self.clyde_button_image = ui_images[7]
        self.clyde_button_rect = self.clyde_button_image.get_rect()
        self.clyde_button_rect.x = self.window_width - self.clyde_button_rect.width - self.scale
        self.clyde_button_rect.y = self.window_height - self.clyde_button_rect.height - self.regenerate_button_rect.height - self.scale * 2

        self.path_button_image = ui_images[8]
        self.path_button_rect = self.path_button_image.get_rect()
        self.path_button_rect.x = self.window_width - self.path_button_rect.width - self.scale
        self.path_button_rect.y = self.window_height - self.path_button_rect.height * 3 - self.regenerate_button_rect.height - self.scale * 3

        self.path_button_hover_image = ui_images[9]
        self.path_button_normal_image = ui_images[8]

        self.pathfinder_button_image = ui_images[10]
        self.pathfinder_button_rect = self.pathfinder_button_image.get_rect()
        self.pathfinder_button_rect.x = self.window_width - self.pathfinder_button_rect.width - self.scale
        self.pathfinder_button_rect.y = self.window_height - self.pathfinder_button_rect.height * 4 - self.regenerate_button_rect.height - self.scale * 4

        self.pathfinder_button_hover_image = ui_images[11]
        self.pathfinder_button_normal_image = ui_images[10]

        self.pathfinder_state_image = ui_images[12]
        self.pathfinder_state_rect = self.pathfinder_state_image.get_rect()
        self.pathfinder_state_rect.x = self.window_width - self.pathfinder_state_rect.width - self.scale
        self.pathfinder_state_rect.y = self.window_height - self.pathfinder_state_rect.height * 4 - self.regenerate_button_rect.height - self.scale * 4

        self.pathfinder_state_a_star_image = ui_images[12]
        self.pathfinder_state_classic_image = ui_images[13]

        self.no_dmg_button_image = ui_images[14]
        self.no_dmg_button_rect = self.no_dmg_button_image.get_rect()
        self.no_dmg_button_rect.x = self.window_width - self.no_dmg_button_rect.width - self.scale
        self.no_dmg_button_rect.y = self.window_height - self.no_dmg_button_rect.height * 5 - self.regenerate_button_rect.height - self.scale * 5

        self.no_dmg_button_hover_image = ui_images[15]
        self.no_dmg_button_normal_image = ui_images[14]

        self.no_dmg_state_image = ui_images[17]
        self.no_dmg_state_rect = self.no_dmg_state_image.get_rect()
        self.no_dmg_state_rect.x = self.window_width - self.no_dmg_state_rect.width - self.scale
        self.no_dmg_state_rect.y = self.window_height - self.no_dmg_state_rect.height * 5 - self.regenerate_button_rect.height - self.scale * 5

        self.no_dmg_state_on_image = ui_images[16]
        self.no_dmg_state_off_image = ui_images[17]

        self.ghost_button_disabled_image = ui_images[18]
        self.ghost_button_disabled_rect = self.ghost_button_disabled_image.get_rect()

        self.ghost_1_enabled = True
        self.ghost_2_enabled = True
        self.ghost_3_enabled = True
        self.ghost_4_enabled = True

        self.lives_text = utilities.get_text_image("Lives: " + str(self.lives), self.font_size, (255, 255, 255))
        self.level_text = utilities.get_text_image("Level: " + str(self.current_level), self.font_size, (255, 255, 255))
        self.score_text = utilities.get_text_image("Score: " + str(0), self.font_size, (255, 255, 255))

        self.lives_rect = self.lives_text.get_rect()
        self.level_rect = self.level_text.get_rect()
        self.score_rect = self.score_text.get_rect()

        self.lives_rect.x = 0
        self.lives_rect.y = 0
        self.level_rect.x = self.window_width - self.level_rect.width
        self.level_rect.y = 0
        self.score_rect.x = self.window_width / 2 - self.score_rect.width / 2
        self.score_rect.y = 0

    def update(self, cursor_click_pos, cursor_hover_pos, lives, current_level, score):
        if cursor_click_pos is not None:
            if self.regenerate_button_rect.collidepoint(cursor_click_pos):
                utilities.set_regenerate_new_maze(True)
                self.regenerate_button_image = self.regenerate_button_normal_image
            if self.blinky_button_rect.collidepoint(cursor_click_pos):
                utilities.update_blinky[0] = not utilities.update_blinky[0]
                self.ghost_1_enabled = utilities.update_blinky[0]
            if self.pinky_button_rect.collidepoint(cursor_click_pos):
                utilities.update_pinky[0] = not utilities.update_pinky[0]
                self.ghost_2_enabled = utilities.update_pinky[0]
            if self.inky_button_rect.collidepoint(cursor_click_pos):
                utilities.update_inky[0] = not utilities.update_inky[0]
                self.ghost_3_enabled = utilities.update_inky[0]
            if self.clyde_button_rect.collidepoint(cursor_click_pos):
                utilities.update_clyde[0] = not utilities.update_clyde[0]
                self.ghost_4_enabled = utilities.update_clyde[0]
            if self.path_button_rect.collidepoint(cursor_click_pos):
                utilities.draw_paths[0] = not utilities.draw_paths[0]
            if self.pathfinder_button_rect.collidepoint(cursor_click_pos):
                if utilities.AStarMode[0] is None:
                    utilities.AStarMode[0] = True
                utilities.AStarMode[0] = not utilities.AStarMode[0]
                if utilities.AStarMode[0]:
                    self.pathfinder_state_image = self.pathfinder_state_a_star_image
                else:
                    self.pathfinder_state_image = self.pathfinder_state_classic_image
            if self.no_dmg_button_rect.collidepoint(cursor_click_pos):
                utilities.invisibility_debug[0] = not utilities.invisibility_debug[0]
                if utilities.invisibility_debug[0]:
                    self.no_dmg_state_image = self.no_dmg_state_on_image
                else:
                    self.no_dmg_state_image = self.no_dmg_state_off_image


        if cursor_hover_pos is not None:
            if self.regenerate_button_rect.collidepoint(cursor_hover_pos):
                self.regenerate_button_image = self.regenerate_button_hover_image
            else:
                self.regenerate_button_image = self.regenerate_button_normal_image

            if self.ghost_button_rect_1.collidepoint(cursor_hover_pos):
                self.ghost_button_image_1 = self.ghost_button_hover_image
            else:
                self.ghost_button_image_1 = self.ghost_button_normal_image

            if self.ghost_button_rect_2.collidepoint(cursor_hover_pos):
                self.ghost_button_image_2 = self.ghost_button_hover_image
            else:
                self.ghost_button_image_2 = self.ghost_button_normal_image

            if self.ghost_button_rect_3.collidepoint(cursor_hover_pos):
                self.ghost_button_image_3 = self.ghost_button_hover_image
            else:
                self.ghost_button_image_3 = self.ghost_button_normal_image

            if self.ghost_button_rect_4.collidepoint(cursor_hover_pos):
                self.ghost_button_image_4 = self.ghost_button_hover_image
            else:
                self.ghost_button_image_4 = self.ghost_button_normal_image

            if self.path_button_rect.collidepoint(cursor_hover_pos):
                self.path_button_image = self.path_button_hover_image
            else:
                self.path_button_image = self.path_button_normal_image

            if self.pathfinder_button_rect.collidepoint(cursor_hover_pos):
                self.pathfinder_button_image = self.pathfinder_button_hover_image
            else:
                self.pathfinder_button_image = self.pathfinder_button_normal_image

            if self.no_dmg_button_rect.collidepoint(cursor_hover_pos):
                self.no_dmg_button_image = self.no_dmg_button_hover_image
            else:
                self.no_dmg_button_image = self.no_dmg_button_normal_image

    def draw(self, screen):
        # screen.blit(self.lives_text, self.lives_rect)
        # screen.blit(self.level_text, self.level_rect)
        # screen.blit(self.score_text, self.score_rect)
        screen.blit(self.regenerate_button_image, self.regenerate_button_rect)
        screen.blit(self.ghost_button_image_1, self.ghost_button_rect_1)
        screen.blit(self.ghost_button_image_2, self.ghost_button_rect_2)
        screen.blit(self.ghost_button_image_3, self.ghost_button_rect_3)
        screen.blit(self.ghost_button_image_4, self.ghost_button_rect_4)
        screen.blit(self.blinky_button_image, self.blinky_button_rect)
        screen.blit(self.pinky_button_image, self.pinky_button_rect)
        screen.blit(self.inky_button_image, self.inky_button_rect)
        screen.blit(self.clyde_button_image, self.clyde_button_rect)
        screen.blit(self.path_button_image, self.path_button_rect)
        screen.blit(self.pathfinder_button_image, self.pathfinder_button_rect)
        screen.blit(self.pathfinder_state_image, self.pathfinder_state_rect)
        screen.blit(self.no_dmg_button_image, self.no_dmg_button_rect)
        screen.blit(self.no_dmg_state_image, self.no_dmg_state_rect)

        if not self.ghost_1_enabled:
            screen.blit(self.ghost_button_disabled_image, self.blinky_button_rect)
        if not self.ghost_2_enabled:
            screen.blit(self.ghost_button_disabled_image, self.pinky_button_rect)
        if not self.ghost_3_enabled:
            screen.blit(self.ghost_button_disabled_image, self.inky_button_rect)
        if not self.ghost_4_enabled:
            screen.blit(self.ghost_button_disabled_image, self.clyde_button_rect)
