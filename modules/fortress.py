import pygame # type: ignore
import random
import numpy as np
from modules.block import *
from modules.variables import *

class Fortress:
    def __init__(self, image_pack,  ground, side, width = fortress_width, height = fortress_height):
        if (ground<0):
            ground = (HEIGHT/7)
            self.theme = "space"
        else:
            self.theme = "not space"
        self.side = side
        block_randoms = [BLOCK_OPTIONS[i%3] for i in range(width * height)]
        random.shuffle(block_randoms)
        if (side=="left"):
            self.list = [Block(image_pack, 50 + i * (BLOCK_SIZE), HEIGHT-ground-BLOCK_SIZE-(BLOCK_SIZE)*j, block_randoms[k],"left") for k,(i,j) in enumerate([(i, j) for i in range(width) for j in range(height)])]
        else :
            self.list = [Block(image_pack, WIDTH - (50+BLOCK_SIZE) - i * (BLOCK_SIZE), HEIGHT-ground-BLOCK_SIZE-(BLOCK_SIZE)*j, block_randoms[k],"right") for k,(i,j) in enumerate([(i, j) for i in range(width) for j in range(height)])]
        self.width = width
        self.height = height
        self.cordinates = [(i, j) for i in range(width) for j in range(height)]
        self.dictionary = dict(zip( self.cordinates, self.list))
        self.ground = ground

    def draw(self, screen):
        for i in self.list:
            i.draw(screen)

    def __bool__(self):
      return bool(self.list)
    
    def update(self, bird):
        if (bird.bird_type=="bomb" and bird.on_power):
            return
        collision_face = None
        collide_mode = False
        for i in self.list:
            has_collided, collision_face = i.check_collision(bird, collision_face)
            if has_collided:
                i.apply_damage(bird)
                collide_mode = True
        if collide_mode:
            if (collision_face=="side"):
                bird.x -= bird.vx*bird.dt/1.5
                bird.vx *= -e
                bird.image = pygame.transform.flip(bird.image, True, False)
                bird.og_image = pygame.transform.flip(bird.og_image, True, False)
                bird.og_astro_image = pygame.transform.flip(bird.og_astro_image, True, False)
                bird.astro_image = pygame.transform.flip(bird.astro_image, True, False)
            else:
                bird.y -= bird.vy*bird.dt/1.5
                bird.vy *= -e
            collide_mode = False
            bird.collisions += 1

    def block_fall(self):
        if (self.theme=="space"):
            return
        for block in self.list:
            if block.is_falling:
                block.y += block.vy*block.dt/1.5
                block.x += block.vx*block.dt/1.5
                block.vy += GRAVITY*block.dt/3
                block.rect = pygame.Rect(block.x, block.y, block.size, block.size)
        for cord in [(i, j) for i in range(self.width) for j in range(self.height)]:
            if cord not in self.cordinates:
                up_block_cords = [(cord[0],j) for j in range(cord[1]+1,self.height)]
                for cord_ in up_block_cords:
                    if cord_ in self.dictionary:
                        self.dictionary[cord_].is_falling = True
        for block in self.list:
            if block.is_falling:
                if block.y + block.size >= HEIGHT - self.ground: 
                    block.y = HEIGHT - self.ground - block.size
                    block.vy = 0
                    block.vx = 0
                    block.is_falling = False
                    continue
                for other in self.list:
                    if other == block or other.is_falling:
                        continue
                    if (abs(block.x - other.x) < 1) and ((block.y + block.size) > other.y):
                        block.y = other.y - block.size
                        block.vy = 0
                        block.vx = 0
                        block.is_falling = False
                        break
            
    
def kill_fortress(*fortress_list):
    for fortress in fortress_list:
        to_be_killed = []
        for i in range(len(fortress.list)):
            if fortress.list[i].health <=0 :
                to_be_killed.append(i)
        to_be_killed.reverse()
        for i in to_be_killed:
            fortress.list.pop(i)
            fortress.dictionary.pop(fortress.cordinates[i])
            fortress.cordinates.pop(i)