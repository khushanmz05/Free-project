import pygame
import math
import os
from settings import *

# Paths
KENNEY_PNG  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "assets", "kenney_top-down-shooter", "PNG")
ICONS_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "assets", "kenney_game-icons", "PNG", "White", "2x")
GUNS_DIR    = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "assets", "Guns Update - V1.01", "01 - Individual sprites", "Guns")

ICON_SIZE   = 36  # scaled size for HUD icons
WEAPON_HUD_SCALE = 3

WEAPON_SPRITE_FILES = {
    ".." "Pistol": "Glock - P80 [64x48].png",
    ".." "Shotgun": "Revolver - Colt 45 [64x32].png",
    ".." "SMG": "Submachine - MP5A3 [80x48].png",
    ".." "Sniper": "AK 47 [96x48].png",
}


def _load_icon(filename, size=ICON_SIZE):
    path = os.path.join(ICONS_DIR, filename)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, (size, size))


def _draw_heart(size=22):
    """Draw a pygame heart shape, returns a Surface."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    r = size // 4
    # Two circles for top of heart
    pygame.draw.circle(surf, RED, (size // 4, size // 4), r)
    pygame.draw.circle(surf, RED, (3 * size // 4, size // 4), r)
    # Triangle for bottom
    pygame.draw.polygon(surf, RED, [
        (0, size // 3),
        (size, size // 3),
        (size // 2, size - 2),
    ])
    return surf


class HUD:
    def __init__(self, font):
        self.font  = font
        self.icon_star = _load_icon("star.png")
        self.icon_trophy = _load_icon("trophy.png")
        self.icon_target = _load_icon("target.png")
        self.icon_warning = _load_icon("warning.png", size=20)
        self.icon_heart = _draw_heart(24)
        self.icon_shield = self._make_shield_icon(24)
        self.weapon_imgs = self._load_weapon_imgs()

    def _make_shield_icon(self, size):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pts  = [
            (size // 2, 2),
            (size - 2, size // 4),
            (size - 2, size * 2 // 3),
            (size // 2, size - 2),
            (2, size * 2 // 3),
            (2, size // 4),
        ]
        pygame.draw.polygon(surf, (0, 220, 220), pts)
        pygame.draw.polygon(surf, WHITE, pts, 2)
        return surf

    def _load_weapon_imgs(self):
        imgs = {}
        for name, filename in WEAPON_SPRITE_FILES.items():
            path = os.path.join(GUNS_DIR, filename)
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            # Scale to fixed height of 24px for HUD
            scale = 40 / h
            imgs[name] = pygame.transform.smoothscale(img, (int(w * scale), 40))
        return imgs

    def draw(self, surface, player, score, mission_text="", wave=0, wave_score=0):
        W, H = surface.get_size()
        self._draw_health(surface, player, W, H)
        self._draw_shield(surface, player, W, H)
        self._draw_weapon(surface, player, W, H)
        self._draw_score(surface, score, W, H)
        self._draw_wave_progress(surface, wave, wave_score, W, H)
        if player.hp <= PLAYER_MAX_HP * 0.3:
            self._draw_low_hp_warning(surface, W, H)

    def _draw_health(self, surface, player, W, H):
        x, y = 20, 20
        bar_w, bar_h = 180, 16
        ratio = max(0, player.hp / PLAYER_MAX_HP)

        surface.blit(self.icon_heart, (x, y - 2))
        bx = x + 30
        pygame.draw.rect(surface, (80, 0, 0),(bx, y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, RED, (bx, y, int(bar_w * ratio), bar_h), border_radius=4)
        pygame.draw.rect(surface, WHITE,(bx, y, bar_w, bar_h), 2, border_radius=4)
        label = self.font.render(f"{max(0, player.hp)}/{PLAYER_MAX_HP}", True, WHITE)
        surface.blit(label, (bx + bar_w + 8, y))

    def _draw_shield(self, surface, player, W, H):
        if not hasattr(player, 'shield') or player.shield <= 0:
            return
        x, y     = 20, 48
        bar_w, bar_h = 180, 12
        display_ratio = min(1.0, player.shield / 100)
        CYAN  = (0, 220, 220)
        GOLD  = (240, 200, 50)
        color = GOLD if player.shield > 100 else CYAN

        surface.blit(self.icon_shield, (x, y - 4))
        bx = x + 30
        pygame.draw.rect(surface, (0, 60, 60),  (bx, y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, color, (bx, y, int(bar_w * display_ratio), bar_h), border_radius=4)
        pygame.draw.rect(surface, WHITE, (bx, y, bar_w, bar_h), 2, border_radius=4)
        label = self.font.render(f"{int(player.shield)}", True, color)
        surface.blit(label, (bx + bar_w + 8, y - 2))

    def _draw_weapon(self, surface, player, W, H):
        w = player.weapon
        ammo_str = "INF" if w.ammo >= 999 else str(w.ammo)
        color = w.color if hasattr(w, 'color') else WHITE

        weapon_img = self.weapon_imgs.get(w.name)
        target_icon = self.icon_target

        # Weapon block — bottom LEFT
        x = 20
        y = H - 70

        name_txt = self.font.render(w.name.upper(), True, color)
        surface.blit(name_txt, (x, y))

        sx = x
        y += 22
        if weapon_img:
            surface.blit(weapon_img, (sx, y))
            sx += weapon_img.get_width() + 10

        surface.blit(target_icon, (sx, y + 2))
        sx += target_icon.get_width() + 6
        ammo_txt = self.font.render(ammo_str, True, color)
        surface.blit(ammo_txt, (sx, y + 10))

    def _draw_score(self, surface, score, W, H):
        star = self.icon_star
        txt = self.font.render(str(score), True, YELLOW)
        total = star.get_width() + 6 + txt.get_width()
        x = W - total - 20
        y = 20
        surface.blit(star, (x, y - 2))
        surface.blit(txt,  (x + star.get_width() + 6, y))

    def _draw_wave_progress(self, surface, wave, wave_score, W, H):
        from settings import wave_target, is_boss_wave
        if is_boss_wave(wave):
            return  # boss bar is drawn separately
        target = wave_target(wave)
        ratio = min(1.0, wave_score / max(1, target))
        bar_w = 220
        bar_h = 12
        x = W // 2 - bar_w // 2
        y = H - 30

        pygame.draw.rect(surface, GREY,  (x, y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, BLUE,  (x, y, int(bar_w * ratio), bar_h), border_radius=4)
        pygame.draw.rect(surface, WHITE, (x, y, bar_w, bar_h), 2, border_radius=4)

        label = self.font.render(f"WAVE {wave + 1}   {wave_score} / {target}", True, WHITE)
        surface.blit(label, (W // 2 - label.get_width() // 2, y - 22))

    def _draw_low_hp_warning(self, surface, W, H):
        # Pulsing red border
        alpha = int(100 + 80 * math.sin(pygame.time.get_ticks() / 200))
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        border = 18
        for i in range(border):
            a = max(0, alpha - i * 6)
            pygame.draw.rect(overlay, (220, 0, 0, a),
                             (i, i, W - i * 2, H - i * 2), 1)
        surface.blit(overlay, (0, 0))
        # Warning icon + text
        surface.blit(self.icon_warning, (W // 2 - 60, 8))
        warn = self.font.render("LOW HP", True, RED)
        surface.blit(warn, (W // 2 - 20, 12))

    def _draw_mission(self, surface, text, W, H):
        lines = _wrap(text, 80)
        for i, line in enumerate(lines[:3]):
            surf = self.font.render(line, True, WHITE)
            surface.blit(surf, (W // 2 - surf.get_width() // 2, 30 + i * 22))


def _wrap(text, limit):
    words = text.split()
    lines, current = [], ""
    for w in words:
        if len(current) + len(w) + 1 <= limit:
            current += (" " if current else "") + w
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines