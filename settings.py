WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
FPS = 60
SIZE_CELL = 50
ROWS = 12
COLS = 16
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