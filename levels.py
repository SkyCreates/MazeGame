import numpy as np
import random
from collections import deque

# Directions for maze generation: right, down, left, up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def generate_maze(level, width, height, grid_size):
    """
    Generate a maze for the given level. The maze size increases with the level to increase difficulty.
    """
    maze_width, maze_height = get_maze_size(level, width, height, grid_size)
    maze = initialize_maze(maze_width, maze_height)
    create_paths(maze, maze_width, maze_height)
    ensure_exit_reachable(maze, maze_width, maze_height)
    min_moves = calculate_min_moves(maze)

    # If no valid path, connect the start and exit
    if min_moves == float('inf'):
        connect_start_and_exit(maze, maze_width, maze_height)
        min_moves = calculate_min_moves(maze)

    return maze, max(min_moves - 1, 0)

def get_maze_size(level, width, height, grid_size):
    """
    Determine the size of the maze based on the level.
    """
    max_cells_width = width // grid_size
    max_cells_height = height // grid_size

    base_size = 5
    size_increment = level // 2

    maze_width = min(base_size + size_increment, max_cells_width)
    maze_height = min(base_size + size_increment, max_cells_height)

    return maze_width, maze_height

def initialize_maze(maze_width, maze_height):
    """
    Initialize the maze with walls (1) and an open starting point.
    """
    maze = np.ones((maze_height, maze_width), dtype=int)
    maze[0][0] = 0  # Starting point
    return maze

def create_paths(maze, maze_width, maze_height):
    """
    Create paths in the maze using a depth-first search algorithm.
    """
    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        neighbors = find_neighbors(maze, x, y, maze_width, maze_height)
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[y + dy][x + dx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

def ensure_exit_reachable(maze, maze_width, maze_height):
    """
    Ensure the exit at the bottom-right corner is reachable by connecting it to the maze if necessary.
    """
    if maze[maze_height - 2][maze_width - 1] == 1 and maze[maze_height - 1][maze_width - 2] == 1:
        maze[maze_height - 1][maze_width - 2] = 0
    maze[maze_height - 1][maze_width - 1] = 0

def find_neighbors(maze, x, y, maze_width, maze_height):
    """
    Find valid neighbors for the current cell during maze generation.
    """
    neighbors = []
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx * 2, y + dy * 2
        if is_valid_cell(maze, nx, ny, maze_width, maze_height):
            neighbors.append((nx, ny, dx, dy))
    return neighbors

def is_valid_cell(maze, x, y, maze_width, maze_height):
    """
    Check if a cell is valid for path creation.
    """
    if 0 <= x < maze_width and 0 <= y < maze_height and maze[y][x] == 1:
        wall_count = 0
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze_width and 0 <= ny < maze_height and maze[ny][nx] == 1:
                wall_count += 1
        return wall_count >= 3
    return False

def calculate_min_moves(maze):
    """
    Calculate the minimum moves required to solve the maze using BFS.
    """
    maze_height, maze_width = maze.shape
    start = (0, 0)
    goal = (maze_height - 1, maze_width - 1)
    queue = deque([start])
    distances = {start: 0}

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return distances[(x, y)]
        
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze_width and 0 <= ny < maze_height and maze[ny][nx] == 0:
                if (nx, ny) not in distances:
                    queue.append((nx, ny))
                    distances[(nx, ny)] = distances[(x, y)] + 1

    return float('inf')  # Return infinity if no path is found

def connect_start_and_exit(maze, maze_width, maze_height):
    """
    Ensure a direct path from the start to the exit if no path exists.
    """
    x, y = 0, 0
    while (x, y) != (maze_height - 1, maze_width - 1):
        if x < maze_width - 1:
            x += 1
        elif y < maze_height - 1:
            y += 1
        maze[y][x] = 0

# For debugging and testing
if __name__ == "__main__":
    width, height, grid_size = 800, 600, 40
    level = 1
    maze, min_moves = generate_maze(level, width, height, grid_size)
    for row in maze:
        print("".join([' ' if cell == 0 else '#' for cell in row]))
    print(f"Minimum moves: {min_moves}")
