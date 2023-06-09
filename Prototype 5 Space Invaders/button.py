import pygame
from pygame import *

class Button():
    #set the parameters of the button class
    def __init__(self, pos, text_input, font, base_color, hovering_color, fileName):
        self.x_pos = pos[0];
        self.y_pos = pos[1];
        self.text_input = text_input;
        self.font = font;
        self.base_color = base_color;
        self.hovering_color = hovering_color;
        self.sound = pygame.mixer.Sound(fileName);
        self.text = self.font.render(self.text_input, True, self.base_color);
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos));

    #update function to blit the button
    def update(self, screen):
        screen.blit(self.text, self.text_rect);

    #function to check for mouse input on the button
    def checkInput(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.sound.play();
            return True;
        return False;

    #change the color of the rect button when its hovered over
    def changeColorHover(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color);
        else:
            self.text = self.font.render(self.text_input, True, self.base_color);
