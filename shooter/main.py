import sys
import pygame
from settings import *
from core.player import Player
from core.enemy import spawn_wave, spawn_boss, BossEnemy
from core.level import build_level
from core.pickups import spawn_pickups, spawn_health_pickups
from core.weapons import spawn_weapon_pickup
from ui.hud import HUD
from ui.menu import main_menu, settings_menu, pause_menu, controls_screen
from ui.background import load_background
from ui.wave_intro import show_wave_intro
from systems.ai_generator import generate_mission_briefing, generate_level_layout, reset_story
from systems.sounds import SoundManager


def next_wave(wave, screen, bg):
    mission = generate_mission_briefing(wave)
    show_wave_intro(screen, wave, mission, bg)
    if is_boss_wave(wave):
        # Boss wave — use a fixed open arena, no obstacles
        walls          = build_level(_boss_arena())
        enemies        = spawn_boss(walls)
        shield_pickups = pygame.sprite.Group()
        weapon_pickups = pygame.sprite.Group()
        health_pickups = pygame.sprite.Group()
    else:
        layout         = generate_level_layout(wave)
        walls          = build_level(layout)
        enemies        = spawn_wave(wave, walls)
        shield_pickups = spawn_pickups(wave)
        weapon_pickups = spawn_weapon_pickup(wave)
        health_pickups = spawn_health_pickups(wave)
    return walls, enemies, shield_pickups, weapon_pickups, health_pickups, mission
 
 
def _boss_arena():
    """Boss arena — borders + cover only on player's left side."""
    screen = pygame.display.get_surface()
    W, H   = screen.get_size()
    t      = WALL_THICKNESS
    return [
        # Borders
        (0,     0,     W, t),
        (0,     H - t, W, t),
        (0,     0,     t, H),
        (W - t, 0,     t, H),
        # Cover on player side only (left half)
        (200, int(H * 0.20), 80, 55),
        (200, int(H * 0.72), 80, 55),
        (350, int(H * 0.35), 60, 55),
        (350, int(H * 0.57), 60, 55),
    ]
 
 
