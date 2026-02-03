"""
Tool B - Pong (ChatGPT)
How to run:
    pip install pygame
    python pong.py

Controls:
    Left paddle:  W (up), S (down)
    Right paddle: Up Arrow (up), Down Arrow (down)
Quit:
    ESC or close the window
"""

import sys
import pygame

# -----------------------
# Game constants
# -----------------------
WIDTH, HEIGHT = 800, 500
FPS = 60

PADDLE_W, PADDLE_H = 12, 100
BALL_SIZE = 12

PADDLE_SPEED = 7
BALL_START_SPEED_X = 6
BALL_START_SPEED_Y = 4
MAX_BALL_Y_SPEED = 8

BLACK = (10, 10, 10)
WHITE = (245, 245, 245)
GRAY = (80, 80, 80)


def clamp(val, lo, hi):
    return max(lo, min(hi, val))


def reset_ball(ball_rect, direction):
    """Reset ball to center; direction is +1 (to right) or -1 (to left)."""
    ball_rect.center = (WIDTH // 2, HEIGHT // 2)
    vx = BALL_START_SPEED_X * direction
    vy = BALL_START_SPEED_Y
    return vx, vy


def draw_center_line(screen):
    dash_h = 14
    gap = 12
    x = WIDTH // 2
    y = 0
    while y < HEIGHT:
        pygame.draw.rect(screen, GRAY, (x - 2, y, 4, dash_h))
        y += dash_h + gap


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong (Tool B - ChatGPT)")
    clock = pygame.time.Clock()

    score_font = pygame.font.SysFont("consolas", 48)
    hint_font = pygame.font.SysFont("consolas", 18)

    # Entities
    left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
    right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

    # State
    left_score, right_score = 0, 0
    ball_vx, ball_vy = reset_ball(ball, direction=1)

    running = True
    while running:
        clock.tick(FPS)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        # Paddle movement
        if keys[pygame.K_w]:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            left_paddle.y += PADDLE_SPEED

        if keys[pygame.K_UP]:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            right_paddle.y += PADDLE_SPEED

        left_paddle.y = clamp(left_paddle.y, 0, HEIGHT - PADDLE_H)
        right_paddle.y = clamp(right_paddle.y, 0, HEIGHT - PADDLE_H)

        # Ball movement
        ball.x += ball_vx
        ball.y += ball_vy

        # Wall collisions
        if ball.top <= 0:
            ball.top = 0
            ball_vy *= -1
        elif ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_vy *= -1

        # Paddle collisions + "spin"
        if ball.colliderect(left_paddle) and ball_vx < 0:
            ball.left = left_paddle.right
            ball_vx *= -1

            # Spin based on hit position
            offset = (ball.centery - left_paddle.centery) / (PADDLE_H / 2)
            ball_vy = int(clamp(offset * MAX_BALL_Y_SPEED, -MAX_BALL_Y_SPEED, MAX_BALL_Y_SPEED))

        if ball.colliderect(right_paddle) and ball_vx > 0:
            ball.right = right_paddle.left
            ball_vx *= -1

            offset = (ball.centery - right_paddle.centery) / (PADDLE_H / 2)
            ball_vy = int(clamp(offset * MAX_BALL_Y_SPEED, -MAX_BALL_Y_SPEED, MAX_BALL_Y_SPEED))

        # Scoring
        if ball.left <= 0:
            right_score += 1
            ball_vx, ball_vy = reset_ball(ball, direction=-1)
        elif ball.right >= WIDTH:
            left_score += 1
            ball_vx, ball_vy = reset_ball(ball, direction=1)

        # Draw
        screen.fill(BLACK)
        draw_center_line(screen)

        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.rect(screen, WHITE, ball)

        # Score
        left_text = score_font.render(str(left_score), True, WHITE)
        right_text = score_font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH * 1 // 4 - left_text.get_width() // 2, 30))
        screen.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width() // 2, 30))

        hint = hint_font.render("Left: W/S   Right: ↑/↓   ESC: Quit", True, GRAY)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 28))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
