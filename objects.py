import pygame
import logging
import AI
from settings import *


# Налаштування логування
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Tank(pygame.sprite.Sprite):
    def __init__(self, image, x, y, hp=100, speed=3.5):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(image), (45, 45))
        self.images = {
            "up": pygame.transform.rotate(self.image, 180),
            "down": self.image,
            "left": pygame.transform.rotate(self.image, -90),
            "right": pygame.transform.rotate(self.image, 90)
        }
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.direction = "up"
        self.speed = speed

        self.stuck = False

        self.render = True

        self.hp = hp
        self.shoot_cooldown = 1000  # секунди між пострілами

        self.vel_x, self.vel_y = 0, 0

    def take_damage(self, dmg):
        self.hp -= dmg
        logger.info(f"Об'єкт отримав {dmg} шкоди. Здоров'я: {self.hp}")
        if self.hp <= 0:
            if isinstance(self, Player):
                logger.info(f"Гравець вмер")
                change_scene('death')
                self.render = False
                self.kill()
            else:
                logger.info(f"Об'єкт вмер")
                self.kill()

    def check_obstacles(self, walls):
        self.rect.x += self.vel_x
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= self.vel_x * 1.1
            self.stuck = True

        self.rect.y += self.vel_y
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y -= self.vel_y * 1.1
            self.stuck = True

    def stop(self):
        self.vel_x, self.vel_y = 0, 0


class Player(Tank):
    bullets = pygame.sprite.Group()

    def __init__(self, player_image, x, y, hp=200, speed=3.5):
        super().__init__(player_image, x, y, hp, speed)
        self.last_shot_time = pygame.time.get_ticks()

    def update(self, scr, walls):
        pressed_keys = pygame.key.get_pressed()
        self.stop()

        if pressed_keys[pygame.K_w]:
            self.vel_y = -self.speed
            self.direction = "up"
            logger.debug("Гравець натиснув 'W' - рух вгору")
        elif pressed_keys[pygame.K_s]:
            self.vel_y = self.speed
            self.direction = "down"
            logger.debug("Гравець натиснув 'S' - рух вниз")
        elif pressed_keys[pygame.K_d]:
            self.vel_x = self.speed
            self.direction = "right"
            logger.debug("Гравець натиснув 'D' - рух праворуч")
        elif pressed_keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.direction = "left"
            logger.debug("Гравець натиснув 'A' - рух ліворуч")

        # Оновлюємо зображення відповідно до напрямку
        self.image = self.images[self.direction]

        self.check_obstacles(walls)

        self.rect.clamp_ip(scr.get_rect())

        # Стрільба
        if pressed_keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot_time >= self.shoot_cooldown:
                new_bullet = Bullet("textures/bullet.png", self.rect.centerx, self.rect.centery, self.direction, 10, self)
                Player.bullets.add(new_bullet)
                self.last_shot_time = now
                logger.info("Гравець зробив постріл")

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Enemy(Tank):
    bullets = pygame.sprite.Group()

    def __init__(self, image, x, y, walls, player, hp=100, speed=2.5):
        super().__init__(image, x, y, hp, speed)
        self.last_shot_time = pygame.time.get_ticks()
        self.walls = walls
        self.hp = 50
        self.AI = AI.Enemy(self.rect.centerx, self.rect.centery, self.walls, player, self)

    def go_left(self):
        self.vel_x = -self.speed
        self.direction = "left"

    def go_right(self):
        self.vel_x = self.speed
        self.direction = "right"

    def go_up(self):
        self.vel_y = -self.speed
        self.direction = "up"

    def go_down(self):
        self.vel_y = self.speed
        self.direction = "down"

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_cooldown:
            new_bullet = Bullet("textures/bullet.png", self.rect.centerx, self.rect.centery, self.direction, 10, self)
            Player.bullets.add(new_bullet)
            self.last_shot_time = now

    def update(self, scr, plr):

        self.check_obstacles(self.walls)

        self.image = self.images[self.direction]

        scr.blit(self.image, self.rect)
        self.AI.update(scr)


class FastEnemy(Enemy):
    bullets = pygame.sprite.Group()

    def __init__(self, image, x, y, walls, player, hp=25, speed=3.5):
        super().__init__(image, x, y, walls, player, hp=hp, speed=speed)


class FatEnemy(Enemy):
    bullets = pygame.sprite.Group()

    def __init__(self, image, x, y, walls, player, hp=200, speed=1):
        super().__init__(image, x, y, walls, player, hp=hp, speed=speed)
        self.shoot_cooldown = 3500

        def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot_time >= self.shoot_cooldown:
                new_bullet = Bullet("textures/bullet.png", self.rect.centerx, self.rect.centery, self.direction, 10, self, dmg=50)
                Player.bullets.add(new_bullet)
                self.last_shot_time = now


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, x, y, direction, speed, owner, dmg=25):
        super().__init__()

        self.base_image = pygame.transform.scale(pygame.image.load(bullet_image).convert_alpha(), (100, 10))
        self.images = {
            "up": pygame.transform.rotate(self.base_image, -90),
            "down": pygame.transform.rotate(self.base_image, 90),
            "left": pygame.transform.rotate(self.base_image, 180),
            "right": self.base_image
        }

        self.x, self.y = x, y

        if direction == 'up':
            self.y -= 20
        elif direction == "down":
            self.y += 20
        elif direction == "right":
            self.x += 20
        elif direction == "left":
            self.x -= 20

        self.image = self.images[direction]
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)
        self.direction = direction

        self.speed = speed
        self.dmg = dmg
        self.owner = owner

    def update(self, walls, entities):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        collides_walls = pygame.sprite.spritecollide(self, walls, False)
        for wall in collides_walls:
            wall.take_damage(self.dmg)
            self.kill()
            logger.debug("Куля зіткнулася зі стіною")

        collides = pygame.sprite.spritecollide(self, entities, False)
        for sprite in collides:
            if sprite != self.owner and isinstance(sprite, Tank):
                sprite.take_damage(self.dmg)
                self.kill()

        # Видаляємо кулю, якщо вона виходить за межі екрану
        if self.rect.bottom < 0 or self.rect.top > 600 or self.rect.right < 0 or self.rect.left > 700:
            self.kill()
            logger.debug("Куля вийшла за межі екрану")
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.img = pygame.Surface((size, size))  # потрібна текстурка
        self.img.fill((120, 60, 0))
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hp = 50

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()