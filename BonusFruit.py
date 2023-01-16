import pygame

import utilities
from Consumable import Consumable
from Ghost import Ghost


class BonusFruit(Consumable):
    def __init__(self, x, y, scale, window_width, window_height, fruit_images, fps, fruit_to_spawn, spawn_trigger,
                 starting_pellet_number, fruit_duration):
        super().__init__(x, y, scale, scale, fruit_images[0])
        self.fruit_queue = []
        self.fruit_images = fruit_images
        self.image = pygame.transform.scale(self.fruit_images[0], (scale, scale))
        self.rect = self.image.get_rect()
        self.int_pos = (int(utilities.get_position_in_maze_int(x, y, scale, window_width, window_height)[0]),
                        int(utilities.get_position_in_maze_int(x, y, scale, window_width, window_height)[1]))
        self.rect.x = x
        self.rect.y = y
        self.window_width = window_width
        self.window_height = window_height
        self.scale = scale
        self.fps = fps
        self.fruit_to_spawn = fruit_to_spawn
        self.starting_pellet_number = starting_pellet_number
        self.spawn_trigger = spawn_trigger
        self.current_fruit = 0
        self.consumable = False
        self.type = "bonus_fruit"
        self.current_fruit_type = None
        self.fruit_duration = fruit_duration
        self.fruit_clock = 0
        self.queue_cooldown = 3
        self.queue_clock = 0

    def update(self, maze_data):
        current_pellet_number = utilities.get_occurrences_in_maze(maze_data, 2) + utilities.get_occurrences_in_maze(
            maze_data, 3)



        # print(len(current_pellet_number), self.starting_pellet_number,
        #       1 - (float(len(current_pellet_number)) / float(self.starting_pellet_number)),
        #       self.spawn_trigger[self.current_fruit] if len(self.spawn_trigger) > self.current_fruit else -1, self.fruit_clock / self.fps, self.current_fruit)

        if len(self.spawn_trigger) > self.current_fruit and (1 - (float(len(current_pellet_number)) / float(self.starting_pellet_number)) > self.spawn_trigger[
            self.current_fruit] and self.current_fruit < len(
                self.fruit_to_spawn)):

            self.fruit_queue.append(self.fruit_to_spawn[self.current_fruit])
            self.current_fruit += 1

        self.queue_clock += 1
        if len(self.fruit_queue) > 0 and self.consumable is False and self.queue_clock > self.queue_cooldown * self.fps:
            self.spawn_fruit(self.fruit_queue.pop(0))

        if self.consumable:
            self.fruit_clock += 1
            if self.fruit_clock >= self.fruit_duration * self.fps:
                self.consumable = False
                self.current_fruit_type = None
                self.fruit_clock = 0
                self.image = pygame.transform.scale(self.fruit_images[0], (self.scale, self.scale))

    def spawn_fruit(self, fruit_type=None):
        self.fruit_clock = 0
        self.consumable = True
        if fruit_type == "cherry":
            self.image = pygame.transform.scale(self.fruit_images[1], (self.scale, self.scale))
            self.current_fruit_type = "cherry"
        elif fruit_type == "strawberry":
            self.image = pygame.transform.scale(self.fruit_images[2], (self.scale, self.scale))
            self.current_fruit_type = "strawberry"
        elif fruit_type == "peach":
            self.image = pygame.transform.scale(self.fruit_images[3], (self.scale, self.scale))
            self.current_fruit_type = "peach"
        elif fruit_type == "apple":
            self.image = pygame.transform.scale(self.fruit_images[4], (self.scale, self.scale))
            self.current_fruit_type = "apple"
        elif fruit_type == "melon":
            self.image = pygame.transform.scale(self.fruit_images[5], (self.scale, self.scale))
            self.current_fruit_type = "melon"
        elif fruit_type == "galaxian":
            self.image = pygame.transform.scale(self.fruit_images[6], (self.scale, self.scale))
            self.current_fruit_type = "galaxian"
        elif fruit_type == "bell":
            self.image = pygame.transform.scale(self.fruit_images[7], (self.scale, self.scale))
            self.current_fruit_type = "bell"
        elif fruit_type == "key":
            self.image = pygame.transform.scale(self.fruit_images[8], (self.scale, self.scale))
            self.current_fruit_type = "key"

    def consume(self):
        if not self.consumable:
            return
        print("Consumed fruit")
        self.queue_clock = 0
        self.consumable = False
        self.current_fruit_type = None
        self.image = pygame.transform.scale(self.fruit_images[0], (self.scale, self.scale))
