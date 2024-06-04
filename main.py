import pygame
import map

pygame.init()

WHITE = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

scr = pygame.display.set_mode(SIZE)
world_map = map.generate_map()

game = True
while game:
    scr.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    for wall in world_map:
        scr.blit(wall.img, wall.rect)

    pygame.display.flip()
