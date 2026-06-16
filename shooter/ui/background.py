import pygame
import os

TILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "assets", "kenney_top-down-shooter", "PNG", "Tiles", "tile_14.png")
TILE_SIZE = 64


def load_background(width, height):
    """
    Returns a surface filled with tiled floor texture.
    Pre-rendered once per resolution change for performance.
    """
    tile = pygame.image.load(TILE_PATH).convert()
    surface = pygame.Surface((width, height))
    for y in range(0, height, TILE_SIZE):
        for x in range(0, width, TILE_SIZE):
            surface.blit(tile, (x, y))
    return surface