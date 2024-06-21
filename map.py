import pygame
from objects import *
import settings
import random


def generate_map():
    world_map = pygame.sprite.Group()
    current_level = settings.get_current_text_map()
    for y, row in enumerate(current_level):
        for x, char in enumerate(row):
            if char == 'W':
                world_map.add(Wall(x * SIZE_CELL, y * SIZE_CELL))
    return world_map


def generate_player():
    player = pygame.sprite.Group()
    current_level = settings.get_current_text_map()
    for y, row in enumerate(current_level):
        for x, char in enumerate(row):
            if char == 'P':
                player = Player("textures/tank.png", x * SIZE_CELL, y * SIZE_CELL)

    return player


def generate_enemy(player, walls):
    enemies = pygame.sprite.Group()
    current_level = settings.get_current_text_map()
    for y, row in enumerate(current_level):
        for x, char in enumerate(row):
            if char == "E":
                factories = [SimpleEnemyFactory(), FastEnemyFactory(), FatEnemyFactory()]
                factory = random.choice(factories)

                enemies.add(factory.create(x * SIZE_CELL, y * SIZE_CELL, walls, player))

    return enemies


def generate_boosts():
    hp_boost = pygame.sprite.Group()
    current_level = settings.get_current_text_map()
    for y, row in enumerate(current_level):
        for x, char in enumerate(row):
            if char == "B":
                factories = [SpeedBoostFactory(), HealthBoostFactory(), DamageBoostFactory()]
                factory = random.choice(factories)

                boost = factory.create(x * SIZE_CELL, y * SIZE_CELL)
                hp_boost.add(boost)
    return hp_boost

