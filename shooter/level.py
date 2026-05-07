import pygame
from settings import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))


def build_level(layout=None):
    """
    Returns a list of Wall sprites.
    layout: list of (x, y, w, h) tuples.
    If None, a default hardcoded arena is used.
    """
    walls = pygame.sprite.Group()

    if layout is None:
        layout = default_layout()

    for (x, y, w, h) in layout:
        walls.add(Wall(x, y, w, h))

    return walls


def default_layout():
    t = WALL_THICKNESS
    W, H = WIDTH, HEIGHT
    return [
        # Border walls
        (0,       0,       W,  t),   # top
        (0,       H - t,   W,  t),   # bottom
        (0,       0,       t,  H),   # left
        (W - t,   0,       t,  H),   # right

        # Inner obstacles
        (150, 150, 20, 120),
        (150, 150, 120, 20),
        (W - 170, 150, 20, 120),
        (W - 270, 150, 120, 20),
        (150, H - 270, 20, 120),
        (150, H - 170, 120, 20),
        (W - 170, H - 270, 20, 120),
        (W - 270, H - 170, 120, 20),
        (W // 2 - 50, H // 2 - 60, 100, 20),
        (W // 2 - 50, H // 2 + 40, 100, 20),
        (W // 2 - 60, H // 2 - 40, 20, 80),
        (W // 2 + 40, H // 2 - 40, 20, 80),
    ]