import pygame


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
            "W..............W",
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
    world_map = list()

    for y, row in enumerate(text_map):
        for x, char in enumerate(row):
            if char == 'W':
                world_map.append(Wall(x * SIZE, y * SIZE, SIZE))

    print(world_map)

    return world_map
