import pygame # type: ignore
from modules.variables import *

class Bird:
    def __init__(self, x, y, bird_type, side, vx = 0, vy = 0, dt = (1/60)):
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

    def update(self):
        if ((not self.alive) or (not self.active)):
            return
        self.x += self.vx*self.dt
        self.y += self.vy*self.dt
        self.vy += GRAVITY*self.dt

        if self.y > 600 or self.y < 0 or self.x > 1200 or self.x < 0:
            self.alive = False
            self.active = False
            self.on_cat = False

    def draw(self, screen):
        if not self.alive:
            return
        bird_image = None
        if (self.bird_type=="red"):
            bird_image = pygame.image.load("./media/red.png")
        elif (self.bird_type=="chuck"):
            bird_image = pygame.image.load("./media/chuck.png")
        elif (self.bird_type=="blues"):
            bird_image = pygame.image.load("./media/blues.png")
        elif (self.bird_type=="bomb"):
            bird_image = pygame.image.load("./media/bomb.png")

        bird_image = pygame.transform.scale(bird_image, (self.size, self.size))
        if (self.side=="right"):
            bird_image = pygame.transform.flip(bird_image, True, False)
        screen.blit(bird_image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

def get_active_bird (*bird_list):
    for listt in bird_list:
        for i in listt:
            if i.active:
                return i
    return None