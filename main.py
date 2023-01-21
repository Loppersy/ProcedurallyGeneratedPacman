import pygame
import os

import utilities
from BonusFruit import BonusFruit
from Ghost import Ghost
from GhostHouse import GhostHouse
from Pacman import Pacman
from Pellet import Pellet
from PowerPellet import PowerPellet
from Wall import Wall

WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")
BLACK = (0, 0, 0)

SCALE = 22
MAZE_SIZE = (32, 32)
FPS = 60

INKY_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "inky.png")).convert_alpha()
PINKY_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "pinky.png")).convert_alpha()
BLINKY_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "blinky.png")).convert_alpha()
CLYDE_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "clyde.png")).convert_alpha()
PACMAN_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "pacman.png")).convert_alpha()
EYES_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "eyes.png")).convert_alpha()
PELLETS_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "pallets.png")).convert_alpha()
FRIGHTENED_GHOST_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "frightened_ghost.png")).convert_alpha()
BONUS_FRUIT_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "bonus_fruit.png")).convert_alpha()
WALLS_SHEET_IMAGE = pygame.image.load(os.path.join("assets", "walls.png")).convert_alpha()

MAZE1 = pygame.image.load(os.path.join("assets", "maze1.png")).convert_alpha()

# times of the different modes for each level. In seconds
LEVEL_STATE_TIMES = [
    # [("scatter", 7), ("chase", 20), ("scatter", 7), ("chase", 20), ("scatter", 5), ("chase", 20),
    #  ("scatter", 5), ("chase", -1)],  # level 1
    [("scatter", 1), ("chase", 50), ("scatter", 5), ("chase", 5), ("scatter", 5), ("chase", 5),
     ("scatter", 5), ("chase", -1)],  # level 1
    [("scatter", 7), ("chase", 20), ("scatter", 7), ("chase", 20), ("scatter", 5), ("chase", 1033),
     ("scatter", 1), ("chase", -1)],  # level 2 - 4
    [("scatter", 5), ("chase", 20), ("scatter", 5), ("chase", 20), ("scatter", 5), ("chase", 1037),
     ("scatter", 1), ("chase", -1)]]  # level 5+

