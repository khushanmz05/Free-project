import sys
import pygame
from settings import *
from player import Player
from enemy import spawn_wave
from level import build_level
from hud import HUD
from ai_generator import generate_mission_briefing, generate_level_layout
from pickups import spawn_pickups


def game_over_screen(screen, font_big, font, score):
    screen.fill(DARK_GREY)
    t1 = font_big.render("GAME OVER", True, RED)
    t2 = font.render(f"Final score: {score}", True, WHITE)
    t3 = font.render("Press R to restart or Q to quit", True, GREY)
    screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2))
    screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return True
                if event.key == pygame.K_q: pygame.quit(); sys.exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    font     = pygame.font.SysFont("monospace", 16, bold=True)
    font_big = pygame.font.SysFont("monospace", 48, bold=True)

    hud = HUD(font)

    while True:  # restart loop
        # --- Init game state ---
        wave   = 0
        score  = 0
        player = Player(150, HEIGHT // 2)

        layout  = generate_level_layout(wave)
        walls   = build_level(layout)
        enemies = spawn_wave(wave, walls)
        pickups = spawn_pickups(wave)
        mission = generate_mission_briefing(wave)

        all_sprites = pygame.sprite.Group()
        bullets     = pygame.sprite.Group()
        all_sprites.add(player)
        all_sprites.add(*enemies)

        running = True
        while running:
            clock.tick(FPS)

            # --- Events ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

            # --- Update ---
            player.update(walls, bullets)
            pickups.update()

            for pickup in list(pickups):
                if player.rect.colliderect(pickup.rect):
                    player.shield += pickup.amount
                    pickup.kill()

            for enemy in enemies:
                enemy.update(player, walls, bullets)

            for bullet in list(bullets):
                bullet.update(walls)

                if bullet.owner == "player":
                    for enemy in list(enemies):
                        if bullet.rect.colliderect(enemy.rect):
                            enemy.take_damage(25)
                            bullet.kill()
                            if not enemy.alive():
                                score += 10
                            break

                elif bullet.owner == "enemy":
                    if bullet.rect.colliderect(player.rect):
                        player.take_damage(getattr(bullet, 'damage', 10))
                        bullet.kill()

            # --- Next wave ---
            if len(enemies) == 0:
                wave += 1
                layout  = generate_level_layout(wave)
                walls   = build_level(layout)
                enemies = spawn_wave(wave, walls)
                pickups = spawn_pickups(wave)
                mission = generate_mission_briefing(wave)
                all_sprites.add(*enemies)
                player.hp = min(PLAYER_MAX_HP, player.hp + 20)

            # --- Game over ---
            if player.hp <= 0:
                restart = game_over_screen(screen, font_big, font, score)
                if restart:
                    break  # restart outer loop
                else:
                    pygame.quit(); sys.exit()

            # --- Draw ---
            screen.fill(DARK_GREY)
            walls.draw(screen)
            pickups.draw(screen)
            bullets.draw(screen)
            enemies.draw(screen)
            screen.blit(player.image, player.rect)

            # Wave label
            wave_txt = font.render(f"WAVE  {wave + 1}", True, BLUE)
            screen.blit(wave_txt, (WIDTH // 2 - wave_txt.get_width() // 2, HEIGHT - 40))

            hud.draw(screen, player, score, mission)
            pygame.display.flip()


if __name__ == "__main__":
    main()