import pygame
import math
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, color=BULLET_COLOR, speed=BULLET_SPEED, owner="player"):
        super().__init__()
        self.image = pygame.Surface((BULLET_SIZE * 2, BULLET_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (BULLET_SIZE, BULLET_SIZE), BULLET_SIZE)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        length = math.hypot(dx, dy) or 1
        self.vel = pygame.math.Vector2(dx / length * speed, dy / length * speed)
        self.owner = owner  # "player" or "enemy"

    def update(self, walls):
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Kill if out of screen
        if not (0 <= self.pos.x <= WIDTH and 0 <= self.pos.y <= HEIGHT):
            self.kill()
            return

        # Kill on wall collision
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.kill()
                return