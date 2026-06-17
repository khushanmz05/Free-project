import pygame
import math
import random
from settings import *
from core.bullet import Bullet
from systems.sprite_loader import load_character, rotate_towards
from systems.sprite_loader import load_character, rotate_towards

class BaseEnemy(pygame.sprite.Sprite):
    CHARACTER = "brown"
 
    def __init__(self, x, y, hp, speed, shoot_range, shoot_cd, bullet_dmg, bullet_speed):
        super().__init__()
        self.hp          = hp
        self.speed       = speed
        self.shoot_range = shoot_range
        self.shoot_cd    = shoot_cd
        self.bullet_dmg  = bullet_dmg
        self.bullet_spd  = bullet_speed
        self.last_shot   = 0
        self.pos         = pygame.math.Vector2(x, y)
        self.sprites     = load_character(self.CHARACTER)
        self.image, self.rect = rotate_towards(
            self.sprites["stand"], x, y, x, y + 1)
 
    def update(self, player, walls, bullets_group):
        self._move(player, walls)
        self._try_shoot(player, bullets_group)
        self._update_sprite(player)
 
    def _update_sprite(self, player):
        now      = pygame.time.get_ticks()
        shooting = now - self.last_shot < 300
        pose     = "gun" if shooting else "stand"
        self.image, self.rect = rotate_towards(
            self.sprites[pose],
            int(self.pos.x), int(self.pos.y),
            player.rect.centerx, player.rect.centery)
        self.rect.center = (int(self.pos.x), int(self.pos.y))
 
    def _move(self, player, walls):
        dx   = player.rect.centerx - self.pos.x
        dy   = player.rect.centery - self.pos.y
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
            b = Bullet(int(self.pos.x), int(self.pos.y), dx, dy,
                       color=ORANGE, speed=self.bullet_spd, owner="enemy")
            b.damage = self.bullet_dmg
            bullets_group.add(b)
 
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
 
 
# ---------------------------------------------------------------------------
# Enemy types with wave scaling
# ---------------------------------------------------------------------------
 
def _scale(base, wave, factor=0.12, cap=None):
    val = base * (1 + wave * factor)
    return min(val, cap) if cap else val
 
 
class BasicEnemy(BaseEnemy):
    CHARACTER = "brown"
    def __init__(self, x, y, wave=0):
        super().__init__(x, y,
            hp=int(_scale(30, wave, 0.15)),
            speed=min(_scale(1.8, wave, 0.1), 3.5),
            shoot_range=300, shoot_cd=max(800, 1500 - wave * 80),
            bullet_dmg=10, bullet_speed=6)
 
 
class FastEnemy(BaseEnemy):
    CHARACTER = "blue"
    def __init__(self, x, y, wave=0):
        super().__init__(x, y,
            hp=int(_scale(15, wave, 0.1)),
            speed=min(_scale(3.5, wave, 0.08), 5.5),
            shoot_range=0, shoot_cd=99999,
            bullet_dmg=0, bullet_speed=0)
    def _try_shoot(self, player, bullets_group):
        pass
 
 
class TankEnemy(BaseEnemy):
    CHARACTER = "robot"
    def __init__(self, x, y, wave=0):
        super().__init__(x, y,
            hp=int(_scale(120, wave, 0.2)),
            speed=min(_scale(0.9, wave, 0.06), 2.0),
            shoot_range=250, shoot_cd=max(600, 2000 - wave * 100),
            bullet_dmg=int(_scale(25, wave, 0.1)), bullet_speed=5)
 
 
class RangedEnemy(BaseEnemy):
    CHARACTER = "hitman"
    def __init__(self, x, y, wave=0):
        super().__init__(x, y,
            hp=int(_scale(20, wave, 0.1)),
            speed=min(_scale(1.2, wave, 0.08), 2.5),
            shoot_range=400, shoot_cd=max(400, 800 - wave * 60),
            bullet_dmg=int(_scale(8, wave, 0.1)), bullet_speed=min(_scale(8, wave, 0.08), 14))
 
    def _move(self, player, walls):
        dx   = player.rect.centerx - self.pos.x
        dy   = player.rect.centery - self.pos.y
        dist = math.hypot(dx, dy) or 1
        PREFERRED_DIST = 280
        if dist < PREFERRED_DIST - 40:
            dx, dy = -dx / dist * self.speed, -dy / dist * self.speed
        elif dist > PREFERRED_DIST + 40:
            dx, dy = dx / dist * self.speed, dy / dist * self.speed
        else:
            dx, dy = -dy / dist * self.speed, dx / dist * self.speed
        self._apply_move(dx, dy, walls)
 
 
# ---------------------------------------------------------------------------
# Boss Enemy — wave 6
# ---------------------------------------------------------------------------
 
