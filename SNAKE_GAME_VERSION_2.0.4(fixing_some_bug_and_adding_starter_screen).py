import os
import pygame
import random
from pygame.locals import MOUSEBUTTONDOWN
import pygame.mixer as mixer
import time

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Set up display variables
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

# Set up color variables
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set window title
pygame.display.set_caption("Snake Game")

# Load background image
bg_image = pygame.image.load(r"C:\Users\Lenovo\DARK_BACKGROUND_FOR_SNAKE_GAME")  # Replace with your game background image path
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Load sound effects
eat_sound = pygame.mixer.Sound(r"C:\Users\Lenovo\eat.wav.mp3")  # Replace with your sound effect path
game_over_sound = pygame.mixer.Sound(r"C:\Users\Lenovo\game_over_sound.wav.wav")  # Replace with your sound effect path

# Load background music
mixer.music.load(r"C:\Users\Lenovo\snake_game_background_song.mp3")  # Replace with the path to your background music file

# Set the volume (optional)
mixer.music.set_volume(0.5)  # Adjust the volume level as needed (0.0 to 1.0)

# Start playing the background music
mixer.music.play(-1)  # The '-1' loops the music infinitely

# Create snake and food
snake = [pygame.Rect(WIDTH // 2, HEIGHT // 2, BLOCK_SIZE, BLOCK_SIZE)]
food = pygame.Rect(random.randint(0, WIDTH - BLOCK_SIZE), random.randint(0, HEIGHT - BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
buffer_food = None
BUFFER_FOOD_TIMEOUT = 5  # Duration in seconds
buffer_food_timer = None

# Set initial direction
dx = BLOCK_SIZE
dy = 0

# Initialize score
score = 0

# Initialize high score
try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except FileNotFoundError:
    with open("highscore.txt", "w") as f:
        f.write("0")
    highscore = 0

# Set up font for score display
font = pygame.font.Font(None, 36)

# Define starting page constants
START_BUTTON_WIDTH = 200
START_BUTTON_HEIGHT = 50
START_BUTTON_COLOR = (0, 0, 255)  # Blue button
START_BUTTON_TEXT_COLOR = WHITE

# Define game over screen constants
GAME_OVER_TEXT_COLOR = RED
GAME_OVER_BUTTON_WIDTH = 100
GAME_OVER_BUTTON_HEIGHT = 50
RESTART_BUTTON_COLOR = GREEN
EXIT_BUTTON_COLOR = RED
RESET_HIGHSCORE_BUTTON_COLOR = BLUE


# Define a function to display the start screen with a different background
def show_start_page():
    start_bg_image = pygame.image.load(r"C:\Users\Lenovo\backgrpond_image.jpg")  # Replace with the path to your start screen background image
    start_bg_image = pygame.transform.scale(start_bg_image, (WIDTH, HEIGHT))

    start_font = pygame.font.Font(None, 48)
    start_text = start_font.render("Snake Game", True, (0, 128, 0))
    start_button_rect = pygame.Rect(WIDTH // 2 - START_BUTTON_WIDTH // 2, HEIGHT // 2 - START_BUTTON_HEIGHT // 2, START_BUTTON_WIDTH, START_BUTTON_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return

        screen.blit(start_bg_image, (0, 0))
        pygame.draw.rect(screen, START_BUTTON_COLOR, start_button_rect)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 3))
        start_button_text = start_font.render("Start", True, START_BUTTON_TEXT_COLOR)
        screen.blit(start_button_text, (WIDTH // 2 - start_button_text.get_width() // 2, HEIGHT // 2 - start_button_text.get_height() // 2))

        pygame.display.flip()

#........


def show_game_over_screen():
    game_over_font = pygame.font.Font(None, 48)
    game_over_text = game_over_font.render("Game Over!", True, GAME_OVER_TEXT_COLOR)
    final_score_text = game_over_font.render("Final Score: " + str(score), True, GAME_OVER_TEXT_COLOR)
    restart_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, GAME_OVER_BUTTON_WIDTH, GAME_OVER_BUTTON_HEIGHT)
    exit_button_rect = pygame.Rect(3 * WIDTH // 4 - GAME_OVER_BUTTON_WIDTH, HEIGHT // 2, GAME_OVER_BUTTON_WIDTH, GAME_OVER_BUTTON_HEIGHT)
    reset_highscore_button_rect = pygame.Rect(WIDTH // 2 - GAME_OVER_BUTTON_WIDTH // 2, HEIGHT // 2 + 70, GAME_OVER_BUTTON_WIDTH, GAME_OVER_BUTTON_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    mixer.music.play(-1)  # Start playing the background music again
                    return True
                elif exit_button_rect.collidepoint(event.pos):
                    return False
                elif reset_highscore_button_rect.collidepoint(event.pos):
                    reset_highscore()
                    return True
        mixer.music.stop()  # Stop the background music before showing the game over screen

        screen.blit(bg_image, (0, 0))
        pygame.draw.rect(screen, RESTART_BUTTON_COLOR, restart_button_rect)
        pygame.draw.rect(screen, EXIT_BUTTON_COLOR, exit_button_rect)
        pygame.draw.rect(screen, RESET_HIGHSCORE_BUTTON_COLOR, reset_highscore_button_rect)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - final_score_text.get_height()))
        restart_button_text = game_over_font.render("Restart", True, WHITE)  # White text
        exit_button_text = game_over_font.render("Exit", True, WHITE)  # White text
        reset_highscore_text = game_over_font.render("Reset High Score", True, WHITE)  # White text
        screen.blit(restart_button_text, (restart_button_rect.centerx - restart_button_text.get_width() // 2, restart_button_rect.centery - restart_button_text.get_height() // 2))
        screen.blit(exit_button_text, (exit_button_rect.centerx - exit_button_text.get_width() // 2, exit_button_rect.centery - exit_button_text.get_height() // 2))
        screen.blit(reset_highscore_text, (reset_highscore_button_rect.centerx - reset_highscore_text.get_width() // 2, reset_highscore_button_rect.centery - reset_highscore_text.get_height() // 2))

        pygame.display.flip()


def reset_highscore():
    with open("highscore.txt", "w") as f:
        f.write("0")
    global highscore
    highscore = 0
    mixer.music.play(-1)


def generate_buffer_food():
    global buffer_food, buffer_food_timer
    buffer_food = pygame.Rect(random.randint(0, WIDTH - BLOCK_SIZE), random.randint(0, HEIGHT - BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
    buffer_food_timer = time.time()


def draw_buffer_food():
    if buffer_food and time.time() - buffer_food_timer < BUFFER_FOOD_TIMEOUT:
        pygame.draw.rect(screen, BLUE, buffer_food)


show_start_page()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -BLOCK_SIZE
            elif event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = BLOCK_SIZE
            elif event.key == pygame.K_LEFT and dx == 0:
                dx = -BLOCK_SIZE
                dy = 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx = BLOCK_SIZE
                dy = 0

    if not snake:
        snake = [pygame.Rect(WIDTH // 2, HEIGHT // 2, BLOCK_SIZE, BLOCK_SIZE)]
        dx = BLOCK_SIZE
        dy = 0

    head = snake[0].copy()
    head.move_ip(dx, dy)
    snake.insert(0, head)

    if (head.collidelist(snake[1:]) != -1 or not head.colliderect(pygame.Rect(0, 0, WIDTH, HEIGHT))):
        game_over_sound.play()
        if score > highscore:
            with open("highscore.txt", "w") as f:
                f.write(str(score))
        game_over = show_game_over_screen()
        if not game_over:
            pygame.quit()
            quit()
        snake = [pygame.Rect(WIDTH // 2, HEIGHT // 2, BLOCK_SIZE, BLOCK_SIZE)]
        food = pygame.Rect(random.randint(0, WIDTH - BLOCK_SIZE), random.randint(0, HEIGHT - BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
        buffer_food = None
        dx = BLOCK_SIZE
        dy = 0
        score = 0

    if head.colliderect(food):
        eat_sound.play()
        score += 1
        snake.append(pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE))

        while True:
            food.x = random.randint(0, WIDTH - BLOCK_SIZE)
            food.y = random.randint(0, HEIGHT - BLOCK_SIZE)
            if food.collidelist(snake) == -1:
                break

    # Check for buffer food collision
    if buffer_food and head.colliderect(buffer_food):
        eat_sound.play()
        score += 10
        buffer_food = None
    else:
        snake.pop()

    if not buffer_food:
        # Generate buffer food after it's consumed or after a timeout
        if random.random() < 0.02:  # Adjust the probability as needed
            generate_buffer_food()

    screen.blit(bg_image, (0, 0))
    for segment in snake:
        pygame.draw.rect(screen, GREEN, segment)
    pygame.draw.rect(screen, RED, food)
    draw_buffer_food()  # Draw the buffer food

    score_text = font.render("Score: " + str(score), True, (0, 128, 0))
    highscore_text = font.render("High Score: " + str(highscore), True, (0, 128, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(highscore_text, (10, 50))

    pygame.display.flip()
    pygame.time.wait(100)
