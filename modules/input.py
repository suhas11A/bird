import pygame # type: ignore
from modules.variables import *
from modules.text import *

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
        self.outline_surface = pygame.image.load(f"./media/images/input_box_{self.state}.png")
        self.outline_surface = pygame.transform.scale(self.outline_surface, (WIDTH/4, HEIGHT/14))
        self.outline_rect = self.outline_surface.get_rect(center=(self.x,self.y))

    def draw(self, screen):
       screen.blit(self.text_surface, self.text_rect)
       screen.blit(self.outline_surface, self.outline_rect)
    
    def update(self):
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))
        self.outline_surface = pygame.image.load(f"./media/images/input_box_{self.state}.png")
        self.outline_surface = pygame.transform.scale(self.outline_surface, (WIDTH/4, HEIGHT/14))
        self.outline_rect = self.outline_surface.get_rect(center=(self.x,self.y))

    def make_text(self, x, y):
        return Text(x, y, self.text, self.font, text_color = self.text_color)

def draw_inputs(screen, *input_list):
    for listt in input_list:
        for i in listt:
            i.draw(screen)

def make_texts(input_list):
    return (input_list[0].make_text(WIDTH/5, HEIGHT/6), input_list[1].make_text(4*WIDTH/5, HEIGHT/6))