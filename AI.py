import random
import pygame
from settings import *


class Pixel(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(x=x, y=y)


class Enemy:
    def __init__(self, x, y, walls, player, me):
        self.x, self.y = x, y
        self.walls = walls
        self.FOV = 300
        self.player = player
        self.me = me
        self.collides = False
        self.directions = ['up', 'down', 'left', 'right']
        self.direction = random.choice(self.directions)
        self.last_plr_pos = (0, 0)

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
        if self.me.stuck:
            self.direction = random.choice(self.directions)
            self.me.stuck = False

        self.me.stop()

        self.move()

        self.cast_rays((self.me.rect.x, self.me.rect.y),scr)

        self.me.image = self.me.images[self.me.direction]

        if self.collides:
            self.me.shoot()
