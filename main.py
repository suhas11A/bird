#!/usr/bin/env python 

import pygame # type: ignore
import random
import math
import numpy as np
from modules.bird import *
from modules.block import *
from modules.variables import *
from modules.text import *
from modules.input import *
from modules.fortress import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
angry_font = lambda x : pygame.font.Font("./media/fonts/angry.ttf", x)
pygame.display.set_caption("Angry Birds - 2 Player")
clock = pygame.time.Clock()

# Menu
main_text = Text(WIDTH/2,HEIGHT/10,"Angry Birds", angry_font(MAIN_FONT), (0,0,0))
player1_text = Text(WIDTH/3.5,HEIGHT/4.5,"Name of player 1", angry_font(PLAYER_NAME_FONT), (0,0,0))
colon1_text = Text(WIDTH/2,HEIGHT/4.5,":", angry_font(PLAYER_NAME_FONT), (0,0,0))
player2_text = Text(WIDTH/3.5,HEIGHT/3,"Name of player 2", angry_font(PLAYER_NAME_FONT), (0,0,0))
colon2_text = Text(WIDTH/2,HEIGHT/3,":", angry_font(PLAYER_NAME_FONT), (0,0,0))
input_list = [Input(WIDTH - WIDTH/3.5,HEIGHT/i,"", angry_font(PLAYER_NAME_FONT), "dead", (0,0,0)) for i in [4.5, 3]]
play_surface = pygame.image.load("./media/images/play.png")
play_surface = pygame.transform.scale(play_surface, (WIDTH/7, HEIGHT/9.5))
play_rect = play_surface.get_rect(center=(WIDTH/2,HEIGHT/1.9))
# Catapults
catapult_image_left = pygame.image.load("./media/images/catapult.png")
catapult_image_left = pygame.transform.scale(catapult_image_left, CATAPULT_SIZE)
catapult_image_right = pygame.transform.flip(catapult_image_left, True, False)
catapult_left = (WIDTH/7, HEIGHT*(6/7)-CATAPULT_SIZE[1])
catapult_right = (WIDTH*(6/7)-CATAPULT_SIZE[0], HEIGHT*(6/7)-CATAPULT_SIZE[1])
# Back-ground
background_img = pygame.image.load("./media/images/back.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
# Fortresses
fortress_left = Fortress("left")
fortress_right = Fortress("right")
# Prediction image
circle_image = pygame.image.load("./media/images/circle.png")
# End Screen
play_again_surface = pygame.image.load("./media/images/play_again.png")
play_again_surface = pygame.transform.scale(play_again_surface, (WIDTH/7.3, HEIGHT/3.7))
play_again_rect = play_again_surface.get_rect(center=(WIDTH/2,HEIGHT/1.9))
play_again_rect_clickable = play_again_rect.copy()
cut_height = play_again_rect_clickable.height / 2.48
play_again_rect_clickable.y += cut_height
play_again_rect_clickable.height -= cut_height
winner_text = None
# Initiation
left_birds = [Bird(catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+4)*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "left") for i,type in enumerate(BIRD_OPTIONS)]
right_birds = [Bird(catapult_right[0]-(BIRD_SIZE+4)*i-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "right") for i,type in enumerate(BIRD_OPTIONS)]
turn = random.choice(["left", "right"]) # Current turn 
start_turn = turn # Who starts the match
running = True
game_state = "menu"
win = None
mouse_pos = None
active_rectangle = None # The rectangle which is clickable when a bird is on catapult
mouse_offset = None # Offset between the bird origin and mose clocked position
mouse_down = False
active_projectile = None # Function to store the projectile function
bird_choosing_left = False # To represent if the left player is choosing birds
bird_choosing_right = False # To represent if the left player is choosing birds
left_no = None # How many birds has left player chosen
right_no = None # How many birds has right player chosen
points_list = [] # Expected projectile points
name_1, name_2 = None, None # Names of players
active_bird = None # The active bird ie the bird which is on catapult or in air
active_fortress = None # The fortress which can be hit by current bird

