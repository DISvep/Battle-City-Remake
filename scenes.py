from settings import *
import pygame


def scenes(scr, plr, world_map, enemies, entities, clock):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    SCENE = get_scene()

    if SCENE == "main":
        scr.fill(WHITE)

        for wall in world_map:
            scr.blit(wall.img, wall.rect)

        if plr.render:
            plr.update(scr, world_map)
            plr.draw(scr)

        for enemy in enemies:
            enemy.update(scr, plr)

        for bullet in plr.bullets:
            bullet.update(world_map, entities)
            bullet.draw(scr)

        pygame.display.flip()
        clock.tick(FPS)

    if SCENE == 'death':
        scr.fill(BLACK)

        pygame.display.flip()
        clock.tick(FPS)
