import copy

import pygame
from pygame.sprite import Group

import utilities
from BonusFruit import BonusFruit
from Ghost import Ghost
from GhostHouse import GhostHouse
from MazeGenerator import MazeGenerator
from Pacman import Pacman
from Pellet import Pellet
from PowerPellet import PowerPellet
from SFXHandler import SFXHandler
from ScorePopup import ScorePopup
from UIHandler import UIHandler
from Wall import Wall

import ResourceManager
import config

pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Procedurally Generated Pacman")

# Load all resources at the start
resources = ResourceManager.initialize_resources()

global_state_stop_time = []
game_over = [False]
draw_ghosts = [True]


def draw_window(sprite_list, maze_data, animated=True):
    screen.fill(config.BLACK)

    for sprite in sprite_list:
        sprite.draw(screen)

    # display the path of the ghosts
    if draw_ghosts[0]:
        for ghost in sprite_list[1]:
            if not ghost.is_enabled():
                continue
            if utilities.AStarMode[0] and utilities.draw_paths[0]:
                ghost.draw_astar_path(screen, maze_data)
            elif utilities.draw_paths[0]:
                ghost.draw_classic_path(screen, maze_data)

            ghost.my_draw(screen)

    for pacman in sprite_list[0]:
        pacman.my_draw(screen, animated)

    for bonus_fruit in sprite_list[6]:
        bonus_fruit.my_draw(screen)

    if utilities.draw_highlighted_tiles[0]:
        size = 5
        last_color = None
        for int_pos in utilities.highlighted_tiles:
            window_pos = utilities.get_position_in_window(int_pos[0][0], int_pos[0][1], config.config.SCALE, config.WIDTH, config.HEIGHT)
            pygame.draw.rect(screen, int_pos[1],
                             (window_pos[0] + config.SCALE / 2 - size / 2, window_pos[1] + config.SCALE / 2 - size / 2, size, size),
                             2)
            if last_color is not None and last_color != int_pos[1] or size > config.SCALE:
                size = 5
            last_color = int_pos[1]
            size += 1
        # utilities.empty_highlighted_tiles()


# pygame.display.update()


