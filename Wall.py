import pygame

import utilities


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, window_width, window_height, wall_images):
        super().__init__()
        self.wall_images = wall_images
        self.image = pygame.transform.scale(self.wall_images[0], (scale, scale))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.int_pos = utilities.get_position_in_maze_int(self.rect.x, self.rect.y, scale, window_width, window_height)

    def update(self, maze_data):
        if maze_data[self.int_pos[1]][self.int_pos[0]] == 0:
            self.kill()
        elif maze_data[self.int_pos[1]][self.int_pos[0]] == 1:
            direct_neighbors = [0] * 8
            # Check up
            if self.int_pos[1] - 1 >= 0 and maze_data[self.int_pos[1] - 1][self.int_pos[0]] == 1:
                direct_neighbors[0] = 1
            # Check left
            if self.int_pos[0] - 1 >= 0 and maze_data[self.int_pos[1]][self.int_pos[0] - 1] == 1:
                direct_neighbors[1] = 1
            # Check down
            if self.int_pos[1] + 1 < len(maze_data) and maze_data[self.int_pos[1] + 1][self.int_pos[0]] == 1:
                direct_neighbors[2] = 1
            # Check right
            if self.int_pos[0] + 1 < len(maze_data[0]) and maze_data[self.int_pos[1]][self.int_pos[0] + 1] == 1:
                direct_neighbors[3] = 1

            # Check corners
            # Check up left if up and left are walls
            if direct_neighbors[0] == 1 and direct_neighbors[1] == 1:
                if maze_data[self.int_pos[1] - 1][self.int_pos[0] - 1] == 1:
                    direct_neighbors[4] = 1
            # Check left down if left and down are walls
            if direct_neighbors[1] == 1 and direct_neighbors[2] == 1:
                if maze_data[self.int_pos[1] + 1][self.int_pos[0] - 1] == 1:
                    direct_neighbors[5] = 1
            # Check down right if down and right are walls
            if direct_neighbors[2] == 1 and direct_neighbors[3] == 1:
                if maze_data[self.int_pos[1] + 1][self.int_pos[0] + 1] == 1:
                    direct_neighbors[6] = 1
            # Check right up if right and up are walls
            if direct_neighbors[3] == 1 and direct_neighbors[0] == 1:
                if maze_data[self.int_pos[1] - 1][self.int_pos[0] + 1] == 1:
                    direct_neighbors[7] = 1

            # Choose image based on direct neighbors
            if direct_neighbors == [0, 0, 0, 0, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[0], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 0, 1, 0, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[1], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 1, 0, 1, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[2], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[3], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 0, 0, 0, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[4], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 1, 0, 0, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[5], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 0, 1, 0, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[6], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 0, 0, 1, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[7], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 0, 0, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[8], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 1, 1, 0, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[9], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 0, 1, 1, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[10], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 0, 0, 1, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[11], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 0, 0, 1, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[12], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 1, 1, 0, 0, 1, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[13], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 0, 1, 1, 0, 0, 1, 0]:
                self.image = pygame.transform.scale(self.wall_images[14], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 0, 0, 1, 0, 0, 0, 1]:
                self.image = pygame.transform.scale(self.wall_images[15], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 0, 1, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[16], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 0, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[17], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 1, 1, 1, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[18], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 0, 1, 1, 0, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[19], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 0, 1, 1, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[20], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 0, 0, 1, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[21], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 1, 1, 1, 0, 0, 1, 0]:
                self.image = pygame.transform.scale(self.wall_images[22], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 0, 1, 1, 0, 0, 0, 1]:
                self.image = pygame.transform.scale(self.wall_images[23], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 0, 1, 0, 0, 0, 1]:
                self.image = pygame.transform.scale(self.wall_images[24], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 0, 1, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[25], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 1, 1, 1, 0, 1, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[26], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 0, 1, 1, 0, 0, 1, 0]:
                self.image = pygame.transform.scale(self.wall_images[27], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 0, 1, 1, 0, 0, 1]:
                self.image = pygame.transform.scale(self.wall_images[28], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 0, 1, 1, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[29], (self.rect.width, self.rect.height))
            elif direct_neighbors == [0, 1, 1, 1, 0, 1, 1, 0]:
                self.image = pygame.transform.scale(self.wall_images[30], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 0, 1, 1, 0, 0, 1, 1]:
                self.image = pygame.transform.scale(self.wall_images[31], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 0, 1, 1, 1]:
                self.image = pygame.transform.scale(self.wall_images[32], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 1, 0, 1, 1]:
                self.image = pygame.transform.scale(self.wall_images[33], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 1, 1, 0, 1]:
                self.image = pygame.transform.scale(self.wall_images[34], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 1, 1, 1, 0]:
                self.image = pygame.transform.scale(self.wall_images[35], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 0, 0, 1, 1]:
                self.image = pygame.transform.scale(self.wall_images[36], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 1, 0, 0, 1]:
                self.image = pygame.transform.scale(self.wall_images[37], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 1, 1, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[38], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 0, 1, 1, 0]:
                self.image = pygame.transform.scale(self.wall_images[39], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 0, 0, 0, 1]:
                self.image = pygame.transform.scale(self.wall_images[40], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 1, 0, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[41], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 0, 1, 0, 0]:
                self.image = pygame.transform.scale(self.wall_images[42], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 0, 0, 1, 0]:
                self.image = pygame.transform.scale(self.wall_images[43], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 0, 1, 0, 1]:
                self.image = pygame.transform.scale(self.wall_images[44], (self.rect.width, self.rect.height))
            elif direct_neighbors == [1, 1, 1, 1, 1, 0, 1, 0]:
                self.image = pygame.transform.scale(self.wall_images[45], (self.rect.width, self.rect.height))
            else:
                self.image = pygame.transform.scale(self.wall_images[47], (self.rect.width, self.rect.height))



        else:
            print("Error: Wall in maze_data is not 0 or 1")
