import pygame
import scenes
import settings
import map
import UI
import moviepy.editor

pygame.init()

start_screen_video = moviepy.editor.VideoFileClip('videos/startgamescreen.mp4')
start_screen_video.preview()

entities = pygame.sprite.Group()

world_map = map.generate_map()

plr = map.generate_player()
enemies = map.generate_enemy(plr, world_map)
entities.add(plr)
entities.add(enemies)

boosts_group = map.generate_boosts()

scr = pygame.display.set_mode(settings.SIZE)

game = True
clock = pygame.time.Clock()

while game != False:
    result = scenes.scenes(scr, plr, world_map, enemies, entities, boosts_group, clock)
    if isinstance(result, tuple):
        world_map, plr, enemies, entities, boosts_group = result
    else:
        game = result

pygame.quit()
