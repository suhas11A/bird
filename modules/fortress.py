import pygame # type: ignore
import random
from modules.block import *
from modules.variables import *

class Fortress:
    def __init__(self, side, width = fortress_width, height = fortress_height):
        self.side = side
        block_randoms = [BLOCK_OPTIONS[i%3] for i in range(width * height)]
        random.shuffle(block_randoms)
        if (side=="left"):
            self.list = [Block(50 + i * 31, HEIGHT*(6/7)-30-31*j, block_randoms[k],"left") for k,(i,j) in enumerate([(i, j) for i in range(width) for j in range(height)])]
        else :
            self.list = [Block(WIDTH - 80 - i * 31, HEIGHT*(6/7)-30-31*j, block_randoms[k],"right") for k,(i,j) in enumerate([(i, j) for i in range(width) for j in range(height)])]
        self.width = width
        self.height = height
    def draw(self, screen):
        for i in self.list:
            i.draw(screen)
    def __bool__(self):
      return bool(self.list)
    def update(self, bird):
        collision_face = None
        collide_mode = False
        for i in self.list:
            has_collided, collision_face = i.check_collision(bird, collision_face)
            if has_collided:
                collide_mode = True
                i.apply_damage(bird)
        if collide_mode:
            if (collision_face=="side"):
                bird.x -= bird.vx*bird.dt
                bird.vx *= -e
                bird.image = pygame.transform.flip(bird.image, True, False)
            else:
                bird.y -= bird.vy*bird.dt
                bird.vy *= -e
            collide_mode = False
            bird.collisions += 1
    
def kill_fortress(*fortress_list):
    for fortress in fortress_list:
        for i in fortress.list:
            if i.health <=0 :
                fortress.list.remove(i)