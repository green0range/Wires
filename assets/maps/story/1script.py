import pygame, os
import objects, root

rootdir = ""

def init():
    objects.update_player_location((2,7))
    snd_welcome = pygame.mixer.Sound(os.path.join(rootdir, "1.welcome.door_power.ogg"))
    snd_welcome.play()
    main()

def main():
    go = True
    while go:
        p = objects.player_position
        if (p[0] + objects.tile_w) > 40*objects.tile_w and p[0] < (40*objects.tile_w + objects.tile_w):
            if (p[1] + objects.tile_h) > (20*objects.tile_w) and p[1] < (20*objects.tile_h + objects.tile_h):
                root.next_level()
                go = False