def register_keys(event):
    if event.key == pygame.K_LEFT:
        return "left"
    elif event.key == pygame.K_RIGHT:
        return "right"
    elif event.key == pygame.K_UP:
        return "up"
    elif event.key == pygame.K_DOWN:
        return "down"


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

        old_pos = pacman.get_pos()  # in window coordinates
        # Move pacman in the direction he is facing by adding the speed to the x or y position.
        # If pacman is at the edge of the maze, move him to the other side taking into account the size of the maze
        # and its offset (using config.SCALE and config.WIDTH and config.HEIGHT).

        # print(last_keys) print(old_pos, pacman.logic_pos) print(pacman.check_open_path(maze_data, "left"),
        # pacman.check_open_path(maze_data, "right"), pacman.check_open_path(maze_data, "up"),
        # pacman.check_open_path(maze_data, "down")) print(pacman.can_change_direction(maze_data, "left"),
        # pacman.can_change_direction(maze_data, "right"), pacman.can_change_direction(maze_data, "up"),
        # pacman.can_change_direction(maze_data, "down"))
        if pacman.direction == "stay":
            pass
        elif pacman.direction == "left" and pacman.check_open_path(maze_data, "left"):
            # position in window of next tile
            next_tile_pos = utilities.get_position_in_window(
                pacman.int_pos[0], pacman.int_pos[1], config.SCALE, config.WIDTH, config.HEIGHT)
            # if pacman where to overshoot the center of the tile, move him back to the center instead
            if old_pos[0] - pacman.current_speed < next_tile_pos[0] and old_pos[0] != next_tile_pos[0]:
                pacman.move(next_tile_pos[0], old_pos[1])
            else:
                pacman.move(old_pos[0] - pacman.current_speed, old_pos[1])

            if pacman.get_pos()[0] < \
                    utilities.get_position_in_window(0, utilities.get_position_in_maze_int(pacman.get_pos()[0],
                                                                                           pacman.get_pos()[1],
                                                                                           config.SCALE, config.WIDTH,
                                                                                           config.HEIGHT)[1],
                                                     config.SCALE, config.WIDTH, config.HEIGHT)[0]:
                pacman.move(utilities.get_position_in_window(31, 0, config.SCALE, config.WIDTH, config.HEIGHT)[0],
                            pacman.get_pos()[1])  # Teleport to other side if needed
        elif pacman.direction == "right" and pacman.check_open_path(maze_data, "right"):
            # if pacman where to overshoot the center of the tile, move him back to the center instead
            next_tile_pos = utilities.get_position_in_window(
                pacman.int_pos[0] + 1, pacman.int_pos[1], config.SCALE, config.WIDTH, config.HEIGHT)
            if old_pos[0] + pacman.current_speed > next_tile_pos[0]:
                pacman.move(next_tile_pos[0], old_pos[1])
            else:
                pacman.move(old_pos[0] + pacman.current_speed, old_pos[1])
            if pacman.get_pos()[0] > \
                    utilities.get_position_in_window(31, utilities.get_position_in_maze_int(pacman.get_pos()[0],
                                                                                            pacman.get_pos()[1],
                                                                                            config.SCALE, config.WIDTH,
                                                                                            config.HEIGHT)[1],
                                                     config.SCALE, config.WIDTH, config.HEIGHT)[0]:
                pacman.move(utilities.get_position_in_window(0, 0, config.SCALE, config.WIDTH, config.HEIGHT)[0], pacman.get_pos()[1])

        elif pacman.direction == "up" and pacman.check_open_path(maze_data, "up"):
            # pacman.get_pos()[1] -= pacman.current_speed
            next_tile_pos = utilities.get_position_in_window(
                pacman.int_pos[0], pacman.int_pos[1], config.SCALE, config.WIDTH, config.HEIGHT)
            if old_pos[1] - pacman.current_speed < next_tile_pos[1] and old_pos[1] != next_tile_pos[1]:
                pacman.move(old_pos[0], next_tile_pos[1])
            else:
                pacman.move(old_pos[0], old_pos[1] - pacman.current_speed)
            if pacman.get_pos()[1] < \
                    utilities.get_position_in_window(utilities.get_position_in_maze_int(pacman.get_pos()[0],
                                                                                        pacman.get_pos()[1],
                                                                                        config.SCALE, config.WIDTH,
                                                                                        config.HEIGHT)[0], 0,
                                                     config.SCALE, config.WIDTH, config.HEIGHT)[1]:
                pacman.move(pacman.get_pos()[0], utilities.get_position_in_window(0, 31, config.SCALE, config.WIDTH, config.HEIGHT)[1])

        elif pacman.direction == "down" and pacman.check_open_path(maze_data, "down"):
            # pacman.get_pos()[1] += pacman.current_speed
            next_tile_pos = utilities.get_position_in_window(
                pacman.int_pos[0], pacman.int_pos[1] + 1, config.SCALE, config.WIDTH, config.HEIGHT)
            if old_pos[1] + pacman.current_speed > next_tile_pos[1]:
                pacman.move(old_pos[0], next_tile_pos[1])
            else:
                pacman.move(old_pos[0], old_pos[1] + pacman.current_speed)
            if pacman.get_pos()[1] > \
                    utilities.get_position_in_window(utilities.get_position_in_maze_int(pacman.get_pos()[0],
                                                                                        pacman.get_pos()[1],
                                                                                        config.SCALE, config.WIDTH,
                                                                                        config.HEIGHT)[0], 31,
                                                     config.SCALE, config.WIDTH, config.HEIGHT)[1]:
                pacman.move(pacman.get_pos()[0], utilities.get_position_in_window(0, 0, config.SCALE, config.WIDTH, config.HEIGHT)[1])

        pacman.moving = not (old_pos[0] == pacman.get_pos()[0] and pacman.get_pos()[1] == old_pos[1])
    # print(last_keys)
    return last_keys


def update_sprites(maze_data, pacmans, ghosts, consumables):
    all_pacmans_dead = True
    for pacman in pacmans:
        maze_data = pacman.update(maze_data, consumables)
        if pacman.consumed_power_pellet or utilities.power_pellet_debug[0]:
            pacman.consumed_power_pellet = False

            frightened_time = 5
            if len(global_state_stop_time) > 0:
                global_state_stop_time.pop()
            else:
                utilities.ghost_eaten_score[0] = 200  # reset score multiplier if power wore off
            global_state_stop_time.append((0, frightened_time))
            for ghost in ghosts:
                if ghost.is_enabled():
                    ghost.overwrite_global_state("frightened", frightened_time)

        if pacman.direction != "dying" and pacman.direction != "dead":
            all_pacmans_dead = False

    if all_pacmans_dead and not utilities.get_stop_time() and not game_over[0]:
        utilities.set_stop_time(1)
        game_over[0] = True

    for ghost in ghosts:
        if not ghost.is_enabled():
            continue
        ghost.update(maze_data, pacmans, ghosts)

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


