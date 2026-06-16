import pygame
import sys
import os
from settings import *
from ui.menu_bg import draw_menu_background

FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts", "Rajdhani")

RESOLUTIONS = [
    (800, 600),
    (900, 600),
    (1280, 720),
    (1920, 1080),
]


def _load_fonts():
    bold   = os.path.join(FONTS_DIR, "Rajdhani-Bold.ttf")
    semi   = os.path.join(FONTS_DIR, "Rajdhani-SemiBold.ttf")
    medium = os.path.join(FONTS_DIR, "Rajdhani-Medium.ttf")
    reg    = os.path.join(FONTS_DIR, "Rajdhani-Regular.ttf")
    return {
        "title":   pygame.font.Font(bold,   72),
        "sub":     pygame.font.Font(medium, 16),
        "btn":     pygame.font.Font(semi,   28),
        "btn_sm":  pygame.font.Font(medium, 22),
        "label":   pygame.font.Font(reg,    13),
        "groq":    pygame.font.Font(medium, 14),
    }


def _dark_overlay(surface, alpha=180):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))


def _draw_grid(surface, W, H, alpha=18):
    grid = pygame.Surface((W, H), pygame.SRCALPHA)
    step = 40
    for x in range(0, W, step):
        pygame.draw.line(grid, (255, 255, 255, alpha), (x, 0), (x, H))
    for y in range(0, H, step):
        pygame.draw.line(grid, (255, 255, 255, alpha), (0, y), (W, y))
    surface.blit(grid, (0, 0))


