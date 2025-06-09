import pygame
import random

# Define the board layout
LEVEL = [
    "####################",
    "#........##........#",
    "#.####.#.##.#.####.#",
    "#..................#",
    "#.##.#.#####.#.##.#",
    "#..................#",
    "#.####.######.####.#",
    "#..................#",
    "####################"
]

TILE_SIZE = 24
WIDTH = len(LEVEL[0]) * TILE_SIZE
HEIGHT = len(LEVEL) * TILE_SIZE

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = LEFT

    def move(self, grid):
        new_x = self.x + self.dir[0]
        new_y = self.y + self.dir[1]
        if grid[new_y][new_x] != '#':
            self.x = new_x
            self.y = new_y


def load_level():
    grid = []
    pellets = set()
    for y, row in enumerate(LEVEL):
        grid_row = []
        for x, ch in enumerate(row):
            grid_row.append(ch)
            if ch == '.':
                pellets.add((x, y))
        grid.append(grid_row)
    return grid, pellets


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    grid, pellets = load_level()

    pacman = Entity(1, 1)
    ghost = Entity(len(LEVEL[0]) - 2, len(LEVEL) - 2)
    ghost.dir = random.choice([UP, DOWN, LEFT, RIGHT])
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.dir = UP
                elif event.key == pygame.K_DOWN:
                    pacman.dir = DOWN
                elif event.key == pygame.K_LEFT:
                    pacman.dir = LEFT
                elif event.key == pygame.K_RIGHT:
                    pacman.dir = RIGHT

        pacman.move(grid)
        if (pacman.x, pacman.y) in pellets:
            pellets.remove((pacman.x, pacman.y))
            score += 10

        # ghost movement
        if random.random() < 0.2:
            ghost.dir = random.choice([UP, DOWN, LEFT, RIGHT])
        ghost.move(grid)

        # check collision
        if pacman.x == ghost.x and pacman.y == ghost.y:
            running = False

        screen.fill((0, 0, 0))
        # draw grid
        for y, row in enumerate(grid):
            for x, ch in enumerate(row):
                if ch == '#':
                    pygame.draw.rect(screen, (0, 0, 255), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        # draw pellets
        for x, y in pellets:
            pygame.draw.circle(screen, (255, 255, 255), (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 4)

        # draw entities
        pygame.draw.circle(screen, (255, 255, 0), (pacman.x * TILE_SIZE + TILE_SIZE // 2, pacman.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 2)
        pygame.draw.rect(screen, (255, 0, 0), (ghost.x * TILE_SIZE, ghost.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(10)
    pygame.quit()
    print("Game Over! Score:", score)

if __name__ == '__main__':
    main()
