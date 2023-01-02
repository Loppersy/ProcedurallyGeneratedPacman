import pygame

from AStar import AStar


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, images, type, window_width, window_height, scale):
        super().__init__()
        self.type = type
        self.images = images
        self.current_image = 0
        self.image = pygame.transform.scale(self.images[self.current_image], (scale * 1, scale * 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 150
        self.window_width = window_width
        self.window_height = window_height
        self.scale = scale

    def update(self, pacmans, maze_data):


        self.check_collision(pacmans)
        self.draw_ghost()

    def check_collision(self, pacmans):
        if pygame.sprite.spritecollide(self, pacmans, False):
            print("collision")
    def update_path(self):
        if self.type == "blinky":
            AStar.get_path((self.rect.x, self.rect.y), (), 0)

    def draw_ghost(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            self.current_image = (self.current_image + 1) % 2
            self.image = self.images[self.current_image]
        # add image[4] (eyes) on top of image
        self.image.blit(self.images[4], (0, 0))
        # TODO: scale image to be 1.5 times bigger than the tile and center it to the middle of the tile
        self.image = pygame.transform.scale(self.images[self.current_image], (self.scale * 1, self.scale * 1))
