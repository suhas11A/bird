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

# Catapults
catapult_image = pygame.image.load("./media/Sling.webp")
catapult_image = pygame.transform.scale(catapult_image, (50, 100))
catapult_left = (100, HEIGHT - 189)
catapult_right = (WIDTH - 150, HEIGHT - 186)
#Back-ground
background_img = pygame.image.load("./media/back.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
# Fortresses
fortress_left = [Block(300 + i * 35, HEIGHT - 60, "stone") for i in range(3)]
fortress_right = [Block(WIDTH - 400 + i * 35, HEIGHT - 60, "wood") for i in range(3)]

# Initiate
bird = None
turn = "left"
running = True

while running:
    clock.tick(FPS)
    # Check-Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not bird:
            mx, my = pygame.mouse.get_pos()
            if turn == "left":
                power_x = (mx - catapult_left[0])
                power_y = (my - catapult_left[1])
                bird = Bird(catapult_left[0], catapult_left[1], power_x, power_y,"red")
            else:
                power_x = (mx - catapult_right[0])
                power_y = (my - catapult_right[1])
                bird = Bird(catapult_right[0], catapult_right[1], power_x, power_y,"red")

    # Update bird
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

    # Draw catapults and background
    screen.blit(background_img, (0, 0))
    screen.blit(catapult_image, catapult_left)
    screen.blit(catapult_image, catapult_right)

    for block in fortress_left:
        block.draw(screen)
    for block in fortress_right:
        block.draw(screen)

    if bird:
        bird.draw(screen)

    pygame.display.flip()

pygame.quit()