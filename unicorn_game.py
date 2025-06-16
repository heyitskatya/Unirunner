import pygame
import random
import sys

# Ініціалізація
pygame.init()

# Розміри вікна
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Unirunner")

# Фон
try:
    background_img = pygame.image.load("background.jpeg").convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
except:
    background_img = pygame.Surface((WIDTH, HEIGHT))
    background_img.fill((135, 206, 235))  # Небо

# Завантаження єдинорога
try:
    unicorn_img = pygame.image.load("pixel.unicorn.png").convert_alpha()
except:
    unicorn_img = pygame.Surface((80, 80))
    unicorn_img.fill((255, 0, 255))

unicorn_img = pygame.transform.scale(unicorn_img, (80, 80))

# Параметри єдинорога
unicorn_x = 100
ground_y = HEIGHT - 100
unicorn_y = ground_y
unicorn_y_velocity = 0
gravity = 0.7
jump_power = -12
super_jump_power = -20
jump_pressed = False
jump_combo_timer = 0
jump_combo_window = 300  # ms

# Перешкоди
obstacle_speed = 7
obstacle_width = 30
obstacle_height = 30
obstacles = []
try:
    obstacle_img = pygame.image.load("poop.png").convert_alpha()
    obstacle_img = pygame.transform.scale(obstacle_img, (30, 30))
except:
    obstacle_img = None

# Шрифти
font = pygame.font.SysFont("Arial", 30)
title_font = pygame.font.SysFont("Arial", 60, bold=True)

# Час і очки
clock = pygame.time.Clock()
score = 0
level = 1
obstacle_timer = 0
obstacle_delay = 2000

bg_x = 0

# Стан стрибка
is_jumping = False
jump_time = 0
combo_window = 300


def draw_text_with_border(text, font, color, border_color, x, y):
    surface = font.render(text, True, border_color)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        screen.blit(surface, (x + dx, y + dy))
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def reset_game():
    global unicorn_y, unicorn_y_velocity, obstacles, score, bg_x, level
    unicorn_y = ground_y
    unicorn_y_velocity = 0
    obstacles = []
    score = 0
    bg_x = 0
    level = 1


def game_loop():
    global unicorn_y, unicorn_y_velocity, score, bg_x, jump_combo_timer, jump_pressed, is_jumping, jump_time, level, obstacle_timer
    running = True
    lost = False

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not jump_pressed:
                now = pygame.time.get_ticks()
                if not is_jumping:
                    unicorn_y_velocity = jump_power
                    is_jumping = True
                    jump_time = now
                elif now - jump_time < combo_window:
                    unicorn_y_velocity = super_jump_power
                jump_pressed = True
        else:
            jump_pressed = False

        # Рух фону
        bg_x -= 2 + level
        if bg_x <= -WIDTH:
            bg_x = 0
        screen.blit(background_img, (bg_x, 0))
        screen.blit(background_img, (bg_x + WIDTH, 0))

        # Фізика
        unicorn_y_velocity += gravity
        unicorn_y += unicorn_y_velocity
        if unicorn_y >= ground_y:
            unicorn_y = ground_y
            unicorn_y_velocity = 0
            is_jumping = False

        # Рівні
        if score // 100 > level - 1:
            level += 1
            print(f"Новий рівень: {level}")

        # Перешкоди
        obstacle_timer += dt
        if obstacle_timer > obstacle_delay:
            obstacle_timer = 0
            obstacles.append(pygame.Rect(WIDTH, ground_y + 50, 30, 30))

        for obs in obstacles[:]:
            obs.x -= 6 + level
            if obs.x < -30:
                obstacles.remove(obs)
            if obs.colliderect(pygame.Rect(unicorn_x, unicorn_y, 80, 80)):
                lost = True
                running = False

        # Очки
        score += 1

        # Рисування
        screen.blit(unicorn_img, (unicorn_x, unicorn_y))
        for obs in obstacles:
            if obstacle_img:
                screen.blit(obstacle_img, obs.topleft)
            else:
                pygame.draw.rect(screen, (139, 69, 19), obs)

        pygame.draw.line(screen, (0, 155, 0), (0, ground_y + 80), (WIDTH, ground_y + 80), 4)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH - 160, 20))

        pygame.display.flip()

    if lost:
        game_over()


def game_over():
    screen.fill((139, 69, 19))
    draw_text_with_border("Play Again", title_font, (255, 255, 255), (0, 0, 0), WIDTH // 2 - 150, HEIGHT // 2 - 30)
    pygame.display.flip()
    pygame.time.wait(1000)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    reset_game()
                    game_loop()


def start_screen():
    screen.blit(background_img, (0, 0))
    draw_text_with_border("Unirunner", title_font, (255, 255, 255), (0, 0, 0), WIDTH // 2 - 150, HEIGHT // 2 - 100)
    draw_text_with_border("Start", font, (255, 255, 255), (0, 0, 0), WIDTH // 2 - 40, HEIGHT // 2 - 30)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


reset_game()
start_screen()
game_loop()
