from pygame import *
from time import sleep
import graphics, hud
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

player_position = []

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
    import map_script
    try:
        map_script.die()
    except:
        print "ERR003. Map Script die() not found/ not functional."
        print "If you are a map make, please note that you map's scripts need a die() function if harmful objects"
        print "are included in said map. It is recommended that this reset the map, although i'm keen for any other"
        print "interesting and/ or unique ideas. ~ William"
        print "PS. Or just print this message 1000 times per second. Why not?!"

handler_output = Surface((map_w, map_h), SRCALPHA)
handler_output_position = []
handler_input_all = []

wires_update = False

class Handler:
    global solid, active_objects, open_doors, handler_output, handler_output_position, nail_list
    def __init__(self):
        global active_objects
        self.graphic = graphics.Objects()
        self.players_items = player_items_crosslevel
        self.door_state = False
    def door_opening_check(self, p):  # FIXME: two wires will trigger door
        position = p
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
                elif "electric" and "wire" in active_objects[detect_item((position[0], position[1]-tile_h))]:# up
                    position = (position[0], position[1]-tile_h)
                elif "electric" and "wire" in active_objects[detect_item((position[0]+tile_w, position[1]))]:# right
                    position = (position[0]+tile_w, position[1])
                elif "electric" and "wire" in active_objects[detect_item((position[0], position[1]+tile_h))]:# down
                    position = (position[0], position[1]+tile_h)
                else:
                    return False
        return False
    def check_collisions(self, pos1, pos2): # Stolen from Player to for nails interaction
        # Pos1 should be player, pos2 should be block size
        tmp = True
        if (pos1[1] + player_size[1]) > pos2[1] and pos1[1] < (pos2[1] + tile_h):
            if (pos1[0] + player_size[0]) > pos2[0] and pos1[0] < (pos2[0] + tile_w):
                tmp = False
        return tmp
    def main_loop(self):
        global solid, open_doors, request, response, handler_output, handler_output_position, first_time, obj_loop_end, obj_loop_start, nail_list, wires_update
        obj_loop_start = 0
        obj_loop_end = len(handler_input_all)
        box_solid_position = len(solid)
        for j in range(obj_loop_start, obj_loop_end):
            block = handler_input_all[j]
            counter = j
            if "door" in active_objects[counter]:
                if wires_update:
                    self.door_state = self.door_opening_check(block)
                    wires_update = False
                if self.door_state == False:
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
                else:
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
                graphics.object_surface.fill((255,0,255))
                if "wall" in active_objects[counter]:
                    if not (block, counter) in solid:
                        solid.append((block, counter))
            # === END OF FIRST TIME === #
            else: # Limit updates to blocks surrounding player.
                '''********************************************************** '''
                start = (int(player_position[0]/tile_h)-1, int(player_position[1]/tile_w)-1)
                end = (int(player_position[0]/tile_h)+1, int(player_position[1]/tile_w)+1)
                obj_loop_start = (start[1]*map_w)+start[0]
                obj_loop_end = (end[1]*map_w)+end[0]
            if "wire" in active_objects[counter]:
                if "electric" in active_objects[counter]:
                    if "insulated" in active_objects[counter]:
                        if "refill" in active_objects[counter]:
                            if self.players_items.wires != 50:
                                self.players_items.wires = 50
                    else:
                        if not self.check_collisions(player_position, block):
                            die()
            if "box" in active_objects[counter]:
                tmp = active_objects[counter].split(" ")
                # push right
                if block[0] + int(tmp[1]) - 5 <= player_position[0] + player_size[0] and block[0] + int(tmp[1]) + 5 >= player_position[0] + player_size[0]:
                    if block[1] + int(tmp[2]) <= player_position[1] + player_size[1] and block[1] + int(tmp[2]) + tile_h >= player_position[1] + player_size[1]:
                        for i in range(0, len(solid)):
                            if solid[i] == ((block[0] + int(tmp[1]), block[1] + int(tmp[2])), counter):
                                solid.pop(i)
                        solid.append(((block[0] + int(tmp[1])+3, block[1] + int(tmp[2])), counter))
                        active_objects[counter] = tmp[0] + " " + str(int(tmp[1])+3) + " " + tmp[2]
                        block_wipe_nail((block[0] + int(tmp[1])+3, block[1] + int(tmp[2])))
                        graphics.redraw(block[0] + int(tmp[1]), block[1] + int(tmp[2]), block[0] + int(tmp[1])+tile_w, block[1] + int(tmp[2])+tile_h)
                # left
                if block[0] + int(tmp[1]) + tile_w -5 <= player_position[0] and block[0] + int(tmp[1]) + tile_w + 5 >= player_position[0]:
                    if block[1] + int(tmp[2]) <= player_position[1] + player_size[1] and block[1] + int(tmp[2]) + tile_h >= player_position[1] + player_size[1]:
                        for i in range(0, len(solid)):
                            if solid[i] == ((block[0] + int(tmp[1]), block[1] + int(tmp[2])), counter):
                                solid.pop(i)
                        solid.append(((block[0] + int(tmp[1])-3, block[1] + int(tmp[2])), counter))
                        active_objects[counter] = tmp[0] + " " + str(int(tmp[1])-3) + " " + tmp[2]
                        block_wipe_nail((block[0] + int(tmp[1])-3, block[1] + int(tmp[2])))
                        graphics.redraw(block[0] + int(tmp[1]), block[1] + int(tmp[2]), block[0] + int(tmp[1])+tile_w, block[1] + int(tmp[2])+tile_h)
                # down
                if block[0] + int(tmp[1]) <= player_position[0] and block[0] + int(tmp[1]) + tile_w >= player_position[0]:
                    if block[1] + int(tmp[2]) -5 <= player_position[1] + player_size[1] and block[1] + int(tmp[2]) + 5>= player_position[1]:
                        for i in range(0, len(solid)):
                            if solid[i] == ((block[0] + int(tmp[1]), block[1] + int(tmp[2])), counter):
                                solid.pop(i)
                        solid.append(((block[0] + int(tmp[1]), block[1] + int(tmp[2])+3), counter))
                        active_objects[counter] = tmp[0] + " " + tmp[1]+ " " + str(int(tmp[2])+3)
                        block_wipe_nail((block[0] + int(tmp[1]), block[1] + int(tmp[2])+3))
                        graphics.redraw(block[0] + int(tmp[1]), block[1] + int(tmp[2]), block[0] + int(tmp[1])+tile_w, block[1] + int(tmp[2])+tile_h)
                    # up
                    if block[1] + int(tmp[2]) + tile_h -5 <= player_position[1] and block[1] + int(tmp[2]) + tile_h + 5>= player_position[1]:
                        for i in range(0, len(solid)):
                            if solid[i] == ((block[0] + int(tmp[1]), block[1] + int(tmp[2])), counter):
                                solid.pop(i)
                        solid.append(((block[0] + int(tmp[1]), block[1] + int(tmp[2])-3), counter))
                        active_objects[counter] = tmp[0] + " " + tmp[1]+ " " + str(int(tmp[2])-3)
                        block_wipe_nail((block[0] + int(tmp[1]), block[1] + int(tmp[2])-3))
                        graphics.redraw(block[0] + int(tmp[1]), block[1] + int(tmp[2]), block[0] + int(tmp[1])+tile_w, block[1] + int(tmp[2])+tile_h)
            if "nails" in active_objects[counter]:
                    if not self.check_collisions(player_position, block):
                        die()
                    if not block in nail_list:
                        nail_list.append((block, counter))
            # noinspection PyInterpreter
            if "computer" in active_objects[counter]:
                if not self.check_collisions(player_position, (block[0], block[1]-1)):
                    comp = hud.Computer_ui()
                    #comp_note = hud.Hud((block[0], block[1]-40), "Hold 'e'", timeout=3)
                    if key.get_pressed()[K_e]:
                        comp = hud.Computer_ui()
                        print "e"
            graphics.prepare_object_blit(active_objects[counter], block)
        first_time = False

