import pygame

pygame.init()

WHITE = (255, 255, 255)
SIZE = (800, 600)

scr = pygame.display.set_mode(SIZE)


game = True
while game:
    scr.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    pygame.display.flip()
