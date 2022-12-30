import pygame


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 150

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_cooldown:
            self.last_update = now
            self.current_image = (self.current_image + 1) % 2
            self.image = self.images[self.current_image]

        # add image[4] on top of image
        self.image.blit(self.images[4], (0, 0))
