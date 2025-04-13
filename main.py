import sys
import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import Shot
import os
import time


HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def show_text(screen, text, size, x_pos, y_offset=0, color="white"):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x_pos, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)

def game_loop(high_score):
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    dt = 0
    score = 0

    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", max(score, high_score)

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                return "game_over", max(score, high_score)

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    score += 1

        screen.fill((46, 52, 64))

        for obj in drawable:
            obj.draw(screen)

        pygame.draw.rect(screen, (67, 76, 89), (0, 0, SCREEN_WIDTH, 50))

        score_surface = font.render(f"SCORE: {score}", True, (191, 97, 106))
        high_surface = font.render(f"HIGH SCORE: {high_score}", True, (255, 203, 107))

        score_y_pos = (50 - score_surface.get_height()) // 2
        high_y_pos = (50 - high_surface.get_height()) // 2

        screen.blit(score_surface, (SCREEN_WIDTH // 4 - score_surface.get_width() // 2, score_y_pos))
        screen.blit(high_surface, (SCREEN_WIDTH * 3 // 4 - high_surface.get_width() // 2, high_y_pos))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 48)

    high_score = load_high_score()

    while True:
        while True:
            screen.fill((46, 52, 64))

            show_text(screen, "ASTEROIDS", 72, SCREEN_WIDTH // 2, y_offset=-80, color=(255, 203, 107))
            show_text(screen, "by: j4ke", 36, SCREEN_WIDTH // 2, y_offset=-20, color=(255, 255, 255))

            if pygame.time.get_ticks() % 1000 < 625:
                show_text(screen, "'ENTER' to start", 32, SCREEN_WIDTH // 2, y_offset=80, color=(191, 97, 106))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_score(high_score)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    break
            else:
                clock.tick(60)
                continue
            break

        result, new_score = game_loop(high_score)
        if new_score > high_score:
            high_score = new_score
            save_high_score(high_score)

        if result == "game_over":
            screen.fill((46, 52, 64))
            show_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, y_offset=0, color=(191, 97, 106))
            pygame.display.flip()
            pygame.time.delay(2000)


if __name__ == "__main__":
    main()