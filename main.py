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
from modules.wind import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
angry_font = lambda x : pygame.font.Font("./media/fonts/angry.ttf", x)
pygame.display.set_caption("Angry Birds - 2 Player")
clock = pygame.time.Clock()
pygame.key.set_repeat(400, 50)

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
catapult_left = (WIDTH/7, HEIGHT-GROUND-CATAPULT_SIZE[1])
catapult_right = (WIDTH*(6/7)-CATAPULT_SIZE[0], HEIGHT-GROUND-CATAPULT_SIZE[1])
# Back-ground
background_img = pygame.image.load("./media/images/back.jpg").convert() # To be changed before submitting
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
# Prediction image
circle_image = pygame.image.load("./media/images/circle.png")
# Difficulty choosing
diff_text = Text(WIDTH/2, HEIGHT/3, "Select Difficulty (1-4)", angry_font(WHO_START_FONT), (0,0,0))
diff_surfaces = [pygame.image.load(f"./media/images/levels/{i}.png").convert_alpha() for i in (1,2,3,4)]
diff_surfaces = [pygame.transform.scale(s, DIFF_SIZE) for s in diff_surfaces]
diff_rects = []
total_width = DIFF_SIZE[0]*4 + 20*3
start_x = (WIDTH - total_width)//2
y = HEIGHT//2
for i, surf in enumerate(diff_surfaces):
    rect = surf.get_rect(topleft=(start_x + i*(DIFF_SIZE[0]+20), y))
    diff_rects.append(rect)