class BossEnemy(BaseEnemy):
    CHARACTER = "zombie"
    BOSS_HP   = 600
 
    def __init__(self, x, y):
        super().__init__(x, y,
            hp=self.BOSS_HP,
            speed=1.4,
            shoot_range=500,
            shoot_cd=400,
            bullet_dmg=20,
            bullet_speed=7)
        self.phase        = 1
        self.spread_timer = 0
        self.max_hp       = self.BOSS_HP
 
        # Pre-scale all poses once — avoid per-frame scaling
        self._scaled_sprites = {}
        for pose, img in self.sprites.items():
            w, h = img.get_size()
            self._scaled_sprites[pose] = pygame.transform.scale(
                img, (int(w * 1.8), int(h * 1.8)))
 
        self.image = self._scaled_sprites["stand"]
        self.rect  = self.image.get_rect(center=(x, y))
 
    def update(self, player, walls, bullets_group):
        # Update phase
        if self.hp < self.max_hp * 0.5:
            self.phase  = 2
            self.speed  = 2.2
            self.shoot_cd = 250
 
        self._move(player, walls)
        self._boss_shoot(player, bullets_group)
        self._update_sprite(player)
 
    def _boss_shoot(self, player, bullets_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot < self.shoot_cd:
            return
        self.last_shot = now
 
        dx = player.rect.centerx - self.pos.x
        dy = player.rect.centery - self.pos.y
 
        if self.phase == 1:
            # Single accurate shot
            b = Bullet(int(self.pos.x), int(self.pos.y), dx, dy,
                       color=(255, 50, 50), speed=self.bullet_spd, owner="enemy")
            b.damage = self.bullet_dmg
            bullets_group.add(b)
        else:
            # Phase 2: spread shot — 5 bullets in a fan
            base_angle = math.atan2(dy, dx)
            for i in range(5):
                angle  = base_angle + math.radians(-40 + i * 20)
                bdx    = math.cos(angle)
                bdy    = math.sin(angle)
                b = Bullet(int(self.pos.x), int(self.pos.y), bdx, bdy,
                           color=(255, 100, 0), speed=self.bullet_spd + 1, owner="enemy")
                b.damage = 15
                bullets_group.add(b)
 
    def _update_sprite(self, player):
        now      = pygame.time.get_ticks()
        shooting = now - self.last_shot < 300
        pose     = "gun" if shooting else "stand"
        img      = self._scaled_sprites[pose]
        angle    = math.degrees(math.atan2(
            -(player.rect.centery - self.pos.y),
              player.rect.centerx - self.pos.x)) - 90
        from systems.sprite_loader import _cached_rotate
        self.image = _cached_rotate(img, angle)
        self.rect  = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
 
    @property
    def hp_ratio(self):
        return self.hp / self.max_hp
 
 
# ---------------------------------------------------------------------------
# Spawn helpers
# ---------------------------------------------------------------------------
 
def spawn_wave(wave, walls):
    enemies   = pygame.sprite.Group()
    positions = [
        (80, 80), (WIDTH - 80, 80),
        (80, HEIGHT - 80), (WIDTH - 80, HEIGHT - 80),
        (WIDTH // 2, 80), (WIDTH // 2, HEIGHT - 80),
        (80, HEIGHT // 2), (WIDTH - 80, HEIGHT // 2),
        (200, 80), (WIDTH - 200, 80),
        (200, HEIGHT - 80), (WIDTH - 200, HEIGHT - 80),
    ]
    random.shuffle(positions)
    count = 3 + wave * 2
 
    if wave <= 1:
        pool = [BasicEnemy]
    elif wave <= 2:
        pool = [BasicEnemy, BasicEnemy, FastEnemy]
    elif wave <= 3:
        pool = [BasicEnemy, FastEnemy, RangedEnemy]
    else:
        pool = [BasicEnemy, FastEnemy, RangedEnemy, TankEnemy]
 
    spawned = 0
    for x, y in positions:
        if spawned >= min(count, len(positions)):
            break
        e = random.choice(pool)(x, y, wave)
        if not any(e.rect.colliderect(w.rect) for w in walls):
            enemies.add(e)
            spawned += 1
 
    safe_spots = [(80, 80), (WIDTH - 80, 80), (80, HEIGHT - 80), (WIDTH - 80, HEIGHT - 80)]
    while spawned < 3:
        x, y = safe_spots[spawned % len(safe_spots)]
        enemies.add(random.choice(pool)(x, y, wave))
        spawned += 1
 
    return enemies
 
 
def spawn_boss(walls):
    """Spawn the boss at a safe position, avoiding walls."""
    safe_positions = [
        (WIDTH * 3 // 4, HEIGHT // 2),
        (WIDTH - 120, HEIGHT // 2),
        (WIDTH * 3 // 4, HEIGHT // 4),
        (WIDTH * 3 // 4, HEIGHT * 3 // 4),
    ]
    for x, y in safe_positions:
        boss = BossEnemy(x, y)
        if not any(boss.rect.colliderect(w.rect) for w in walls):
            print(f"[BOSS] Spawned at ({x}, {y})")
            group = pygame.sprite.Group()
            group.add(boss)
            return group
    # Fallback — force spawn at centre right regardless
    print("[BOSS] Force spawned at centre right")
    boss = BossEnemy(WIDTH * 3 // 4, HEIGHT // 2)
    group = pygame.sprite.Group()
    group.add(boss)
    return group