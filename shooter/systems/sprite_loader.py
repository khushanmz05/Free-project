import pygame
import math
import os

KENNEY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "assets", "kenney_top-down-shooter", "PNG")

CHARACTER_FOLDERS = {
    "soldier": ("Soldier 1",  "soldier1"),
    "brown":   ("Man Brown",  "manBrown"),
    "blue":    ("Man Blue",   "manBlue"),
    "robot":   ("Robot 1",    "robot1"),
    "hitman":  ("Hitman 1",   "hitman1"),
    "zombie":  ("Zombie 1",   "zoimbie1"),
}

POSES = ["stand", "gun", "hold", "machine", "reload", "silencer"]

_rotation_cache = {}
MAX_CACHE_SIZE  = 512


def load_character(character_key):
    folder_name, prefix = CHARACTER_FOLDERS[character_key]
    folder_path = os.path.join(KENNEY_DIR, folder_name)
    images = {}
    for pose in POSES:
        path = os.path.join(folder_path, f"{prefix}_{pose}.png")
        if os.path.exists(path):
            images[pose] = pygame.image.load(path).convert_alpha()
        else:
            images[pose] = pygame.Surface((64, 64), pygame.SRCALPHA)
    return images


def _cached_rotate(image, angle):
    """Rotate with caching — avoids recalculating identical rotations."""
    key = (id(image), round(angle))
    if key in _rotation_cache:
        return _rotation_cache[key]
    rotated = pygame.transform.rotate(image, angle)
    if len(_rotation_cache) > MAX_CACHE_SIZE:
        _rotation_cache.clear()
    _rotation_cache[key] = rotated
    return rotated


def rotate_to_mouse(image, px, py):
    mx, my  = pygame.mouse.get_pos()
    dx, dy  = mx - px, my - py
    angle   = math.degrees(math.atan2(-dy, dx)) - 90
    rotated = _cached_rotate(image, round(angle))
    rect    = rotated.get_rect(center=(px, py))
    return rotated, rect


def rotate_towards(image, px, py, tx, ty):
    dx, dy  = tx - px, ty - py
    angle   = math.degrees(math.atan2(-dy, dx)) - 90
    rotated = _cached_rotate(image, round(angle))
    rect    = rotated.get_rect(center=(px, py))
    return rotated, rect