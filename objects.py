from pygame import *
from time import sleep
import graphics
tile_w, tile_h = 0, 0
map_w, map_h = 0, 0
solids_in_use = False

def give_tile_data(w, h, mw, mh):
    global tile_w, tile_h, map_w, map_h
    tile_w, tile_h = w, h
    map_w, map_h = mw, mh

active_objects = []  # this includes placed objects, Handler's self.objects MUST be updated to this after placing.

solid = []

class Handler:
    global solid, active_objects
    def __init__(self, obj):
        global active_objects
        active_objects = obj
        self.graphic = graphics.Objects()
        o = Wire((0,0))
    def main_loop(self, block=(0,0), counter=0):
        global solid
        if "door" in active_objects[counter]:
            # TODO: door stuff
            pass
        if "wall" in active_objects[counter]:
            solid.append(block)
            # TODO: solidise
        if "wire" in active_objects[counter]:
            # TODO: Wire stuff
            pass
        return active_objects[counter]

class Player:
    global solid, tile_w, tile_h
    def __init__(self):
        # TODO: Start positions
        self.x = 500
        self.y = 200
        self.current = "north"
    def check_collisions(self, pos):  # TODO: fix slow warp through block thing
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


class Wire:
    global tile_w, tile_h, map_w, map_h
    def __init__(self, position, type="electric.insulated"):
        global tile_w, tile_h, map_w, map_h
        try:
            self.x = int(position[0]/tile_w) * tile_w
        except ZeroDivisionError:
            self.x = 0
        try:
            self.y = int(position[1]/tile_h) * tile_h
        except ZeroDivisionError:
            self.y = 0
        self.object_w_positions = []
        print self.x, self.y
        for i in range(0, len(active_objects)):
            # Find x,y coordinates for ordered object list
            try:
                x = (i - (int(i/map_w) * map_w)) * tile_w
            except ZeroDivisionError:
                x = 0
            try:
                y = int(i/map_h) * tile_h
            except ZeroDivisionError:
                y = 0
            self.object_w_positions.append((x,y,i))
            if self.x == x and self.y == y:
                # Placing on top of other object
                if active_objects[i] == "none":
                    active_objects[i] = "wire_electric_insulated"
                    print i
                else:
                    print "dsfdsgdg" + str(i)
                    raise ValueError("ERR-IN-003")

        print self.object_w_positions