def update_score_popups(score_popups):
    if len(utilities.queued_popups) > 0:
        popup_info = utilities.queued_popups.pop()
        score_popups.add(
            ScorePopup(popup_info[0], popup_info[1], popup_info[5], config.WIDTH, config.HEIGHT, config.FPS, popup_info[2], popup_info[3],
                       popup_info[4]))

    for popup in score_popups:
        popup.update()


def spawn_pacmans(pacmans, maze_data):
    pacman_image = resources["images"]["pacman_sheet_image"]
    for y in range(len(maze_data)):
        for x in range(len(maze_data[y])):
            if maze_data[y][x] == 5: # Assuming 5 indicates the starting position of a pacman
                pacmans.add(
                    Pacman(x * config.SCALE + (config.WIDTH - 32 * config.SCALE) / 2 + config.SCALE / 2,
                           y * config.SCALE + (config.HEIGHT - 32 * config.SCALE) / 2,
                           config.WIDTH, config.HEIGHT,
                           pacman_image,
                           config.SCALE,
                           2.5))


def main():


    clock = pygame.time.Clock()
    run = True

    maze_gen = MazeGenerator(config.MAZE_SIZE[0], config.MAZE_SIZE[1])

    # Load the maze image from the resources
    maze_image = resources["images"]["maze_image"]

    # Generate the maze data based on the maze image
    maze_data = []
    for y in range(config.MAZE_SIZE[1]):  # Dynamically use the maze size from config
        maze_data.append([])
        for x in range(config.MAZE_SIZE[0]):
            color = maze_image.get_at((x, y))

            # Color guide:
            # (0, 0, 0, 255): Black - Empty space
            # (255, 255, 0, 255): Yellow - Pellet
            # (0, 255, 0, 255): Green - Power Pellet
            # (255, 0, 0, 255): Red - Ghost House
            # (0, 0, 255, 255): Blue - Player's starting position
            # (255, 128, 0, 255): Orange - Bonus fruit spawning position
            # Any other color: Wall

            if color == (0, 0, 0, 255):  # Black - Empty space
                maze_data[y].append(0)
            elif color == (255, 255, 0, 255):  # Yellow - Pellet
                maze_data[y].append(2)
            elif color == (0, 255, 0, 255):  # Green - Power Pellet
                maze_data[y].append(3)
            elif color == (255, 0, 0, 255):  # Red - Ghost House
                maze_data[y].append(4)
            elif color == (0, 0, 255, 255):  # Blue - Player's starting position
                maze_data[y].append(5)
            elif color == (255, 128, 0, 255):  # Orange - Bonus fruit spawning position
                maze_data[y].append(6)
            else:  # Any other color - Wall
                maze_data[y].append(1)

    # Create a list for the sprites
    walls = Group()
    pellets = Group()
    power_pellets = Group()
    ghost_houses = Group()
    ghosts = Group()
    pacmans = Group()
    bonus_fruits = Group()
    score_popups = Group()

    sprite_groups = [walls, pellets, power_pellets, ghost_houses, ghosts, pacmans, bonus_fruits, score_popups]

    # TEST: ghosts
    # ghosts.add(Ghost(3 * config.SCALE + (config.WIDTH - 32 * config.SCALE) / 2, 2 * config.SCALE + (config.HEIGHT - 32 * config.SCALE) / 2,
    #                  utilities.load_ghost_sheet(INKY_SHEET_IMAGE, 1, 4, 16, 16, EYES_SHEET_IMAGE),
    #                  utilities.load_sheet(FRIGHTENED_GHOST_SHEET_IMAGE, 1, 4, 16, 16), "inky", config.WIDTH,
    #                  config.HEIGHT, config.SCALE, config.FPS, 1.9, None, 0))

    last_keys = ["none", "none", "none", "none"]
    current_tim = 0
    current_level = 0
    wall_change = False  # To update the wall connections when needed
    stop_time_clock = 0  # To keep track of the time when the time is stopped
    generate_old_maze = False  # To generate the old maze when needed
    new_maze_animation_clock = 0  # To keep track of the time when the new maze animation is playing
    NEW_MAZE_ANIMATION_TIME = 5  # The time the new maze animation takes (in seconds)
    OLD_MAZE_ANIMATION_TIME = 3
    maze_animation_time = 0
    win_animation = False
    win_animation_clock = 0
    WIN_ANIMATION_STOP_TIME = 2
    WIN_ANIMATION_TIME = 5

    og_maze_data = copy.deepcopy(maze_data)

    lives = 5
    extra_life = 10000
    extra_life_given = False

    # Initialize sfx and music handlers
    sfx_handler = SFXHandler(resources, config.FPS)
    og_pellet_count = 0

    # UI handler
    ui_handler = UIHandler(
        config.SCALE,
        config.WIDTH,
        config.HEIGHT,
        config.FPS,
        lives,
        0, # High score
        sfx_handler,
        resources,
        config.BONUS_FRUIT
    )
    # Get high score from file
    high_score_file = open("high_score.txt", "a+")
    high_score_file.seek(0)
    try:
        utilities.high_score[0] = int(high_score_file.read())
    except ValueError:
        utilities.high_score[0] = 0
    high_score_file.close()

    while run:
        clock.tick(config.FPS)
        cursor_click_pos = None
        cursor_hover_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor_click_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEMOTION:
                cursor_hover_pos = pygame.mouse.get_pos()

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

                if event.key == pygame.K_r and utilities.new_maze[0]:
                    utilities.set_regenerate_new_maze(True)

                if event.key == pygame.K_t:
                    utilities.draw_paths[0] = not utilities.draw_paths[0]

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

        if win_animation:
            sfx_handler.stop_music()
            utilities.sfx_queue.clear()
            win_animation_clock += 1
            if win_animation_clock >= WIN_ANIMATION_STOP_TIME * config.FPS:

                if win_animation_clock % 25 * config.FPS == 0:
                    for wall in walls:
                        wall.switch_color()

                ghosts.empty()
                bonus_fruits.empty()
                draw_window([pacmans, ghosts, walls, pellets, power_pellets, ghost_houses, bonus_fruits], maze_data,
                            False)
                ui_handler.update(cursor_click_pos, cursor_hover_pos, lives, utilities.high_score[0],utilities.current_score[0], current_level)
                ui_handler.draw(screen)
                pygame.display.update()

            if win_animation_clock >= WIN_ANIMATION_TIME * config.FPS:
                win_animation = False
                win_animation_clock = 0
                current_level += 1
                utilities.set_regenerate_new_maze(True)
            continue

        if utilities.get_regenerate_new_maze():
            utilities.set_regenerate_new_maze(False)
            sfx_handler.stop_music()
            utilities.empty_highlighted_tiles()
            if not utilities.classic_mode[0]:
                if not maze_gen.generate():
                    utilities.set_regenerate_new_maze(True)
                    continue
                maze_data = maze_gen.get_maze_data()
            else:
                maze_data = copy.deepcopy(og_maze_data)

            for group in sprite_groups:
                group.empty()

            populate_maze(bonus_fruits, ghost_houses, ghosts, maze_data, pacmans, pellets, power_pellets, walls,
                          current_level)

            og_pellet_count = len(utilities.get_occurrences_in_maze(maze_data, 2))
            walls.update(maze_data)
            new_maze_animation_clock = 0
            maze_animation_time = NEW_MAZE_ANIMATION_TIME
            ready_text_pos = utilities.get_position_in_window(16, 18, config.SCALE, config.WIDTH, config.HEIGHT)
            utilities.queued_popups.append((ready_text_pos[0], ready_text_pos[1] + config.SCALE / 2,
                                            "READY!", (255, 255, 0), NEW_MAZE_ANIMATION_TIME, 20))

            game_over[0] = False
            draw_ghosts[0] = True
            current_tim = 0
            stop_time_clock = 0

            sfx_handler.play_sfx("game_start")
            continue

        if generate_old_maze:
            sfx_handler.stop_music()
            # respawn ghosts and pacmans
            for ghost_house in ghost_houses:
                ghost_house.clear_ghosts()
            ghosts.empty()
            pacmans.empty()
            spawn_ghosts(ghosts, ghost_houses)
            spawn_pacmans(pacmans, maze_data)
            new_maze_animation_clock = 0
            maze_animation_time = OLD_MAZE_ANIMATION_TIME
            ready_text_pos = utilities.get_position_in_window(16, 18, config.SCALE, config.WIDTH, config.HEIGHT)
            utilities.queued_popups.append((ready_text_pos[0], ready_text_pos[1] + config.SCALE / 2,
                                            "READY!", (255, 255, 0), OLD_MAZE_ANIMATION_TIME, 20))

            generate_old_maze = False
            game_over[0] = False
            draw_ghosts[0] = True
            current_tim = 0
            stop_time_clock = 0
            continue

        if new_maze_animation_clock < maze_animation_time * config.FPS:
            new_maze_animation_clock += 1

            draw_window([pacmans, ghosts, walls, pellets, power_pellets, ghost_houses, bonus_fruits], maze_data)
            update_score_popups(score_popups)
            score_popups.draw(screen)
            ui_handler.update(cursor_click_pos, cursor_hover_pos, lives, utilities.high_score[0],utilities.current_score[0], current_level)
            ui_handler.draw(screen)
            pygame.display.update()
            continue

        if len(pacmans) == 0 and game_over[0] and lives > 0:
            generate_old_maze = True
            lives -= 1

        if len(pacmans) == 0 and game_over[0] and lives == 0:
            utilities.set_regenerate_new_maze(True)
            generate_old_maze = False
            lives = 5
            current_level = 0
            utilities.current_score[0] = 0
            # write high score to file after deleting its previous contents
            with open("high_score.txt", "w") as file:
                file.write(str(utilities.high_score[0]))
            continue

        if len(pellets) == 0 and len(power_pellets) == 0:
            win_animation = True
            continue

        if wall_change:  # needs to be rewritten to only update the walls that have changed
            walls.update(maze_data)
            wall_change = False

        update_score_popups(score_popups)

        update_music(sfx_handler, maze_data, og_pellet_count, ghosts)

        if not utilities.get_stop_time():
            last_keys = move_pacmans(last_keys, pacmans, maze_data)
            maze_data = update_sprites(maze_data, pacmans, ghosts, [pellets, power_pellets, bonus_fruits])
            draw_window([pacmans, ghosts, walls, pellets, power_pellets, ghost_houses, bonus_fruits], maze_data)

            if len(global_state_stop_time) > 0:
                global_state_stop_time[0] = (global_state_stop_time[0][0] + 1, global_state_stop_time[0][1])
                if global_state_stop_time[0][0] >= global_state_stop_time[0][1] * config.FPS:
                    global_state_stop_time.pop(0)
            else:
                current_tim += 1
            if current_level == 0:
                update_states(config.LEVEL_STATE_TIMES[current_level], current_tim / config.FPS, ghosts)
            elif 0 < current_level < 4:
                update_states(config.LEVEL_STATE_TIMES[1], current_tim / config.FPS, ghosts)
            else:
                update_states(config.LEVEL_STATE_TIMES[2], current_tim / config.FPS, ghosts)
            if game_over[0]:
                draw_ghosts[0] = False
                for bonus_fruit in bonus_fruits:
                    bonus_fruit.despawn_fruit()
        else:
            stop_time_clock += 1
            if stop_time_clock >= utilities.get_stop_time() * config.FPS:
                utilities.set_stop_time(0)
                stop_time_clock = 0

        score_popups.draw(screen)

        # if score reaches 10000 add a life
        if utilities.current_score[0] >= extra_life and not extra_life_given:
            lives += 1
            extra_life_given = True
            utilities.sfx_queue.append("extend")

        ui_handler.update(cursor_click_pos, cursor_hover_pos, lives, utilities.high_score[0],utilities.current_score[0], current_level)
        ui_handler.draw(screen)



        pygame.display.update()

    pygame.quit()


