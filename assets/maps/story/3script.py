import pygame, os
import objects, root
from time import sleep

rootdir = ""

def init():
    objects.update_player_location((1,1))
    sleep(0.25) # Wait for rest of level to load
    snd_congrats = pygame.mixer.Sound(os.path.join(rootdir, "2.Congratulations.ogg"))
    snd_congrats.set_volume(0.25)
    snd_congrats.play()
    sleep(6)
    snd_music = pygame.mixer.Sound(os.path.join(rootdir, "music.Kevin_MacLeod.Ossuary5-Rest.ogg"))
    snd_music.set_volume(1)
    snd_music.play()
    main()

def main():
    go = True
    while go:
        p = objects.player_position
        if (p[0] + objects.tile_w) > 40*objects.tile_w and p[0] < (40*objects.tile_w + objects.tile_w):
            if (p[1] + objects.tile_h) > (1*objects.tile_w) and p[1] < (1*objects.tile_h + objects.tile_h):
                root.next_level()
                go = False

def die():
    objects.update_player_location((1,1))