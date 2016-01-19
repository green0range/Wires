from pygame import *
from time import sleep
import graphics
tile_w, tile_h = 0, 0
map_w, map_h = 0, 0

def give_tile_data(w, h, mw, mh):
    global tile_w, tile_h, map_w, map_h
    tile_w, tile_h = w, h
    map_w, map_h = mw, mh

open_doors = []  # This lets the rendering rendering thread know which doors to render as open
first_time = True
active_objects = []  # this includes placed objects, Handler's self.objects MUST be updated to this after placing.

solid = []

request = "" # used to get player data without having access to the player object (which is in root)
response = ""

def player_position_request():
    global request, response
    if request == "answered":
        request = ""
        return response
    else:
        request = "posxy"

# Trivia: "mea tuara" (accented last a) is "spiky thing" in Maori, which has been shortened and de-accented to meatuara
# as the in game ceature which runs around which a spiky back - don't touch it.


class Player_items:
    def __init__(self):
        self.wires = 50

def detect_item(position):
    global tile_w, tile_h, map_w, map_h
    try:
        x = int(position[0]/tile_w) * tile_w
    except ZeroDivisionError:
        x = 0
    try:
        y = int(position[1]/tile_h) * tile_h
    except ZeroDivisionError:
        y = 0
    x_order = int(x/tile_w)
    y_order = int(y/tile_h)
    order = (y_order * map_w) + x_order
    return order

def die():
    print "you died!"

handler_output = Surface((map_w, map_h), SRCALPHA)
handler_input = []
handler_output_position = []
handler_input_all = []

class Handler:
    global solid, active_objects, open_doors, handler_output, handler_output_position
    def __init__(self):
        global active_objects
        self.graphic = graphics.Objects()
    def door_opening_check(self, position):  # FIXME: two wires will trigger door
        for i in range(0, 100):# Timeout in case break fails
            if "power_station" in active_objects[detect_item((position[0]-tile_w, position[1]))]:
                return True
            elif "power_station" in active_objects[detect_item((position[0]+tile_w, position[1]))]:
                return True
            elif "power_station" in active_objects[detect_item((position[0], position[1]-tile_h))]:
                return True
            elif "power_station" in active_objects[detect_item((position[0]-tile_w, position[1]+tile_h))]:
                return True
            else:
                if "electric" and "wire" in active_objects[detect_item((position[0]-tile_w, position[1]))]:# left
                    position = (position[0]-tile_w, position[1])
                elif "electric" and "wire" in active_objects[detect_item((position[0]+tile_w, position[1]))]:# right
                    position = (position[0]+tile_w, position[1])
                elif "electric" and "wire" in active_objects[detect_item((position[0], position[1]-tile_h))]:# up
                    position = (position[0], position[1]-tile_h)
                elif "electric" and "wire" in active_objects[detect_item((position[0], position[1]+tile_h))]:# down
                    position = (position[0], position[1]+tile_h)
                else:
                    return False
    def check_collisions(self, pos1, pos2): # Stolen from Player to for nails interaction
        # Pos1 should be player, pos2 should be block size
        tmp = True
        if (pos1[1] + 32) > pos2[1] and pos1[1] < (pos2[1] + tile_h):
            if (pos1[0] + 32) > pos2[0] and pos1[0] < (pos2[0] + tile_w):
                tmp = False
        return tmp
    def main_loop(self):
        global solid, open_doors, request, response, handler_output, handler_output_position, first_time
        #graphics.object_surface.fill((255,0,255))
        for j in range(0, len(handler_input_all)):
            block = handler_input_all[j]
            counter = j
            if "door" in active_objects[counter]:
                state = self.door_opening_check(block)
                if state == False:
                    if not (block, counter) in solid:
                        solid.append((block, counter))
                    if block in open_doors:
                        tmp = []
                        for i in range(0, len(open_doors)):
                            if open_doors[i] == block:
                                pass
                        else:
                            tmp.append(open_doors[i])
                        open_doors = tmp
                else: # FIXME: only one door will unlock at a time
                    if not block in open_doors:
                        open_doors.append(block)
                    if (block, counter) in solid:
                        tmp = []
                        for i in range(0, len(solid)):
                            if solid[i] == (block, counter):
                                pass
                            else:
                                tmp.append(solid[i])
                        solid = tmp
            if "meatuara_ns" in active_objects[counter]:
                graphics.object_surface.fill((255,0,255))
                tmp = active_objects[counter].split(" ")
                tmp[1] = int(tmp[1])
                tmp[2] = int(tmp[2])
                tmp[3] = int(tmp[3])
                if tmp[4] == "s":
                    tmp[3] += 1
                    if tmp[3] > tmp[1] * tile_h:
                        tmp[4] = "n"
                elif tmp[4] == "n":
                    tmp[3] -= 1
                    if tmp[3] < tmp[2] * tile_h * -1:
                        tmp[4] = "s"
                active_objects[counter] = tmp[0] + " " + str(tmp[1]) + " " + str(tmp[2]) + " " + str(tmp[3]) + " " + tmp[4]
                if request == "answered":
                    request = ""
                    if not self.check_collisions(response, (block[0], block[1] + tmp[3])):
                        die()
                else:
                    request = "posxy"
            # Put objects that only need be loaded once here
            if first_time:
                if "wall" in active_objects[counter]:
                    if not (block, counter) in solid:
                        solid.append((block, counter))
            # === END OF FIRST TIME === #
            if "wire" in active_objects[counter]:
                # TODO: Wire stuff
                pass
            if "nails" in active_objects[counter]:
                if request == "answered":
                    request = ""
                    if not self.check_collisions(response, block):
                        die()
                else:
                    request = "posxy"
            graphics.prepare_object_blit(active_objects[counter], block)
        first_time = False

