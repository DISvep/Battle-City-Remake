import pygame
from objects import *
from settings import *


def generate_map(map=text_map):
    world_map = pygame.sprite.Group()
    for y, row in enumerate(text_map):
        for x, char in enumerate(row):
            if char == 'W':
                world_map.add(Wall(x * SIZE_CELL, y * SIZE_CELL, SIZE_CELL))

    return world_map


def generate_player(map=text_map):
    player = pygame.sprite.Group()
    for y, row in enumerate(text_map):
        for x, char in enumerate(row):
            if char == 'P':
                player = Player("textures/tank.png", x * SIZE_CELL, y * SIZE_CELL)

    return player


def generate_enemy(player, walls, map=text_map):
    enemies = pygame.sprite.Group()
    for y, row in enumerate(text_map):
        for x, char in enumerate(row):
            if char == "E":
                enemies.add(Enemy("textures/enemy.png", x * SIZE_CELL, y * SIZE_CELL, walls, player))
            if char == "S":
                enemies.add(FastEnemy("textures/fast_enemy.png", x * SIZE_CELL, y * SIZE_CELL, walls, player))
            if char == "F":
                enemies.add(FatEnemy("textures/fat_enemy.png", x * SIZE_CELL, y * SIZE_CELL, walls, player))

    return enemies
