# How to run:
# 1. Make sure you have pygame installed: pip install pygame
# 2. Run the script from your terminal: python pong.py

import pygame
import sys
import random

# --- Constants ---
# Screen dimensions
WIDTH, HEIGHT = 800, 500

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game object dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_RADIUS = 8

# Speeds
PADDLE_SPEED = 7
BALL_SPEED_X = 6
BALL_SPEED_Y = 6


def ball_reset(ball, ball_speed_x, ball_speed_y):
    """Resets the ball to the center with a random direction."""
    ball.center = (WIDTH // 2, HEIGHT // 2)
    # Randomize direction after a score
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))
    return ball_speed_x, ball_speed_y

def main():
    """Main function to run the Ping-Pong game."""
    # --- Pygame Initialization ---
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping-Pong")
    clock = pygame.time.Clock()

    # --- Game Objects ---
    # Paddles
    left_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Ball
    ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

    # --- Game Variables ---
    # Speeds
    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))
    left_paddle_speed = 0
    right_paddle_speed = 0

    # Scores
    left_player_score = 0
    right_player_score = 0
    score_font = pygame.font.Font(None, 74)

    # --- Main Game Loop ---
    while True:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Key presses for paddle movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Left paddle
                if event.key == pygame.K_w:
                    left_paddle_speed -= PADDLE_SPEED
                if event.key == pygame.K_s:
                    left_paddle_speed += PADDLE_SPEED
                # Right paddle
                if event.key == pygame.K_UP:
                    right_paddle_speed -= PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    right_paddle_speed += PADDLE_SPEED
            # Key releases to stop paddle movement
            if event.type == pygame.KEYUP:
                # Left paddle
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    left_paddle_speed = 0
                # Right paddle
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    right_paddle_speed = 0
        
        # --- Game Logic ---
        # Move paddles
        left_paddle.y += left_paddle_speed
        right_paddle.y += right_paddle_speed

        # Paddle boundary checks
        if left_paddle.top <= 0:
            left_paddle.top = 0
        if left_paddle.bottom >= HEIGHT:
            left_paddle.bottom = HEIGHT
        if right_paddle.top <= 0:
            right_paddle.top = 0
        if right_paddle.bottom >= HEIGHT:
            right_paddle.bottom = HEIGHT

        # Move ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with walls (top/bottom)
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Ball collision with paddles
        if ball.colliderect(left_paddle) and ball_speed_x < 0:
            ball_speed_x *= -1
        if ball.colliderect(right_paddle) and ball_speed_x > 0:
            ball_speed_x *= -1

        # Scoring
        if ball.left <= 0:
            right_player_score += 1
            ball_speed_x, ball_speed_y = ball_reset(ball, ball_speed_x, ball_speed_y)
        
        if ball.right >= WIDTH:
            left_player_score += 1
            ball_speed_x, ball_speed_y = ball_reset(ball, ball_speed_x, ball_speed_y)

        # --- Drawing ---
        screen.fill(BLACK)
        
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        
        # Draw center line
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Draw scores
        left_text = score_font.render(f"{left_player_score}", True, WHITE)
        screen.blit(left_text, (WIDTH // 4, 20))
        
        right_text = score_font.render(f"{right_player_score}", True, WHITE)
        screen.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width(), 20))

        # --- Update Display ---
        pygame.display.flip()
        clock.tick(60) # Limit frame rate to 60 FPS

if __name__ == "__main__":
    main()
