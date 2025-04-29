import pygame # type: ignore
import numpy as np
from modules.variables import *

class Bird:
    def __init__(self, image_pack, ground, x, y, bird_type, side, vx = 0, vy = 0, size = BIRD_SIZE, alive = True, active = False, on_cat = False, on_power = False):
        self.image_pack = image_pack
        self.ground = ground
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dt = (1/FPS)
        self.bird_type = bird_type
        self.side = side
        self.size = size
        self.alive = alive
        self.active = active
        self.on_cat = on_cat
        self.on_power = on_power
        self.collisions = 0
        self.og_astro_image = image_pack[1]
        if (self.side=="right"): # Flip the bird if its a right bird
            self.og_astro_image = pygame.transform.flip(self.og_astro_image, True, False)
        self.astro_image = pygame.transform.scale(self.og_astro_image, (1.5*self.size, 1.8*self.size))
        self.og_image = image_pack[0][bird_type]
        if (self.side=="right"):
                self.og_image = pygame.transform.flip(self.og_image, True, False)
        self.image = pygame.transform.scale(self.og_image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.wind = None
        self.explosion_frames = []
        self.explosion_index = 0
        self.explosion_time = 0
        self.explosion_pos = None
        if self.bird_type == "bomb":
            self.explosion_frames = image_pack[2]

    def update(self): # go in a parabola and if bomb powered adjust the timer
        if ((not self.alive) or (not self.active)):
            return
        self.x += self.vx*self.dt/1.5
        self.y += self.vy*self.dt/1.5
        if (self.ground<0):
            pass
        else:
            self.vy += GRAVITY*self.dt/1.5
        wind = self.wind
        if (wind!=0):
            self.vx += (wind**2)*(wind/abs(wind))*WIND_MUL*self.dt/1.5

        if self.y < -(50) or self.x > (WIDTH+(40)) or self.x < -(40) or self.y> HEIGHT+80:
            self.alive = False
            self.active = False
            self.on_cat = False
        if self.y>((HEIGHT-self.ground)-self.size) and self.vy>0 :
            self.y = (HEIGHT-self.ground)-self.size
            self.vy *= -e
            self.collisions += 1

        if self.bird_type == "bomb" and self.on_power and self.alive:
            self.x = self.explosion_pos[0]
            self.y = self.explosion_pos[1]
            self.vx = 0
            self.vy = 0
            now = pygame.time.get_ticks()
            if self.explosion_index < len(self.explosion_frames):
                if now - self.explosion_time > 75:
                    self.explosion_time = now
                    self.explosion_index += 1
            else:
                self.alive = False

    def apply_power(self, bird_list, fortress): # Is called on powering up the bird
        if self.bird_type == "blues":
            self.active = False
            self.alive = False
            self.on_power = True
            wind = self.wind
            bird_list.append(Bird(self.image_pack, self.ground, self.x, self.y, self.bird_type, self.side, self.vx, self.vy, self.size, True, True, False, True))
            temp_bird = bird_list[-1]
            temp_bird.explosion_pos = (temp_bird.x, temp_bird.y)
            bird_list.append(Bird(self.image_pack, self.ground, self.x, self.y, self.bird_type, self.side, self.vx+50, self.vy+200, self.size, True, True, False, True))
            bird_list.append(Bird(self.image_pack, self.ground, self.x, self.y, self.bird_type, self.side, self.vx-50, self.vy-200, self.size, True, True, False, True))
            for i in range(3):
                bird_list[-(i+1)].wind = wind
        elif self.bird_type == "red":
            self.x -= (FACTOR_RED-1)*(BIRD_SIZE)/2
            self.y -= (FACTOR_RED-1)*(BIRD_SIZE)/2
            self.size += (FACTOR_RED-1)*BIRD_SIZE
            self.image = pygame.transform.scale(self.og_image, (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)
            self.astro_image = pygame.transform.scale(self.og_astro_image, (1.5*self.size, 1.8*self.size))
            if (self.size >= 1.5*BIRD_SIZE):
                self.on_power = True
        elif self.bird_type == "bomb":
            self.on_power = True
            self.vy = 0
            self.vx = 0
            self.explosion_pos = (self.x, self.y)
            self.explosion_time = pygame.time.get_ticks()
            for block in fortress.list:
                dist = np.linalg.norm(np.array(self.explosion_pos)-np.array(block.get_centre())+np.array((self.size, self.size)))
                damage = BIRD_DAMAGE[self.bird_type][block.type]*(2/(1+(abs(round(dist/75))**2)))
                block.health -= damage
                block.update_image(damage)
        elif self.bird_type == "chuck":
            self.on_power = True
            self.vx *= FACTOR_CHUCK
            self.vy *= FACTOR_CHUCK

    def draw(self, screen): # Draws the bird or the bomb explosion at a position
        if not self.alive:
            return
        if self.bird_type == "bomb" and self.on_power and self.explosion_index < len(self.explosion_frames):
            img = self.explosion_frames[self.explosion_index]
            screen.blit(img, (self.explosion_pos[0] - img.get_width() / 2, self.explosion_pos[1] - img.get_height() / 1.8))
            return
        elif (self.bird_type!="bomb" or not self.on_power):
            screen.blit(self.image, (self.x, self.y))
            if (self.ground<0):
                if (self.vx>0):
                    screen.blit(self.astro_image, (self.x-(self.size/2.4), self.y-(self.size/3)))
                elif(self.vx<0):
                    screen.blit(self.astro_image, (self.x-(self.size*0.5-self.size/2.4), self.y-(self.size/3)))
                else:
                    if (self.side == "left"):
                        screen.blit(self.astro_image, (self.x-(self.size/2.4), self.y-(self.size/3)))
                    else:
                        screen.blit(self.astro_image, (self.x-(self.size*0.5-self.size/2.4), self.y-(self.size/3)))

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

def kill_birds(*bird_list): # Removes the bird from bird list if its dead or if its has more than MAX_COLLISIONS
    for listt in bird_list:
        for i in listt:
            if not i.alive or i.collisions >= MAX_COLLISIONS:
                listt.remove(i)

def draw_prediction (points_prediction, screen, image):
    if not points_prediction:
        return
    for i, point in enumerate(points_prediction):
        size = BALL_SIZE - BALL_SIZE*i/50
        screen.blit(pygame.transform.scale(image, (size, size)), (point[0]-size/2, point[1]-size/2))

def draw_path(path_points, screen, image, bird):
    if bird is None:
        return
    if not path_points:
        return
    for i, point in enumerate(path_points):
        size = max(BALL_SIZE - BALL_SIZE*i/75, 0)
        screen.blit(pygame.transform.scale(image, (size, size)), (point[0]-size/2, point[1]-size/2))
    if bird.explosion_pos is None:
        return
    point = bird.explosion_pos
    size = 1.5*BALL_SIZE
    screen.blit(pygame.transform.scale(image, (size, size)), (point[0]+BIRD_SIZE/2-size/2, point[1]+BIRD_SIZE/2-size/2))