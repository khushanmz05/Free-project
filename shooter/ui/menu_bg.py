import pygame
import math
import random


def draw_menu_background(surface, tick):
    """
    Draws an animated scrolling battlefield silhouette.
    Call every frame with pygame.time.get_ticks() as tick.
    """
    W, H = surface.get_size()

    # Sky gradient — dark blue to near black
    for y in range(H):
        ratio = y / H
        r = int(5  + ratio * 8)
        g = int(8  + ratio * 5)
        b = int(20 + ratio * 10)
        pygame.draw.line(surface, (r, g, b), (0, y), (W, y))

    # Stars — static dots in upper half
    rng = random.Random(42)
    for _ in range(120):
        sx = rng.randint(0, W)
        sy = rng.randint(0, H // 2)
        brightness = rng.randint(80, 200)
        twinkle = int(brightness * (0.7 + 0.3 * math.sin(tick / 600 + sx)))
        pygame.draw.circle(surface, (twinkle, twinkle, twinkle), (sx, sy), 1)

    # Moon
    pygame.draw.circle(surface, (200, 200, 180), (W - 100, 70), 28)
    pygame.draw.circle(surface, (5, 8, 20), (W - 88, 62), 22)  # crescent shadow

    # Fog layer at horizon
    fog_y = int(H * 0.55)
    fog   = pygame.Surface((W, 60), pygame.SRCALPHA)
    for i in range(60):
        alpha = int(30 * (1 - i / 60))
        pygame.draw.line(fog, (150, 160, 180, alpha), (0, i), (W, i))
    surface.blit(fog, (0, fog_y))

    # Far city layer — slow scroll
    scroll1 = (tick // 8) % W
    _draw_city_layer(surface, W, H,
                     scroll=scroll1,
                     base_y=int(H * 0.55),
                     color=(25, 28, 45),
                     min_h=60, max_h=160,
                     min_w=40, max_w=100,
                     seed=1, windows=True, window_color=(60, 70, 100))

    # Mid city layer — medium scroll
    scroll2 = (tick // 4) % W
    _draw_city_layer(surface, W, H,
                     scroll=scroll2,
                     base_y=int(H * 0.65),
                     color=(15, 18, 30),
                     min_h=40, max_h=110,
                     min_w=25, max_w=70,
                     seed=2, windows=True, window_color=(80, 90, 50))

    # Near rubble/foreground — fast scroll
    scroll3 = (tick // 2) % W
    _draw_rubble_layer(surface, W, H, scroll3)

    # Ground fill
    pygame.draw.rect(surface, (10, 12, 20), (0, H - 30, W, 30))

    # Subtle red glow on horizon (fire effect)
    glow = pygame.Surface((W, 80), pygame.SRCALPHA)
    for i in range(80):
        alpha = int(18 * math.sin(math.pi * i / 80) *
                    (0.6 + 0.4 * math.sin(tick / 400)))
        pygame.draw.line(glow, (180, 40, 0, alpha), (0, i), (W, i))
    surface.blit(glow, (0, int(H * 0.58)))


def _draw_city_layer(surface, W, H, scroll, base_y, color,
                     min_h, max_h, min_w, max_w, seed,
                     windows=False, window_color=(80, 80, 50)):
    rng     = random.Random(seed)
    x       = -scroll
    while x < W + max_w:
        bw = rng.randint(min_w, max_w)
        bh = rng.randint(min_h, max_h)
        by = base_y - bh
        pygame.draw.rect(surface, color, (int(x), by, bw, bh + (H - base_y)))

        if windows:
            wr, wc = 6, 4
            for row in range(int(bh / (wr + 4))):
                for col in range(int(bw / (wc + 6))):
                    wx = int(x) + 6 + col * (wc + 6)
                    wy = by + 8 + row * (wr + 5)
                    if rng.random() > 0.4:
                        lit = rng.random() > 0.3
                        wcolor = window_color if lit else (20, 20, 30)
                        pygame.draw.rect(surface, wcolor, (wx, wy, wc, wr))

        x += bw + rng.randint(2, 12)


def _draw_rubble_layer(surface, W, H, scroll):
    rng   = random.Random(99)
    color = (8, 10, 16)
    x     = -scroll
    base  = H - 30
    while x < W + 80:
        # Irregular rubble chunks
        points = []
        chunk_w = rng.randint(20, 60)
        for i in range(5):
            px = int(x) + int(chunk_w * i / 4)
            py = base - rng.randint(5, 35)
            points.append((px, py))
        points.append((int(x) + chunk_w, base))
        points.append((int(x), base))
        if len(points) >= 3:
            pygame.draw.polygon(surface, color, points)
        x += chunk_w + rng.randint(0, 20)