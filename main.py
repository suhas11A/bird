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
from modules.helper import *

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
angry_font = lambda x : pygame.font.Font("./media/fonts/angry.ttf", x)
font = angry_font
pygame.display.set_caption("Angry Birds - 2 Player")
clock = pygame.time.Clock()
pygame.key.set_repeat(400, 50)
# Sounds
pygame.mixer.music.load("./media/audio/music/background.wav")  
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(loops=-1)
on_launch_sfx = pygame.mixer.Sound("./media/audio/sounds/on_launch.wav")
on_select_sfx = pygame.mixer.Sound("./media/audio/sounds/on_select.wav")
on_power_sfx = pygame.mixer.Sound("./media/audio/sounds/on_power.wav")
collision_sfx = pygame.mixer.Sound("./media/audio/sounds/collision.wav")
# Default theme
selected_theme = "default"
GROUND = GROUND_LEVEL[selected_theme]
# Menu
main_text = Text(WIDTH/2,HEIGHT/10,"Angry Birds", font(BIG_FONT), TEXT_COLOR[selected_theme])
player1_text = Text(WIDTH/3.5,HEIGHT/4.5,"Name of player 1", font(SMALL_FONT), TEXT_COLOR[selected_theme])
colon1_text = Text(WIDTH/2,HEIGHT/4.5,":", font(SMALL_FONT), TEXT_COLOR[selected_theme])
player2_text = Text(WIDTH/3.5,HEIGHT/3,"Name of player 2", font(SMALL_FONT), TEXT_COLOR[selected_theme])
colon2_text = Text(WIDTH/2,HEIGHT/3,":", font(SMALL_FONT), TEXT_COLOR[selected_theme])
input_list = [Input(WIDTH - WIDTH/3.5,HEIGHT/i,"", font(SMALL_FONT), "dead", TEXT_COLOR[selected_theme]) for i in [4.5, 3]]
play_surface = pygame.image.load("./media/images/play.png").convert_alpha()
play_surface = pygame.transform.scale(play_surface, (WIDTH/8, HEIGHT/11))
play_rect = play_surface.get_rect(center=(WIDTH/2,HEIGHT/2))
choose_theme_surface = pygame.image.load("./media/images/theme.png").convert_alpha()
choose_theme_surface = pygame.transform.scale(choose_theme_surface, (WIDTH/8, HEIGHT/11))
choose_theme_rect = choose_theme_surface.get_rect(center=(WIDTH/2, HEIGHT/1.65))
mute_img = pygame.image.load("./media/images/sound_options/unmute.png").convert_alpha()
mute_img = pygame.transform.scale(mute_img, SOUND_SIZE)
unmute_img = pygame.image.load("./media/images/sound_options/mute.png").convert_alpha()
unmute_img = pygame.transform.scale(unmute_img, SOUND_SIZE)
sound_img = mute_img
sound_rect = unmute_img.get_rect(center=(WIDTH*(1/25), HEIGHT/16))
# Themes
THEME_BACKGROUNDS = {}
for theme in THEME_BACKGROUNDS_PATH:
    background_img = pygame.image.load(THEME_BACKGROUNDS_PATH[theme]).convert_alpha()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    THEME_BACKGROUNDS[theme] = background_img
