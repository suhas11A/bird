import pygame # type: ignore
from modules.variables import *

class Block:
    def __init__(self, x, y, block_type, side = "left", size = BLOCK_SIZE):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.type = block_type
        self.block_type = block_type
        self.health = BLOCK_HEALTH[block_type]
        self.side = side
        self.image = pygame.image.load(f"./media/images/blocks/{self.block_type}_1.png")
        if (self.side=="right"):
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.vx = 0
        self.vy = 0
        self.is_falling = False
        self.dt = 1/FPS
        self.mask = pygame.mask.from_surface(self.image)

    def get_centre(self):
        return (self.x+self.size/2, self.y+self.size/2)
    
    def draw(self, screen):
        if self.health > 0:
            screen.blit(self.image, (self.x, self.y))

    def check_collision(self, bird, collision_face):
        if (self.health <= 0):
            return False, collision_face
        block_rect = self.rect
        bird_rect  = bird.get_rect()
        offset = (
            int(bird_rect.x - block_rect.x),
            int(bird_rect.y - block_rect.y)
        )
        if self.mask.overlap(bird.mask, offset):
            if ((self.x < bird.x + bird.size <= self.x + bird.vx * bird.dt* 2) and bird.side=="left"):
                return True, "side"
            elif ((self.x + self.size + bird.vx * bird.dt * 2 <= bird.x < self.x + self.size) and bird.side=="right"):
                return True, "side"
            else:
                return True, "top"
        return False, collision_face

    def update_image(self):
        if (self.health<=50):
            self.image = pygame.image.load(f"./media/images/blocks/{self.block_type}_2.png")
            if (self.side == "right"):
                self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def apply_damage(self, bird):
        damage = BIRD_DAMAGE[bird.bird_type][self.type]*(((bird.vx**2+bird.vy**2)**0.5)/1000)*(self.size/BIRD_SIZE)
        self.health -= damage
        self.update_image()
        if self.health < 0:
            self.health = 0

def draw_blocks(screen, *block_list):
    for listt in block_list:
        for i in listt:
            i.draw(screen)