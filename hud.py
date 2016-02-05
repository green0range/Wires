import pygame

class Hud:
    def __init__(self, position, text, style="default"):
        self.x = position[0]
        self.y = position[1]
        self.txt = text
        self.font_default = pygame.font.Font("Nimbus Mono L", 12)

    def update(self, new_text):
        self.txt = new_text