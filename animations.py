import pygame
import os
from settings import *


class Animation(pygame.sprite.Sprite):
    def __init__(self, path, loops, size, parent):
        super().__init__()

        self.images = os.listdir(path)
        self.length = len(self.images)
        self.FPS = FPS / self.length
        self.cur_image = 0
        self.loops = loops
        self.loop = 0
        self.size = size
        self.path = path
        self.parent = parent

        self.image = pygame.transform.scale(pygame.image.load(f"{self.path}/{self.images[self.cur_image]}"), (self.size, self.size))
        self.rect = self.image.get_rect(x=self.parent.rect.x, y=self.parent.rect.y)

        self.last_time = pygame.time.get_ticks()

    def update(self, scr):
        self.image = pygame.transform.scale(pygame.image.load(f"{self.path}/{self.images[self.cur_image]}"), (self.size, self.size))
        self.rect = self.image.get_rect(x=self.parent.rect.x, y=self.parent.rect.y)
        scr.blit(self.image, self.rect)

        if self.cur_image <= self.length-1:
            cur_time = pygame.time.get_ticks()
            if self.last_time + self.FPS*10 < cur_time:
                self.cur_image += 1
                self.last_time = pygame.time.get_ticks()
        if self.cur_image > self.length - 1:
            if self.loop < self.loops:
                self.cur_image = 0
                self.loop += 1
            else:
                self.kill()