def draw_boss_bar(screen, boss, font, W, H):
    """Draw boss HP bar at the top centre."""
    bar_w, bar_h = 400, 20
    x = W // 2 - bar_w // 2
    y = 20
    ratio = max(0, boss.hp_ratio)
    color = RED if boss.phase == 1 else ORANGE
    pygame.draw.rect(screen, (80, 0, 0),  (x, y, bar_w, bar_h), border_radius=6)
    pygame.draw.rect(screen, color,        (x, y, int(bar_w * ratio), bar_h), border_radius=6)
    pygame.draw.rect(screen, WHITE,        (x, y, bar_w, bar_h), 2, border_radius=6)
    label = font.render(f"BOSS  {max(0, boss.hp)} / {boss.max_hp}", True, WHITE)
    screen.blit(label, (W // 2 - label.get_width() // 2, y + 26))
    if boss.phase == 2:
        phase = font.render("⚠  PHASE 2", True, ORANGE)
        screen.blit(phase, (W // 2 - phase.get_width() // 2, y + 46))
 
 
def end_screen(screen, font_big, font, score, bg, victory=False, checkpoint=0):
    W, H = screen.get_size()
 
    while True:
        screen.blit(bg, (0, 0))
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))
 
        color = YELLOW if victory else RED
        t1 = font_big.render("VICTORY!" if victory else "GAME OVER", True, color)
        t2 = font.render(f"Final score: {score}", True, WHITE)
        screen.blit(t1, (W // 2 - t1.get_width() // 2, H // 2 - 100))
        screen.blit(t2, (W // 2 - t2.get_width() // 2, H // 2 - 40))
 
        if not victory and checkpoint > 0:
            # Two options
            opt1 = font.render(f"R — Restart from Wave {checkpoint + 1}", True, GREEN)
            opt2 = font.render("N — New game from beginning", True, GREY)
            opt3 = font.render("Q — Quit", True, (100, 100, 100))
            screen.blit(opt1, (W // 2 - opt1.get_width() // 2, H // 2 + 10))
            screen.blit(opt2, (W // 2 - opt2.get_width() // 2, H // 2 + 40))
            screen.blit(opt3, (W // 2 - opt3.get_width() // 2, H // 2 + 70))
        else:
            opt1 = font.render("R — Restart", True, WHITE)
            opt3 = font.render("Q — Quit", True, (100, 100, 100))
            screen.blit(opt1, (W // 2 - opt1.get_width() // 2, H // 2 + 10))
            screen.blit(opt3, (W // 2 - opt3.get_width() // 2, H // 2 + 40))
 
        pygame.display.flip()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return "checkpoint"
                if event.key == pygame.K_n: return "new"
                if event.key == pygame.K_q: pygame.quit(); sys.exit()
 
 
def run_game(screen, bg):
    W, H     = screen.get_size()
    font     = pygame.font.SysFont("monospace", 16, bold=True)
    font_big = pygame.font.SysFont("monospace", 48, bold=True)
    hud      = HUD(font)
    clock    = pygame.time.Clock()
    sfx      = SoundManager()
 
    while True:
        reset_story()
        wave       = 5
        score      = 0
        wave_score = 0
        checkpoint = 5
        player     = Player(150, H // 2)
        bullets    = pygame.sprite.Group()
 
        walls, enemies, shield_pickups, weapon_pickups, health_pickups, mission = next_wave(wave, screen, bg)
 
        restart_from = 0  # wave to restart from if checkpoint used
 
        running = True
        while running:
            clock.tick(FPS)
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    result = pause_menu(screen, bg)
                    if result == "settings":
                        new_res = settings_menu(screen, bg, screen.get_size())
                        if new_res != screen.get_size():
                            return ("settings", new_res)
 
            # --- Update ---
            prev_hp = player.hp
            player.update(walls, bullets)
 
            # Shoot sound — detect new bullets
            if len(bullets) > 0:
                for b in bullets:
                    if getattr(b, '_sound_played', False) is False:
                        sfx.play_shoot(player.weapon.name)
                        b._sound_played = True
                        break
 
            sfx.update(player)
            shield_pickups.update()
            weapon_pickups.update()
            health_pickups.update()
 
            for pickup in list(shield_pickups):
                if player.rect.colliderect(pickup.rect):
                    player.shield += pickup.amount
                    sfx.play("pickup")
                    pickup.kill()
 
            for pickup in list(weapon_pickups):
                if player.rect.colliderect(pickup.rect):
                    player.pickup_weapon(pickup.weapon_name)
                    sfx.play("pickup")
                    pickup.kill()
 
            for pickup in list(health_pickups):
                if player.rect.colliderect(pickup.rect):
                    player.hp = min(PLAYER_MAX_HP, player.hp + pickup.amount)
                    sfx.play("pickup")
                    pickup.kill()
 
            for enemy in list(enemies.sprites()):
                enemy.update(player, walls, bullets)
                if not isinstance(enemy, BossEnemy) and any(enemy.rect.colliderect(w.rect) for w in walls):
                    enemy.kill()
 
            for bullet in list(bullets):
                bullet.update(walls)
                if bullet.owner == "player":
                    for enemy in list(enemies.sprites()):
                        if bullet.rect.colliderect(enemy.rect):
                            enemy.take_damage(getattr(bullet, 'damage', 25))
                            bullet.kill()
                            if not enemy.alive():
                                sfx.play("boss_hit" if isinstance(enemy, BossEnemy) else "death")
                                pts        = 50 if isinstance(enemy, BossEnemy) else 10
                                score      += pts
                                wave_score += pts
                            else:
                                sfx.play("boss_hit" if isinstance(enemy, BossEnemy) else "hit")
                            break
                elif bullet.owner == "enemy":
                    if bullet.rect.colliderect(player.rect):
                        player.take_damage(getattr(bullet, 'damage', 10))
                        bullet.kill()
 
            # --- Boss wave logic ---
            if is_boss_wave(wave):
                boss_list = enemies.sprites()
                if len(boss_list) == 0:
                    # Boss defeated — victory!
                    restart = end_screen(screen, font_big, font, score, bg, victory=True, checkpoint=0)
                    if restart: break
                    else: pygame.quit(); sys.exit()
            else:
                # Respawn enemies if all dead but wave not complete
                if len(enemies.sprites()) == 0 and wave_score < wave_target(wave):
                    new_enemies = spawn_wave(wave, walls)
                    for e in new_enemies:
                        enemies.add(e)
 
                # Point-based wave progression
                if wave_score >= wave_target(wave):
                    wave       += 1
                    wave_score  = 0
                    checkpoint  = wave  # save checkpoint
                    player.hp     = PLAYER_MAX_HP
                    # Give shield on harder waves
                    if wave == 3:
                        player.shield += 25
                    elif wave == 4:
                        player.shield += 50
                    elif wave >= 5:
                        player.shield += 100
                    bullets.empty()
                    walls, enemies, shield_pickups, weapon_pickups, health_pickups, mission = next_wave(wave, screen, bg)
 
            # --- Game over ---
            if player.hp <= 0:
                result = end_screen(screen, font_big, font, score, bg,
                                    victory=False, checkpoint=checkpoint)
                if result == "checkpoint":
                    # Restart from last checkpoint wave
                    wave       = checkpoint
                    wave_score = 0
                    score      = 0
                    player     = Player(150, H // 2)
                    bullets.empty()
                    walls, enemies, shield_pickups, weapon_pickups, health_pickups, mission = next_wave(wave, screen, bg)
                elif result == "new":
                    break  # restart outer loop from wave 0
 
            # --- Draw ---
            screen.blit(bg, (0, 0))
            walls.draw(screen)
            shield_pickups.draw(screen)
            weapon_pickups.draw(screen)
            health_pickups.draw(screen)
            bullets.draw(screen)
            enemies.draw(screen)
            screen.blit(player.image, player.rect)
            player.draw_marker(screen)
            player.draw_marker(screen)
 
            if is_boss_wave(wave) and enemies.sprites():
                draw_boss_bar(screen, enemies.sprites()[0], font, W, H)
                hud.draw(screen, player, score, mission, wave, 0)
            else:
                hud.draw(screen, player, score, mission, wave, wave_score)
 
            pygame.display.flip()
 
    return ("menu", None)
 
 
def main():
    pygame.init()
    current_res = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(current_res, pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption(TITLE)
    bg = load_background(*current_res)
 
    while True:
        action = main_menu(screen, bg)
        if action == "play":
            result = run_game(screen, bg)
            if isinstance(result, tuple) and result[0] == "settings":
                current_res = result[1]
                screen      = pygame.display.set_mode(current_res, pygame.HWSURFACE | pygame.DOUBLEBUF)
                bg          = load_background(*current_res)
        elif action == "controls":
            controls_screen(screen, bg)
        elif action == "settings":
            new_res = settings_menu(screen, bg, current_res)
            if new_res != current_res:
                current_res = new_res
                screen      = pygame.display.set_mode(current_res, pygame.HWSURFACE | pygame.DOUBLEBUF)
                bg          = load_background(*current_res)
 
 
if __name__ == "__main__":
    main()
 