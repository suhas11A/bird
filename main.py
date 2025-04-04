import pygame # type: ignore
import random
from modules.bird import *
from modules.block import *
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
block_randoms = [BLOCK_OPTIONS[i%3] for i in range(10)]
random.shuffle(block_randoms)
fortress_left = [Block(50 + i * 31, HEIGHT*(6/7)-30-31*j, block_randoms[k],"left") for k,(i,j) in enumerate([(i, j) for i in range(2) for j in range(5)])]
fortress_right = [Block(WIDTH - 80 - i * 31, HEIGHT*(6/7)-30-31*j, block_randoms[k],"right") for k,(i,j) in enumerate([(i, j) for i in range(2) for j in range(5)])]

# Initiation
left_birds = [Bird(catapult_left[0]+CATAPULT_SIZE[0]+38*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE[type], type, "left") for i,type in enumerate(BIRD_OPTIONS)]
right_birds = [Bird(catapult_right[0]-38*i-35, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE[type], type, "right") for i,type in enumerate(BIRD_OPTIONS)]
turn = "left"
running = True
mouse_pos = None
active_rectangle = None
mouse_offset = None
mouse_down = False
active_projectile = None


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
    draw_blocks(screen, fortress_right, fortress_left)
    draw_birds(screen, left_birds, right_birds)

    active_bird = get_active_bird(left_birds, right_birds)
    if not active_bird:
        for event in events:
            for i in (left_birds if turn=="left" else right_birds):
                if (event.type == pygame.MOUSEBUTTONDOWN and i.get_rect().collidepoint(pygame.mouse.get_pos())):
                    active_bird = i
                    active_bird.active = True
                    active_bird.on_cat = True
                    break
        if active_bird:
            active_bird.x = (catapult_left if turn=="left" else catapult_right)[0]
            active_bird.y = (catapult_left if turn=="left" else catapult_right)[1]
    elif active_bird.on_cat and not mouse_down:
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN and active_bird.get_rect().collidepoint(pygame.mouse.get_pos())):
                mouse_down = True
                mouse_pos = pygame.mouse.get_pos()
                active_rectangle = active_bird.get_rect()
                mouse_offset = (mouse_pos[0]-active_bird.x), (mouse_pos[1]-active_bird.y)
                active_bird_home_box = active_bird.get_rect()
    elif active_bird.on_cat and mouse_down:
        active_bird.x, active_bird.y = (pygame.mouse.get_pos()[0] - mouse_offset[0], pygame.mouse.get_pos()[1] - mouse_offset[1])
        for event in events:
            if (event.type == pygame.MOUSEBUTTONUP and not active_rectangle.collidepoint(pygame.mouse.get_pos())):
                active_bird.on_cat = False
                mouse_down = False
                active_bird.vx, active_bird.vy = (10*(mouse_pos[0]-pygame.mouse.get_pos()[0]),10*(mouse_pos[1]-pygame.mouse.get_pos()[1]))
                turn = "left" if turn=="right" else "right"
            elif (event.type == pygame.MOUSEBUTTONUP and active_rectangle.collidepoint(pygame.mouse.get_pos())):
                active_bird.on_cat = True
                mouse_down = False
                active_bird.x, active_bird.y = [active_rectangle[i] for i in (0,1)]

    else:
        active_fortress = fortress_left if turn=="left" else fortress_right
        for i in active_fortress:
            if i.check_collision(active_bird):
                active_bird.collide_mode = True
                i.apply_damage(active_bird)
        if active_bird.collide_mode:
            active_bird.vx *= -e
            active_bird.collide_mode = False
            active_bird.collisions += 1
        active_bird.update()

    kill_birds(left_birds, right_birds)
    kill_blocks(fortress_left, fortress_right)
    pygame.display.flip()

pygame.quit()