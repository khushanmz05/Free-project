import pygame
import math
from settings import *


class ShieldPickup(pygame.sprite.Sprite):
    """Base shield pickup class."""

    def __init__(self, x, y, amount, color, size):
        super().__init__()
        self.amount = amount
        self.size   = size
        self.color  = color

        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        self._draw()
        self.rect = self.image.get_rect(center=(x, y))

        # Bobbing animation
        self._base_y  = float(y)
        self._tick    = 0

    def _draw(self):
        # Outer glow ring
        pygame.draw.circle(self.image, (*self.color, 60),  (self.size, self.size), self.size)
        # Main circle
        pygame.draw.circle(self.image, self.color,          (self.size, self.size), self.size - 4)
        # Inner highlight
        pygame.draw.circle(self.image, WHITE,               (self.size, self.size), self.size - 8, 2)
        # Shield icon — simple "S" shape using lines
        cx, cy = self.size, self.size
        r = self.size - 10
        pygame.draw.arc(self.image, WHITE,
                        (cx - r, cy - r, r * 2, r * 2), math.pi * 0.2, math.pi * 1.0, 2)
        pygame.draw.arc(self.image, WHITE,
                        (cx - r, cy - r, r * 2, r * 2), math.pi * 1.2, math.pi * 2.0, 2)

    def update(self, *args):
        # Gentle bob up and down
        self._tick += 0.05
        self.rect.centery = int(self._base_y + math.sin(self._tick) * 4)


class SmallShield(ShieldPickup):
    """Gives 25 shield. Spawns from wave 2."""
    def __init__(self, x, y):
        super().__init__(x, y, amount=25, color=(0, 220, 220), size=14)  # cyan


class LargeShield(ShieldPickup):
    """Gives 100 shield. Spawns from wave 5."""
    def __init__(self, x, y):
        super().__init__(x, y, amount=100, color=(240, 200, 50), size=20)  # gold


# ---------------------------------------------------------------------------
# Spawn helper
# ---------------------------------------------------------------------------

def spawn_pickups(wave):
    """
    Return a Group of pickups appropriate for the current wave.
    Small shield available from wave 2, large shield from wave 5.
    Positions are spread around the map away from spawn corners.
    """
    pickups = pygame.sprite.Group()

    small_positions = [
        (WIDTH // 2 - 120, HEIGHT // 2),
        (WIDTH // 2 + 120, HEIGHT // 2),
        (WIDTH // 2, HEIGHT // 2 - 120),
        (WIDTH // 2, HEIGHT // 2 + 120),
    ]

    large_positions = [
        (WIDTH // 4, HEIGHT // 4),
        (WIDTH * 3 // 4, HEIGHT * 3 // 4),
    ]

    if wave >= 2:
        for pos in small_positions[:2]:
            pickups.add(SmallShield(*pos))

    if wave >= 5:
        for pos in large_positions[:1]:
            pickups.add(LargeShield(*pos))

    return pickups