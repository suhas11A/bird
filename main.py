import pygame # type: ignore
import random
from modules.bird import Bird
from modules.block import Block
from modules.variables import *

pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Birds - 2 Player")
clock = pygame.time.Clock()

# Catapults
catapult_image = pygame.image.load("./media/Sling.webp")
catapult_image = pygame.transform.scale(catapult_image, CATAPULT_SIZE)
catapult_left = (WIDTH/7, HEIGHT*(6/7)-CATAPULT_SIZE[1])
catapult_right = (WIDTH*(6/7)-CATAPULT_SIZE[0], HEIGHT*(6/7)-CATAPULT_SIZE[1])
# Back-ground
background_img = pygame.image.load("./media/back.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
# Fortresses
block_randoms = random.choices(BLOCK_OPTIONS, k=10)
fortress_left = [Block(50 + i * 31, HEIGHT*(6/7)-30-31*j, block_randoms[k]) for k,(i,j) in enumerate([(i, j) for i in range(2) for j in range(5)])]
fortress_right = [Block(WIDTH - 80 - i * 31, HEIGHT*(6/7)-30-31*j, block_randoms[k]) for k,(i,j) in enumerate([(i, j) for i in range(2) for j in range(5)])]

# Initiation
left_birds = [Bird(catapult_left[0]+CATAPULT_SIZE[0]+38*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE[type], type, "left") for i,type in enumerate(BIRD_OPTIONS)]
right_birds = [Bird(catapult_right[0]-38*i-20, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE[type], type, "right") for i,type in enumerate(BIRD_OPTIONS)]
turn = "left"
running = True

def get_active_bird (*bird_list):
    for listt in bird_list:
        for i in listt:
            if i.active:
                return i
    return None

while running:
    dt = clock.tick(FPS)
    # Check-Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Draw catapults and background
    screen.fill((255, 255, 255))
    screen.blit(background_img, (0, 0))
    screen.blit(catapult_image, catapult_left)
    screen.blit(catapult_image, catapult_right)

    for block in fortress_left:
        block.draw(screen)
    for block in fortress_right:
        block.draw(screen)
    
    if not get_active_bird(left_birds, right_birds):
        for i in left_birds:
            i.draw(screen)
        for i in right_birds:
            i.draw(screen)


    pygame.display.flip()

pygame.quit()