# What bonus fruit will appear in each level (repeat last level's bonus fruit if there are more levels than bonus fruits)
BONUS_FRUIT = [["cherry", "strawberry"],  # level 1
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
# After how many dots the fruits will appear as percentage of the total dots
FRUIT_SPAWN_TRIGGER = [0.3, 0.7]

# For how long the fruit will remain on the screen (in seconds)
FRUIT_DURATION = 10

global_state_stop_time = []
game_over = [False]
draw_ghosts = [True]


def draw_window(sprite_list, maze_data):
    screen.fill(BLACK)

    for sprite in sprite_list:
        sprite.draw(screen)

    # display the path of the ghosts
    if draw_ghosts[0]:
        for ghost in sprite_list[1]:
            ghost.draw_classic_path(screen, maze_data)
            ghost.my_draw(screen)

    for pacman in sprite_list[0]:
        pacman.my_draw(screen)

    for bonus_fruit in sprite_list[6]:
        bonus_fruit.my_draw(screen)

    pygame.display.update()


def register_keys(event):
    if event.key == pygame.K_LEFT:
        return "left"
    elif event.key == pygame.K_RIGHT:
        return "right"
    elif event.key == pygame.K_UP:
        return "up"
    elif event.key == pygame.K_DOWN:
        return "down"


power_pellet_debug = False
invisibility_debug = False
debug = [power_pellet_debug, invisibility_debug]


# last_keys[0] is the current direction that all pacmans are moving and will continue to move in that direction unless
# there is a wall in the way or the user presses the opposite direction key.
# If there is a queued key that is 90 degrees from the current direction, then the current direction will be changed to
# the queued key once there is no wall in the way in the new direction.
def move_pacmans(last_keys, pacmans, maze_data):
    for pacman in pacmans:
        # print(pacman.can_change_direction(maze_data, "up", True), " ",
        #        pacman.can_change_direction(maze_data, "down", True), " ",
        #        pacman.can_change_direction(maze_data, "left", True), " ",
        #        pacman.can_change_direction(maze_data, "right", True))

        # if pacman is dying, don't move it
        if pacman.direction == "dying":
            continue

        if last_keys[0] != "none" and pacman.direction == "stay" and pacman.can_change_direction(maze_data,
                                                                                                 last_keys[0], True):
            pacman.direction = last_keys[0]
        if last_keys[0] == "left":

            if pacman.direction == "left" and last_keys[1] == "up" and pacman.can_change_direction(maze_data, "up"):
                pacman.direction = "up"
                last_keys[0] = "up"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "left"
                        break
            elif pacman.direction == "left" and last_keys[1] == "down" and pacman.can_change_direction(maze_data,
                                                                                                       "down"):
                pacman.direction = "down"
                last_keys[0] = "down"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "left"
                        break
            elif pacman.direction == "left" and last_keys[1] == "right" and pacman.can_change_direction(maze_data,
                                                                                                        "right"):
                pacman.direction = "right"
                last_keys[0] = "right"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "left"
                        break
            elif pacman.can_change_direction(maze_data, "left"):
                pacman.direction = "left"
        elif last_keys[0] == "right":
            if pacman.direction == "right" and last_keys[1] == "up" and pacman.can_change_direction(maze_data, "up"):
                pacman.direction = "up"
                last_keys[0] = "up"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "right"
                        break
            elif pacman.direction == "right" and last_keys[1] == "down" and pacman.can_change_direction(maze_data,
                                                                                                        "down"):
                pacman.direction = "down"
                last_keys[0] = "down"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "right"
                        break
            elif pacman.direction == "right" and last_keys[1] == "left" and pacman.can_change_direction(maze_data,
                                                                                                        "left"):
                pacman.direction = "left"
                last_keys[0] = "left"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "right"
                        break
            elif pacman.can_change_direction(maze_data, "right"):
                pacman.direction = "right"
        elif last_keys[0] == "up":
            if pacman.direction == "up" and last_keys[1] == "right" and pacman.can_change_direction(maze_data, "right"):
                pacman.direction = "right"
                last_keys[0] = "right"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "up"
                        break
            elif pacman.direction == "up" and last_keys[1] == "left" and pacman.can_change_direction(maze_data, "left"):
                pacman.direction = "left"
                last_keys[0] = "left"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "up"
                        break
            elif pacman.direction == "up" and last_keys[1] == "down" and pacman.can_change_direction(maze_data, "down"):
                pacman.direction = "down"
                last_keys[0] = "down"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "up"
                        break
            elif pacman.can_change_direction(maze_data, "up"):
                pacman.direction = "up"
        elif last_keys[0] == "down":
            if pacman.direction == "down" and last_keys[1] == "right" and pacman.can_change_direction(maze_data,
                                                                                                      "right"):
                pacman.direction = "right"
                last_keys[0] = "right"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "down"
                        break
            elif pacman.direction == "down" and last_keys[1] == "left" and pacman.can_change_direction(maze_data,
                                                                                                       "left"):
                pacman.direction = "left"
                last_keys[0] = "left"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "down"
                        break
            elif pacman.direction == "down" and last_keys[1] == "up" and pacman.can_change_direction(maze_data, "up"):
                pacman.direction = "up"
                last_keys[0] = "up"
                last_keys[1] = last_keys[2]
                last_keys[2] = last_keys[3]
                last_keys[3] = "none"
                for i in range(1, len(last_keys)):
                    if last_keys[i] == "none":
                        last_keys[i] = "down"
                        break
            elif pacman.can_change_direction(maze_data, "down"):
                pacman.direction = "down"

        old_pos = pacman.get_pos()
        # Move pacman in the direction he is facing by adding the speed to the x or y position.
        # If pacman is at the edge of the maze, move him to the other side taking into account the size of the maze
        # and its offset (using SCALE and WIDTH and HEIGHT).

        # print(last_keys)
        # print(old_pos, pacman.logic_pos)
        # print(pacman.check_open_path(maze_data, "left"), pacman.check_open_path(maze_data, "right"), pacman.check_open_path(maze_data, "up"), pacman.check_open_path(maze_data, "down"))
        # print(pacman.can_change_direction(maze_data, "left"), pacman.can_change_direction(maze_data, "right"), pacman.can_change_direction(maze_data, "up"), pacman.can_change_direction(maze_data, "down"))
        if pacman.direction != "stay":
            if pacman.direction == "left" and pacman.check_open_path(maze_data, "left"):
                # pacman.get_pos()[0] -= pacman.current_speed

                pacman.move(old_pos[0] - pacman.current_speed, old_pos[1])
                # print(old_pos[0] - pacman.current_speed)
                if pacman.get_pos()[0] < \
                        utilities.get_position_in_window(0, utilities.get_position_in_maze_int(pacman.get_pos()[0],
                                                                                               pacman.get_pos()[1],
                                                                                               SCALE, WIDTH,
                                                                                               HEIGHT)[1],
                                                         SCALE, WIDTH, HEIGHT)[0]:
                    pacman.move(utilities.get_position_in_window(31, 0, SCALE, WIDTH, HEIGHT)[0],
                                pacman.get_pos()[1])  # Teleport to other side if needed
            elif pacman.direction == "right" and pacman.check_open_path(maze_data, "right"):
                # pacman.get_pos()[0] += pacman.current_speed
                pacman.move(old_pos[0] + pacman.current_speed, old_pos[1])
                if pacman.get_pos()[0] > \
                        utilities.get_position_in_window(31, utilities.get_position_in_maze_int(pacman.get_pos()[0],
                                                                                                pacman.get_pos()[1],
                                                                                                SCALE, WIDTH,
                                                                                                HEIGHT)[1],
                                                         SCALE, WIDTH, HEIGHT)[0]:
                    pacman.move(utilities.get_position_in_window(0, 0, SCALE, WIDTH, HEIGHT)[0], pacman.get_pos()[1])

            elif pacman.direction == "up" and pacman.check_open_path(maze_data, "up"):
                # pacman.get_pos()[1] -= pacman.current_speed
                pacman.move(old_pos[0], old_pos[1] - pacman.current_speed)
                if pacman.get_pos()[1] < \
                        utilities.get_position_in_window(utilities.get_position_in_maze_int(pacman.get_pos()[0],
                                                                                            pacman.get_pos()[1],
                                                                                            SCALE, WIDTH,
                                                                                            HEIGHT)[0], 0,
                                                         SCALE, WIDTH, HEIGHT)[1]:
                    pacman.move(pacman.get_pos()[0], utilities.get_position_in_window(0, 31, SCALE, WIDTH, HEIGHT)[1])


            elif pacman.direction == "down" and pacman.check_open_path(maze_data, "down"):
                # pacman.get_pos()[1] += pacman.current_speed
                pacman.move(old_pos[0], old_pos[1] + pacman.current_speed)
                if pacman.get_pos()[1] > \
                        utilities.get_position_in_window(utilities.get_position_in_maze_int(pacman.get_pos()[0],
                                                                                            pacman.get_pos()[1],
                                                                                            SCALE, WIDTH,
                                                                                            HEIGHT)[0], 31,
                                                         SCALE, WIDTH, HEIGHT)[1]:
                    pacman.move(pacman.get_pos()[0], utilities.get_position_in_window(0, 0, SCALE, WIDTH, HEIGHT)[1])

        pacman.moving = not (old_pos[0] == pacman.get_pos()[0] and pacman.get_pos()[1] == old_pos[1])
    # print(last_keys)
    return last_keys


def update_sprites(maze_data, pacmans, ghosts, consumables, ghost_houses):
    all_pacmans_dead = True
    for pacman in pacmans:
        maze_data = pacman.update(maze_data, consumables)
        if pacman.consumed_power_pellet or power_pellet_debug:
            pacman.consumed_power_pellet = False
            frightened_time = 5
            if len(global_state_stop_time) > 0:
                global_state_stop_time.pop()
            global_state_stop_time.append((0, frightened_time))
            for ghost in ghosts:
                ghost.overwrite_global_state("frightened", frightened_time)

        if pacman.direction != "dying" and pacman.direction != "dead":
            all_pacmans_dead = False

    if all_pacmans_dead and not utilities.get_stop_time() and not game_over[0]:
        utilities.set_stop_time(1)
        game_over[0] = True


    for ghost_house in ghost_houses:
        ghost_house.update(pacmans, maze_data)

    for ghost in ghosts:
        ghost.update(maze_data, pacmans, ghosts, debug)

    for consumable in consumables:
        consumable.update(maze_data)

    return maze_data


def update_states(level_times, current_time, ghosts):
    # get current time of pygame in seconds
    state = "scatter"
    time = level_times[0][1]

    for i in range(0, len(level_times)):
        if current_time < time:
            state = level_times[i][0]
            break

        if i != len(level_times) - 1 or level_times[i][1] != -1:
            time += level_times[i + 1][1]
        else:
            state = level_times[i][0]
            break

    for ghost in ghosts:
        ghost.set_global_state(state)


def main():
    clock = pygame.time.Clock()
    run = True

    maze_data = []
    for y in range(32):
        maze_data.append([])
        for x in range(32):
            # If the pixel is black, add a 0 to the maze_data list (representing empty space)
            if MAZE1.get_at((x, y)) == (0, 0, 0):
                maze_data[y].append(0)
            # If the pixel is yellow, add a 2 to the maze_data list (representing a pellet)
            elif MAZE1.get_at((x, y)) == (255, 255, 0):
                maze_data[y].append(2)
            # If the pixel is green, add a 3 to the maze_data list (representing a power pellet)
            elif MAZE1.get_at((x, y)) == (0, 255, 0):
                maze_data[y].append(3)
            # If the pixel is red, add a 4 to the maze_data list (representing a ghost house)
            elif MAZE1.get_at((x, y)) == (255, 0, 0):
                maze_data[y].append(4)
            # If the pixel is blue, add a 5 to the maze_data list (representing the player's starting position)
            elif MAZE1.get_at((x, y)) == (0, 0, 255):
                maze_data[y].append(5)
            # If the pixel is orange, add a 6 to the maze_data list (representing a bonus fruit spawning position)
            elif MAZE1.get_at((x, y)) == (255, 128, 0):
                maze_data[y].append(6)
            # If the pixel is any other color, add a 1 to the maze_data list (representing a wall)
            else:
                maze_data[y].append(1)

    # Create a list for the sprites
    walls = pygame.sprite.Group()
    pellets = pygame.sprite.Group()
    power_pellets = pygame.sprite.Group()
    ghost_houses = pygame.sprite.Group()
    ghosts = pygame.sprite.Group()
    pacmans = pygame.sprite.Group()
    bonus_fruits = pygame.sprite.Group()

    # Destroy the surrounding objects of the ghost house to prevent the ghosts from getting stuck
    # pellets and power pellets are fine, but walls, pacmans and other ghost houses are not
    # ghost house is 8x5 tiles
    ghost_house_placements = []  # list of ghost house placements to stop generation of new ghost houses if they overlap

    ghost_house_dimensions = (8, 5)
    for y in range(MAZE_SIZE[1]):
        for x in range(MAZE_SIZE[0]):
            if maze_data[y][x] == 4:
                print("Found ghost house at " + str(x) + ", " + str(y))
                # check if ghost house overlaps with another ghost house
                if check_ghost_house_overlap(ghost_house_dimensions, ghost_house_placements, x, y):
                    maze_data[y][x] = 0

                # check if ghost house would generate out of bounds
                if x + ghost_house_dimensions[0] > MAZE_SIZE[0] or y + ghost_house_dimensions[1] > MAZE_SIZE[1]:
                    print("Error trying to place ghost house at", x, y, ": Out of bounds")
                    maze_data[y][x] = 0

                # skip ghost house generation if the above checks failed
                if maze_data[y][x] != 4:
                    continue

                # generate ghost house
                for i in range(ghost_house_dimensions[1]):
                    for j in range(ghost_house_dimensions[0]):

                        # check if another ghost would be generated in the location and log an error before deleting it
                        if maze_data[y + i][x + j] == 4 and (x + j, y + i) != (x, y):
                            print("Error trying to place ghost house at", x + j, y + i,
                                  ": Overlaps with ghost house at", x, y)

                        maze_data[y + i][x + j] = 0
                        ghost_house_placements.append((y + i, x + j))
                        # create walls in a hollow square around the ghost house (8x5 tiles) and clear any
                        # pellets in the square inside
                        if (i == 0 or i == ghost_house_dimensions[1] - 1) and 0 <= j <= ghost_house_dimensions[
                            0] - 1:
                            maze_data[y + i][x + j] = 1
                        elif (j == 0 or j == ghost_house_dimensions[0] - 1) and 0 <= i <= ghost_house_dimensions[
                            1] - 1:
                            maze_data[y + i][x + j] = 1

                # create ghost house instance
                ghosts_images = [utilities.load_ghost_sheet(BLINKY_SHEET_IMAGE, 1, 4, 16, 16, EYES_SHEET_IMAGE),
                                 utilities.load_ghost_sheet(PINKY_SHEET_IMAGE, 1, 4, 16, 16, EYES_SHEET_IMAGE)]
                pos_in_window = utilities.get_position_in_window(x, y, SCALE, WIDTH, HEIGHT)

                ghost_house = GhostHouse(pos_in_window[0], pos_in_window[1], ["blinky", "pinky"], ghosts_images,
                                         utilities.load_sheet(FRIGHTENED_GHOST_SHEET_IMAGE, 1, 4, 16, 16), WIDTH,
                                         HEIGHT, SCALE, FPS)
                ghost_houses.add(ghost_house)
                ghost_house_entrance = utilities.get_position_in_window(ghost_house.get_entrance()[0],
                                                                        ghost_house.get_entrance()[1], SCALE, WIDTH,
                                                                        HEIGHT)
                ghosts.add(Ghost(ghost_house_entrance[0], ghost_house_entrance[1],
                                 utilities.load_ghost_sheet(BLINKY_SHEET_IMAGE, 1, 4, 16, 16, EYES_SHEET_IMAGE),
                                 utilities.load_sheet(FRIGHTENED_GHOST_SHEET_IMAGE, 1, 4, 16, 16), "blinky", WIDTH,
                                 HEIGHT, SCALE, FPS, 1.9, ghost_house, 0))
                ghosts.add(Ghost(ghost_house_entrance[0], ghost_house_entrance[1],
                                 utilities.load_ghost_sheet(PINKY_SHEET_IMAGE, 1, 4, 16, 16, EYES_SHEET_IMAGE),
                                 utilities.load_sheet(FRIGHTENED_GHOST_SHEET_IMAGE, 1, 4, 16, 16), "pinky", WIDTH,
                                 HEIGHT, SCALE, FPS, 1.9, ghost_house, 1))
                ghosts.add(Ghost(ghost_house_entrance[0], ghost_house_entrance[1],
                                 utilities.load_ghost_sheet(INKY_SHEET_IMAGE, 1, 4, 16, 16, EYES_SHEET_IMAGE),
                                 utilities.load_sheet(FRIGHTENED_GHOST_SHEET_IMAGE, 1, 4, 16, 16), "inky", WIDTH,
                                 HEIGHT, SCALE, FPS, 1.9, ghost_house, 2))
                ghosts.add(Ghost(ghost_house_entrance[0], ghost_house_entrance[1],
                                 utilities.load_ghost_sheet(CLYDE_SHEET_IMAGE, 1, 4, 16, 16, EYES_SHEET_IMAGE),
                                 utilities.load_sheet(FRIGHTENED_GHOST_SHEET_IMAGE, 1, 4, 16, 16), "clyde", WIDTH,
                                 HEIGHT, SCALE, FPS, 1.9, ghost_house, 3))
                # TODO: add the entrance to the ghost house

    # populate maze with sprites based on maze_data. Maze centered and scaled to fit screen (using SCALE)
    for y in range(32):
        for x in range(32):
            if maze_data[y][x] == 1:
                walls.add(
                    Wall(x * SCALE + (WIDTH - 32 * SCALE) / 2, y * SCALE + (HEIGHT - 32 * SCALE) / 2, SCALE, WIDTH,
                         HEIGHT, utilities.load_sheet(WALLS_SHEET_IMAGE, 12, 4, 16, 16)))
            elif maze_data[y][x] == 2:
                pellets.add(
                    Pellet(x * SCALE + (WIDTH - 32 * SCALE) / 2, y * SCALE + (HEIGHT - 32 * SCALE) / 2, SCALE, SCALE,
                           PELLETS_SHEET_IMAGE))
            elif maze_data[y][x] == 3:
                power_pellets.add(
                    PowerPellet(x * SCALE + (WIDTH - 32 * SCALE) / 2, y * SCALE + (HEIGHT - 32 * SCALE) / 2, SCALE,
                                SCALE, PELLETS_SHEET_IMAGE))
            elif maze_data[y][x] == 4:
                # if (somehow) there is a ghost house in the maze data still, replace it with a wall
                maze_data[y][x] = 1
                walls.add(
                    Wall(x * SCALE + (WIDTH - 32 * SCALE) / 2, y * SCALE + (HEIGHT - 32 * SCALE) / 2, SCALE, WIDTH,
                         HEIGHT, utilities.load_sheet(WALLS_SHEET_IMAGE, 12, 4, 16, 16)))
            elif maze_data[y][x] == 5:
                # pacmans.add( Pacman(x * SCALE + (WIDTH - 31 * SCALE) / 2, y * SCALE + (HEIGHT - 32.4 * SCALE) / 2,
                # SCALE, SCALE, 2))
                pacmans.add(
                    Pacman(x * SCALE + (WIDTH - 32 * SCALE) / 2 + SCALE / 2,
                           y * SCALE + (HEIGHT - 32 * SCALE) / 2,
                           WIDTH, HEIGHT,
                           PACMAN_SHEET_IMAGE,
                           SCALE,
                           2))
            elif maze_data[y][x] == 6:
                bonus_fruits.add(
                    BonusFruit(x * SCALE + (WIDTH - 32 * SCALE) / 2 + SCALE / 2, y * SCALE + (HEIGHT - 32 * SCALE) / 2,
                               SCALE, WIDTH, HEIGHT,
                               utilities.load_sheet(BONUS_FRUIT_SHEET_IMAGE, 1, 9, 16, 16), FPS,
                               BONUS_FRUIT[0], FRUIT_SPAWN_TRIGGER,
                               len(utilities.get_occurrences_in_maze(maze_data,
                                                                     2) + utilities.get_occurrences_in_maze(
                                   maze_data, 3)), FRUIT_DURATION))

    # TEST: ghosts
    # ghosts.add(Ghost(3 * SCALE + (WIDTH - 32 * SCALE) / 2, 2 * SCALE + (HEIGHT - 32 * SCALE) / 2,
    #                  utilities.load_ghost_sheet(INKY_SHEET_IMAGE, 1, 4, 16, 16, EYES_SHEET_IMAGE),
    #                  utilities.load_sheet(FRIGHTENED_GHOST_SHEET_IMAGE, 1, 4, 16, 16), "inky", WIDTH,
    #                  HEIGHT, SCALE, FPS, 1.9, None, 0))

    last_keys = ["none", "none", "none", "none"]
    current_tim = 0
    current_level = 0
    wall_change = True  # To update the wall connections when needed
    stop_time_clock = 0  # To keep track of the time when the time is stopped

    while run:
        clock.tick(FPS)

        if wall_change:  # needs to be rewritten to only update the walls that have changed
            walls.update(maze_data)
            wall_change = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Queue up the last 4 keys pressed, so that the player can easily change directions. Remove keys from the
            # queue if they are released and move the ones that are still pressed to the front of the queue.
            elif event.type == pygame.KEYDOWN:
                if last_keys[0] == "none" or last_keys[0] == register_keys(event):
                    last_keys[0] = register_keys(event)
                elif last_keys[1] == "none":
                    last_keys[1] = register_keys(event)
                elif last_keys[2] == "none":
                    last_keys[2] = register_keys(event)
                elif last_keys[3] == "none":
                    last_keys[3] = register_keys(event)

            elif event.type == pygame.KEYUP:
                if last_keys[0] == register_keys(event):
                    last_keys[0] = last_keys[1]
                    last_keys[1] = last_keys[2]
                    last_keys[2] = last_keys[3]
                    last_keys[3] = "none"
                elif last_keys[1] == register_keys(event):
                    last_keys[1] = last_keys[2]
                    last_keys[2] = last_keys[3]
                    last_keys[3] = "none"
                elif last_keys[2] == register_keys(event):
                    last_keys[2] = last_keys[3]
                    last_keys[3] = "none"
                elif last_keys[3] == register_keys(event):
                    last_keys[3] = "none"

        if not utilities.get_stop_time():
            last_keys = move_pacmans(last_keys, pacmans, maze_data)
            maze_data = update_sprites(maze_data, pacmans, ghosts, [pellets, power_pellets, bonus_fruits], ghost_houses)
            draw_window([pacmans, ghosts, walls, pellets, power_pellets, ghost_houses, bonus_fruits], maze_data)

            if len(global_state_stop_time) > 0:
                global_state_stop_time[0] = (global_state_stop_time[0][0] + 1, global_state_stop_time[0][1])
                if global_state_stop_time[0][0] >= global_state_stop_time[0][1] * FPS:
                    global_state_stop_time.pop(0)
            else:
                current_tim += 1
            update_states(LEVEL_STATE_TIMES[current_level], current_tim / FPS, ghosts)
            if game_over[0]:
                draw_ghosts[0] = False
        else:
            stop_time_clock += 1
            if stop_time_clock >= utilities.get_stop_time() * FPS:
                utilities.set_stop_time(0)
                stop_time_clock = 0

    #        spawn_fruit(current_level, BONUS_FRUIT, FRUIT_SPAWN_TRIGGER, maze_data)

    pygame.quit()


def check_ghost_house_overlap(ghost_house_dimensions, ghost_house_placements, x, y):
    for j in range(ghost_house_dimensions[1]):
        for i in range(ghost_house_dimensions[0]):
            if (y + j, x + i) in ghost_house_placements:
                print("Error trying to place ghost house at", x, y, ": ghost house would overlap with "
                                                                    "another already generated ghost house at", x + i,
                      y + j)
                return True
    return False


if __name__ == "__main__":
    main()