theme_rects = []
for i, theme in enumerate(THEMES):
    x = (WIDTH/4 - 20)  + (i%3) * (WIDTH/4+20)
    y = HEIGHT/3.5 + (i // 3) * (HEIGHT/4+20)
    image = THEME_BACKGROUNDS[theme]
    image = pygame.transform.scale(image, (WIDTH // 5, HEIGHT // 4))
    rect = image.get_rect(center=(x, y))
    theme_rects.append((theme, image, rect))
# Catapults
catapult_image_left = pygame.image.load("./media/images/catapult.png").convert_alpha()
catapult_image_left = pygame.transform.scale(catapult_image_left, CATAPULT_SIZE)
catapult_image_right = pygame.transform.flip(catapult_image_left, True, False)
catapult_left = (WIDTH/7, HEIGHT-GROUND-CATAPULT_SIZE[1])
catapult_right = (WIDTH*(6/7)-CATAPULT_SIZE[0], HEIGHT-GROUND-CATAPULT_SIZE[1])
# Back-ground
background_img = THEME_BACKGROUNDS[selected_theme]
# Loading bird, explosion, helmet and block, broken blocks images for better latency
BIRD_OG_IMAGES = {}
for bird in BIRD_OPTIONS:
    image = pygame.image.load(f"./media/images/birds/{bird}.png").convert_alpha()
    BIRD_OG_IMAGES[bird] = image
OG_HELMET_IMAGE = pygame.image.load(f"./media/images/birds/helmet.png").convert_alpha()
EXPLOSION_FRAMES = []
for i in range(NUM_FRAMES):
    img = pygame.image.load(f"./media/images/explosion_frames/frame_{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (BIRD_SIZE * 7, BIRD_SIZE * 7))
    EXPLOSION_FRAMES.append(img)
BIRD_PACK = (BIRD_OG_IMAGES, OG_HELMET_IMAGE, EXPLOSION_FRAMES)
BLOCK_IMAGES = {}
for i in range(1, 5):
    BLOCK_IMAGES[i] = {}
    for block in BLOCK_OPTIONS:
        img = pygame.image.load(f"./media/images/blocks/{block}_{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
        BLOCK_IMAGES[i][block] = img
BLOCK_PACK = (BLOCK_IMAGES[1], BLOCK_IMAGES[2], BLOCK_IMAGES[3], BLOCK_IMAGES[4])
# Prediction image
circle_image = pygame.image.load("./media/images/circle.png").convert_alpha()
# Difficulty choosing
diff_surfaces = [pygame.image.load(f"./media/images/levels/{i}.png").convert_alpha() for i in (1,2,3,4)]
diff_surfaces = [pygame.transform.scale(s, DIFF_SIZE) for s in diff_surfaces]
diff_rects = []
total_width = DIFF_SIZE[0]*4 + 20*3
start_x = (WIDTH - total_width)//2
y = HEIGHT/2.5
for i, surf in enumerate(diff_surfaces):
    rect = surf.get_rect(topleft=(start_x + i*(DIFF_SIZE[0]+20), y))
    diff_rects.append(rect)
arrow_image_og = pygame.image.load("./media/images/arrow.png").convert_alpha()
# Pause screen
pause_image = pygame.image.load("./media/images/pause_options/pause.png").convert_alpha()
pause_image = pygame.transform.scale(pause_image, PAUSE_SIZE)
pause_rect = pause_image.get_rect(center = (WIDTH*(15/16), HEIGHT/10))
dim_surface = pygame.Surface((WIDTH, HEIGHT))  # same size as screen
dim_surface.set_alpha(50)
dim_surface.fill((0, 0, 0))
resume_img = pygame.image.load("./media/images/pause_options/resume.png").convert_alpha()
resume_img = pygame.transform.scale(resume_img, (BUTTON_W, BUTTON_H))
resume_rect = resume_img.get_rect(center=(WIDTH/2, HEIGHT/2.5))
replay_img = pygame.image.load("./media/images/pause_options/replay.png").convert_alpha()
replay_img = pygame.transform.scale(replay_img, (BUTTON_W, BUTTON_H))
replay_rect = replay_img.get_rect(center=(WIDTH/2, HEIGHT/2.02381))
quit_img = pygame.image.load("./media/images/pause_options/quit.png").convert_alpha()
quit_img = pygame.transform.scale(quit_img, (BUTTON_W, BUTTON_H))
quit_rect = quit_img.get_rect(center=(WIDTH/2, HEIGHT/1.7))
# End Screen
play_again_surface = pygame.image.load("./media/images/play_again.png").convert_alpha()
play_again_surface = pygame.transform.scale(play_again_surface, (WIDTH/7.3, HEIGHT/3.7))
play_again_rect = play_again_surface.get_rect(center=(WIDTH/2,HEIGHT/2.5))
play_again_rect_clickable = play_again_rect.copy()
cut_height = play_again_rect_clickable.height / 2.48
play_again_rect_clickable.y += cut_height
play_again_rect_clickable.height -= cut_height
winner_text = None
# Initiation
bird_space = 4 * (WIDTH/1600)
left_birds = [Bird(BIRD_PACK, GROUND, catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+bird_space)*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "left") for i,type in enumerate(BIRD_OPTIONS)]
right_birds = [Bird(BIRD_PACK, GROUND, catapult_right[0]-(BIRD_SIZE+bird_space)*i-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "right") for i,type in enumerate(BIRD_OPTIONS)]
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
wind_locked = False
locked_wind = 0
last_turn = turn # For wind timer
muted = False

while running:
    dt = clock.tick(FPS)
    # Check-Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: # To close the game
            running = False
        if (event.type == pygame.MOUSEBUTTONDOWN and sound_rect.collidepoint(event.pos)): # To mute and unmute
            muted = not muted
            if muted:
                pygame.mixer.music.set_volume(0)
                on_launch_sfx.set_volume(0)
                on_select_sfx.set_volume(0)
                on_power_sfx.set_volume(0)
                collision_sfx.set_volume(0)
                sound_img = unmute_img
            else:
                pygame.mixer.music.set_volume(0.8)
                on_launch_sfx.set_volume(1.0)
                on_select_sfx.set_volume(1.0)
                on_power_sfx.set_volume(1.0)
                collision_sfx.set_volume(1.0)
                sound_img = mute_img
    if game_state=="menu":
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        screen.blit(sound_img, sound_rect)
        main_text.draw(screen)
        player1_text.draw(screen)
        colon1_text.draw(screen)
        player2_text.draw(screen)
        colon2_text.draw(screen)
        draw_inputs(screen, input_list)
        screen.blit(play_surface, play_rect) 
        screen.blit(choose_theme_surface, choose_theme_rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: # To choose theme
                if choose_theme_rect.collidepoint(event.pos):
                    game_state = "theme"
                    break
                if (play_rect.collidepoint(event.pos) and len(input_list[0].text)>0 and len(input_list[1].text)>0): # To choose difficulty
                    game_state="difficulty"
                    name_1, name_2 = make_texts(input_list, selected_theme)
                for my_input in input_list:
                    if my_input.outline_rect.collidepoint(event.pos):
                        my_input.state = "alive"
                    else:
                        my_input.state = "dead"
                    my_input.update()
            if event.type == pygame.KEYDOWN: # To write names
                for i,my_input in enumerate(input_list):
                    if my_input.state=="alive":
                        if event.key == pygame.K_RETURN:
                            if i==0 and my_input.text!="":
                                my_input.state = "dead"
                                input_list[i+1].state = "alive"
                            elif i==1 and my_input.text!="":
                                my_input.state = "dead"
                                game_state="difficulty"
                                name_1, name_2 = make_texts(input_list, selected_theme)
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
                    if event.key == pygame.K_t:
                        game_state = "theme"
                        break
                    if event.key == pygame.K_RETURN:
                        if len(input_list[0].text)>0 and len(input_list[1].text)>0:
                            game_state="difficulty"
                            name_1, name_2 = make_texts(input_list, selected_theme)
                        elif len(input_list[0].text)>0 and len(input_list[1].text)==0:
                            input_list[1].state="alive"
                            input_list[1].update()
                        elif len(input_list[0].text)==0:
                            input_list[0].state="alive"
                            input_list[0].update()

    elif game_state == "theme": # To choose theme
        screen.fill((255,255,255))
        screen.blit(background_img, (0,0))
        screen.blit(sound_img, sound_rect)
        Text(WIDTH/2, HEIGHT/10, "Choose a Theme", font(BIG_FONT), TEXT_COLOR[selected_theme]).draw(screen)
        for theme, image, rect in theme_rects:
            draw_rounded_image_with_border(screen, image, rect, border_color=(0, 0, 0), border_thickness=3, radius=25)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for theme, _, rect in theme_rects:
                    if rect.collidepoint(event.pos):
                        selected_theme = theme
                        background_img = THEME_BACKGROUNDS[theme]
                        GROUND = GROUND_LEVEL[theme]
                        if (selected_theme=="space"):
                            catapult_left = (WIDTH/7, HEIGHT-HEIGHT/7-CATAPULT_SIZE[1])
                            catapult_right = (WIDTH*(6/7)-CATAPULT_SIZE[0], HEIGHT-HEIGHT/7-CATAPULT_SIZE[1])
                            bird_space = 23 * (WIDTH/1600)
                        else:
                            catapult_left = (WIDTH/7, HEIGHT-GROUND-CATAPULT_SIZE[1])
                            catapult_right = (WIDTH*(6/7)-CATAPULT_SIZE[0], HEIGHT-GROUND-CATAPULT_SIZE[1])
                            bird_space = 4 * (WIDTH/1600)
                        left_birds = [Bird(BIRD_PACK, GROUND, catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+bird_space)*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "left") for i,type in enumerate(BIRD_OPTIONS)]
                        right_birds = [Bird(BIRD_PACK, GROUND, catapult_right[0]-(BIRD_SIZE+bird_space)*i-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "right") for i,type in enumerate(BIRD_OPTIONS)]
                        game_state = "menu"
                        main_text = Text(WIDTH/2,HEIGHT/10,"Angry Birds", font(BIG_FONT), TEXT_COLOR[selected_theme])
                        player1_text = Text(WIDTH/3.5,HEIGHT/4.5,"Name of player 1", font(SMALL_FONT), TEXT_COLOR[selected_theme])
                        colon1_text = Text(WIDTH/2,HEIGHT/4.5,":", font(SMALL_FONT), TEXT_COLOR[selected_theme])
                        player2_text = Text(WIDTH/3.5,HEIGHT/3,"Name of player 2", font(SMALL_FONT), TEXT_COLOR[selected_theme])
                        colon2_text = Text(WIDTH/2,HEIGHT/3,":", font(SMALL_FONT), TEXT_COLOR[selected_theme])


    elif game_state == "difficulty":
        screen.fill((255,255,255))
        screen.blit(background_img, (0,0))
        screen.blit(sound_img, sound_rect)
        Text(WIDTH/2, HEIGHT/3, "Select Difficulty (1-4)", font(SMALL_FONT), TEXT_COLOR[selected_theme]).draw(screen)
        for surf, rect in zip(diff_surfaces, diff_rects):
            screen.blit(surf, rect)
        for event in events:
            if event.type == pygame.KEYDOWN and event.unicode in ("1","2","3","4"):
                diff = int(event.unicode)
                this_game_width  = DIFFICULTY_SETTINGS[diff]["width"]
                this_game_height = DIFFICULTY_SETTINGS[diff]["height"]
                this_game_WIND_MAX = DIFFICULTY_SETTINGS[diff]["wind_max"]
                if (selected_theme=="space"):
                    this_game_WIND_MAX=0
                fortress_left  = Fortress(BLOCK_PACK, GROUND, "left", this_game_width, this_game_height)
                fortress_right = Fortress(BLOCK_PACK, GROUND, "right", this_game_width, this_game_height, fortress_left)
                game_state = "game"
                wind = 0
                wind_timer = 0
                wind_lock_start = pygame.time.get_ticks()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, rect in enumerate(diff_rects, start=1):
                    if rect.collidepoint(event.pos):
                        diff = idx
                        this_game_width  = DIFFICULTY_SETTINGS[diff]["width"]
                        this_game_height = DIFFICULTY_SETTINGS[diff]["height"]
                        this_game_WIND_MAX = DIFFICULTY_SETTINGS[diff]["wind_max"]
                        if (selected_theme=="space"):
                            this_game_WIND_MAX=0
                        fortress_left  = Fortress(BLOCK_PACK, GROUND, "left", this_game_width, this_game_height)
                        fortress_right = Fortress(BLOCK_PACK, GROUND, "right", this_game_width, this_game_height, fortress_left)
                        game_state = "game"
                        wind = 0
                        wind_timer = 0
                        wind_lock_start = pygame.time.get_ticks()
                        break


    elif game_state=="game":
        # Draw catapults and background
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        screen.blit(sound_img, sound_rect)
        fortress_right.draw(screen)
        fortress_left.draw(screen)
        screen.blit(catapult_image_left, catapult_left)
        screen.blit(catapult_image_right, catapult_right)
        screen.blit(pause_image, pause_rect)
        name_1.draw(screen)
        name_2.draw(screen)
        Text(WIDTH/2, HEIGHT/4, f'{(name_1.text if start_turn=="left" else name_2.text)} Starts first', font(SMALL_FONT), TEXT_COLOR[selected_theme]).draw(screen)
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
                    events.remove(event)
                    break
                
        now = pygame.time.get_ticks()
        if turn != last_turn:
            last_turn = turn
            wind_lock_start = now
            wind_locked = False

        if not wind_locked:
            wind_timer += dt/1000.0
            raw_noise = fractal_noise_1d(wind_timer*0.5, seed=NOISE_SEED, octaves=5)
            wind = this_game_WIND_MAX * raw_noise
            if now - wind_lock_start >= 1000*TIME_LIMIT:
                wind_locked = True
                locked_wind = wind
        else:
            wind = locked_wind
        arrow_image = pygame.transform.scale(arrow_image_og, ((50*abs(wind)), 70))
        arrow_rect = arrow_image.get_rect(center=(WIDTH/2, HEIGHT/10))
        if (wind>0):
            pass
        else:
            arrow_image = pygame.transform.flip(arrow_image, True, False)
        screen.blit(arrow_image, arrow_rect) # Arrow to show the bir speed
        remaining = max(0, TIME_LIMIT - (now - wind_lock_start)/1000.0)
        timer_surf = font(EXTRA_SMALL_FONT).render(f"Wait: {remaining:.1f}s", True, ((200, 0, 0) if selected_theme!="lava" else (255,255, 255)))
        screen.blit(timer_surf, (WIDTH - 180, 20)) if this_game_WIND_MAX>0 else None # Show the time reamining 

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
                        active_bird_home_box = active_bird.get_rect() # Get the bird to go to dragging mode
            if not mouse_down:
                for event in events:
                    for i in (left_birds if turn=="left" else right_birds):
                        if (event.type == pygame.MOUSEBUTTONDOWN and i.get_rect().collidepoint(pygame.mouse.get_pos())):
                            if active_bird is None or i != active_bird:
                                on_select_sfx.play() # To play the sound on selecting the bird
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
                            break # To change bird selected or to select a bird
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
            active_projectile = (lambda x: (vy*x/vx) + (0.5*GRAVITY*(x**2/vx**2))) if selected_theme!="space" else (lambda x: (vy*x/vx))
            if (not active_rectangle.collidepoint(pygame.mouse.get_pos())): # To draw the prediction parabola
                points_prediction = []
                if (vx>0):
                    for i in range(23):
                        points_prediction.append(((active_bird.x + BIRD_SIZE/2 + (WIDTH/50)*i), (active_bird.y + BIRD_SIZE/2 +active_projectile((WIDTH/50)*i))))
                elif (vx<0):
                    for i in range(23):
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
                    on_launch_sfx.play() # To play the sound on release
                elif (event.type == pygame.MOUSEBUTTONUP and active_rectangle.collidepoint(pygame.mouse.get_pos())):
                    active_bird.on_cat = True
                    mouse_down = False
                    active_bird.x, active_bird.y = [active_rectangle[i] for i in (0,1)]

        else:
            points_prediction = []
            active_fortress = fortress_left if turn=="left" else fortress_right
            if (not active_bird.on_power) and (active_bird.collisions==0):
                for event in events:
                    if (event.type == pygame.MOUSEBUTTONDOWN or (event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE)): # Tp power up the burd
                        on_power_sfx.play()
                        active_bird.apply_power(left_birds if turn=="left" else right_birds, active_fortress)
                        active_bird.explosion_pos = (active_bird.x, active_bird.y)
            if active_bird.bird_type == "blues" and active_bird.on_power == True:
                active_birds = [x for x in (left_birds if turn == "left" else right_birds) if x.active == True]
                for i in range(len(active_birds)):
                    active_fortress.update(active_birds[i], collision_sfx)
                    active_birds[i].update()
            else:
                active_fortress.update(active_bird, collision_sfx)
                active_bird.update()
            if ((active_bird.bird_type=="red" and active_bird.size-BIRD_SIZE>0) and active_bird.on_power == False):
                active_bird.apply_power(left_birds if turn=="left" else right_birds, active_fortress)
            trail_timer += dt
            if trail_timer >= 40: # To draw the trail
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
            temp_game_choosing_time = pygame.time.get_ticks()

        
        if bird_choosing_right and not bird_choosing_left: # to choose the birds
            wind_lock_start += pygame.time.get_ticks()-temp_game_choosing_time
            temp_game_choosing_time = pygame.time.get_ticks()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        right_birds.append(Bird(BIRD_PACK, GROUND, catapult_right[0]-(BIRD_SIZE+bird_space)*right_no-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "red", "right"))
                        right_no += 1
                    elif event.key == pygame.K_c:
                        right_birds.append(Bird(BIRD_PACK, GROUND, catapult_right[0]-(BIRD_SIZE+bird_space)*right_no-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "chuck", "right"))
                        right_no += 1
                    elif event.key == pygame.K_b:
                        right_birds.append(Bird(BIRD_PACK, GROUND, catapult_right[0]-(BIRD_SIZE+bird_space)*right_no-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "blues", "right"))
                        right_no += 1
                    elif event.key == pygame.K_m:
                        right_birds.append(Bird(BIRD_PACK, GROUND, catapult_right[0]-(BIRD_SIZE+bird_space)*right_no-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "bomb", "right"))
                        right_no += 1
            if right_no>2: # Stop bird choosing
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

        if bird_choosing_left and not bird_choosing_right: # To choose the birds
            wind_lock_start += pygame.time.get_ticks()-temp_game_choosing_time
            temp_game_choosing_time = pygame.time.get_ticks()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        left_birds.append(Bird(BIRD_PACK, GROUND, catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+bird_space)*left_no, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "red", "left"))
                        left_no += 1
                        break
                    elif event.key == pygame.K_c:
                        left_birds.append(Bird(BIRD_PACK, GROUND, catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+bird_space)*left_no, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "chuck", "left"))
                        left_no += 1
                        break
                    elif event.key == pygame.K_b:
                        left_birds.append(Bird(BIRD_PACK, GROUND, catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+bird_space)*left_no, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "blues", "left"))
                        left_no += 1
                        break
                    elif event.key == pygame.K_m:
                        left_birds.append(Bird(BIRD_PACK, GROUND, catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+bird_space)*left_no, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, "bomb", "left"))
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
        fortress_right.draw(screen)
        fortress_left.draw(screen)
        screen.blit(catapult_image_left, catapult_left)
        screen.blit(catapult_image_right, catapult_right)
        name_1.draw(screen)
        name_2.draw(screen)
        screen.blit(timer_surf, (WIDTH - 180, 20)) if this_game_WIND_MAX>0 else None
        screen.blit(arrow_image, arrow_rect)
        draw_birds(screen, left_birds, right_birds)
        screen.blit(dim_surface, (0, 0))
        screen.blit(sound_img, sound_rect)
        Text(WIDTH/2, HEIGHT/4, "PAUSED", font(BIG_FONT), TEXT_COLOR[selected_theme]).draw(screen)
        screen.blit(resume_img, resume_rect)
        screen.blit(replay_img, replay_rect)
        screen.blit(quit_img, quit_rect)
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_p) or (event.type == pygame.MOUSEBUTTONDOWN and resume_rect.collidepoint(event.pos)):
                game_state = "game"
                wind_lock_start += pygame.time.get_ticks()-temp_game_pause_time
                break
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or (event.type == pygame.MOUSEBUTTONDOWN and replay_rect.collidepoint(event.pos)): # Replay variables re initilizing
                fortress_left  = Fortress(BLOCK_PACK, GROUND, "left",  this_game_width,  this_game_height)
                fortress_right = Fortress(BLOCK_PACK, GROUND, "right", this_game_width,  this_game_height, fortress_left)
                left_birds  = [Bird(BIRD_PACK, GROUND, catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+bird_space)*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, t, "left") for i,t in enumerate(BIRD_OPTIONS)]
                right_birds = [Bird(BIRD_PACK, GROUND, catapult_right[0]-(BIRD_SIZE+bird_space)*i-BIRD_SIZE, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, t, "right") for i,t in enumerate(BIRD_OPTIONS)]
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
                break
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or (event.type == pygame.MOUSEBUTTONDOWN and quit_rect.collidepoint(event.pos)):
                game_state = "end"
                win = "quit"
                break # sending to end screen

    elif game_state == "end":
        if (win=="left"):
            winner_text = Text(WIDTH/2, HEIGHT/1.7, f"{name_1.text} Won", font(MED_FONT), TEXT_COLOR[selected_theme])
        elif (win=="right"):
            winner_text = Text(WIDTH/2, HEIGHT/1.7, f"{name_2.text} Won", font(MED_FONT), TEXT_COLOR[selected_theme])
        elif (win=="quit"):
            winner_text = Text(WIDTH/2, HEIGHT/1.7, f"Game Quit", font(MED_FONT), TEXT_COLOR[selected_theme])
        screen.fill((255, 255, 255))
        screen.blit(background_img, (0, 0))
        screen.blit(sound_img, sound_rect)
        main_text.draw(screen)
        winner_text.draw(screen)
        screen.blit(play_again_surface, play_again_rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and play_again_rect_clickable.collidepoint(event.pos): # resetting all the variables
                game_state = "menu"
                for my_input in input_list:
                    my_input.text = ""
                    my_input.update()
                winner_text = None
                left_birds = [Bird(BIRD_PACK, GROUND, catapult_left[0]+CATAPULT_SIZE[0]+(BIRD_SIZE+bird_space)*i, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "left") for i,type in enumerate(BIRD_OPTIONS)]
                right_birds = [Bird(BIRD_PACK, GROUND, catapult_right[0]-(BIRD_SIZE+bird_space)*i-35, catapult_left[1]+CATAPULT_SIZE[1]-BIRD_SIZE, type, "right") for i,type in enumerate(BIRD_OPTIONS)]
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