def update_music(sfx_handler, maze_data, og_pellets_count, ghosts):
    if not utilities.SFX_and_Music[0]:
        sfx_handler.stop_music()
        return
    sfx_handler.play_sfx(utilities.get_next_sfx())
    if game_over[0]:
        sfx_handler.stop_music()
        return

    current_state = None
    for ghost in ghosts:
        if ghost.get_state() == "dead" and ghost.is_enabled():
            current_state = "dead"

        if ghost.get_state() == "frightened" and current_state != "dead" and ghost.is_enabled():
            current_state = "frightened"

    if current_state == "dead":
        sfx_handler.play_music("retreating")
        return
    elif current_state == "frightened":
        sfx_handler.play_music("power_pellet")
        return

    pellets_left = len(utilities.get_occurrences_in_maze(maze_data, 2))
    if pellets_left / og_pellets_count > 0.8:
        sfx_handler.play_music("siren_1")
    elif pellets_left / og_pellets_count > 0.6:
        sfx_handler.play_music("siren_2")
    elif pellets_left / og_pellets_count > 0.4:
        sfx_handler.play_music("siren_3")
    elif pellets_left / og_pellets_count > 0.2:
        sfx_handler.play_music("siren_4")
    else:
        sfx_handler.play_music("siren_5")


def spawn_ghosts(ghosts, ghost_houses):
    blinky_sheet = utilities.load_ghost_sheet(resources["images"]["blinky_sheet_image"], 1, 4, 16, 16, resources["images"]["eyes_sheet_image"])
    pinky_sheet = utilities.load_ghost_sheet(resources["images"]["pinky_sheet_image"], 1, 4, 16, 16, resources["images"]["eyes_sheet_image"])
    inky_sheet = utilities.load_ghost_sheet(resources["images"]["inky_sheet_image"], 1, 4, 16, 16, resources["images"]["eyes_sheet_image"])
    clyde_sheet = utilities.load_ghost_sheet(resources["images"]["clyde_sheet_image"], 1, 4, 16, 16, resources["images"]["eyes_sheet_image"])
    frightened_ghost_sheet = utilities.load_sheet(resources["images"]["frightened_ghost_sheet_image"], 1, 4, 16, 16)

    for ghost_house in ghost_houses:
        ghost_house_entrance = ghost_house.get_entrance()
        # Instantiate Ghost objects with pre-loaded sprite sheets
        ghosts.add(Ghost(
            ghost_house_entrance[0], ghost_house_entrance[1],
            blinky_sheet,
            frightened_ghost_sheet, "blinky", config.WIDTH,
            config.HEIGHT, config.SCALE, config.FPS, 2.3, ghost_house, 0
        ))

        ghosts.add(Ghost(
            ghost_house_entrance[0], ghost_house_entrance[1],
            pinky_sheet,
            frightened_ghost_sheet, "pinky", config.WIDTH,
            config.HEIGHT, config.SCALE, config.FPS, 2.3, ghost_house, 1
        ))
        ghosts.add(Ghost(
            ghost_house_entrance[0], ghost_house_entrance[1],
            inky_sheet,
            frightened_ghost_sheet, "inky", config.WIDTH,
            config.HEIGHT, config.SCALE, config.FPS, 2.3, ghost_house, 2
        ))
        ghosts.add(Ghost(
            ghost_house_entrance[0], ghost_house_entrance[1],
            clyde_sheet,
            frightened_ghost_sheet, "clyde", config.WIDTH,
            config.HEIGHT, config.SCALE, config.FPS, 2.3, ghost_house, 3
        ))


