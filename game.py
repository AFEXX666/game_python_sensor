import serial
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
BALL_RADIUS = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def reset_game():
    global platform_x, platform_y, ball_x, ball_y, ball_speed_x, ball_speed_y, game_time, score, playing
    platform_x = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
    platform_y = SCREEN_HEIGHT - PLATFORM_HEIGHT - 10
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_speed_x = 3
    ball_speed_y = -3
    game_time = 0
    score = 0
    playing = True

reset_game()

ser = serial.Serial('COM10', 9600)

pygame.key.set_repeat(50, 50)

elapsed_time = 0
acceleration_interval = 5000
acceleration_amount = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not playing and event.key == pygame.K_SPACE:  # Reiniciar el juego al presionar la tecla Espacio
                reset_game()

    if ser.in_waiting > 0:
        value = ser.readline().decode('utf-8').strip()
        platform_value = round(float(value))
        platform_x = int(SCREEN_WIDTH * (platform_value / 100)) - PLATFORM_WIDTH // 2

    keys = pygame.key.get_pressed()
    platform_x = max(0, min(platform_x, SCREEN_WIDTH - PLATFORM_WIDTH))
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_x < 0 or ball_x > SCREEN_WIDTH - BALL_RADIUS:
        ball_speed_x *= -1
    if ball_y < 0:
        ball_speed_y *= -1
    if ball_y > SCREEN_HEIGHT:
        playing = False

    if ball_y + BALL_RADIUS >= platform_y and ball_x + BALL_RADIUS >= platform_x and ball_x <= platform_x + PLATFORM_WIDTH:
        ball_speed_y *= -1

    elapsed_time += clock.get_time()
    if elapsed_time >= acceleration_interval:
        elapsed_time = 0
        ball_speed_x += acceleration_amount
        ball_speed_y += acceleration_amount

    game_time += clock.get_time()

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (platform_x, platform_y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

    font = pygame.font.SysFont(None, 24)
    text = font.render("Tiempo: " + str(game_time // 1000), True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(60)

    if not playing:
        screen.fill(BLACK)
        text = font.render("Puntuación: " + str(game_time // 1000) + " segundos", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Esperar 3 segundos antes de reiniciar el juego
        reset_game()