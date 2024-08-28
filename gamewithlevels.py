import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
LEVELS = [
    {'hats': 3, 'tries': 2},
    {'hats': 5, 'tries': 3},
    {'hats': 9, 'tries': 4}
]
LEVEL = 0
GRID_SIZE = 9
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# Setup the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Find the Coin")


def initialize_level(level):
    global grid, hat_positions, coin_position, attempts, found
    hats = LEVELS[level]['hats']
    tries = LEVELS[level]['tries']

    # Create a 9x9 empty grid
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Place exactly `hats` hats randomly
    all_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
    hat_positions = random.sample(all_positions, hats)

    for pos in hat_positions:
        grid[pos[1]][pos[0]] = 1  # Place a hat

    # Randomly choose one of the hat positions to hide the coin
    coin_position = random.choice(hat_positions)
    grid[coin_position[1]][coin_position[0]] = 1  # Still place a hat in the coin position

    # Initialize game variables
    attempts = 0
    found = False


def draw_grid():
    screen.fill(BLACK)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:  # Draw hat if not found
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Grid lines


def check_click(pos):
    global attempts, found
    x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    if grid[y][x] == 1:  # Only allow clicking on hats
        attempts += 1
        if (x, y) == coin_position:
            found = True
        grid[y][x] = 0  # Remove the hat after checking


def display_message(message):
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, GOLD)
    screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, WINDOW_SIZE // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)


# Initialize the first level
initialize_level(LEVEL)

# Game loop
running = True
while running:
    draw_grid()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and attempts < LEVELS[LEVEL]['tries'] and not found:
            check_click(pygame.mouse.get_pos())
            if found:
                # Reveal the coin if found
                draw_grid()
                pygame.draw.rect(screen, GOLD,
                                 pygame.Rect(coin_position[0] * CELL_SIZE, coin_position[1] * CELL_SIZE, CELL_SIZE,
                                             CELL_SIZE))
                pygame.display.flip()
                display_message("You found the coin!")

                # Move to next level if available
                LEVEL += 1
                if LEVEL < len(LEVELS):
                    initialize_level(LEVEL)
                else:
                    display_message("Congrats")
                    running = False
            elif attempts >= LEVELS[LEVEL]['tries']:
                display_message("Out of tries!")
                running = False

pygame.quit()
sys.exit()