import pygame
import map
import player

pygame.init()

WHITE = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
FPS = 60

scr = pygame.display.set_mode(SIZE)
world_map = map.generate_map()

plr = player.Player("textures/tank.png", 50, 50, 2)

game = True
clock = pygame.time.Clock()
while game:
    scr.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    for wall in world_map:
        scr.blit(wall.img, wall.rect)

    plr.update(scr, world_map)
    plr.draw(scr)

    for bullet in plr.bullets:
        bullet.update(world_map)
        bullet.draw(scr)

    pygame.display.flip()
    clock.tick(FPS)
