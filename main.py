import pygame # type: ignore
import random
import math
from modules.bird import *
from modules.block import *
from modules.variables import *
from modules.text import *
from modules.input import *

pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
angry_font = lambda x : pygame.font.Font("./media/fonts/angry.ttf", x)
pygame.display.set_caption("Angry Birds - 2 Player")
clock = pygame.time.Clock()

# Menu
main_text = Text(WIDTH/2,HEIGHT/10,"Angry Birds", angry_font(50), (0,0,0))
player1_text = Text(WIDTH/3.5,HEIGHT/4.5,"Name of player 1", angry_font(30), (0,0,0))
colon1_text = Text(WIDTH/2,HEIGHT/4.5,":", angry_font(30), (0,0,0))
player2_text = Text(WIDTH/3.5,HEIGHT/3,"Name of player 2", angry_font(30), (0,0,0))
colon2_text = Text(WIDTH/2,HEIGHT/3,":", angry_font(30), (0,0,0))
input_list = [Input(WIDTH - WIDTH/3.5,HEIGHT/i,"", angry_font(30), "dead", (0,0,0)) for i in [4.5, 3]]
play_surface = pygame.image.load("./media/images/play.png")
play_surface = pygame.transform.scale(play_surface, (WIDTH/7, HEIGHT/9.5))
play_rect = play_surface.get_rect(center=(WIDTH/2,HEIGHT/1.9))
# Catapults
catapult_image = pygame.image.load("./media/images/Sling.webp")
catapult_image = pygame.transform.scale(catapult_image, CATAPULT_SIZE)
catapult_left = (WIDTH/7, HEIGHT*(6/7)-CATAPULT_SIZE[1])
catapult_right = (WIDTH*(6/7)-CATAPULT_SIZE[0], HEIGHT*(6/7)-CATAPULT_SIZE[1])
# Back-ground
background_img = pygame.image.load("./media/images/back.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
# Fortresses
block_randoms = [BLOCK_OPTIONS[i%3] for i in range(10)]
random.shuffle(block_randoms)
fortress_left = [Block(50 + i * 31, HEIGHT*(6/7)-30-31*j, block_randoms[k],"left") for k,(i,j) in enumerate([(i, j) for i in range(2) for j in range(5)])]
fortress_right = [Block(WIDTH - 80 - i * 31, HEIGHT*(6/7)-30-31*j, block_randoms[k],"right") for k,(i,j) in enumerate([(i, j) for i in range(2) for j in range(5)])]
# Prediction image
circle_image = pygame.image.load("./media/images/circle.png")
# Initiation
left_birds = [Bird(catapult_left[0]+CATAPULT_SIZE[0]+38*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE[type], type, "left") for i,type in enumerate(BIRD_OPTIONS)]
right_birds = [Bird(catapult_right[0]-38*i-35, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE[type], type, "right") for i,type in enumerate(BIRD_OPTIONS)]
turn = "left"
running = True
running_menu = not False
running_game = True
running_end_screen = False
win = None
mouse_pos = None
active_rectangle = None
mouse_offset = None
mouse_down = False
active_projectile = None
bird_choosing_left = False
bird_choosing_right = False
left_no = None
right_no = None
points_list = []

while running:
    dt = clock.tick(FPS)
    # Check-Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    if running_menu:
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        main_text.draw(screen)
        player1_text.draw(screen)
        colon1_text.draw(screen)
        player2_text.draw(screen)
        colon2_text.draw(screen)
        draw_inputs(screen, input_list)
        screen.blit(play_surface, play_rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (play_rect.collidepoint(event.pos) and len(input_list[0].text)>0 and len(input_list[1].text)>0):
                    running_menu = False
                    running_game = True
                for my_input in input_list:
                    if my_input.outline_rect.collidepoint(event.pos):
                        my_input.state = "alive"
                    else:
                        my_input.state = "dead"
                    my_input.update()
            if event.type == pygame.KEYDOWN:
                for i,my_input in enumerate(input_list):
                    if my_input.state=="alive":
                        if event.key == pygame.K_RETURN:
                            if i==0 and my_input.text!="":
                                print(9)
                                my_input.state = "dead"
                                input_list[i+1].state = "alive"
                            elif i==1 and my_input.text!="":
                                my_input.state = "dead"
                                running_menu = False
                                running_game = True
                            my_input.update()
                        elif event.key == pygame.K_BACKSPACE:
                            my_input.text = my_input.text[:-1]
                            my_input.update()
                        else:
                            if (len(my_input.text)>=14):
                                continue
                            my_input.text += event.unicode
                            my_input.update()

    elif running_game:
        # Draw catapults and background
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        screen.blit(catapult_image, catapult_left)
        screen.blit(catapult_image, catapult_right)
        draw_blocks(screen, fortress_right, fortress_left)
        draw_birds(screen, left_birds, right_birds)
        draw_prediction(points_list, screen, circle_image)

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
            points_list=[]
            if (math.dist(mouse_pos, pygame.mouse.get_pos()) < 100):
                active_bird.x, active_bird.y = (pygame.mouse.get_pos()[0] - mouse_offset[0], pygame.mouse.get_pos()[1] - mouse_offset[1])
                vx = 10*(mouse_pos[0]-pygame.mouse.get_pos()[0])
                vy = 10*(mouse_pos[1]-pygame.mouse.get_pos()[1])
            else:
                vx = 10*(mouse_pos[0]-active_bird.x + mouse_offset[0])
                vy = 10*(mouse_pos[1]-active_bird.y + mouse_offset[1])
            active_projectile = lambda x: (vy*x/vx) + (0.5*GRAVITY*(x**2/vx**2))
            if (vx>0):
                for i in range(25):
                    points_list.append(((active_bird.x + mouse_offset[0]+25*i), (active_bird.y + mouse_offset[1]+active_projectile(25*i))))
            elif (vx<0):
                for i in range(25):
                    points_list.append(((active_bird.x + mouse_offset[0]-25*i), (active_bird.y + mouse_offset[1]+active_projectile(-25*i))))
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
                    active_bird.image = pygame.transform.flip(active_bird.image, True, False)
                    i.apply_damage(active_bird)
            if active_bird.collide_mode:
                active_bird.vx *= -e
                active_bird.collide_mode = False
                active_bird.collisions += 1
            active_bird.update()

        kill_birds(left_birds, right_birds)
        kill_blocks(fortress_left, fortress_right)
        if not right_birds and not bird_choosing_left and not bird_choosing_right:
            bird_choosing_left = True
            left_no = 0
            bird_choosing_right = False
        
        if bird_choosing_right and not bird_choosing_left:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        right_birds.append(Bird(catapult_right[0]-38*right_no-35, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE["red"], "red", "right"))
                        right_no += 1
            if right_no>2:
                bird_choosing_right = False
                right_no = None

        if bird_choosing_left and not bird_choosing_right:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        left_birds.append(Bird(catapult_left[0]+CATAPULT_SIZE[0]+38*left_no, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE["red"], "red", "left"))
                        left_no += 1
                        break
            if left_no>2:
                bird_choosing_left = False
                bird_choosing_right = True
                left_no = None
                right_no = 0

        if (turn=="left" and not active_bird):
            if not fortress_right and fortress_right:
                win = "draw"
                running_game = False
                running_end_screen = True
            elif not fortress_left:
                win = "right"
                running_game = False
                running_end_screen = True
            elif not fortress_right:
                win = "left"
                running_game = False
                running_end_screen = True
        

    elif running_end_screen:
        screen.fill((255, 255, 255))

    pygame.display.flip()

pygame.quit()