def populate_maze(bonus_fruits, ghost_houses, ghosts, maze_data, pacmans, pellets, power_pellets, walls, current_level):
    # Destroy the surrounding objects of the ghost house to prevent the ghosts from getting stuck
    # pellets and power pellets are fine, but walls, pacmans and other ghost houses are not
    # ghost house is 8x5 tiles
    ghost_house_placements = []  # list of ghost house placements to stop generation of new ghost houses if they overlap
    ghost_house_dimensions = (8, 5)
    for y in range(config.MAZE_SIZE[1]):
        for x in range(config.MAZE_SIZE[0]):
            if maze_data[y][x] == 4:
                print("Found ghost house at " + str(x) + ", " + str(y))
                # check if ghost house overlaps with another ghost house
                if check_ghost_house_overlap(ghost_house_dimensions, ghost_house_placements, x, y):
                    maze_data[y][x] = 0

                # check if ghost house would generate out of bounds
                if x + ghost_house_dimensions[0] > config.MAZE_SIZE[0] or y + ghost_house_dimensions[1] > config.MAZE_SIZE[1]:
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
                pos_in_window = utilities.get_position_in_window(x, y, config.SCALE, config.WIDTH, config.HEIGHT)

                ghost_house = GhostHouse(pos_in_window[0], pos_in_window[1], config.WIDTH,
                                         config.HEIGHT, config.SCALE, config.FPS)
                ghost_houses.add(ghost_house)
                ghost_house_entrance = utilities.get_position_in_window(ghost_house.get_entrance()[0],
                                                                        ghost_house.get_entrance()[1], config.SCALE, config.WIDTH,
                                                                        config.HEIGHT)
                # TODO: add the entrance to the ghost house
    # add ghosts to the ghost house
    spawn_ghosts(ghosts, ghost_houses)
    # populate maze with sprites based on maze_data. Maze centered and config.scaled to fit screen (using config.SCALE)
    for y in range(config.MAZE_SIZE[1]):
        for x in range(config.MAZE_SIZE[0]):
            if maze_data[y][x] == 1:
                walls.add(
                    Wall(x * config.SCALE + (config.WIDTH - 32 * config.SCALE) / 2,
                         y * config.SCALE + (config.HEIGHT - 32 * config.SCALE) / 2,
                         config.SCALE, config.WIDTH, config.HEIGHT,
                         utilities.load_sheet(resources["images"]["walls_sheet_image"], 12, 4, 16, 16),
                         utilities.load_sheet(resources["images"]["walls_white_sheet_image"], 12, 4, 16, 16)))
            elif maze_data[y][x] == 2:
                pellets.add(
                    Pellet(x * config.SCALE + (config.WIDTH - 32 * config.SCALE) / 2,
                           y * config.SCALE + (config.HEIGHT - 32 * config.SCALE) / 2,
                           config.SCALE, config.SCALE,
                           resources["images"]["pellets_sheet_image"]))
            elif maze_data[y][x] == 3:
                power_pellets.add(
                    PowerPellet(x * config.SCALE + (config.WIDTH - 32 * config.SCALE) / 2,
                                y * config.SCALE + (config.HEIGHT - 32 * config.SCALE) / 2,
                                config.SCALE, config.SCALE,
                                resources["images"]["pellets_sheet_image"]))
            elif maze_data[y][x] == 4:
                # if (somehow) there is a ghost house in the maze data still, replace it with a wall
                maze_data[y][x] = 1
                walls.add(
                    Wall(x * config.SCALE + (config.WIDTH - 32 * config.SCALE) / 2, y * config.SCALE + (config.HEIGHT - 32 * config.SCALE) / 2, config.SCALE, config.WIDTH,
                         config.HEIGHT, utilities.load_sheet(resources["images"]["walls_sheet_image"], 12, 4, 16, 16),
                         utilities.load_sheet(resources["images"]["walls_white_sheet_image"], 12, 4, 16, 16)))
            elif maze_data[y][x] == 5:
                # pacmans.add( Pacman(x * config.SCALE + (config.WIDTH - 31 * config.SCALE) / 2, y * config.SCALE + (config.HEIGHT - 32.4 * config.SCALE) / 2,
                # config.SCALE, config.SCALE, 2))
                pacmans.add(
                    Pacman(x * config.SCALE + (config.WIDTH - 32 * config.SCALE) / 2 + config.SCALE / 2,
                           y * config.SCALE + (config.HEIGHT - 32 * config.SCALE) / 2,
                           config.WIDTH, config.HEIGHT,
                           resources["images"]["pacman_sheet_image"],
                           config.SCALE,
                           2.5))
            elif maze_data[y][x] == 6:
                if current_level < len(config.BONUS_FRUIT):
                    level = current_level
                else:
                    level = len(config.BONUS_FRUIT) - 1
                bonus_fruits.add(
                    BonusFruit(x * config.SCALE + (config.WIDTH - 32 * config.SCALE) / 2 + config.SCALE / 2, y * config.SCALE + (config.HEIGHT - 32 * config.SCALE) / 2,
                               config.SCALE, config.WIDTH, config.HEIGHT,
                               utilities.load_sheet(resources["images"]["bonus_fruit_sheet_image"], 1, 9, 16, 16), config.FPS,
                               config.BONUS_FRUIT[level], config.FRUIT_SPAWN_TRIGGER,
                               len(utilities.get_occurrences_in_maze(maze_data,
                                                                     2) + utilities.get_occurrences_in_maze(
                                   maze_data, 3)), config.FRUIT_DURATION))


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