while running:
    dt = clock.tick(FPS)
    # Check-Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    if game_state=="menu":
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
                    game_state="game"
                    name_1, name_2 = make_texts(input_list)
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
                                my_input.state = "dead"
                                input_list[i+1].state = "alive"
                            elif i==1 and my_input.text!="":
                                my_input.state = "dead"
                                game_state="game"
                                name_1, name_2 = make_texts(input_list)
                            my_input.update()
                        elif event.key == pygame.K_BACKSPACE:
                            my_input.text = my_input.text[:-1]
                            my_input.update()
                        elif event.key == pygame.K_ESCAPE:
                            my_input.state = "dead"
                            my_input.update()
                        else:
                            if (len(my_input.text)>=14):
                                continue
                            my_input.text += event.unicode
                            my_input.update()
                if input_list[0].state=="dead" and input_list[1].state=="dead":
                    if event.key == pygame.K_RETURN:
                        if len(input_list[0].text)>0 and len(input_list[1].text)>0:
                            game_state="game"
                            name_1, name_2 = make_texts(input_list)
                        elif len(input_list[0].text)>0 and len(input_list[1].text)==0:
                            input_list[1].state="alive"
                            input_list[1].update()
                        elif len(input_list[0].text)==0:
                            input_list[0].state="alive"
                            input_list[0].update()


    elif game_state=="game":
        # Draw catapults and background
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        fortress_right.draw(screen)
        fortress_left.draw(screen)
        screen.blit(catapult_image_left, catapult_left)
        screen.blit(catapult_image_right, catapult_right)
        name_1.draw(screen)
        name_2.draw(screen)
        Text(WIDTH/2, HEIGHT/4, f'{(name_1.text if start_turn=="left" else name_2.text)} Starts first', angry_font(WHO_START_FONT), (0,0,0)).draw(screen)
        draw_birds(screen, left_birds, right_birds)
        draw_prediction(points_list, screen, circle_image)

        active_bird = get_active_bird(left_birds, right_birds)
        if not active_bird:
            points_list=[]
        if (not active_bird) or (active_bird.on_cat and not mouse_down):
            if active_bird:
                for event in events:
                    if (event.type == pygame.MOUSEBUTTONDOWN and active_bird.get_rect().collidepoint(pygame.mouse.get_pos())):
                        mouse_down = True
                        mouse_pos = pygame.mouse.get_pos()
                        active_rectangle = active_bird.get_rect()
                        mouse_offset = (mouse_pos[0]-active_bird.x), (mouse_pos[1]-active_bird.y)
                        active_bird_home_box = active_bird.get_rect()
            if not mouse_down:
                for event in events:
                    for i in (left_birds if turn=="left" else right_birds):
                        if (event.type == pygame.MOUSEBUTTONDOWN and i.get_rect().collidepoint(pygame.mouse.get_pos())):
                            if active_bird:
                                active_bird.x = i.x
                                active_bird.y = i.y
                                active_bird.active = False
                                active_bird.on_cat = False
                            active_bird = i
                            active_bird.active = True
                            active_bird.on_cat = True
                            if active_bird:
                                if turn=="left":
                                    active_bird.x = (catapult_left)[0]+CATAPULT_SIZE[0]*0.3
                                    active_bird.y = (catapult_left)[1]
                                else:
                                    active_bird.x = (catapult_right)[0]
                                    active_bird.y = (catapult_right)[1]
                            break
        elif active_bird.on_cat and mouse_down:
            my_dist = math.dist(mouse_pos, pygame.mouse.get_pos())
            if (my_dist < MAX_RADIUS):
                active_bird.x, active_bird.y = (pygame.mouse.get_pos()[0] - mouse_offset[0], pygame.mouse.get_pos()[1] - mouse_offset[1])
                vx = (10**0.5)*((WIDTH/120)**0.5)*(mouse_pos[0]-pygame.mouse.get_pos()[0])
                vy = (10**0.5)*((WIDTH/120)**0.5)*(mouse_pos[1]-pygame.mouse.get_pos()[1])
            else:
                temp_pos = np.array(mouse_pos)-np.array(mouse_offset)+(MAX_RADIUS/my_dist)*(np.array(pygame.mouse.get_pos())-np.array(mouse_pos))
                active_bird.x, active_bird.y = (temp_pos[0], temp_pos[1])
                temp_v = (10**0.5)*((WIDTH/120)**0.5)*(np.array(mouse_pos) - np.array(mouse_offset) - np.array((active_bird.x, active_bird.y)))
                active_bird.vx, active_bird.vy = temp_v[0], temp_v[1]
                vx = temp_v[0]
                vy = temp_v[1]
            active_projectile = lambda x: (vy*x/vx) + (0.5*GRAVITY*(x**2/vx**2))
            if (not active_rectangle.collidepoint(pygame.mouse.get_pos())):
                points_list = []
                if (vx>0):
                    for i in range(30):
                        points_list.append(((active_bird.x + BIRD_SIZE/2 + (WIDTH/50)*i), (active_bird.y + BIRD_SIZE/2 +active_projectile((WIDTH/50)*i))))
                elif (vx<0):
                    for i in range(30):
                        points_list.append(((active_bird.x + BIRD_SIZE/2 - (WIDTH/50)*i), (active_bird.y + BIRD_SIZE/2 + active_projectile(-(WIDTH/50)*i))))
            else:
                points_list = []
            for event in events:
                if (event.type == pygame.MOUSEBUTTONUP and not active_rectangle.collidepoint(pygame.mouse.get_pos())):
                    active_bird.on_cat = False
                    mouse_down = False
                    active_bird.vx, active_bird.vy = vx, vy
                    turn = "left" if turn=="right" else "right"
                elif (event.type == pygame.MOUSEBUTTONUP and active_rectangle.collidepoint(pygame.mouse.get_pos())):
                    active_bird.on_cat = True
                    mouse_down = False
                    active_bird.x, active_bird.y = [active_rectangle[i] for i in (0,1)]

        else:
            active_fortress = fortress_left if turn=="left" else fortress_right
            active_fortress.update(active_bird)
            active_bird.update()

        kill_birds(left_birds, right_birds)
        kill_fortress(fortress_left, fortress_right)
        if not right_birds and not bird_choosing_left and not bird_choosing_right:
            bird_choosing_left = True
            left_no = 0
            bird_choosing_right = False
        
        if bird_choosing_right and not bird_choosing_left:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        right_birds.append(Bird(catapult_right[0]-(BIRD_SIZE+4)*right_no-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "red", "right"))
                        right_no += 1
                    elif event.key == pygame.K_c:
                        right_birds.append(Bird(catapult_right[0]-(BIRD_SIZE+4)*right_no-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "chuck", "right"))
                        right_no += 1
                    elif event.key == pygame.K_b:
                        right_birds.append(Bird(catapult_right[0]-(BIRD_SIZE+4)*right_no-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "blues", "right"))
                        right_no += 1
                    elif event.key == pygame.K_m:
                        right_birds.append(Bird(catapult_right[0]-(BIRD_SIZE+4)*right_no-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "bomb", "right"))
                        right_no += 1
            if right_no>2:
                bird_choosing_right = False
                right_no = None

        if bird_choosing_left and not bird_choosing_right:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        left_birds.append(Bird(catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+4)*left_no, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "red", "left"))
                        left_no += 1
                        break
                    elif event.key == pygame.K_c:
                            left_birds.append(Bird(catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+4)*left_no, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "chuck", "left"))
                            left_no += 1
                            break
                    elif event.key == pygame.K_b:
                            left_birds.append(Bird(catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+4)*left_no, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "blues", "left"))
                            left_no += 1
                            break
                    elif event.key == pygame.K_m:
                            left_birds.append(Bird(catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+4)*left_no, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "bomb", "left"))
                            left_no += 1
                            break
            if left_no>2:
                bird_choosing_left = False
                bird_choosing_right = True
                left_no = None
                right_no = 0

        if (not active_bird):
            if not fortress_left:
                win = "right"
                game_state = "end"
            elif not fortress_right:
                win = "left"
                game_state = "end"
        

    elif game_state == "end":
        if (win=="left"):
            winner_text = Text(WIDTH/2, HEIGHT/1.3, f"{name_1.text} Won", angry_font(WINNER_TEXT_FONT), (0,0,0))
        elif (win=="right"):
            winner_text = Text(WIDTH/2, HEIGHT/1.3, f"{name_2.text} Won", angry_font(WINNER_TEXT_FONT), (0,0,0))
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        main_text.draw(screen)
        winner_text.draw(screen)
        screen.blit(play_again_surface, play_again_rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and play_again_rect_clickable.collidepoint(event.pos):
                game_state = "menu"
                for my_input in input_list:
                    my_input.text = ""
                    my_input.update()
                fortress_left = Fortress("left")
                fortress_right = Fortress("right")
                winner_text = None
                left_birds = [Bird(catapult_left[0]+CATAPULT_SIZE[0]+38*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "left") for i,type in enumerate(BIRD_OPTIONS)]
                right_birds = [Bird(catapult_right[0]-38*i-35, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "right") for i,type in enumerate(BIRD_OPTIONS)]
                turn = random.choice(["left", "right"])
                start_turn = turn
                win = None

    pygame.display.flip()

pygame.quit()