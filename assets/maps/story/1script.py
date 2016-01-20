import pygame, os
import objects

rootdir = ""

def init():
    objects.update_player_location((2,7))
    snd_welcome = pygame.mixer.Sound(os.path.join(rootdir, "1.welcome.door_power.ogg"))
    snd_welcome.play()
    main()

def main():
    while True:
        p = objects.player_position_request()
        print p
        if (p[0] + objects.tile_w) > 39*objects.tile_w and p[0] < (39*objects.tile_w + objects.tile_w):
            print "x"
            if (p[1] + objects.tile_h) > (39*objects.tile_w) and p[1] < (39*objects.tile_h + objects.tile_h):
                print "level completed"