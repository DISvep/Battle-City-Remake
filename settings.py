import UI
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND = (41, 27, 30)
YELLOW = (255, 255, 0)
RED_HP = (92, 23, 36)
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
FPS = 60
SIZE_CELL = 50
ROWS = 12
COLS = 16
wall = pygame.transform.scale(pygame.image.load('textures/wall.jpg'), (SIZE_CELL, SIZE_CELL))
text_map = ["WWWWWWWWWWWWWWWW",
            "W......W.......W",
            "W...P..........W",
            "WWWWWWWWWWWW...W",
            "W........E.....W",
            "W....WWWWWWWWWWW",
            "W..............W",
            "W.........F....W",
            "W.WWWWWWWWWWW..W",
            "W.......W......W",
            "W.S........WWW.W",
            "WWWWWWWWWWWWWWWW"]
SCENE = "main"


def change_scene(name):
    global SCENE

    SCENE = name


def get_scene():
    return SCENE


damage_ui = UI.DealDamage()