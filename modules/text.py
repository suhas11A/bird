import pygame # type: ignore
from modules.variables import *

class Text:
    def __init__(self, x, y, text, font, text_color = (255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color
        self.font = font
        self.surface = font.render(text, True, text_color)
        self.rect = self.surface.get_rect(center=(x, y))

    def draw(self, screen):
       screen.blit(self.surface, self.rect)
    
    def update(self):
        self.surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))