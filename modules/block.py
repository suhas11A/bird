import pygame

BLOCK_COLORS = {
    "wood": (160, 82, 45),
    "ice": (173, 216, 230),
    "stone": (169, 169, 169)
}

BLOCK_HEALTH = {
    "wood": 160,
    "ice": 100,
    "stone": 200
}

BIRD_DAMAGE = {
    "red": {"wood": 40, "ice": 40, "stone": 40},
    "chuck": {"wood": 40, "ice": 10, "stone": 10},
    "blues": {"wood": 10, "ice": 40, "stone": 10},
    "bomb": {"wood": 10, "ice": 10, "stone": 50}
}

class Block:
    def __init__(self, x, y, block_type):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = block_type
        self.color = BLOCK_COLORS[block_type]
        self.health = BLOCK_HEALTH[block_type]

    def draw(self, screen):
        if self.health > 0:
            pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, projectile):
        if (self.health > 0):
            self.rect.colliderect(projectile.get_rect())

    def apply_damage(self, bird_type):
        damage = BIRD_DAMAGE[bird_type][self.type]
        self.health -= damage
        if self.health < 0:
            self.health = 0
