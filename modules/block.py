import pygame # type: ignore
from modules.variables import *

class Block:
    def __init__(self, x, y, block_type, size=30):
        self.size = size
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.type = block_type
        self.color = BLOCK_COLORS[block_type]
        self.health = BLOCK_HEALTH[block_type]

    def draw(self, screen):
        if self.health > 0:
            pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, bird):
        if (self.health > 0):
            return self.rect.colliderect(bird.get_rect())

    def apply_damage(self, bird_type):
        damage = BIRD_DAMAGE[bird_type][self.type]
        self.health -= damage
        if self.health < 0:
            self.health = 0
