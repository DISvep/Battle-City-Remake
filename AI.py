import random
import pygame
from settings import *
import heapq
from abc import ABC, abstractmethod


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(text_map, start, goal):
    rows, cols = len(text_map), len(text_map[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if text_map[neighbor[0]][neighbor[1]] == "W":
                    continue
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


def get_text_pos(y, x):
    return y // SIZE_CELL, x // SIZE_CELL


class Pixel(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(x=x, y=y)


class Factory(ABC):
    @abstractmethod
    def create(self, *args):
        pass


class Enemy:
    def __init__(self, x, y, walls, player, me):
        self.x, self.y = x, y
        self.walls = walls
        self.player = player
        self.me = me
        self.all_seeing = False
        self.collides = False
        self.directions = ['up', 'down', 'left', 'right']
        self.direction = random.choice(self.directions)
        self.saw_player = False
        self.last_plr_pos = (0, 0)
        self.text_plr_pos = (0, 0)
        self.path = []
        self.step = None
        self.pixels = pygame.sprite.Group()
        self.text_map = get_current_text_map()

    def cast_rays(self, start, scr):
        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }

        x, y = start

        for direction, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            while 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                rect = Pixel(nx, ny, 35, 35)

                if rect.rect.colliderect(self.player):
                    self.collides = True
                    break
                if pygame.sprite.spritecollideany(rect, self.walls):
                    self.collides = False
                    break

                nx += dx
                ny += dy
            if rect.rect.colliderect(self.player):
                self.me.direction = direction
                break

    def goto(self, cur_pos, pos):
        if cur_pos[0] > pos[0]:
            self.direction = "up"
        elif cur_pos[0] < pos[0]:
            self.direction = "down"
        elif cur_pos[1] < pos[1]:
            self.direction = "right"
        elif cur_pos[1] > pos[1]:
            self.direction = "left"

        self.move()

        if self.me.stuck:
            self.direction = random.choice(self.directions)
            self.move()
            self.me.stuck = False

    def moving_to_player(self):
        if self.path:
            cur_pos = (self.me.rect.centery, self.me.rect.centerx)
            if self.step:
                self.goto(cur_pos, self.step)
                if self.step[0]-1 < cur_pos[0] < self.step[0]+1 and self.step[1]-1 < cur_pos[1] < self.step[1]+1:
                    try:
                        self.step = self.path.__next__()
                    except StopIteration:
                        self.path = []
                        self.step = None
                        self.saw_player = False
            else:
                try:
                    self.step = self.path.__next__()
                except StopIteration:
                    self.path = []
                    self.step = None
                    self.saw_player = False

    def move(self):
        if self.direction == "stay":
            self.me.stop()
        elif self.direction == "right":
            self.me.go_right()
        elif self.direction == "left":
            self.me.go_left()
        elif self.direction == "up":
            self.me.go_up()
        elif self.direction == "down":
            self.me.go_down()

    def update(self, scr):
        self.text_map = get_current_text_map()
        if self.me.stuck and not self.saw_player:
            self.direction = random.choice(self.directions)
            self.me.stuck = False

        self.moving_to_player()

        self.me.stop()

        self.move()

        for point in self.pixels:
            scr.blit(point.image, point.rect)

        self.cast_rays((self.me.rect.x, self.me.rect.y), scr)

        self.me.image = self.me.images[self.me.direction]

        if self.all_seeing:
            self.last_plr_pos = (self.player.rect.y, self.player.rect.x)
            self.text_plr_pos = get_text_pos(*self.last_plr_pos)
            self.path = find_path(self.text_map, get_text_pos(self.me.rect.y, self.me.rect.x), self.text_plr_pos)
            if self.path:
                for step in range(len(self.path)):
                    self.path[step] = self.path[step][0]*SIZE_CELL + SIZE_CELL/2, self.path[step][1]*SIZE_CELL + SIZE_CELL/2
                self.path = iter(self.path)

        if self.collides:
            self.me.shoot()
            if not self.all_seeing:
                self.last_plr_pos = (self.player.rect.y, self.player.rect.x)
                self.text_plr_pos = get_text_pos(*self.last_plr_pos)
                self.path = find_path(self.text_map, get_text_pos(self.me.rect.bottom, self.me.rect.right), self.text_plr_pos)
                if self.path:
                    for step in range(len(self.path)):
                        self.path[step] = self.path[step][0] * SIZE_CELL + SIZE_CELL / 2, self.path[step][1] * SIZE_CELL + SIZE_CELL / 2
                    self.path = iter(self.path)


class AllSeeingEnemy(Enemy):
    def __init__(self, x, y, walls, player, me):
        super().__init__(x, y, walls, player, me)
        self.all_seeing = True


class SimpleAiFactory(Factory):
    def create(self, *args):
        return Enemy(*args)


class AllSeeingAiFactory(Factory):
    def create(self, *args):
        return AllSeeingEnemy(*args)

