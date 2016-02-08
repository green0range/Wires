import pygame, os
import objects, root
from time import sleep

rootdir = ""

def init():
    objects.update_player_location((1,1))
    sleep(0.25) # Wait for rest of level to load
    snd_congrats = pygame.mixer.Sound(os.path.join(rootdir, "3.spilt_nails.ogg"))
    snd_congrats.set_volume(0.25)
    snd_congrats.play()
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