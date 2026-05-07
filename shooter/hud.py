import pygame
from settings import *


class HUD:
    def __init__(self, font):
        self.font = font

    def draw(self, surface, player, score, mission_text=""):
        self._draw_health_bar(surface, player)
        self._draw_shield_bar(surface, player)
        self._draw_score(surface, score)
        if mission_text:
            self._draw_mission(surface, mission_text)

    def _draw_health_bar(self, surface, player):
        bar_w, bar_h = 200, 18
        x, y = 30, HEIGHT - 40
        ratio = max(0, player.hp / PLAYER_MAX_HP)
        pygame.draw.rect(surface, GREY,  (x, y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, GREEN, (x, y, int(bar_w * ratio), bar_h), border_radius=4)
        pygame.draw.rect(surface, WHITE, (x, y, bar_w, bar_h), 2, border_radius=4)
        label = self.font.render(f"HP  {max(0, player.hp)}/{PLAYER_MAX_HP}", True, WHITE)
        surface.blit(label, (x, y - 20))

    def _draw_shield_bar(self, surface, player):
        if not hasattr(player, 'shield') or player.shield <= 0:
            return
        bar_w, bar_h = 200, 14
        x, y = 30, HEIGHT - 70
        # Cap display width at bar_w, but allow shield to exceed 100
        display_ratio = min(1.0, player.shield / 100)
        CYAN = (0, 220, 220)
        GOLD = (240, 200, 50)
        color = GOLD if player.shield > 100 else CYAN
        pygame.draw.rect(surface, GREY,  (x, y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, color, (x, y, int(bar_w * display_ratio), bar_h), border_radius=4)
        pygame.draw.rect(surface, WHITE, (x, y, bar_w, bar_h), 2, border_radius=4)
        label = self.font.render(f"SHIELD  {int(player.shield)}", True, color)
        surface.blit(label, (x, y - 20))

    def _draw_score(self, surface, score):
        txt = self.font.render(f"SCORE  {score}", True, YELLOW)
        surface.blit(txt, (WIDTH - txt.get_width() - 30, HEIGHT - 40))

    def _draw_mission(self, surface, text):
        # Show mission briefing at the top centre, max 80 chars per line
        lines = _wrap(text, 80)
        for i, line in enumerate(lines[:3]):
            surf = self.font.render(line, True, WHITE)
            surface.blit(surf, (WIDTH // 2 - surf.get_width() // 2, 30 + i * 22))


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