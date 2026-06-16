import pygame
from settings import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((max(1, w), max(1, h)))
        self.image.fill(WALL_COLOR)
        self.rect  = self.image.get_rect(topleft=(x, y))


def build_level(layout=None):
    """
    Returns a Group of Wall sprites.
    If layout is None, uses default_layout scaled to current resolution.
    If layout is provided (from AI), it's already in screen coordinates.
    """
    walls  = pygame.sprite.Group()
    screen = pygame.display.get_surface()
    W, H   = screen.get_size()

    if layout is None:
        layout = _scale_default_layout(W, H)

    for (x, y, w, h) in layout:
        walls.add(Wall(int(x), int(y), max(1, int(w)), max(1, int(h))))

    return walls


def _scale_default_layout(W, H):
    """Default layout scaled to any resolution."""
    t = WALL_THICKNESS
    return [
        # Borders
        (0,0,W,t),
        (0,H - t, W, t),
        (0,0,t,H),
        (W - t,0, t, H),
        # Inner obstacles
        (W*0.16, H*0.25, 20, H*0.20),
        (W*0.16, H*0.25, W*0.13, 20),
        (W*0.78, H*0.25, 20, H*0.20),
        (W*0.65, H*0.25, W*0.13, 20),
        (W*0.16, H*0.55, 20, H*0.20),
        (W*0.16, H*0.72, W*0.13, 20),
        (W*0.78, H*0.55, 20, H*0.20),
        (W*0.65, H*0.72, W*0.13, 20),
        (W*0.44, H*0.40, W*0.11, 20),
        (W*0.44, H*0.57, W*0.11, 20),
        (W*0.43, H*0.43, 20, H*0.13),
        (W*0.55, H*0.43, 20, H*0.13),
    ]