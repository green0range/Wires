import pygame
from os import path
from time import sleep
import random

HUDs_to_render = []
comp = 0

# These should be changed dynamically from level scripts.
command1 = ""
command1_response = ""

tmp = 0

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

class Computer_ui:
    global comp, tmp
    def __init__(self):
        self.cs = pygame.Surface((400,400))
        self.colour = (249,249,249)
        self.font = pygame.font.Font(path.join("assets", "fonts", "ShareTechMono-Regular.ttf"), 14)
        self.run = True
        self.txt = "[USR943@GOVSYS~]$  "
        self.main()
    def text_blit_with_spaces(self, text, colour):
        textarray = text.split("\n")
        textsurface = pygame.Surface((400,100))
        for i in range(0, len(textarray)):
            textsurface.blit(self.font.render(textarray[i], 1, colour), (0, i*15))
        return textsurface
    def main(self):
        global comp, tmp
        self.ftxt = "[USR943@GOVSYS~]$ " + command1
        # Do command1
        if "sudo" in command1:
            for i in range(1, random.randint(1, 15)):
                sleep(0.1)
                self.hud = self.font.render(self.ftxt, 1, self.colour)
                self.cs.blit(self.hud, (0,0))
                self.hud = self.font.render(self.txt, 1, self.colour)
                self.cs.blit(self.hud, (0,15))
                self.txt = self.randtxt()
                comp = self.cs
                # TODO: stop bliting over top of other blits
        self.hud = self.text_blit_with_spaces(command1_response, self.colour)
        self.cs.blit(self.hud, (0,30))
        comp = self.cs
        while tmp < 100000:
            tmp +=1
        else:
            comp = 0
    def randtxt(self):
        letters = [
            "q",
            "w",
            "e",
            "r",
            "t",
            "y",
            "u",
            "i",
            "o",
            "p",
            "a",
            "s",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "l",
            "z",
            "x",
            "c",
            "v",
            "b",
            "n",
            "m"
        ]
        word = "[sudo] Password for USR943: "
        for i in range(1, random.randint(1, 12)):
            word += letters[random.randint(0, 25)]
        return word
