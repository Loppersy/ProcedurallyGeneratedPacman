# Display settings
WIDTH, HEIGHT = 1080, 720
SCALE = 22
FPS = 60

# Maze configuration
MAZE_SIZE = (32, 32)

# Gameplay settings
# times of the different modes for each level. In seconds
LEVEL_STATE_TIMES = [
    [("scatter", 7), ("chase", 20), ("scatter", 7), ("chase", 20), ("scatter", 5), ("chase", 20),
     ("scatter", 5), ("chase", -1)],  # level 1
    [("scatter", 7), ("chase", 20), ("scatter", 7), ("chase", 20), ("scatter", 5), ("chase", 1033),
     ("scatter", 1), ("chase", -1)],  # level 2 - 4
    [("scatter", 5), ("chase", 20), ("scatter", 5), ("chase", 20), ("scatter", 5), ("chase", 1037),
     ("scatter", 1), ("chase", -1)]]  # level 5+

# What bonus fruit will appear in each level (repeat last level's bonus fruit if there are more levels than bonus fruits)
BONUS_FRUIT = [["cherry", "cherry"],  # level 1
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

# Colors
BLACK = (0, 0, 0)

#Assets
ASSET_PATHS = {
    "inky_sheet_image": "assets/inky.png",
    "pinky_sheet_image": "assets/pinky.png",
    "blinky_sheet_image": "assets/blinky.png",
    "clyde_sheet_image": "assets/clyde.png",
    "pacman_sheet_image": "assets/pacman.png",
    "eyes_sheet_image": "assets/eyes.png",
    "pellets_sheet_image": "assets/pallets.png",
    "frightened_ghost_sheet_image": "assets/frightened_ghost.png",
    "bonus_fruit_sheet_image": "assets/bonus_fruit.png",
    "walls_sheet_image": "assets/walls.png",
    "walls_white_sheet_image": "assets/walls_white.png",
    "regenerate_button": "assets/UI/regen_button.png",
    "regenerate_button_hover": "assets/UI/regen_button_hover.png",
    "ghost_button": "assets/UI/ghost_button.png",
    "ghost_button_hover": "assets/UI/ghost_button_hover.png",
    "blinky_button": "assets/UI/blinky_button.png",
    "pinky_button": "assets/UI/pinky_button.png",
    "inky_button": "assets/UI/inky_button.png",
    "clyde_button": "assets/UI/clyde_button.png",
    "path_button": "assets/UI/path_button.png",
    "path_button_hover": "assets/UI/path_button_hover.png",
    "pathfinder_button": "assets/UI/pathfinder_button.png",
    "pathfinder_button_hover": "assets/UI/pathfinder_button_hover.png",
    "a_star_text": "assets/UI/a_star.png",
    "classic_text": "assets/UI/classic.png",
    "no_dmg_button": "assets/UI/no_dmg.png",
    "no_dmg_button_hover": "assets/UI/no_dmg_hover.png",
    "on_button": "assets/UI/on.png",
    "off_button": "assets/UI/off.png",
    "disabled_button": "assets/UI/disabled_button.png",
    "sound_button": "assets/UI/sound_button.png",
    "sound_button_hover": "assets/UI/sound_button_hover.png",
    "sound_on": "assets/UI/sound_on.png",
    "sound_off": "assets/UI/sound_off.png",
    "classic_button": "assets/UI/classic_button.png",
    "classic_button_hover": "assets/UI/classic_button_hover.png",
    "maze_image": "assets/maze_test.png",
}

# Music and SFX

SOUND_EFFECTS_PATHS = {
    "credit": "sound_effects/credit.wav",
    "death_1": "sound_effects/death_1.wav",
    "death_2": "sound_effects/death_2.wav",
    "eat_fruit": "sound_effects/eat_fruit.wav",
    "eat_ghost": "sound_effects/eat_ghost.wav",
    "extend": "sound_effects/extend.wav",
    "game_start": "sound_effects/game_start.wav",
    "intermission": "sound_effects/intermission.wav",
    "munch_1": "sound_effects/munch_1.wav",
    "munch_2": "sound_effects/munch_2.wav",
}

MUSIC_PATHS = {
    "power_pellet": "sound_effects/power_pellet.wav",
    "retreating": "sound_effects/retreating.wav",
    "siren_1": "sound_effects/siren_1.wav",
    "siren_2": "sound_effects/siren_2.wav",
    "siren_3": "sound_effects/siren_3.wav",
    "siren_4": "sound_effects/siren_4.wav",
    "siren_5": "sound_effects/siren_5.wav",
}