import pygame
import math
from settings import *
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE * 2, PLAYER_SIZE * 2), pygame.SRCALPHA)
        self._draw_sprite()
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.hp = PLAYER_MAX_HP
        self.shield = 0
        self.last_shot = 0

    def _draw_sprite(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, PLAYER_COLOR, (PLAYER_SIZE, PLAYER_SIZE), PLAYER_SIZE)
        # little direction indicator
        pygame.draw.circle(self.image, WHITE, (PLAYER_SIZE + 8, PLAYER_SIZE), 4)

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
        return dx * PLAYER_SPEED, dy * PLAYER_SPEED

    def move(self, dx, dy, walls):
        # X axis
        self.pos.x += dx
        self.rect.centerx = int(self.pos.x)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: self.rect.right  = wall.rect.left
                else:       self.rect.left   = wall.rect.right
                self.pos.x = self.rect.centerx

        # Y axis
        self.pos.y += dy
        self.rect.centery = int(self.pos.y)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0: self.rect.bottom = wall.rect.top
                else:       self.rect.top    = wall.rect.bottom
                self.pos.y = self.rect.centery

    def try_shoot(self, bullets_group):
        now = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] and now - self.last_shot > SHOOT_COOLDOWN:
            self.last_shot = now
            mx, my = pygame.mouse.get_pos()
            dx = mx - self.rect.centerx
            dy = my - self.rect.centery
            b = Bullet(self.rect.centerx, self.rect.centery, dx, dy,
                       color=BULLET_COLOR, speed=BULLET_SPEED, owner="player")
            bullets_group.add(b)

    def take_damage(self, amount):
        if self.shield > 0:
            absorbed = min(self.shield, amount)
            self.shield -= absorbed
            amount -= absorbed
        self.hp = max(0, self.hp - amount)

    def update(self, walls, bullets_group):
        dx, dy = self.handle_input()
        self.move(dx, dy, walls)
        self.try_shoot(bullets_group)