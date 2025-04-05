import pygame # type: ignore
from modules.variables import *

class Block:
    def __init__(self, x, y, block_type, side = "left", size=30):
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

    def draw(self, screen):
        if self.health > 0:
            screen.blit(self.image, (self.x, self.y))

    def check_collision(self, bird):
        if (self.health > 0):
            return self.rect.colliderect(bird.get_rect())

    def apply_damage(self, bird):
        damage = BIRD_DAMAGE[bird.bird_type][self.type]
        self.health -= damage
        if (self.health<=50):
            self.image = pygame.image.load(f"./media/images/blocks/{self.block_type}_2.png")
            if (self.side == "right"):
                self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            
        if self.health < 0:
            self.health = 0

def draw_blocks(screen, *block_list):
    for listt in block_list:
        for i in listt:
            i.draw(screen)

def kill_blocks(*block_list):
    for listt in block_list:
        for i in listt:
            if i.health <=0 :
                listt.remove(i)