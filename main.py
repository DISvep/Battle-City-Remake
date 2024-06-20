import pygame
import scenes
import settings
import map


pygame.init()

entities = pygame.sprite.Group()

world_map = map.generate_map()

plr = map.generate_player()
enemies = map.generate_enemy(plr, world_map)
entities.add(plr)
entities.add(enemies)

boosts_group = pygame.sprite.Group()
hp = map.generate_hp_boost()
boosts_group.add(hp)
speed = map.generate_speed_boost()
boosts_group.add(speed)

scr = pygame.display.set_mode(settings.SIZE)


game = True
clock = pygame.time.Clock()

while game != False:
    game = scenes.scenes(scr, plr, world_map, enemies, entities, boosts_group, clock)

pygame.quit()