arrow_image_og = pygame.image.load("./media/images/arrow.png")
# Pause screen
pause_image = pygame.image.load("./media/images/pause.png")
pause_image = pygame.transform.scale(pause_image, DIFF_SIZE)
pause_rect = pause_image.get_rect(center = (WIDTH*(15/16), HEIGHT/10))
dim_surface = pygame.Surface((WIDTH, HEIGHT))  # same size as screen
dim_surface.set_alpha(50)  # 0 = fully transparent, 255 = fully opaque
dim_surface.fill((0, 0, 0)) 
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
mouse_down = False # Flag for dragging of the bird
active_projectile = None # Function to store the projectile function
bird_choosing_left = False # To represent if the left player is choosing birds
bird_choosing_right = False # To represent if the left player is choosing birds
left_no = None # How many birds has left player chosen
right_no = None # How many birds has right player chosen
points_prediction = [] # Expected projectile points
path_points  = [] # Path as bird progresses
trail_timer = 0 # To track time so that i can draw points on birds path
name_1, name_2 = None, None # Names of players
active_bird = None # The active bird ie the bird which is on catapult or in air
active_fortress = None # The fortress which can be hit by current bird
wind = 0 # Current wind
wind_locked = False     ################################
locked_wind = 0     ################################
last_turn = turn # For wind timer

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
                    game_state="difficulty"
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
                                game_state="difficulty"
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
                            game_state="difficulty"
                            name_1, name_2 = make_texts(input_list)
                        elif len(input_list[0].text)>0 and len(input_list[1].text)==0:
                            input_list[1].state="alive"
                            input_list[1].update()
                        elif len(input_list[0].text)==0:
                            input_list[0].state="alive"
                            input_list[0].update()

    elif game_state == "difficulty":
        screen.fill((255,255,255))
        screen.blit(background_img, (0,0))
        diff_text.draw(screen)
        for surf, rect in zip(diff_surfaces, diff_rects):
            screen.blit(surf, rect)
        for event in events:
            if event.type == pygame.KEYDOWN and event.unicode in ("1","2","3","4"):
                diff = int(event.unicode)
                this_game_width  = DIFFICULTY_SETTINGS[diff]["width"]
                this_game_height = DIFFICULTY_SETTINGS[diff]["height"]
                this_game_WIND_MAX = DIFFICULTY_SETTINGS[diff]["wind_max"]
                fortress_left  = Fortress("left", this_game_width, this_game_height)
                fortress_right = Fortress("right", this_game_width, this_game_height)
                game_state = "game"
                wind = 0
                wind_timer = 0
                wind_lock_start = pygame.time.get_ticks()     ################################
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, rect in enumerate(diff_rects, start=1):
                    if rect.collidepoint(event.pos):
                        diff = idx
                        this_game_width  = DIFFICULTY_SETTINGS[diff]["width"]
                        this_game_height = DIFFICULTY_SETTINGS[diff]["height"]
                        this_game_WIND_MAX = DIFFICULTY_SETTINGS[diff]["wind_max"]
                        fortress_left  = Fortress("left", this_game_width, this_game_height)
                        fortress_right = Fortress("right", this_game_width, this_game_height)
                        game_state = "game"
                        wind = 0
                        wind_timer = 0
                        wind_lock_start = pygame.time.get_ticks()     ################################
                        break


    elif game_state=="game":
        # Draw catapults and background
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        fortress_right.draw(screen)
        fortress_left.draw(screen)
        screen.blit(catapult_image_left, catapult_left)
        screen.blit(catapult_image_right, catapult_right)
        screen.blit(pause_image, pause_rect)
        name_1.draw(screen)
        name_2.draw(screen)
        Text(WIDTH/2, HEIGHT/4, f'{(name_1.text if start_turn=="left" else name_2.text)} Starts first', angry_font(WHO_START_FONT), (0,0,0)).draw(screen)
        draw_birds(screen, left_birds, right_birds)
        draw_prediction(points_prediction, screen, circle_image)
        fortress_left.block_fall()
        fortress_right.block_fall()

        active_bird = get_active_bird(left_birds, right_birds)
        draw_path(path_points, screen, circle_image, active_bird)

        for event in events:
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_p) or (event.type==pygame.MOUSEBUTTONDOWN and pause_rect.collidepoint(pygame.mouse.get_pos()))):
                    game_state = "pause"
                    temp_game_pause_time = pygame.time.get_ticks()
                    break
                
        now = pygame.time.get_ticks()     ################################
        if turn != last_turn:     ################################
            last_turn = turn
            wind_lock_start = now
            wind_locked = False

        if not wind_locked:     ################################
            wind_timer += dt/1000.0     ################################
            raw_noise = fractal_noise_1d(wind_timer, seed=NOISE_SEED, octaves=5)     ################################
            wind = this_game_WIND_MAX * raw_noise     ################################
            if now - wind_lock_start >= 1000*TIME_LIMIT:
                wind_locked = True
                locked_wind = wind
        else:     ################################
            wind = locked_wind
        arrow_image = pygame.transform.scale(arrow_image_og, ((50*abs(wind)), 70))
        arrow_rect = arrow_image.get_rect(center=(WIDTH/2, HEIGHT/10))
        if (wind>0):
            pass
        else:
            arrow_image = pygame.transform.flip(arrow_image, True, False)
        screen.blit(arrow_image, arrow_rect)
        remaining = max(0, TIME_LIMIT - (now - wind_lock_start)/1000.0)
        timer_surf = angry_font(30).render(f"Wait: {remaining:.1f}s", True, (200, 0, 0))
        screen.blit(timer_surf, (WIDTH - 180, 20)) if diff>1 else None

        if not active_bird:
            points_prediction=[]
            path_points = []
            trail_timer = 0
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
                points_prediction = []
                if (vx>0):
                    for i in range(30):
                        points_prediction.append(((active_bird.x + BIRD_SIZE/2 + (WIDTH/50)*i), (active_bird.y + BIRD_SIZE/2 +active_projectile((WIDTH/50)*i))))
                elif (vx<0):
                    for i in range(30):
                        points_prediction.append(((active_bird.x + BIRD_SIZE/2 - (WIDTH/50)*i), (active_bird.y + BIRD_SIZE/2 + active_projectile(-(WIDTH/50)*i))))
            else:
                points_prediction = []
            for event in events:
                if (event.type == pygame.MOUSEBUTTONUP and not active_rectangle.collidepoint(pygame.mouse.get_pos())):
                    active_bird.on_cat = False
                    mouse_down = False
                    active_bird.vx, active_bird.vy = vx, vy
                    active_bird.wind = wind
                    turn = "left" if turn=="right" else "right"
                elif (event.type == pygame.MOUSEBUTTONUP and active_rectangle.collidepoint(pygame.mouse.get_pos())):
                    active_bird.on_cat = True
                    mouse_down = False
                    active_bird.x, active_bird.y = [active_rectangle[i] for i in (0,1)]

        else:
            points_prediction = []
            active_fortress = fortress_left if turn=="left" else fortress_right
            if (not active_bird.on_power) and (active_bird.collisions==0):
                for event in events:
                    if (event.type == pygame.MOUSEBUTTONDOWN or (event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE)):
                        active_bird.apply_power(left_birds if turn=="left" else right_birds, active_fortress)
                        active_bird.explosion_pos = (active_bird.x, active_bird.y)
            if active_bird.bird_type == "blues" and active_bird.on_power == True:
                active_birds = [x for x in (left_birds if turn == "left" else right_birds) if x.active == True]
                for i in range(len(active_birds)):
                    active_fortress.update(active_birds[i])
                    active_birds[i].update()
            else:
                active_fortress.update(active_bird)
                active_bird.update()
            if ((active_bird.bird_type=="red" and active_bird.size-BIRD_SIZE>0) and active_bird.on_power == False):
                active_bird.apply_power(left_birds if turn=="left" else right_birds, active_fortress)
            trail_timer += dt
            if trail_timer >= 40:
                trail_x = active_bird.x + active_bird.size/2
                trail_y = active_bird.y + active_bird.size/2
                path_points.append((trail_x, trail_y))
                trail_timer = 0

        kill_birds(left_birds, right_birds)
        kill_fortress(fortress_left, fortress_right)
        if not right_birds and not bird_choosing_left and not bird_choosing_right and not left_birds:
            bird_choosing_left = (True if start_turn=="left" else False)
            left_no = 0
            right_no = 0
            bird_choosing_right = not bird_choosing_left
        
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
                if (start_turn=="left"):
                    bird_choosing_right = False
                    right_no = None
                else:
                    bird_choosing_right = False
                    bird_choosing_left = True
                    left_no = 0
                    right_no = None
                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            events.remove(event)
                            break

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
                if (start_turn=="left"):
                    bird_choosing_left = False
                    bird_choosing_right = True
                    left_no = None
                    right_no = 0
                else:
                    bird_choosing_left = False
                    left_no = None

        if (not active_bird):
            if not fortress_left:
                win = "right"
                game_state = "end"
            elif not fortress_right:
                win = "left"
                game_state = "end"

    elif game_state == "pause":
        screen.blit(background_img, (0,0))
        screen.blit(dim_surface, (0, 0))
        Text(WIDTH/2, HEIGHT/4,  "PAUSED",      angry_font(MAIN_FONT),  (0,0,0)).draw(screen)
        Text(WIDTH/2, HEIGHT/2.5,"Resume",  angry_font(WHO_START_FONT),(100,100,100)).draw(screen)
        Text(WIDTH/2, HEIGHT/2,  "Restart", angry_font(WHO_START_FONT),(100,100,100)).draw(screen)
        Text(WIDTH/2, HEIGHT/1.7,"Quit",    angry_font(WHO_START_FONT),(100,100,100)).draw(screen)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = "game"
                    wind_lock_start += pygame.time.get_ticks()-temp_game_pause_time
                elif event.key == pygame.K_r:
                    fortress_left  = Fortress("left",  this_game_width,  this_game_height)
                    fortress_right = Fortress("right", this_game_width,  this_game_height)
                    left_birds  = [Bird(catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+4)*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, t, "left") for i,t in enumerate(BIRD_OPTIONS)]
                    right_birds = [Bird(catapult_right[0]-(BIRD_SIZE+4)*i-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, t, "right") for i,t in enumerate(BIRD_OPTIONS)]
                    start_turn = random.choice(["left", "right"])
                    turn = start_turn
                    wind = 0
                    wind_timer = 0.0
                    wind_lock_start = pygame.time.get_ticks()
                    points_prediction = []
                    path_points = []
                    game_state = "game"
                    bird_choosing_right = False
                    bird_choosing_left = False
                    right_no = None
                    left_no = None
                    wind = 0 # Current wind
                    wind_locked = False
                    locked_wind = 0
                    last_turn = turn
                    trail_timer = 0
                elif event.key == pygame.K_q:
                    game_state = "end"
                    win = "quit"

    elif game_state == "end":
        if (win=="left"):
            winner_text = Text(WIDTH/2, HEIGHT/1.3, f"{name_1.text} Won", angry_font(WINNER_TEXT_FONT), (0,0,0))
        elif (win=="right"):
            winner_text = Text(WIDTH/2, HEIGHT/1.3, f"{name_2.text} Won", angry_font(WINNER_TEXT_FONT), (0,0,0))
        elif (win=="quit"):
            winner_text = Text(WIDTH/2, HEIGHT/1.3, f"Game Quit", angry_font(WINNER_TEXT_FONT), (0,0,0))
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
                bird_choosing_right = False
                bird_choosing_left = False
                right_no = None
                left_no = None
                trail_timer = 0
                wind = 0 # Current wind
                wind_locked = False
                locked_wind = 0
                last_turn = turn

    pygame.display.flip()

pygame.quit()