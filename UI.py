from abc import ABC, abstractmethod
import pygame
import settings
import logger


pygame.font.init()
font = pygame.font.SysFont(None, 80)


class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.font = pygame.font.SysFont(None, 36)
        self.text = self.font.render(f"-{text}", False, settings.RED)
        self.time = 300
        self.last_time = pygame.time.get_ticks()
        self.pos = (x, y)

    def update(self, scr):
        now = pygame.time.get_ticks()
        if now - self.last_time <= self.time:
            scr.blit(self.text, self.pos)
        else:
            self.kill()


class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass


class DealDamage(Observer):
    def __init__(self):
        self.objects = pygame.sprite.Group()

    def update(self, message):
        text = Text(*message[2], message[1])
        self.objects.add(text)

    def scr_update(self, scr):
        for text in self.objects:
            text.update(scr)


class PlayerHealthBar(Observer):
    def __init__(self, width, height, x, y, hp, max_hp):
        self.pos = (x, y)
        self.width, self.height = width, height

        self.font = pygame.font.SysFont(None, 36)

        self.hp = hp
        self.max_hp = max_hp

    def update(self, message):
        self.hp = message[0]

    def hp_color(self):
        if self.hp > self.max_hp:
            return settings.BLUE
        elif self.hp > self.max_hp // 2:
            return settings.GREEN
        elif self.hp >= self.max_hp // 4:
            return settings.YELLOW
        else:
            return settings.RED

    def scr_update(self, scr):
        ratio = self.hp / self.max_hp
        text = self.font.render(f"{self.hp}/{self.max_hp}", True, settings.BLACK)

        pygame.draw.rect(scr, settings.RED_HP, (*self.pos, self.width, self.height))
        pygame.draw.rect(scr, self.hp_color(), (*self.pos, self.width*ratio, self.height))
        scr.blit(text, self.pos)


class Subject(ABC):
    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self, message):
        pass


class Health(Subject):
    def __init__(self, max_hp):
        self.observers = []

        self.pos = (100, 100)
        self.hp = max_hp
        self.max_hp = max_hp

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def take_damage(self, dmg, x, y):
        self.hp -= dmg
        self.notify_observers((self.hp, dmg, (x, y)))


if __name__ == "__main__":
    pygame.init()

    scr = pygame.display.set_mode(settings.SIZE)

    plr_hp = Health(100)

    hp_bar = PlayerHealthBar(200, 20, 50, 50, plr_hp.hp, plr_hp.max_hp)
    dmg_ui = DealDamage()

    plr_hp.add_observer(hp_bar)
    plr_hp.add_observer(dmg_ui)

    dmg = 0

    game = True
    clock = pygame.time.Clock()
    while game:
        scr.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False

        hp_bar.scr_update(scr)
        dmg_ui.scr_update(scr)

        dmg += 0.3
        take_damage = int(dmg)
        if take_damage > 0:
            plr_hp.take_damage(take_damage)

        if dmg >= 1:
            dmg = 0

        pygame.display.flip()
        clock.tick(settings.FPS)


def create_button(screen, msg, x, y, w, h, ic, ac, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            logger.log(f"Гравець натиснув кнопку, викликаю функцію: {action.__name__}")
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    text_surf = font.render(msg, True, settings.WHITE)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)
