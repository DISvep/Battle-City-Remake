import UI
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (52, 207, 235)
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
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_COLOR = (50, 50, 50)
HOVER_COLOR = (100, 100, 100)
FONT_SIZE = 50
BG_COLOR = (30, 30, 30)
wall = pygame.transform.scale(pygame.image.load('textures/wall.jpg'), (SIZE_CELL, SIZE_CELL))
SHOW_FPS = False
VOLUME = 0.5
text_map = ["WWWWWWWWWWWWWWWW",
            "W......W....B..W",
            "W...P..........W",
            "WWWWWWWWWWWW...W",
            "W........E.....W",
            "W..U.WWWWWWWWWWW",
            "W..............W",
            "W.........F....W",
            "W.WWWWWWWWWWW..W",
            "W.......W......W",
            "W.S........WWW.W",
            "WWWWWWWWWWWWWWWW"]
SCENE = "menu"
damage_ui = UI.DealDamage()


def change_scene(name):
    global SCENE

    SCENE = name


def get_scene():
    return SCENE


def get_volume():
    return VOLUME


def change_volume(value):
    global VOLUME

    VOLUME = value


def get_FPS_show():
    return FPS


def change_FPS_show(value):
    global FPS

    FPS = value
