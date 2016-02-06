import pygame
from os import path
from time import sleep

HUDs_to_render = []

class Hud:
    def __init__(self, position, text, timeout=0, style="default"):
        self.txt = text
        self.colour = (0,0,0)
        self.font = pygame.font.Font(path.join("assets", "fonts", "ShareTechMono-Regular.ttf"), 25)
        self.hud = self.font.render(self.txt, 1, self.colour)
        HUDs_to_render.append((self.hud, position))
        if timeout > 0:
            self.timeout(timeout)

    def timeout(self, timeout):
        sleep(timeout)
        for i in range(0, len(HUDs_to_render)):
            if self.hud in HUDs_to_render[i]:
                HUDs_to_render.pop(i)