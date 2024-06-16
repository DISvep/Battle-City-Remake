import pygame
import heapq

# Инициализация Pygame
pygame.init()

# Константы
CELL_SIZE = 40
ROWS, COLS = 6, 20  # Размер лабиринта
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
START_POS = (1, 1)
END_POS = (5, 5)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding")

# Лабиринт (1 - стена, 0 - проход)
maze = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def search(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS:
                if maze[neighbor[0]][neighbor[1]] == 0:
                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        if neighbor not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # Визуализация текущего состояния поиска
        screen.fill(WHITE)
        draw_grid()
        draw_path(came_from)
        pygame.draw.rect(screen, GREEN, (START_POS[1] * CELL_SIZE, START_POS[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (END_POS[1] * CELL_SIZE, END_POS[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, YELLOW, (current[1] * CELL_SIZE, current[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(100)  # Задержка для визуализации процесса

    return None


def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def draw_path(came_from):
    for (current, parent) in came_from.items():
        if parent:
            pygame.draw.line(screen, CYAN,
                             (parent[1] * CELL_SIZE + CELL_SIZE // 2, parent[0] * CELL_SIZE + CELL_SIZE // 2),
                             (current[1] * CELL_SIZE + CELL_SIZE // 2, current[0] * CELL_SIZE + CELL_SIZE // 2), 2)


path = a_star_search(START_POS, END_POS)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    draw_grid()
    if path:
        draw_path({node: node for node in path})
        for node in path:
            pygame.draw.rect(screen, YELLOW, (node[1] * CELL_SIZE, node[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            pygame.time.delay(100)
    pygame.draw.rect(screen, GREEN, (START_POS[1] * CELL_SIZE, START_POS[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (END_POS[1] * CELL_SIZE, END_POS[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

pygame.quit()
