import pygame
from settings import *

def show_wave_intro(screen, wave, mission_text, bg):
    """
    Cinematic wave intro card.
    Slides in from top, holds, then fades out.
    """
    W, H = screen.get_size()
    clock = pygame.time.Clock()

    font_wave    = pygame.font.SysFont("monospace", 42, bold=True)
    font_label   = pygame.font.SysFont("monospace", 12, bold=True)
    font_mission = pygame.font.SysFont("monospace", 15)
    font_skip    = pygame.font.SysFont("monospace", 11)

    # Card dimensions — wide and roomy
    CARD_W  = int(W * 0.72)
    CARD_H  = 160
    CARD_X  = W // 2 - CARD_W // 2
    CARD_Y  = H // 2 - CARD_H // 2

    SLIDE_MS = 450
    HOLD_MS  = 2800
    FADE_MS  = 400
    TOTAL_MS = SLIDE_MS + HOLD_MS + FADE_MS

    start         = pygame.time.get_ticks()
    mission_lines = _wrap(mission_text, 58)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        elapsed = pygame.time.get_ticks() - start
        if elapsed >= TOTAL_MS:
            return

        # Animation state
        if elapsed < SLIDE_MS:
            t        = _ease_out(elapsed / SLIDE_MS)
            offset_y = int((1 - t) * (-(CARD_H + 60)))
            alpha    = 255
        elif elapsed < SLIDE_MS + HOLD_MS:
            offset_y = 0
            alpha    = 255
        else:
            t        = (elapsed - SLIDE_MS - HOLD_MS) / FADE_MS
            offset_y = 0
            alpha    = int(255 * (1 - t))

        # Draw game frame behind
        screen.blit(bg, (0, 0))

        # Full screen dark overlay
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Card surface
        card = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
        card.fill((12, 12, 18, 230))

        # Red left accent bar
        pygame.draw.rect(card, RED, (0, 0, 5, CARD_H), border_radius=3)

        # Outer border
        pygame.draw.rect(card, (60, 60, 80), (0, 0, CARD_W, CARD_H), 2, border_radius=6)

        # "MISSION BRIEFING" small label top left
        label = font_label.render("— MISSION BRIEFING", True, (140, 140, 160))
        card.blit(label, (20, 14))

        # Wave number — big
        wave_txt = font_wave.render(f"WAVE  {wave + 1}", True, WHITE)
        card.blit(wave_txt, (20, 30))

        # Horizontal divider
        pygame.draw.line(card, (60, 60, 80), (20, 88), (CARD_W - 20, 88), 1)

        # Mission lines
        for i, line in enumerate(mission_lines[:3]):
            color = (210, 210, 210) if i == 0 else (150, 150, 150)
            surf  = font_mission.render(line, True, color)
            card.blit(surf, (20, 98 + i * 20))

        # Skip hint bottom right
        skip = font_skip.render("SPACE  skip", True, (70, 70, 90))
        card.blit(skip, (CARD_W - skip.get_width() - 14, CARD_H - 16))

        # Apply alpha + blit
        card.set_alpha(alpha)
        screen.blit(card, (CARD_X, CARD_Y + offset_y))

        pygame.display.flip()


def _ease_out(t):
    return 1 - (1 - t) ** 3


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