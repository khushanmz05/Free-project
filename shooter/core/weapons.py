import pygame
import os
import math
import random
from settings import *
from core.bullet import Bullet

class Weapon:
    """Base weapon class."""

    def __init__(self, name, damage, fire_rate, bullet_speed, ammo, spread, bullets_per_shot, color):
        self.name            = name
        self.damage          = damage
        self.fire_rate       = fire_rate       # ms between shots
        self.bullet_speed    = bullet_speed
        self.ammo            = ammo
        self.max_ammo        = ammo
        self.spread          = spread          # degrees of random spread
        self.bullets_per_shot = bullets_per_shot
        self.color           = color
        self.last_shot       = 0

    def can_shoot(self):
        return self.ammo > 0 and pygame.time.get_ticks() - self.last_shot > self.fire_rate

    def shoot(self, x, y, tx, ty, bullets_group):
        if not self.can_shoot():
            return False

        self.last_shot = pygame.time.get_ticks()
        self.ammo -= 1

        base_angle = math.atan2(ty - y, tx - x)

        for _ in range(self.bullets_per_shot):
            angle = base_angle + math.radians(random.uniform(-self.spread / 2, self.spread / 2))
            dx = math.cos(angle)
            dy = math.sin(angle)
            b = Bullet(x, y, dx, dy, color=self.color,
                       speed=self.bullet_speed, owner="player")
            b.damage = self.damage
            bullets_group.add(b)

        return True


# ---------------------------------------------------------------------------
# Weapon definitions
# ---------------------------------------------------------------------------

def make_pistol():
    return Weapon(
        name="Pistol",
        damage=25,
        fire_rate=300,
        bullet_speed=10,
        ammo=999,          # effectively infinite
        spread=2,
        bullets_per_shot=1,
        color=YELLOW
    )

def make_shotgun():
    return Weapon(
        name="Shotgun",
        damage=15,
        fire_rate=800,
        bullet_speed=9,
        ammo=20,
        spread=25,
        bullets_per_shot=6,
        color=(255, 120, 50)
    )

def make_smg():
    return Weapon(
        name="SMG",
        damage=10,
        fire_rate=100,
        bullet_speed=11,
        ammo=60,
        spread=8,
        bullets_per_shot=1,
        color=(100, 220, 255)
    )

def make_sniper():
    return Weapon(
        name="Sniper",
        damage=80,
        fire_rate=1200,
        bullet_speed=20,
        ammo=10,
        spread=0,
        bullets_per_shot=1,
        color=(255, 255, 255)
    )


WEAPON_FACTORIES = {
    "Shotgun": make_shotgun,
    "SMG":     make_smg,
    "Sniper":  make_sniper,
}


# ---------------------------------------------------------------------------
# Weapon pickup sprite
# ---------------------------------------------------------------------------

# Map weapon names to their sprite paths and sizes
GUNS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "assets", "Guns Update - V1.01", "01 - Individual sprites", "Guns")

WEAPON_SPRITE_FILES = {
    "Pistol":  "Glock - P80 [64x48].png",
    "Shotgun": "Revolver - Colt 45 [64x32].png",
    "SMG":     "Submachine - MP5A3 [80x48].png",
    "Sniper":  "AK 47 [96x48].png",
}

WEAPON_COLORS = {
    "Pistol":  YELLOW,
    "Shotgun": (255, 120, 50),
    "SMG":     (100, 220, 255),
    "Sniper":  (220, 220, 220),
}

PICKUP_SCALE = 1  # sprites are already a good size


class WeaponPickup(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_name):
        super().__init__()
        self.weapon_name = weapon_name
        color = WEAPON_COLORS.get(weapon_name, WHITE)

        # Load and scale the actual weapon sprite
        filename   = WEAPON_SPRITE_FILES.get(weapon_name, "Glock - P80 [64x48].png")
        path       = os.path.join(GUNS_DIR, filename)
        raw        = pygame.image.load(path).convert_alpha()
        rw, rh     = raw.get_size()
        weapon_img = pygame.transform.scale(raw, (rw * PICKUP_SCALE, rh * PICKUP_SCALE))
        iw, ih   = weapon_img.get_size()

        # Pad with a glowing circle background
        pad      = 6
        size     = max(iw, ih) // 2 + pad
        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (*color, 60), (size, size), size)
        pygame.draw.circle(self.image, (*color, 160), (size, size), size - 4)
        pygame.draw.circle(self.image, WHITE, (size, size), size, 2)
        # Blit weapon sprite centred
        self.image.blit(weapon_img, (size - iw // 2, size - ih // 2))

        self.rect    = self.image.get_rect(center=(x, y))
        self._base_y = float(y)
        self._tick   = 0

    def update(self, *args):
        self._tick += 0.05
        self.rect.centery = int(self._base_y + math.sin(self._tick) * 4)


def spawn_weapon_pickup(wave):
    """Spawn one random weapon pickup per wave."""
    pickups = pygame.sprite.Group()

    candidates = ["Shotgun", "SMG"]
    if wave >= 3:
        candidates.append("Sniper")

    name = random.choice(candidates)

    # Place near centre but offset
    positions = [
        (WIDTH // 2 - 200, HEIGHT // 3),
        (WIDTH // 2 + 200, HEIGHT // 3),
        (WIDTH // 2, HEIGHT * 2 // 3),
    ]
    x, y = random.choice(positions)
    pickups.add(WeaponPickup(x, y, name))
    return pickups