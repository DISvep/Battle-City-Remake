import pygame
from player import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.img = pygame.Surface((size, size))  # потрібна текстурка
        self.img.fill((120, 60, 0))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y


SIZE = 50

text_map = ["WWWWWWWWWWWWWWWW",
            "W..............W",
            "W...P..........W",
            "W..............W",
            "W..............W",
            "W..............W",
            "W..............W",
            "W..............W",
            "W..............W",
            "W.......W......W",
            "W..............W",
            "WWWWWWWWWWWWWWWW"]


def generate_map(map=text_map):
    world_map = pygame.sprite.Group()
    for y, row in enumerate(text_map):
        for x, char in enumerate(row):
            if char == 'W':
                world_map.add(Wall(x * SIZE, y * SIZE, SIZE))
    
    return world_map


def generate_player(map=text_map):
    player = pygame.sprite.Group()
    for y, row in enumerate(text_map):
        for x, char in enumerate(row):
            if char == 'P':
                player = Player("textures/tank.png", x * SIZE, y * SIZE, SIZE, 5)

    return player