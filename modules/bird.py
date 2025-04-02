import pygame # type: ignore
from modules.variables import *

GRAVITY = -359.8

class Bird:
    def __init__(self, x, y, vx, vy, bird_type, FPS=60, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.bird_type = bird_type
        self.FPS = FPS
        self.radius = 10
        self.color = color
        self.active = True

    def update(self):
        if not self.active:
            return
        self.x += self.vx*(1/self.FPS)
        self.y += self.vy*(1/self.FPS)
        self.vy -= GRAVITY*(1/self.FPS)

        if self.y > 600 or self.x < 0 or self.x > 1200 or self.y < 0:
            self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