nail_list = []

def block_wipe_nail(box):
    try:
        for i in range(0, len(nail_list)):
            if box[0] <= nail_list[i][0][0] and box[0] + tile_w >= nail_list[i][0][0]:
                if box[1] <= nail_list[i][0][1] and box[1] + tile_h >= nail_list[i][0][1]:
                    active_objects[nail_list[i][1]] = "none"
                    nail_list.pop(i)
    except IndexError:
        pass


player_request = ""

def update_player_location(new):
    global player_request, tile_w, tile_h
    player_request = "location_update " + str(new[0]*tile_h) + " " + str(new[1]*tile_w)

player_items_crosslevel = Player_items()

class Player:
    global solid, tile_w, tile_h, player_position, player_size
    def __init__(self):
        global player_size
        # TODO: Start positions
        self.x = 500
        self.y = 200
        i = graphics.PlayerImg()
        self.width = i.get_size()[0]
        self.height = i.get_size()[1]
        player_size = (self.width, self.height)
        i = 0
        self.current = "north"
        self.items = player_items_crosslevel
        self.collision_check_limiter = 0
        self.collision_check_oldstate = True
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
        tmp = self.collision_check_oldstate
        print len(solid)
        # This means it only checks every 5 keypresses
        self.collision_check_limiter +=1
        if self.collision_check_limiter > 4:
            tmp = True
            for i in range(0, len(solid)):
                try:
                    if (pos[1] + self.width) > solid[i][0][1] and pos[1] < (solid[i][0][1] + tile_h):
                        if (pos[0] + self.height) > solid[i][0][0] and pos[0] < (solid[i][0][0] + tile_w):
                            tmp = False
                except IndexError:
                    print "Index error in movement solid checker. Did another thread remove a solid?"
            self.collision_check_limiter = 0
            self.collision_check_oldstate = tmp
        return tmp
    def move(self, keys):
        global solid, tile_w, tile_h, request, response, player_position
        cant_move = False
        if keys[K_w] or keys[K_UP]:
            if self.check_collisions((self.x, self.y-5)):
                self.y -= 1
                self.current = "north"
                sleep(0.001)
        if keys[K_s] or keys[K_DOWN]:
            if self.check_collisions((self.x, self.y+5)):
                self.y += 1
                self.current = "south"
                sleep(0.001)
        if keys[K_a] or keys[K_LEFT]:
            if self.check_collisions((self.x-5, self.y)):
                self.x -= 1
                self.current = "east"
                sleep(0.001)
        if keys[K_d] or keys[K_RIGHT]:
            if self.check_collisions((self.x+5, self.y)):
                self.x += 1
                self.current = "west"
                sleep(0.001)
        if keys[K_e]:
            if "none" in active_objects[detect_item((self.x, self.y))] or "box" in active_objects[detect_item((self.x, self.y))]:
                if self.items.wires > 0:
                    if create_wire((self.x, self.y)):
                        self.items.wires -=1
                        graphics.object_surface.fill((255,0,255))
                        sleep(0.3)
            elif "wire" in active_objects[detect_item((self.x, self.y))]:
                if remove_wire((self.x, self.y)):
                    self.items.wires +=1
                    graphics.object_surface.fill((255,0,255))
                sleep(0.3)
        if request == "posxy":
            response = (self.x, self.y)
            request = "answered"
    def render(self):
        global player_position
        player_position = (self.x, self.y)
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
    global active_objects, wires_update
    wires_update = True
    order = detect_item(position)
    if active_objects[order] == "none":
        active_objects[order] = "electric_insulated_wire_connect"
        graphics.redraw(position[0], position[1], position[0]+tile_w, position[1]+tile_h)
        return True
    elif "box" in active_objects[order]:
        active_objects[order] += " electric_insulated_wire_connect"
        graphics.redraw(position[0], position[1], position[0]+tile_w, position[1]+tile_h)
    else:
        return False  # attempted place on other item

def remove_wire(position):
    global active_objects
    order = detect_item(position)
    if "wire" in active_objects[order]:
        active_objects[order] = "none"
        graphics.redraw(position[0], position[1], position[0]+tile_w, position[1]+tile_h)
        return True
    else:
        return False  # not on a wire