import pygame
from levels import generate_maze

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Maze Game")

# Screen dimensions
WIDTH, HEIGHT = 800, 600
PADDING = 30  # Padding to avoid text overlap with the maze

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)

# Font
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

def draw_maze(maze, x_offset, y_offset, visited, grid_size):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            color = LIGHT_BLUE if (x, y) in visited else (WHITE if maze[y][x] == 0 else BLACK)
            pygame.draw.rect(screen, color, (x * grid_size + x_offset, y * grid_size + y_offset, grid_size, grid_size))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text('Maze Game', font, WHITE, screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        draw_text('Press any key to start', small_font, WHITE, screen, WIDTH // 2 - 150, HEIGHT // 2)
        draw_text('WASD or Arrow keys to move', small_font, WHITE, screen, WIDTH // 2 - 150, HEIGHT // 2 + 50)
        draw_text('Press Q to quit anytime', small_font, WHITE, screen, WIDTH // 2 - 150, HEIGHT // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                return

        pygame.display.update()
        clock.tick(15)

def display_level(level):
    """ Display the current level number """
    screen.fill(BLACK)
    draw_text(f'Level {level}', font, WHITE, screen, WIDTH // 2 - 100, HEIGHT // 2 - 50)
    pygame.display.update()
    pygame.time.wait(2000)  # Display for 2 seconds

def game_loop(level, score):
    print(f"Starting game loop for level {level}...")

    # Calculate the grid size based on the level to create the zoom-out effect
    base_grid_size = 50
    grid_size = max(20, base_grid_size - level)  # Decrease grid size with each level but not less than 20

    player_x, player_y = 0, 0
    maze, par = generate_maze(level, WIDTH - 2 * PADDING, HEIGHT - 2 * PADDING, grid_size)
    maze_width, maze_height = len(maze[0]), len(maze)
    x_offset = (WIDTH - maze_width * grid_size) // 2
    y_offset = (HEIGHT - maze_height * grid_size) // 2

    exit_x, exit_y = maze_width - 1, maze_height - 1
    move_count = 0
    visited = set()
    visited.add((player_x, player_y))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        keys = pygame.key.get_pressed()
        moved = False

        # Prevent diagonal movement by checking one key press at a time
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if player_x > 0 and maze[player_y][player_x - 1] == 0:
                player_x -= 1
                move_count += 1
                moved = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if player_x < maze_width - 1 and maze[player_y][player_x + 1] == 0:
                player_x += 1
                move_count += 1
                moved = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if player_y > 0 and maze[player_y - 1][player_x] == 0:
                player_y -= 1
                move_count += 1
                moved = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if player_y < maze_height - 1 and maze[player_y + 1][player_x] == 0:
                player_y += 1
                move_count += 1
                moved = True

        if moved:
            visited.add((player_x, player_y))

        screen.fill(BLACK)
        draw_maze(maze, x_offset, y_offset, visited, grid_size)
        pygame.draw.rect(screen, BLUE, (player_x * grid_size + x_offset, player_y * grid_size + y_offset, grid_size, grid_size))
        pygame.draw.rect(screen, RED, (exit_x * grid_size + x_offset, exit_y * grid_size + y_offset, grid_size, grid_size))
        draw_text(f'Moves: {move_count}', small_font, WHITE, screen, 10, 10)
        draw_text(f'Par: {par}', small_font, WHITE, screen, 10, 50)
        draw_text(f'Level: {level}', small_font, WHITE, screen, 10, HEIGHT - 40)
        draw_text('Press Q to quit', small_font, WHITE, screen, WIDTH - 200, HEIGHT - 40)

        # Calculate and display the live score
        live_score = score + max(1000 - move_count, 0)
        draw_text(f'Score: {live_score}', small_font, WHITE, screen, WIDTH - 150, 10)

        pygame.display.update()
        clock.tick(18)  # Adjust FPS for smoother movement

        if player_x == exit_x and player_y == exit_y:
            print(f"Level {level} completed with {move_count} moves!")
            running = False

    return move_count  # Return the move count for the level

if __name__ == '__main__':
    while True:
        main_menu()
        current_level = 1
        total_score = 0
        while True:
            display_level(current_level)
            moves = game_loop(current_level, total_score)
            total_score += max(1000 - moves, 0)  # Calculate score based on moves
            current_level += 1
