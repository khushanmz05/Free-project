import pygame
import math
import random
from settings import *
from bullet import Bullet


class BaseEnemy(pygame.sprite.Sprite):
    """Base class — all enemy types inherit from this."""

    def __init__(self, x, y, hp, speed, size, color, shoot_range, shoot_cd, bullet_dmg, bullet_speed):
        super().__init__()
        self.hp          = hp
        self.speed       = speed
        self.size        = size
        self.color       = color
        self.shoot_range = shoot_range
        self.shoot_cd    = shoot_cd
        self.bullet_dmg  = bullet_dmg
        self.bullet_spd  = bullet_speed
        self.last_shot   = 0

        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        self._draw()
        self.rect = self.image.get_rect(center=(x, y))
        self.pos  = pygame.math.Vector2(x, y)

    def _draw(self):
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)

    def update(self, player, walls, bullets_group):
        self._move(player, walls)
        self._try_shoot(player, bullets_group)

    def _move(self, player, walls):
        dx = player.rect.centerx - self.pos.x
        dy = player.rect.centery - self.pos.y
        dist = math.hypot(dx, dy) or 1
        dx, dy = dx / dist * self.speed, dy / dist * self.speed
        self._apply_move(dx, dy, walls)

    def _apply_move(self, dx, dy, walls):
        self.pos.x += dx
        self.rect.centerx = int(self.pos.x)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: self.rect.right  = wall.rect.left
                else:       self.rect.left   = wall.rect.right
                self.pos.x = self.rect.centerx

        self.pos.y += dy
        self.rect.centery = int(self.pos.y)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0: self.rect.bottom = wall.rect.top
                else:       self.rect.top    = wall.rect.bottom
                self.pos.y = self.rect.centery

    def _try_shoot(self, player, bullets_group):
        now = pygame.time.get_ticks()
        dx  = player.rect.centerx - self.pos.x
        dy  = player.rect.centery - self.pos.y
        if math.hypot(dx, dy) < self.shoot_range and now - self.last_shot > self.shoot_cd:
            self.last_shot = now
            b = Bullet(self.rect.centerx, self.rect.centery, dx, dy,
                       color=ORANGE, speed=self.bullet_spd, owner="enemy")
            b.damage = self.bullet_dmg
            bullets_group.add(b)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()


# ---------------------------------------------------------------------------
# Enemy Types
# ---------------------------------------------------------------------------

class BasicEnemy(BaseEnemy):
    """Balanced — chases and shoots. The standard threat."""
    LABEL = "BASIC"

    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=30, speed=1.8, size=18,
            color=RED,
            shoot_range=300, shoot_cd=1500,
            bullet_dmg=10, bullet_speed=6
        )
        # Red circle with dark outline
        pygame.draw.circle(self.image, (140, 0, 0), (self.size, self.size), self.size, 3)


class FastEnemy(BaseEnemy):
    """Fast and aggressive — low HP, no shooting, rushes the player."""
    LABEL = "FAST"

    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=15, speed=3.5, size=13,
            color=(255, 140, 0),   # orange
            shoot_range=0,         # never shoots
            shoot_cd=99999,
            bullet_dmg=15, bullet_speed=0
        )
        # Small triangle indicator
        pygame.draw.polygon(self.image, WHITE, [
            (self.size, 4),
            (self.size - 5, self.size + 4),
            (self.size + 5, self.size + 4)
        ])

    def _try_shoot(self, player, bullets_group):
        pass  # Fast enemy never shoots


class TankEnemy(BaseEnemy):
    """Slow and tough — high HP, high damage, hard to kill."""
    LABEL = "TANK"

    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=120, speed=0.9, size=26,
            color=(100, 60, 180),  # purple
            shoot_range=250, shoot_cd=2000,
            bullet_dmg=25, bullet_speed=5
        )
        # Heavy outer ring
        pygame.draw.circle(self.image, (60, 20, 120), (self.size, self.size), self.size, 5)


class RangedEnemy(BaseEnemy):
    """Keeps distance — fragile but shoots fast and accurately."""
    LABEL = "RANGED"

    def __init__(self, x, y):
        super().__init__(
            x, y,
            hp=20, speed=1.2, size=15,
            color=(0, 200, 220),   # cyan
            shoot_range=400, shoot_cd=800,
            bullet_dmg=8, bullet_speed=8
        )
        # Cross/scope indicator
        pygame.draw.line(self.image, WHITE, (self.size, 4), (self.size, self.size * 2 - 4), 2)
        pygame.draw.line(self.image, WHITE, (4, self.size), (self.size * 2 - 4, self.size), 2)

    def _move(self, player, walls):
        """Ranged enemy tries to keep a comfortable distance."""
        dx = player.rect.centerx - self.pos.x
        dy = player.rect.centery - self.pos.y
        dist = math.hypot(dx, dy) or 1

        PREFERRED_DIST = 280

        if dist < PREFERRED_DIST - 40:
            # Too close — back away
            dx, dy = -dx / dist * self.speed, -dy / dist * self.speed
        elif dist > PREFERRED_DIST + 40:
            # Too far — move closer
            dx, dy = dx / dist * self.speed, dy / dist * self.speed
        else:
            # In sweet spot — strafe sideways
            dx, dy = -dy / dist * self.speed, dx / dist * self.speed

        self._apply_move(dx, dy, walls)


# ---------------------------------------------------------------------------
# Spawn helper
# ---------------------------------------------------------------------------

ENEMY_TYPES = [BasicEnemy, FastEnemy, TankEnemy, RangedEnemy]

def spawn_wave(wave, walls):
    """
    Spawn a mixed group of enemies scaled to the wave number.
    Early waves are mostly basic; later waves mix in tougher types.
    """
    enemies = pygame.sprite.Group()

    positions = [
        (80, 80), (WIDTH - 80, 80),
        (80, HEIGHT - 80), (WIDTH - 80, HEIGHT - 80),
        (WIDTH // 2, 80), (WIDTH // 2, HEIGHT - 80),
        (80, HEIGHT // 2), (WIDTH - 80, HEIGHT // 2),
        (200, 80), (WIDTH - 200, 80),
    ]
    random.shuffle(positions)

    count = 3 + wave * 2

    for i in range(min(count, len(positions))):
        x, y = positions[i]

        # Wave 1-2: only basic
        # Wave 3+: mix in fast
        # Wave 5+: mix in ranged
        # Wave 7+: mix in tanks
        if wave <= 1:
            pool = [BasicEnemy]
        elif wave <= 2:
            pool = [BasicEnemy, BasicEnemy, FastEnemy]
        elif wave <= 4:
            pool = [BasicEnemy, FastEnemy, RangedEnemy]
        else:
            pool = [BasicEnemy, FastEnemy, RangedEnemy, TankEnemy]

        EnemyClass = random.choice(pool)
        enemies.add(EnemyClass(x, y))

    return enemies