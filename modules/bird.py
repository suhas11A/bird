import pygame # type: ignore
from modules.variables import *

class Bird:
    def __init__(self, x, y, bird_type, side, vx = 0, vy = 0, size = BIRD_SIZE):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dt = (1/FPS)
        self.bird_type = bird_type
        self.side = side
        self.size = size
        self.alive = True
        self.active = False
        self.on_cat = False
        self.collisions = 0
        self.image = pygame.image.load(f"./media/images/birds/{self.bird_type}.png")
        if (self.side=="right"):
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def update(self):
        if ((not self.alive) or (not self.active)):
            return
        self.x += self.vx*self.dt
        self.y += self.vy*self.dt
        self.vy += GRAVITY*self.dt

        if self.y < -(HEIGHT/2) or self.x > (WIDTH*4/3) or self.x < -(WIDTH/3):
            self.alive = False
            self.active = False
            self.on_cat = False
        if self.y>((HEIGHT*6/7)-self.size) and self.vy>0 :
            self.y = (HEIGHT*6/7)-self.size
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
            if not i.alive or i.collisions >= MAX_COLLISIONS:
                listt.remove(i)

def draw_prediction (points_list, screen, image):
    if not points_list:
        return
    for i, point in enumerate(points_list):
        size = 17 - 17*i/50
        screen.blit(pygame.transform.scale(image, (size, size)), (point[0]-size/2, point[1]-size/2))