import pygame # type: ignore
from modules.variables import *
from modules.text import *
from modules.helper import *

class Input:
    def __init__(self, x, y, text, font, state, text_color = (255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color
        self.font = font
        self.state = state
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=(x, y))
        self.outline_surface = pygame.image.load(f"./media/images/input_images/input_box_{self.state}.png")
        self.outline_surface = pygame.transform.scale(self.outline_surface, (WIDTH/4, HEIGHT/14))
        self.outline_rect = self.outline_surface.get_rect(center=(self.x,self.y))

    def draw(self, screen):
        draw_rounded_image_with_border(screen, self.outline_surface, self.outline_rect, border_color=(0, 0, 0), border_thickness=0, radius=round(14*(WIDTH/1600)))
        screen.blit(self.text_surface, self.text_rect)
    
    def update(self): # If its deadens or alivens the images is refetched
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))
        self.outline_surface = pygame.image.load(f"./media/images/input_images/input_box_{self.state}.png")
        self.outline_surface = pygame.transform.scale(self.outline_surface, (WIDTH/4, HEIGHT/14))
        self.outline_rect = self.outline_surface.get_rect(center=(self.x,self.y))

    def make_text(self, x, y, color): # Makes text object from names so that i can use it in the game play screen
        return Text(x, y, self.text, self.font, text_color = color)

def draw_inputs(screen, *input_list):
    for listt in input_list:
        for i in listt:
            i.draw(screen)

def make_texts(input_list,theme):
    return (input_list[0].make_text(WIDTH/5, HEIGHT/6, TEXT_COLOR[theme]), input_list[1].make_text(4*WIDTH/5, HEIGHT/6, TEXT_COLOR[theme]))