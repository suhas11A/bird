import pygame # type: ignore
from modules.bird import *
from modules.block import Block
from modules.variables import *

pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Birds - 2 Player")
clock = pygame.time.Clock()
FPS = 60

# Catapult positions
catapult_left = pygame.Rect(100, HEIGHT - 150, 50, 100)
catapult_right = pygame.Rect(WIDTH - 150, HEIGHT - 150, 50, 100)

# Fortresses
fortress_left = [Block(300 + i * 35, HEIGHT - 60, "stone") for i in range(3)]
fortress_right = [Block(WIDTH - 400 + i * 35, HEIGHT - 60, "wood") for i in range(3)]

# Launch state
bird = None
turn = "left"
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not bird:
            mx, my = pygame.mouse.get_pos()
            if turn == "left":
                power_x = (mx - catapult_left.x)
                power_y = (my - catapult_left.y)
                bird = Bird(catapult_left.centerx, catapult_left.centery, power_x, power_y,"red")
            else:
                power_x = (mx - catapult_right.x)
                power_y = (my - catapult_right.y)
                bird = Bird(catapult_right.centerx, catapult_right.centery, power_x, power_y,"red")

    # Update
    if bird:
        bird.update()
        # Check collision
        blocks = fortress_right if turn == "left" else fortress_left
        for block in blocks:
            if block.check_collision(bird):
                block.apply_damage("red")
                bird.active = False

        if not bird.active:
            bird = None
            turn = "right" if turn == "left" else "left"

    # Draw
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (139, 69, 19), catapult_left)
    pygame.draw.rect(screen, (139, 69, 19), catapult_right)

    for block in fortress_left:
        block.draw(screen)
    for block in fortress_right:
        block.draw(screen)

    if bird:
        bird.draw(screen)

    pygame.display.flip()

pygame.quit()