def _draw_button(surface, font, text, rect, hovered, primary=False):
    border_color = RED if hovered and primary else (
        (220, 50, 50, 180) if primary else
        (120, 120, 120) if hovered else (60, 60, 60)
    )
    bg_alpha = 50 if hovered and primary else (30 if hovered else 10)
    bg_color = (220, 50, 50, bg_alpha) if primary else (255, 255, 255, bg_alpha)

    bg = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    bg.fill(bg_color)
    surface.blit(bg, rect.topleft)
    pygame.draw.rect(surface, border_color, rect, 1, border_radius=3)

    # Red left accent on primary button
    if primary:
        pygame.draw.rect(surface, RED, (rect.left, rect.top + 6, 3, rect.height - 12), border_radius=2)

    text_color = WHITE if hovered or primary else (160, 160, 160)
    label = font.render(text, True, text_color)
    surface.blit(label, (rect.centerx - label.get_width() // 2,
                          rect.centery - label.get_height() // 2))


def main_menu(screen, bg):
    fonts = _load_fonts()
    W, H  = screen.get_size()
    cx    = W // 2
    clock = pygame.time.Clock()

    btn_w, btn_h = 280, 50
    bx = cx - btn_w // 2
    title_y = H * 10 // 100
    btn_start = H * 42 // 100
    buttons = [
        ("PLAY",     pygame.Rect(bx, btn_start,        btn_w, btn_h), True),
        ("SETTINGS", pygame.Rect(bx, btn_start + 62,   btn_w, btn_h), False),
        ("CONTROLS", pygame.Rect(bx, btn_start + 124,  btn_w, btn_h), False),
        ("QUIT",     pygame.Rect(bx, btn_start + 186,  btn_w, btn_h), False),
    ]

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        screen.fill((5, 8, 20))
        draw_menu_background(screen, pygame.time.get_ticks())
        _draw_grid(screen, W, H)
        _dark_overlay(screen, 100)

        # Classified label
        classified = fonts["label"].render("— CLASSIFIED OPERATION —", True, (140, 140, 140))
        screen.blit(classified, (cx - classified.get_width() // 2, title_y))

        # Title
        title = fonts["title"].render("RUN & GUN", True, WHITE)
        screen.blit(title, (cx - title.get_width() // 2, title_y + 18))

        # Red underline
        line_w = title.get_width() // 2
        pygame.draw.rect(screen, RED, (cx - line_w // 2, title_y + title.get_height() + 10, line_w, 3), border_radius=2)

        # Subtitle
        sub = fonts["sub"].render("WAVE-BASED  •  AI-GENERATED LEVELS", True, (160, 160, 160))
        screen.blit(sub, (cx - sub.get_width() // 2, title_y + title.get_height() + 20))

        # Divider
        pygame.draw.line(screen, (40, 40, 40), (cx - 140, btn_start - 18), (cx + 140, btn_start - 18), 1)

        # Buttons
        for text, rect, primary in buttons:
            hovered = rect.collidepoint(mx, my)
            font    = fonts["btn"] if primary else fonts["btn_sm"]
            _draw_button(screen, font, text, rect, hovered, primary)

        # Powered by Groq badge
        groq_txt = fonts["groq"].render("POWERED BY", True, (50, 50, 50))
        groq_val = fonts["groq"].render("GROQ", True, (240, 100, 30))
        bx2 = W - 110
        by2 = H - 28
        screen.blit(groq_txt, (bx2, by2))
        screen.blit(groq_val, (bx2 + groq_txt.get_width() + 5, by2))

        # Version
        ver = fonts["label"].render("v1.0 BETA", True, (40, 40, 40))
        screen.blit(ver, (20, H - 24))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buttons[0][1].collidepoint(mx, my): return "play"
                if buttons[1][1].collidepoint(mx, my): return "settings"
                if buttons[2][1].collidepoint(mx, my): return "controls"
                if buttons[3][1].collidepoint(mx, my): pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "play"


def controls_screen(screen, bg):
    fonts = _load_fonts()
    W, H  = screen.get_size()
    cx    = W // 2
    clock = pygame.time.Clock()

    controls = [
        ("W A S D",       "Move player"),
        ("Mouse",         "Aim"),
        ("Left Click",    "Shoot"),
        ("ESC",           "Pause game"),
        ("SPACE",         "Skip wave intro"),
        ("R",             "Restart (game over)"),
    ]

    back_rect = pygame.Rect(cx - 140, H - 80, 280, 46)

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        screen.fill((5, 8, 20))
        draw_menu_background(screen, pygame.time.get_ticks())
        _draw_grid(screen, W, H)
        _dark_overlay(screen, 120)

        title = fonts["btn"].render("CONTROLS", True, WHITE)
        screen.blit(title, (cx - title.get_width() // 2, 60))
        pygame.draw.rect(screen, RED, (cx - 40, 96, 80, 3), border_radius=2)

        for i, (key, action) in enumerate(controls):
            y = 140 + i * 46
            # Key box
            key_surf  = fonts["btn_sm"].render(key, True, WHITE)
            act_surf  = fonts["btn_sm"].render(action, True, (120, 120, 120))
            key_rect  = pygame.Rect(cx - 240, y, 180, 36)
            pygame.draw.rect(screen, (30, 30, 30), key_rect, border_radius=3)
            pygame.draw.rect(screen, (60, 60, 60), key_rect, 1, border_radius=3)
            screen.blit(key_surf, (key_rect.centerx - key_surf.get_width() // 2,
                                   key_rect.centery - key_surf.get_height() // 2))
            screen.blit(act_surf, (cx - 40, y + 8))

        hovered = back_rect.collidepoint(mx, my)
        _draw_button(screen, fonts["btn_sm"], "BACK", back_rect, hovered)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(mx, my): return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return


def settings_menu(screen, bg, current_res):
    fonts = _load_fonts()
    W, H  = screen.get_size()
    cx    = W // 2
    clock = pygame.time.Clock()

    btn_w, btn_h = 280, 46
    buttons = []
    for i, (rw, rh) in enumerate(RESOLUTIONS):
        label = f"{rw} × {rh}" + ("   ✓" if (rw, rh) == current_res else "")
        color = GREEN if (rw, rh) == current_res else None
        buttons.append((label, pygame.Rect(cx - btn_w // 2, H // 3 + i * 58, btn_w, btn_h), (rw, rh), color))

    back_rect = pygame.Rect(cx - btn_w // 2, H // 3 + len(RESOLUTIONS) * 58 + 16, btn_w, btn_h)

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        screen.fill((5, 8, 20))
        draw_menu_background(screen, pygame.time.get_ticks())
        _draw_grid(screen, W, H)
        _dark_overlay(screen, 120)

        title = fonts["btn"].render("SETTINGS", True, WHITE)
        screen.blit(title, (cx - title.get_width() // 2, H // 5))
        pygame.draw.rect(screen, RED, (cx - 40, H // 5 + 38, 80, 3), border_radius=2)

        res_label = fonts["sub"].render("RESOLUTION", True, (80, 80, 80))
        screen.blit(res_label, (cx - res_label.get_width() // 2, H // 3 - 28))

        for label, rect, res, color in buttons:
            hovered  = rect.collidepoint(mx, my)
            is_active = res == current_res
            font     = fonts["btn_sm"]
            _draw_button(screen, font, label, rect, hovered, primary=is_active)

        hovered = back_rect.collidepoint(mx, my)
        _draw_button(screen, fonts["btn_sm"], "BACK", back_rect, hovered)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(mx, my): return current_res
                for _, rect, res, _ in buttons:
                    if rect.collidepoint(mx, my): return res
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return current_res


def pause_menu(screen, bg):
    fonts  = _load_fonts()
    W, H   = screen.get_size()
    cx     = W // 2
    frozen = screen.copy()
    clock  = pygame.time.Clock()

    btn_w, btn_h = 260, 48
    buttons = [
        ("RESUME",   pygame.Rect(cx - btn_w // 2, H // 2 - 20,  btn_w, btn_h), True),
        ("SETTINGS", pygame.Rect(cx - btn_w // 2, H // 2 + 48,  btn_w, btn_h), False),
        ("QUIT",     pygame.Rect(cx - btn_w // 2, H // 2 + 116, btn_w, btn_h), False),
    ]

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        screen.blit(frozen, (0, 0))
        _dark_overlay(screen, 160)
        _draw_grid(screen, W, H, alpha=10)

        title = fonts["title"].render("PAUSED", True, WHITE)
        screen.blit(title, (cx - title.get_width() // 2, H // 3 - 20))
        pygame.draw.rect(screen, RED, (cx - 40, H // 3 + 58, 80, 3), border_radius=2)

        for text, rect, primary in buttons:
            hovered = rect.collidepoint(mx, my)
            font    = fonts["btn"] if primary else fonts["btn_sm"]
            _draw_button(screen, font, text, rect, hovered, primary)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "resume"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buttons[0][1].collidepoint(mx, my): return "resume"
                if buttons[1][1].collidepoint(mx, my): return "settings"
                if buttons[2][1].collidepoint(mx, my): pygame.quit(); sys.exit()