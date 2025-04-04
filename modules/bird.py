import pygame # type: ignore
from modules.variables import *

class Bird:
    def __init__(self, x, y, bird_type, side, vx = 0, vy = 0, dt = (1/120)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dt = dt
        self.bird_type = bird_type
        self.side = side
        self.size = BIRD_SIZE[bird_type]
        self.alive = True
        self.active = False
        self.on_cat = False
        self.collisions = 0
        self.collide_mode = False
        self.image = pygame.image.load(f"./media/birds/{self.bird_type}.png")
        if (self.side=="right"):
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def update(self):
        if ((not self.alive) or (not self.active)):
            return
        self.x += self.vx*self.dt
        self.y += self.vy*self.dt
        self.vy += GRAVITY*self.dt

        if self.y < 0 or self.x > 1200 or self.x < 0:
            self.alive = False
            self.active = False
            self.on_cat = False
        if self.y>((600*6/7)-self.size) :
            self.y = (600*6/7)-self.size
            self.vy *= -e
            self.collisions += 1

    def draw(self, screen):
        if not self.alive:
            return
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

def get_active_bird (*bird_list):
    for listt in bird_list:
        for i in listt:
            if i.active:
                return i
    return None

def draw_birds(screen, *bird_list):
    for listt in bird_list:
        for i in listt:
            i.draw(screen)

def kill_birds(*bird_list):
    for listt in bird_list:
        for i in listt:
            if not i.alive or i.collisions>5:
                listt.remove(i)