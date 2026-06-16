import pygame
from settings import *
from core.weapons import make_pistol, WEAPON_FACTORIES
from systems.sprite_loader import load_character, rotate_to_mouse


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = load_character("soldier")
        self.pos     = pygame.math.Vector2(x, y)
        self.hp      = PLAYER_MAX_HP
        self.shield  = 0
        self.weapon  = make_pistol()
        self._shooting = False

        # Set initial image
        self.image, self.rect = rotate_to_mouse(
            self.sprites["stand"], int(self.pos.x), int(self.pos.y))

    def _get_pose(self):
        if self._shooting:
            if self.weapon.name == "SMG":      return "machine"
            elif self.weapon.name == "Sniper": return "silencer"
            else:                               return "gun"
        return "hold" if self._moving else "stand"

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1
        if dx and dy:
            dx *= 0.707
            dy *= 0.707
        self._moving = dx != 0 or dy != 0
        return dx * PLAYER_SPEED, dy * PLAYER_SPEED

    def move(self, dx, dy, walls):
        self.pos.x += dx
        self.rect.centerx = int(self.pos.x)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: self.rect.right = wall.rect.left
                else:       self.rect.left  = wall.rect.right
                self.pos.x = self.rect.centerx

        self.pos.y += dy
        self.rect.centery = int(self.pos.y)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0: self.rect.bottom = wall.rect.top
                else:       self.rect.top    = wall.rect.bottom
                self.pos.y = self.rect.centery

        # Clamp away from edges so rotated sprite never clips off screen
        W, H   = pygame.display.get_surface().get_size()
        margin = 60
        self.pos.x = max(margin, min(W - margin, self.pos.x))
        self.pos.y = max(margin, min(H - margin, self.pos.y))
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def try_shoot(self, bullets_group):
        self._shooting = pygame.mouse.get_pressed()[0]
        if self._shooting:
            mx, my = pygame.mouse.get_pos()
            self.weapon.shoot(int(self.pos.x), int(self.pos.y),
                              mx, my, bullets_group)
            if self.weapon.ammo <= 0 and self.weapon.name != "Pistol":
                self.weapon = make_pistol()

    def pickup_weapon(self, weapon_name):
        if self.weapon.name == weapon_name:
            self.weapon.ammo = self.weapon.max_ammo
        else:
            self.weapon = WEAPON_FACTORIES[weapon_name]()

    def take_damage(self, amount):
        if self.shield > 0:
            absorbed    = min(self.shield, amount)
            self.shield -= absorbed
            amount      -= absorbed
        self.hp = max(0, self.hp - amount)

    def draw_marker(self, surface):
        """Draw a green triangle marker above the player."""
        x = int(self.pos.x)
        y = int(self.pos.y) - 50
        points = [(x, y), (x - 12, y + 18), (x + 12, y + 18)]
        pygame.draw.polygon(surface, GREEN, points)
        pygame.draw.polygon(surface, WHITE, points, 2)

    def update(self, walls, bullets_group):
        dx, dy = self.handle_input()
        self.move(dx, dy, walls)
        self.try_shoot(bullets_group)
        pose = self._get_pose()
        self.image, self.rect = rotate_to_mouse(
            self.sprites[pose], int(self.pos.x), int(self.pos.y))
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def draw_marker(self, surface):
        """Draw a green triangle marker above the player."""
        x = int(self.pos.x)
        y = int(self.pos.y) - self.rect.height // 2 - 14
        points = [(x, y), (x - 8, y + 12), (x + 8, y + 12)]
        pygame.draw.polygon(surface, GREEN, points)
        pygame.draw.polygon(surface, WHITE, points, 1)