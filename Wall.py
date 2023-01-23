import pygame

import utilities


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, window_width, window_height, wall_blue_images, wall_white_images):
        super().__init__()
        self.wall_blue_images = wall_blue_images
        self.wall_white_images = wall_white_images
        self.color = "blue"
        self.current_image = 0
        self.image = pygame.transform.scale(self.wall_blue_images[0], (scale, scale))
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
                self.current_image = 0
            elif direct_neighbors == [1, 0, 1, 0, 0, 0, 0, 0]:
                self.current_image = 1
            elif direct_neighbors == [0, 1, 0, 1, 0, 0, 0, 0]:
                self.current_image = 2
            elif direct_neighbors == [1, 1, 1, 1, 0, 0, 0, 0]:
                self.current_image = 3
            elif direct_neighbors == [1, 0, 0, 0, 0, 0, 0, 0]:
                self.current_image = 4
            elif direct_neighbors == [0, 1, 0, 0, 0, 0, 0, 0]:
                self.current_image = 5
            elif direct_neighbors == [0, 0, 1, 0, 0, 0, 0, 0]:
                self.current_image = 6
            elif direct_neighbors == [0, 0, 0, 1, 0, 0, 0, 0]:
                self.current_image = 7
            elif direct_neighbors == [1, 1, 0, 0, 0, 0, 0, 0]:
                self.current_image = 8
            elif direct_neighbors == [0, 1, 1, 0, 0, 0, 0, 0]:
                self.current_image = 9
            elif direct_neighbors == [0, 0, 1, 1, 0, 0, 0, 0]:
                self.current_image = 10
            elif direct_neighbors == [1, 0, 0, 1, 0, 0, 0, 0]:
                self.current_image = 11
            elif direct_neighbors == [1, 1, 0, 0, 1, 0, 0, 0]:
                self.current_image = 12
            elif direct_neighbors == [0, 1, 1, 0, 0, 1, 0, 0]:
                self.current_image = 13
            elif direct_neighbors == [0, 0, 1, 1, 0, 0, 1, 0]:
                self.current_image = 14
            elif direct_neighbors == [1, 0, 0, 1, 0, 0, 0, 1]:
                self.current_image = 15
            elif direct_neighbors == [1, 1, 0, 1, 0, 0, 0, 0]:
                self.current_image = 16
            elif direct_neighbors == [1, 1, 1, 0, 0, 0, 0, 0]:
                self.current_image = 17
            elif direct_neighbors == [0, 1, 1, 1, 0, 0, 0, 0]:
                self.current_image = 18
            elif direct_neighbors == [1, 0, 1, 1, 0, 0, 0, 0]:
                self.current_image = 19
            elif direct_neighbors == [1, 1, 0, 1, 1, 0, 0, 0]:
                self.current_image = 20
            elif direct_neighbors == [1, 1, 1, 0, 0, 1, 0, 0]:
                self.current_image = 21
            elif direct_neighbors == [0, 1, 1, 1, 0, 0, 1, 0]:
                self.current_image = 22
            elif direct_neighbors == [1, 0, 1, 1, 0, 0, 0, 1]:
                self.current_image = 23
            elif direct_neighbors == [1, 1, 0, 1, 0, 0, 0, 1]:
                self.current_image = 24
            elif direct_neighbors == [1, 1, 1, 0, 1, 0, 0, 0]:
                self.current_image = 25
            elif direct_neighbors == [0, 1, 1, 1, 0, 1, 0, 0]:
                self.current_image = 26
            elif direct_neighbors == [1, 0, 1, 1, 0, 0, 1, 0]:
                self.current_image = 27
            elif direct_neighbors == [1, 1, 0, 1, 1, 0, 0, 1]:
                self.current_image = 28
            elif direct_neighbors == [1, 1, 1, 0, 1, 1, 0, 0]:
                self.current_image = 29
            elif direct_neighbors == [0, 1, 1, 1, 0, 1, 1, 0]:
                self.current_image = 30
            elif direct_neighbors == [1, 0, 1, 1, 0, 0, 1, 1]:
                self.current_image = 31
            elif direct_neighbors == [1, 1, 1, 1, 0, 1, 1, 1]:
                self.current_image = 32
            elif direct_neighbors == [1, 1, 1, 1, 1, 0, 1, 1]:
                self.current_image = 33
            elif direct_neighbors == [1, 1, 1, 1, 1, 1, 0, 1]:
                self.current_image = 34
            elif direct_neighbors == [1, 1, 1, 1, 1, 1, 1, 0]:
                self.current_image = 35
            elif direct_neighbors == [1, 1, 1, 1, 0, 0, 1, 1]:
                self.current_image = 36
            elif direct_neighbors == [1, 1, 1, 1, 1, 0, 0, 1]:
                self.current_image = 37
            elif direct_neighbors == [1, 1, 1, 1, 1, 1, 0, 0]:
                self.current_image = 38
            elif direct_neighbors == [1, 1, 1, 1, 0, 1, 1, 0]:
                self.current_image = 39
            elif direct_neighbors == [1, 1, 1, 1, 0, 0, 0, 1]:
                self.current_image = 40
            elif direct_neighbors == [1, 1, 1, 1, 1, 0, 0, 0]:
                self.current_image = 41
            elif direct_neighbors == [1, 1, 1, 1, 0, 1, 0, 0]:
                self.current_image = 42
            elif direct_neighbors == [1, 1, 1, 1, 0, 0, 1, 0]:
                self.current_image = 43
            elif direct_neighbors == [1, 1, 1, 1, 0, 1, 0, 1]:
                self.current_image = 44
            elif direct_neighbors == [1, 1, 1, 1, 1, 0, 1, 0]:
                self.current_image = 45
            else:
                self.current_image = 47

            self.image = pygame.transform.scale(self.wall_blue_images[self.current_image],
                                                (self.rect.width, self.rect.height))
        else:
            print("Error: Wall in maze_data is not 0 or 1")

    def switch_color(self):
        if self.color == "blue":
            self.color = "white"
            self.image = pygame.transform.scale(self.wall_white_images[self.current_image],
                                                (self.rect.width, self.rect.height))
        elif self.color == "white":
            self.color = "blue"
            self.image = pygame.transform.scale(self.wall_blue_images[self.current_image],
                                                (self.rect.width, self.rect.height))
