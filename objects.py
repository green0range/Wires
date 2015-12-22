from pygame import *
from time import sleep
import graphics
tile_w, tile_h = 0, 0
solids_in_use = False

def give_tile_data(w, h):
    global tile_w, tile_h
    tile_w, tile_h = w, h


solid = []

class Handler:
    global solid
    def __init__(self, obj):
        self.objects = obj
        self.graphic = graphics.Objects()
    def main_loop(self, block=(0,0), counter=0):
        global solid
        if "door" in self.objects[counter]:
            # TODO: door stuff
            pass
        if "wall" in self.objects[counter]:
            solid.append(block)
            # TODO: solidise
        return self.objects[counter]

class Player:
    global solid, tile_w, tile_h
    def __init__(self):
        # TODO: Start positions
        self.x = 100
        self.y = 100
        self.current = "north"
    def check_collisions(self, pos):
        try:
            solids_in_use = True
            tmp = True
            for i in range(0, len(solid)):
                if pos[0] > solid[i][0] - 32 and pos[0] < solid[i][0] + tile_w:
                    if pos[1] + 32 > solid[i][1] and pos[1] < solid[i][1] + tile_w:
                        solids_in_use = False
                        tmp = False
            solids_in_use = False
            return tmp
        except:
            return False
    def move(self, keys):
        global solid, tile_w, tile_h
        cant_move = False
        if keys[K_w] or keys[K_UP]:
            if self.check_collisions((self.x, self.y-5)):
                self.y -= 1
                sleep(0.001)
        if keys[K_s] or keys[K_DOWN]:
            if self.check_collisions((self.x, self.y+5)):
                self.y += 1
                sleep(0.001)
        if keys[K_a] or keys[K_LEFT]:
            if self.check_collisions((self.x-5, self.y)):
                self.x -= 1
                sleep(0.001)
        if keys[K_d] or keys[K_RIGHT]:
            if self.check_collisions((self.x+5, self.y)):
                self.x += 1
                sleep(0.001)
    def render(self):
        return self.current, (self.x, self.y)

    '''def check_collisions(self, pos):
        go = True
        for i in range(0, len(solid)):
            if pos[0] > solid[i][0] - 32 and self.x < solid[i][0] + tile_w:
                if pos[1] > solid[i][1] - 32 and self.x < solid[i][1] + tile_w:
                    go = False
                    print "faldse"'''