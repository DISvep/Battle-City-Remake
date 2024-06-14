import pygame
import map
import objects
from settings import *
import scenes

pygame.init()

scr = pygame.display.set_mode(SIZE)
world_map = map.generate_map()

entities = pygame.sprite.Group()

plr = map.generate_player()
enemies = map.generate_enemy(plr, world_map)
entities.add(plr)
entities.add(enemies)

game = True
clock = pygame.time.Clock()

while game != False:
    game = scenes.scenes(scr, plr, world_map, enemies, entities, clock)
