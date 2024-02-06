import os
import pygame
from config import ASSET_PATHS, SOUND_EFFECTS_PATHS, MUSIC_PATHS

pygame.mixer.init()


def load_image(name: str, convert_alpha: bool = False) -> pygame.Surface:
    """
    Loads an image from the specified asset name.
    """
    path = ASSET_PATHS[name]
    image = pygame.image.load(path)
    if convert_alpha:
        return image.convert_alpha()
    return image


def load_sound_effect(name: str) -> pygame.mixer.Sound:
    """
    Loads a sound effect from the specified name defined in SOUND_EFFECTS_PATHS.
    """
    path = os.path.join("assets", SOUND_EFFECTS_PATHS[name])
    return pygame.mixer.Sound(path)


def get_music_path(name: str) -> str:
    """
    Returns the full path for a music file given its logical name defined in MUSIC_PATHS.
    """
    return os.path.join("assets", MUSIC_PATHS[name])


def load_ui_images() -> dict:
    """
    Loads and returns a dictionary of UI images using their names defined in ASSET_PATHS.
    """
    ui_image_names = [
        "regenerate_button", "regenerate_button_hover",
        "ghost_button", "ghost_button_hover",
        "blinky_button", "pinky_button", "inky_button", "clyde_button",
        "path_button", "path_button_hover",
        "pathfinder_button", "pathfinder_button_hover",
        "a_star_text", "classic_text",
        "no_dmg_button", "no_dmg_button_hover",
        "on_button", "off_button", "disabled_button",
        "sound_button", "sound_button_hover",
        "sound_on", "sound_off",
        "classic_button", "classic_button_hover",
        "maze_image",
    ]
    return {name: load_image(name, True) for name in ui_image_names}


def initialize_resources() -> dict:
    """
    Loads and initializes all game resources (images, sound effects, etc.).
    """
    images = {name: load_image(name, True) for name in ASSET_PATHS}
    sounds = {name: load_sound_effect(name) for name in SOUND_EFFECTS_PATHS}
    music_paths = {name: get_music_path(name) for name in MUSIC_PATHS}

    return {
        "images": images,
        "sounds": sounds,
        "music_paths": music_paths,
        "ui_images": load_ui_images(),
    }
