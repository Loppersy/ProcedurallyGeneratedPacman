import os

import pygame

import utilities


class UIHandler:

    def __init__(self, scale, window_width, window_height, fps, lives, high_score, sfx_handler, resources,
                 fruit_per_level):
        self.high_score = high_score
        self.score = 0
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.fps = fps
        self.lives = lives
        self.sfx_handler = sfx_handler
        self.font_size = int(scale // 2)

        print(resources)

        self.regenerate_button_image = resources["ui_images"]["regenerate_button"]
        self.regenerate_button_rect = self.regenerate_button_image.get_rect()
        self.regenerate_button_rect.x = self.window_width - self.regenerate_button_rect.width - self.scale
        self.regenerate_button_rect.y = self.window_height - self.regenerate_button_rect.height - self.scale

        self.regenerate_button_hover_image = resources["ui_images"]["regenerate_button_hover"]
        self.regenerate_button_normal_image = resources["ui_images"]["regenerate_button"]

        self.ghost_button_image_1 = resources["ui_images"]["ghost_button"]
        self.ghost_button_rect_1 = self.ghost_button_image_1.get_rect()
        self.ghost_button_rect_1.x = self.window_width - self.ghost_button_rect_1.width * 2 - self.scale
        self.ghost_button_rect_1.y = self.window_height - self.ghost_button_rect_1.height * 2 - self.regenerate_button_rect.height * 2 - self.scale * 3

        self.ghost_button_image_2 = resources["ui_images"]["ghost_button"]
        self.ghost_button_rect_2 = self.ghost_button_image_2.get_rect()
        self.ghost_button_rect_2.x = self.window_width - self.ghost_button_rect_2.width - self.scale
        self.ghost_button_rect_2.y = self.window_height - self.ghost_button_rect_2.height * 2 - self.regenerate_button_rect.height * 2 - self.scale * 3

        self.ghost_button_image_3 = resources["ui_images"]["ghost_button"]
        self.ghost_button_rect_3 = self.ghost_button_image_3.get_rect()
        self.ghost_button_rect_3.x = self.window_width - self.ghost_button_rect_3.width * 2 - self.scale
        self.ghost_button_rect_3.y = self.window_height - self.ghost_button_rect_3.height - self.regenerate_button_rect.height * 2 - self.scale * 3

        self.ghost_button_image_4 = resources["ui_images"]["ghost_button"]
        self.ghost_button_rect_4 = self.ghost_button_image_4.get_rect()
        self.ghost_button_rect_4.x = self.window_width - self.ghost_button_rect_4.width - self.scale
        self.ghost_button_rect_4.y = self.window_height - self.ghost_button_rect_4.height - self.regenerate_button_rect.height * 2 - self.scale * 3

        self.ghost_button_hover_image = resources["ui_images"]["ghost_button_hover"]
        self.ghost_button_normal_image = resources["ui_images"]["ghost_button"]

        self.blinky_button_image = resources["ui_images"]["blinky_button"]
        self.blinky_button_rect = self.blinky_button_image.get_rect()
        self.blinky_button_rect.x = self.window_width - self.blinky_button_rect.width * 2 - self.scale
        self.blinky_button_rect.y = self.window_height - self.blinky_button_rect.height * 2 - self.regenerate_button_rect.height * 2 - self.scale * 3

        self.pinky_button_image = resources["ui_images"]["pinky_button"]
        self.pinky_button_rect = self.pinky_button_image.get_rect()
        self.pinky_button_rect.x = self.window_width - self.pinky_button_rect.width - self.scale
        self.pinky_button_rect.y = self.window_height - self.pinky_button_rect.height * 2 - self.regenerate_button_rect.height * 2 - self.scale * 3

        self.inky_button_image = resources["ui_images"]["inky_button"]
        self.inky_button_rect = self.inky_button_image.get_rect()
        self.inky_button_rect.x = self.window_width - self.inky_button_rect.width * 2 - self.scale
        self.inky_button_rect.y = self.window_height - self.inky_button_rect.height - self.regenerate_button_rect.height * 2 - self.scale * 3

        self.clyde_button_image = resources["ui_images"]["clyde_button"]
        self.clyde_button_rect = self.clyde_button_image.get_rect()
        self.clyde_button_rect.x = self.window_width - self.clyde_button_rect.width - self.scale
        self.clyde_button_rect.y = self.window_height - self.clyde_button_rect.height - self.regenerate_button_rect.height * 2 - self.scale * 3

        self.path_button_image = resources["ui_images"]["path_button"]
        self.path_button_rect = self.path_button_image.get_rect()
        self.path_button_rect.x = self.window_width - self.path_button_rect.width - self.scale
        self.path_button_rect.y = self.window_height - self.path_button_rect.height * 4 - self.regenerate_button_rect.height - self.scale * 4

        self.path_button_hover_image = resources["ui_images"]["path_button_hover"]
        self.path_button_normal_image = resources["ui_images"]["path_button"]

        self.pathfinder_button_image = resources["ui_images"]["pathfinder_button"]
        self.pathfinder_button_rect = self.pathfinder_button_image.get_rect()
        self.pathfinder_button_rect.x = self.window_width - self.pathfinder_button_rect.width - self.scale
        self.pathfinder_button_rect.y = self.window_height - self.pathfinder_button_rect.height * 5 - self.regenerate_button_rect.height - self.scale * 5

        self.pathfinder_button_hover_image = resources["ui_images"]["pathfinder_button_hover"]
        self.pathfinder_button_normal_image = resources["ui_images"]["pathfinder_button"]

        self.pathfinder_state_image = resources["ui_images"]["a_star_text"]
        self.pathfinder_state_rect = self.pathfinder_state_image.get_rect()
        self.pathfinder_state_rect.x = self.window_width - self.pathfinder_state_rect.width - self.scale
        self.pathfinder_state_rect.y = self.window_height - self.pathfinder_state_rect.height * 5 - self.regenerate_button_rect.height - self.scale * 5

        self.pathfinder_state_a_star_image = resources["ui_images"]["a_star_text"]
        self.pathfinder_state_classic_image = resources["ui_images"]["classic_text"]

        self.no_dmg_button_image = resources["ui_images"]["no_dmg_button"]
        self.no_dmg_button_rect = self.no_dmg_button_image.get_rect()
        self.no_dmg_button_rect.x = self.window_width - self.no_dmg_button_rect.width - self.scale
        self.no_dmg_button_rect.y = self.window_height - self.no_dmg_button_rect.height * 6 - self.regenerate_button_rect.height - self.scale * 6

        self.no_dmg_button_hover_image = resources["ui_images"]["no_dmg_button_hover"]
        self.no_dmg_button_normal_image = resources["ui_images"]["no_dmg_button"]

        self.no_dmg_state_image = resources["ui_images"]["on_button"]
        self.no_dmg_state_rect = self.no_dmg_state_image.get_rect()
        self.no_dmg_state_rect.x = self.window_width - self.no_dmg_state_rect.width - self.scale
        self.no_dmg_state_rect.y = self.window_height - self.no_dmg_state_rect.height * 6 - self.regenerate_button_rect.height - self.scale * 6

        self.no_dmg_state_on_image = resources["ui_images"]["on_button"]
        self.no_dmg_state_off_image = resources["ui_images"]["off_button"]

        self.ghost_button_disabled_image = resources["ui_images"]["disabled_button"]
        self.ghost_button_disabled_rect = self.ghost_button_disabled_image.get_rect()

        self.ghost_1_enabled = True
        self.ghost_2_enabled = True
        self.ghost_3_enabled = True
        self.ghost_4_enabled = True

        self.sound_button_image = resources["ui_images"]["sound_button"]
        self.sound_button_rect = self.sound_button_image.get_rect()
        self.sound_button_rect.x = self.window_width - self.sound_button_rect.width - self.scale
        self.sound_button_rect.y = self.window_height - self.sound_button_rect.height * 7 - self.regenerate_button_rect.height - self.scale * 7

        self.sound_button_hover_image =  resources["ui_images"]["sound_button_hover"]
        self.sound_button_normal_image =  resources["ui_images"]["sound_button"]

        self.sound_state_image = resources["ui_images"]["sound_on"]
        self.sound_state_rect = self.sound_state_image.get_rect()
        self.sound_state_rect.x = self.window_width - self.sound_state_rect.width - self.scale
        self.sound_state_rect.y = self.window_height - self.sound_state_rect.height * 7 - self.regenerate_button_rect.height - self.scale * 7

        self.sound_state_on_image = resources["ui_images"]["sound_on"]
        self.sound_state_off_image = resources["ui_images"]["sound_off"]

        self.high_score = 0
        self.score = 0
        self.high_score_text = utilities.get_text_image("HIGH SCORE", self.font_size,
                                                        (255, 255, 255))
        self.high_score_number = utilities.get_text_image(str(high_score), self.font_size, (255, 255, 255))
        self.score_text = utilities.get_text_image("SCORE", self.font_size, (255, 255, 255))
        self.score_number = utilities.get_text_image(str(self.score), self.font_size, (255, 255, 255))

        self.high_score_text_rect = self.high_score_text.get_rect()
        self.high_score_number_rect = self.high_score_number.get_rect()
        self.score_text_rect = self.score_text.get_rect()
        self.score_number_rect = self.score_number.get_rect()

        self.high_score_text_rect.x = self.font_size
        self.high_score_text_rect.y = self.font_size
        self.high_score_number_rect.x = self.font_size
        self.high_score_number_rect.y = self.high_score_text_rect.height + self.font_size + 5

        self.score_text_rect.x = self.font_size
        self.score_text_rect.y = self.high_score_number_rect.y + self.high_score_number_rect.height + 5 + self.font_size
        self.score_number_rect.x = self.font_size
        self.score_number_rect.y = self.score_text_rect.y + self.score_text_rect.height + 5

        self.current_lives = lives
        self.pacman_image = utilities.load_sheet(resources["images"]["pacman_sheet_image"], 1, 5, 16, 16)[4]
        self.live_image = pygame.transform.scale(self.pacman_image, (self.scale * 1.5, self.scale * 1.5))
        self.live_rect = self.live_image.get_rect()
        bottom_left_corner = utilities.get_position_in_window(0, 31, self.scale, self.window_width, self.window_height)
        self.live_rect.x = bottom_left_corner[0] - self.live_rect.width
        self.live_rect.y = bottom_left_corner[1] - self.live_rect.height

        self.current_level = 0
        self.current_level_images = []
        self.possible_fruits = fruit_per_level
        self.current_levels_displayed = ["cherry"]
        self.fruit_images = utilities.load_sheet(resources["images"]["bonus_fruit_sheet_image"], 1, 9, 16, 16)
        for i in range(len(self.fruit_images)):
            self.current_level_images.append(
                pygame.transform.scale(self.fruit_images[i], (self.scale * 1.5, self.scale * 1.5)))
        self.current_level_rect = self.current_level_images[0].get_rect()
        top_left_corner = utilities.get_position_in_window(0, 0, self.scale, self.window_width, self.window_height)
        self.current_level_rect.x = top_left_corner[0] - self.current_level_rect.width
        self.current_level_rect.y = top_left_corner[1] + self.current_level_rect.height

        self.classic_button_image = resources["ui_images"]["classic_button"]
        self.classic_button_rect = self.classic_button_image.get_rect()
        self.classic_button_rect.x = self.window_width - self.classic_button_rect.width - self.scale
        self.classic_button_rect.y = self.window_height - self.classic_button_rect.height - self.regenerate_button_rect.height - self.scale * 2

        self.classic_button_hover_image = resources["ui_images"]["classic_button_hover"]
        self.classic_button_normal_image = resources["ui_images"]["classic_button"]

        self.classic_button_state_image = resources["ui_images"]["on_button"]
        self.classic_button_state_rect = self.classic_button_state_image.get_rect()
        self.classic_button_state_rect.x = self.window_width - self.classic_button_state_rect.width - self.scale
        self.classic_button_state_rect.y = self.window_height - self.classic_button_state_rect.height - self.regenerate_button_rect.height - self.scale * 2

        self.classic_button_state_on_image = resources["ui_images"]["on_button"]
        self.classic_button_state_off_image = resources["ui_images"]["off_button"]

        self.author_text = utilities.get_text_image("by", self.font_size, (255, 255, 255))
        self.author_text_2 = utilities.get_text_image("Sebastian", self.font_size, (255, 255, 255))
        self.author_text_3 = utilities.get_text_image("Lopez", self.font_size, (255, 255, 255))
        self.author_text_4 = utilities.get_text_image("Figueroa", self.font_size, (255, 255, 255))
        self.author_text_rect = self.author_text.get_rect()
        self.author_text_rect_2 = self.author_text_2.get_rect()
        self.author_text_rect_3 = self.author_text_3.get_rect()
        self.author_text_rect_4 = self.author_text_4.get_rect()
        self.author_text_rect_4.x = self.font_size
        self.author_text_rect_4.y = self.window_height - self.author_text_rect_4.height - self.font_size
        self.author_text_rect_3.x = self.font_size
        self.author_text_rect_3.y = self.author_text_rect_4.y - self.author_text_rect_3.height - self.font_size
        self.author_text_rect_2.x = self.font_size
        self.author_text_rect_2.y = self.author_text_rect_3.y - self.author_text_rect_2.height - self.font_size
        self.author_text_rect.x = self.font_size
        self.author_text_rect.y = self.author_text_rect_2.y - self.author_text_rect.height - self.font_size

    def update(self, cursor_click_pos, cursor_hover_pos, lives, high_score, score, current_level):
        if cursor_click_pos is not None:
            if self.regenerate_button_rect.collidepoint(cursor_click_pos):
                utilities.set_regenerate_new_maze(True)
                self.regenerate_button_image = self.regenerate_button_normal_image
            if self.blinky_button_rect.collidepoint(cursor_click_pos):
                utilities.update_blinky[0] = not utilities.update_blinky[0]
            if self.pinky_button_rect.collidepoint(cursor_click_pos):
                utilities.update_pinky[0] = not utilities.update_pinky[0]
            if self.inky_button_rect.collidepoint(cursor_click_pos):
                utilities.update_inky[0] = not utilities.update_inky[0]
            if self.clyde_button_rect.collidepoint(cursor_click_pos):
                utilities.update_clyde[0] = not utilities.update_clyde[0]
            if self.path_button_rect.collidepoint(cursor_click_pos):
                utilities.draw_paths[0] = not utilities.draw_paths[0]
            if self.pathfinder_button_rect.collidepoint(cursor_click_pos):
                utilities.AStarMode[0] = not utilities.AStarMode[0]
            if self.no_dmg_button_rect.collidepoint(cursor_click_pos):
                utilities.invisibility_debug[0] = not utilities.invisibility_debug[0]
            if self.sound_button_rect.collidepoint(cursor_click_pos):
                utilities.SFX_and_Music[0] = not utilities.SFX_and_Music[0]
            if self.classic_button_rect.collidepoint(cursor_click_pos):
                utilities.classic_mode[0] = not utilities.classic_mode[0]
                utilities.set_regenerate_new_maze(True)
                self.classic_button_image = self.classic_button_normal_image

        self.ghost_1_enabled = utilities.update_blinky[0]
        self.ghost_2_enabled = utilities.update_pinky[0]
        self.ghost_3_enabled = utilities.update_inky[0]
        self.ghost_4_enabled = utilities.update_clyde[0]

        if utilities.invisibility_debug[0]:
            self.no_dmg_state_image = self.no_dmg_state_on_image
        else:
            self.no_dmg_state_image = self.no_dmg_state_off_image

        if utilities.SFX_and_Music[0]:
            self.sound_state_image = self.sound_state_on_image
        else:
            self.sound_state_image = self.sound_state_off_image

        if utilities.AStarMode[0]:
            self.pathfinder_state_image = self.pathfinder_state_a_star_image
        else:
            self.pathfinder_state_image = self.pathfinder_state_classic_image

        if utilities.classic_mode[0]:
            self.classic_button_state_image = self.classic_button_state_on_image
        else:
            self.classic_button_state_image = self.classic_button_state_off_image

        if self.high_score != high_score:
            self.high_score_number = utilities.get_text_image(str(high_score), self.font_size, (255, 255, 255))
            self.high_score = high_score

        self.score_number = utilities.get_text_image(str(score), self.font_size, (255, 255, 255))

        self.current_lives = lives
        if current_level != self.current_level:
            self.current_level = current_level
            self.current_levels_displayed.clear()
            temp_current_level = current_level
            while temp_current_level >= 0 and len(self.current_levels_displayed) < 7:
                max_fruit = temp_current_level
                if max_fruit > len(self.possible_fruits) - 1:
                    max_fruit = len(self.possible_fruits) - 1
                self.current_levels_displayed.insert(0, self.possible_fruits[max_fruit][0])
                temp_current_level -= 1

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

            if self.sound_button_rect.collidepoint(cursor_hover_pos):
                self.sound_button_image = self.sound_button_hover_image
            else:
                self.sound_button_image = self.sound_button_normal_image

            if self.classic_button_rect.collidepoint(cursor_hover_pos):
                self.classic_button_image = self.classic_button_hover_image
            else:
                self.classic_button_image = self.classic_button_normal_image

    def draw(self, screen):
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
        screen.blit(self.sound_button_image, self.sound_button_rect)
        screen.blit(self.sound_state_image, self.sound_state_rect)
        screen.blit(self.classic_button_image, self.classic_button_rect)
        screen.blit(self.classic_button_state_image, self.classic_button_state_rect)

        screen.blit(self.author_text, self.author_text_rect)
        screen.blit(self.author_text_2, self.author_text_rect_2)
        screen.blit(self.author_text_3, self.author_text_rect_3)
        screen.blit(self.author_text_4, self.author_text_rect_4)

        if not self.ghost_1_enabled:
            screen.blit(self.ghost_button_disabled_image, self.blinky_button_rect)
        if not self.ghost_2_enabled:
            screen.blit(self.ghost_button_disabled_image, self.pinky_button_rect)
        if not self.ghost_3_enabled:
            screen.blit(self.ghost_button_disabled_image, self.inky_button_rect)
        if not self.ghost_4_enabled:
            screen.blit(self.ghost_button_disabled_image, self.clyde_button_rect)

        screen.blit(self.high_score_text, self.high_score_text_rect)
        screen.blit(self.high_score_number, self.high_score_number_rect)
        screen.blit(self.score_text, self.score_text_rect)
        screen.blit(self.score_number, self.score_number_rect)

        for i in range(self.current_lives - 1):
            screen.blit(self.live_image, self.live_rect.move(0, i * -(self.live_rect.height + self.scale // 2)))

        for i in range(len(self.current_levels_displayed)):
            screen.blit(self.get_fruit_image(self.current_levels_displayed[i]),
                        self.current_level_rect.move(0, i * (self.current_level_rect.height + self.scale // 3)))

    def get_fruit_image(self, fruit):
        if fruit == "cherry":
            return self.current_level_images[1]
        elif fruit == "strawberry":
            return self.current_level_images[2]
        elif fruit == "peach":
            return self.current_level_images[3]
        elif fruit == "apple":
            return self.current_level_images[4]
        elif fruit == "melon":
            return self.current_level_images[5]
        elif fruit == "galaxian":
            return self.current_level_images[6]
        elif fruit == "bell":
            return self.current_level_images[7]
        elif fruit == "key":
            return self.current_level_images[8]
        else:
            return self.current_level_images[0]
