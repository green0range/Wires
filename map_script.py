import pygame, os

rootdir = ""

def init():
    snd_welcome = pygame.mixer.Sound(os.path.join(rootdir, "1.welcome.door_power.mp3"))
    snd_welcome.play()