class Player:
    global solid, tile_w, tile_h
    def __init__(self):
        # TODO: Start positions
        self.x = 500
        self.y = 200
        i = graphics.PlayerImg()
        self.width = i.get_size()[0]
        self.height = i.get_size()[1]
        self.current = "north"
        self.items = Player_items()
    def check_collisions(self, pos):
        '''try:
            x = int(pos[0]/tile_w) * tile_w
        except ZeroDivisionError:
            x = 0
        try:
            y = int(pos[1]/tile_h) * tile_h
        except ZeroDivisionError:
            y = 0
        j = ((y/tile_h)*map_h) + (x/tile_w)
        for i in range(0, len(solid)):
            if solid[i][1] == j:
                print solid'''
        tmp = True
        for i in range(0, len(solid)):
            if (pos[1] + self.width) > solid[i][0][1] and pos[1] < (solid[i][0][1] + tile_h):
                if (pos[0] + self.height) > solid[i][0][0] and pos[0] < (solid[i][0][0] + tile_w):
                    tmp = False
        return tmp
    def move(self, keys):
        global solid, tile_w, tile_h, request, response
        cant_move = False
        if keys[K_w] or keys[K_UP]:
            if self.check_collisions((self.x, self.y-1)):
                self.y -= 1
        if keys[K_s] or keys[K_DOWN]:
            if self.check_collisions((self.x, self.y+1)):
                self.y += 1
        if keys[K_a] or keys[K_LEFT]:
            if self.check_collisions((self.x-1, self.y)):
                self.x -= 1
        if keys[K_d] or keys[K_RIGHT]:
            if self.check_collisions((self.x+1, self.y)):
                self.x += 1
        if keys[K_e]:
            if "none" in active_objects[detect_item((self.x, self.y))]:
                if self.items.wires > 0:
                    if create_wire((self.x, self.y)):
                        self.items.wires -=1
                        sleep(0.3)
            elif "wire" in active_objects[detect_item((self.x, self.y))]:
                if remove_wire((self.x, self.y)):
                    self.items.wires +=1
                sleep(0.3)
        if request == "posxy":
            response = (self.x, self.y)
            request = "answered"
    def render(self):
        return self.current, (self.x, self.y)

def get_wire_direction(position):
    global tile_w, tile_h, map_w, map_h, active_objects
    try:
        x = int(position[0]/tile_w) * tile_w
    except ZeroDivisionError:
        x = 0
    try:
        y = int(position[1]/tile_h) * tile_h
    except ZeroDivisionError:
        y = 0
    if "connect" in active_objects[detect_item((x+tile_w+10, y))] and "connect" in active_objects[detect_item((x, y+tile_h+10))]:
        return "es"
    elif "connect" in active_objects[detect_item((x+tile_w+10, y))] and "connect" in active_objects[detect_item((x, y-tile_h+10))]:
        return "ne"
    elif "connect" in active_objects[detect_item((x-tile_w+10, y))] and "connect" in active_objects[detect_item((x, y-tile_h+10))]:
        return "nw"
    elif "connect" in active_objects[detect_item((x-tile_w+10, y))] and "connect" in active_objects[detect_item((x, y+tile_h+10))]:
        return "sw"
    elif "connect" in active_objects[detect_item((x+tile_w+10, y))] or "connect" in active_objects[detect_item((x-tile_w+10, y))]:
        return "ew"
    else:
        return "ns"

def create_wire(position, type="electric_insulated"):  # TODO: wiretypes
    global active_objects
    order = detect_item(position)
    if active_objects[order] == "none":
        active_objects[order] = "electric_insulated_wire_connect"
        return True
    else:
        return False  # attempted place on other item

def remove_wire(position):
    global active_objects
    order = detect_item(position)
    if "wire" in active_objects[order]:
        active_objects[order] = "none"
        return True
    else:
        return False  # not on a wire