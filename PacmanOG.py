import pygame

import utilities
from utilities import load_sheet
"""
Loppersy: This class is used for visualizing pacman on the screen, rather than for the actual logic of the game.
pacman are controlled by the pacmanDQN_Agent class, which is a subclass of the Agent class in the game.py file.

File taken from: https://github.com/Loppersy/ProcedurallyGeneratedPacman (where the class actually have
game logic in it)
"""


class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, window_width, window_height, pacman_sheet_image, scale, speed):
        super().__init__()
        self.dead_sounds_played = False
        self.consumed_power_pellet = False
        self.images = load_sheet(pacman_sheet_image, 2, 11, 16, 16)
        self.current_image = 0
        self.image = pygame.Surface((scale * 1, scale * 1), pygame.SRCALPHA)  # Do not update this surface
        self.rect = pygame.transform.scale(self.image, (scale * 0.5, scale * 0.5)).get_rect()
        self.image_scale = 1.5
        self.my_image = pygame.transform.scale(self.images[self.current_image],
                                               (scale * self.image_scale, scale * self.image_scale))

        self.last_update = pygame.time.get_ticks()

        self.current_speed = speed
        self.direction = "stay"
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.moving = False

        self.logic_pos = round(x), round(y)
        self.int_pos = utilities.get_position_in_maze_int(x, y, scale, window_width, window_height)
        self.move(x, y)

        self.animation_cooldown = 50
        self.dying_animation_cooldown = 175
        self.dying_animation_start_cooldown = 1300
        self.dying_animation_end_cooldown = 75
        self.start_animation_completed = False
        self.dead_animation_completed = False

    def move(self, x, y, teleport=False):
        old_pos = self.logic_pos
        self.logic_pos = x, y
        self.direction = utilities.get_movement_direction(old_pos, self.logic_pos) if not teleport else self.direction
        self.moving = self.direction != "stay"
        self.int_pos = utilities.get_position_in_maze_int(x, y, self.scale, self.window_width, self.window_height)
        self.rect.topleft = round(x + self.scale * 0.25), round(y + self.scale * 0.25)

    def get_pos(self):
        return self.logic_pos

    def my_update(self, consumables):

        # check if pacman is touching any consumables. If so, consume them
        for pellet in consumables[0]:
            if self.rect.colliderect(pellet.rect):
                pellet.kill()

        for power_pellet in consumables[1]:
            if self.rect.colliderect(power_pellet.rect):
                power_pellet.kill()

    def my_draw(self, screen, animated=True):
        now = pygame.time.get_ticks()
        if self.direction == "dying" and animated:
            if self.current_image == 13 and not self.dead_sounds_played:
                utilities.add_sfx_to_queue("death_1.wav")
                self.dead_sounds_played = True
            if not self.start_animation_completed:
                self.current_image = 11

            if now - self.last_update > self.dying_animation_start_cooldown:
                self.start_animation_completed = True

            if now - self.last_update > self.dying_animation_end_cooldown and self.dead_animation_completed:
                self.last_update = now
                self.current_image = 10
                self.direction = "dead"
                self.dead_sounds_played = False

            if now - self.last_update > self.dying_animation_cooldown and self.start_animation_completed:
                self.last_update = now
                if self.current_image == 20:
                    utilities.add_sfx_to_queue("death_2.wav")
                if self.current_image != 21:
                    self.current_image = (self.current_image + 1) % len(self.images)
                else:
                    self.dead_animation_completed = True
                    utilities.add_sfx_to_queue("death_2.wav")

            self.my_image = pygame.transform.scale(self.images[self.current_image],
                                                   (self.scale * self.image_scale, self.scale * self.image_scale))

        elif now - self.last_update > self.animation_cooldown and self.moving and animated:
            self.last_update = now
            if self.direction == "right":
                if self.current_image >= 2:
                    self.current_image = 0
                elif self.current_image < 1:
                    self.current_image = 1
                else:
                    self.current_image = self.current_image + 1
            elif self.direction == "left":
                if self.current_image >= 4:
                    self.current_image = 0
                elif self.current_image < 3:
                    self.current_image = 3
                else:
                    self.current_image = self.current_image + 1
            elif self.direction == "up":
                if self.current_image >= 6:
                    self.current_image = 0
                elif self.current_image < 5:
                    self.current_image = 5
                else:
                    self.current_image = self.current_image + 1
            elif self.direction == "down":
                if self.current_image >= 8:
                    self.current_image = 0
                elif self.current_image < 7:
                    self.current_image = 7
                else:
                    self.current_image = self.current_image + 1

            self.my_image = pygame.transform.scale(self.images[self.current_image],
                                                   (self.scale * self.image_scale, self.scale * self.image_scale))

        screen.blit(self.my_image, (self.rect.x - self.scale * 0.5, self.rect.y - self.scale * 0.5))

        # visualize rect boundaries
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)



    def get_int_pos(self):
        return self.int_pos

    def teleport(self, position, direction):
        new_pos = utilities.get_position_in_window(position[0], position[1], self.scale, self.window_width, self.window_height)

        # move pacman to the new position slighly behid the center of the tile
        if direction == "West":
            new_pos = (new_pos[0] + self.scale * .5, new_pos[1])
        elif direction == "East":
            new_pos = (new_pos[0] - self.scale * .5, new_pos[1])
        elif direction == "North":
            new_pos = (new_pos[0], new_pos[1] + self.scale * .5)
        elif direction == "South":
            new_pos = (new_pos[0], new_pos[1] - self.scale * .5)

        self.move(new_pos[0], new_pos[1], True)
