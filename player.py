import pygame


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed=0):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (50, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def is_collide(self, sprite):
        return self.rect.colliderect(sprite.rect)


class Player(GameSprite):
    bullets = pygame.sprite.Group()

    def __init__(self, player_image, player_x, player_y, player_speed=0):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.base_image = pygame.transform.scale(pygame.image.load(player_image), (50, 50))
        self.images = {
            "up": pygame.transform.rotate(self.base_image, 180),
            "down": self.base_image,
            "left": pygame.transform.rotate(self.base_image, -90),
            "right": pygame.transform.rotate(self.base_image, 90)
        }
        self.direction = "up"
        self.rect = self.image.get_rect(x=player_x, y=player_y)
        self.shoot_cooldown = 1000  # секунди між пострілами
        self.last_shot_time = pygame.time.get_ticks()

    def update(self, scr, walls):
        pressed_keys = pygame.key.get_pressed()
        vel_x, vel_y = 0, 0  # куди рухається танк

        if pressed_keys[pygame.K_w]:
            vel_y = -self.speed
            self.direction = "up"
        elif pressed_keys[pygame.K_s]:
            vel_y = self.speed
            self.direction = "down"
        elif pressed_keys[pygame.K_d]:
            vel_x = self.speed
            self.direction = "right"
        elif pressed_keys[pygame.K_a]:
            vel_x = -self.speed
            self.direction = "left"

        # Оновлюємо зображення відповідно до напрямку
        self.image = self.images[self.direction]

        # Перевірка на зіткнення зі стінами
        self.rect.x += vel_x
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x -= vel_x

        self.rect.y += vel_y
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y -= vel_y

        self.rect.clamp_ip(scr.get_rect())

        # Стрільба
        if pressed_keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot_time >= self.shoot_cooldown:
                new_bullet = Bullet("textures/bullet.png", self.rect.centerx, self.rect.centery, self.direction, 10)
                Player.bullets.add(new_bullet)
                self.last_shot_time = now

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, x, y, direction, speed):
        super().__init__()

        self.base_image = pygame.transform.scale(pygame.image.load(bullet_image).convert_alpha(), (100, 100))
        self.images = {
            "up": pygame.transform.rotate(self.base_image, -90),
            "down": pygame.transform.rotate(self.base_image, 90),
            "left": pygame.transform.rotate(self.base_image, 180),
            "right": self.base_image
        }

        self.image = self.images[direction]
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.direction = direction
        self.speed = speed

    def update(self, walls):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        if pygame.sprite.spritecollideany(self, walls):
            self.kill()

        # Видаляємо кулю, якщо вона виходить за межі екрану
        if self.rect.bottom < 0 or self.rect.top > 600 or self.rect.right < 0 or self.rect.left > 700:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)