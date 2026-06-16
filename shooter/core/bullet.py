import pygame
import math
from settings import *

# Pre-render bullet surfaces at startup for performance
_BULLET_CACHE = {}

def _get_bullet_surface(color, size):
    key = (color, size)
    if key not in _BULLET_CACHE:
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (size, size), size)
        _BULLET_CACHE[key] = surf.convert_alpha()
    return _BULLET_CACHE[key]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, color=BULLET_COLOR, speed=BULLET_SPEED, owner="player"):
        super().__init__()
        self.image = _get_bullet_surface(color, BULLET_SIZE)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        length = math.hypot(dx, dy) or 1
        self.vel = pygame.math.Vector2(dx / length * speed, dy / length * speed)
        self.owner = owner
        self.damage = 10
        self._sound_played = False

    def update(self, walls):
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        W, H = pygame.display.get_surface().get_size()
        if not (0 <= self.pos.x <= W and 0 <= self.pos.y <= H):
            self.kill()
            return

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.kill()
                return