from pygame import *
from os import path
import objects

tile_w = 0
tile_h = 0
screen_size = (1200, 750)

script = ""

# This class stores all terrain graphics, accessible via Terrain.<graphicname>
# When creating a Terrain object, the screen size and tile amount of level must
# be passed, so that the correct scaling can be calculated. This should be passed
# in the correct aspect ratio. Because of this Terrain objects will have to be re-generated
# Terrain is opaque, and should be in jpg format. It is the lowest drawing level
class Terrain:
    global tile_w, tile_h, screen_size
    def __init__(self, screen=(800, 600), tile=(8,6)):
        global tile_w, tile_h, screen_size
        screen_size = screen
        tile_w = screen[0]/tile[0]
        tile_h = screen[1]/tile[1]
        objects.give_tile_data(tile_w, tile_h, tile[0], tile[1])
        # Bulk imports
        import_list = [
            path.join("assets", "terrain", "wood_floor.jpg"),
            path.join("assets", "terrain", "marble_floor.jpg"),
            path.join("assets", "terrain", "stone_floor.jpg")
        ]
        export_list = []
        for i in range (0, len(import_list)):
            tmp = image.load(import_list[i]).convert()
            export_list.append(transform.scale(tmp, (tile_w, tile_h)))
        tmp = 0
        # Convert to easier naming system
        self.wood_floor = export_list[0]
        self.marble_floor = export_list[1]
        self.stone_floor = export_list[2]
        # Clear export list to save space
        export_list = 0

# This class stores all graphics for the in game items and objects, i.e doors, drops etc.
# Accessible via Objects.<object/item name>. Objects are transparent and must be in png
# They are drawn over top of terrain
class Objects:
    global tile_w, tile_h
    def __init__(self):
        global tile_w, tile_h
        # Bulk imports
        import_list = [
            path.join("assets", "objects", "wood_door_base_ns.png"),
            path.join("assets", "objects", "wood_door_ns.png"),
            path.join("assets", "objects", "wood_door_base_ew.png"),
            path.join("assets", "objects", "wood_door_ew.png"),
            path.join("assets", "objects", "wood_wall.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_es.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_ew.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_ne.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_ns.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_nw.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_sw.png"),
            path.join("assets", "objects", "wires", "power_station.png"),
            path.join("assets", "objects", "nails.png"),
            path.join("assets", "objects", "marble_wall.png"),
            path.join("assets", "objects", "meatuara_ns.png"),
            path.join("assets", "objects", "stone_wall.png"),
            path.join("assets", "objects", "wood_box.png"),
            path.join("assets", "objects", "wire_refill.png")
        ]
        export_list = []
        for i in range (0, len(import_list)):
            tmp = image.load(import_list[i]).convert_alpha()
            export_list.append(transform.scale(tmp, (tile_w, tile_h)))
        tmp = 0
        # Convert to easier naming system
        self.wood_door_base_ns = export_list[0]
        self.wood_door_ns = export_list[1]
        self.wood_door_base_ew = export_list[2]
        self.wood_door_ew = export_list[3]
        self.wood_wall = export_list[4]
        self.wire_electric_insulated_es = export_list[5]
        self.wire_electric_insulated_ew = export_list[6]
        self.wire_electric_insulated_ne = export_list[7]
        self.wire_electric_insulated_ns = export_list[8]
        self.wire_electric_insulated_nw = export_list[9]
        self.wire_electric_insulated_sw = export_list[10]
        self.power_station = export_list[11]
        self.nails = export_list[12]
        self.marble_wall = export_list[13]
        self.meatuara_ns = export_list[14]
        self.stone_wall = export_list[15]
        self.wood_box = export_list[16]
        self.wire_electric_insulated_refill = export_list[17]
        # Clear export list to save space
        export_list = 0

class PlayerImg:
    def __init__(self):
        self.north = transform.scale(image.load(path.join("assets", "objects", "player", "north.png")).convert_alpha(), (int(tile_w*0.5), int(tile_h*0.5)))
        self.east = transform.scale(image.load(path.join("assets", "objects", "player", "east.png")).convert_alpha(), (int(tile_w*0.5), int(tile_h*0.5)))
        self.south = transform.scale(image.load(path.join("assets", "objects", "player", "south.png")).convert_alpha(), (int(tile_w*0.5), int(tile_h*0.5)))
        self.west = transform.scale(image.load(path.join("assets", "objects", "player", "west.png")).convert_alpha(), (int(tile_w*0.5), int(tile_h*0.5)))
    def get_size(self):
        return int(tile_w*0.5), int(tile_h*0.5)

object_surface = Surface(screen_size)#((objects.map_w, objects.map_h), SRCALPHA) screen_size
object_surface.set_colorkey((255,0,255))
object_surface.fill((255,0,255))

# This class imports map files, separates data, and then perpares for rendering. The import_map
# function must be called once first, and then for every new map. The render function runs off'
# data prepared in the import_map function, and should be looped after the import is called.
# It does not full render the images but sorts out all their coordinates, which are then returned
# to the caller with the terrain image for full rendering. This can be done by bliting the return
# value. Objects are passed to the object handle after being read from the map file. Meta data
# about the map, such as title, author and description can also be gained with the get_info function.
class MapImports:
    global object_surface, script
    def __init__(self, screen):
        self.screen = screen
        self.background_imagery = Surface(screen)
        self.moving_objects = Surface(screen, SRCALPHA, 32)
        self.moving_objects.convert_alpha()
        self.i = 0
        self.i_unlock = True
    def import_map(self, m=(path.join("assets", "maps", "testmap.wrm")), want_meta=False):
        print "IMPORTING:"
        print m
        global script
        try:
            f = open(m, "r")
            f_raw = f.readlines()
            f.close()
        except:
            print "ERR002: File not found"
            f_raw = ""
        # Find start points of each data type
        for i in range(0, len(f_raw)):
            f_raw[i] = f_raw[i].strip("\n\r")
            if f_raw[i] == "!HEIGHT:":
                height_point = i
            if f_raw[i] == "!WIDTH:":
                width_point = i
            if f_raw[i] == "!TERRAIN:":
                terrain_point = i
            if f_raw[i] == "!TITLE:":
                title_point = i
            if f_raw[i] == "!DESCRIPTION:":
                description_point = i
            if f_raw[i] == "!AUTHOR:":
                author_point = i
            if f_raw[i] == "!DATESTAMP:":
                date_point = i
            if f_raw[i] == "!OBJECT:":
                object_point = i
            if f_raw[i] == "!DESCRIPTIONLENGTH:":
                descriptionlength_point = i
            if f_raw[i] == "!SCRIPT:":
                script_point = i
        # Extracts data from beyond start point marker
        try:
            self.map_h = int(f_raw[height_point + 1])
            self.map_w = int(f_raw[width_point + 1])
            area = self.map_h * self.map_w
            self.terrain = []
            self.objects = []
            script = f_raw[script_point + 1]
            for i in range(0, area):
                self.terrain.append(f_raw[terrain_point+1+i])
            for i in range(0, area):
                self.objects.append(f_raw[object_point+1+i])
            objects.active_objects = self.objects
            if want_meta:
                self.title = (f_raw[title_point + 1])
                self.author = (f_raw[author_point + 1])
                self.datestamp = (f_raw[date_point + 1])
                self.descriptionlength = int(f_raw[descriptionlength_point + 1])
                self.description = ""
                for i in range(0, self.descriptionlength):
                    self.description += f_raw[description_point+1+i]
                return(self.title, self.description, self.author, self.datestamp)
        except UnboundLocalError:
            print "ERR001: Map data is incomplete"
            # TODO: Pass to error handler and show graphical warning.
        self.t = Terrain(screen=self.screen, tile=(self.map_w, self.map_h))
        self.x_counter = -(self.screen[0]/self.map_w)
        self.y_counter = 0
        self.terrain_counter = -1

    def render(self):
        global object_surface, object_surface_done
        # Terrain rendering starts at top left tile then left -> right -> Next line repeat. Until all is rendered.
        # This relies on being constantly repeated in another function. It forwards all object render data from
        # the object controller. Yeah, it's pass the parcel in here.
        self.restart = False
        while not self.restart:
            self.terrain_counter += 1
            self.x_counter += (self.screen[0]/self.map_w)
            if self.x_counter >= self.screen[0]-3:
                self.x_counter = 0
                self.y_counter += (self.screen[1]/self.map_h)
            if self.y_counter >= self.screen[1]-3:
                self.x_counter = -(self.screen[0]/self.map_w)
                self.y_counter = 0
                self.terrain_counter = -1
                self.restart = True
            if not self.restart:
                if self.terrain[self.terrain_counter] == "wood_floor":
                    self.background_imagery.blit(self.t.wood_floor, (self.x_counter, self.y_counter))
                elif self.terrain[self.terrain_counter] == "marble_floor":
                    self.background_imagery.blit(self.t.marble_floor, (self.x_counter, self.y_counter))
                elif self.terrain[self.terrain_counter] == "stone_floor":
                    self.background_imagery.blit(self.t.stone_floor, (self.x_counter, self.y_counter))
                objects.handler_input = ((self.x_counter, self.y_counter), self.terrain_counter)
                obj_tmp_renderer = objects.handler_output
                self.i +=1
                if self.i < objects.map_w * objects.map_h:
                    objects.handler_input_all.append((self.x_counter, self.y_counter))
                """if "wire" in obj_tmp_renderer:
                    if "electric" in obj_tmp_renderer:
                        i = objects.get_wire_direction((objects.handler_output_position[0], objects.handler_output_position[1]))
                        if i == "ns":
                            self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_ns, (objects.handler_output_position[0], objects.handler_output_position[1]))
                        elif i == "ew":
                            self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_ew, (objects.handler_output_position[0], objects.handler_output_position[1]))
                        elif i == "es":
                            self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_es, (objects.handler_output_position[0], objects.handler_output_position[1]))
                        elif i == "ne":
                            self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_ne, (objects.handler_output_position[0], objects.handler_output_position[1]))
                        elif i == "nw":
                            self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_nw, (objects.handler_output_position[0], objects.handler_output_position[1]))
                        elif i == "sw":
                            self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_sw, (objects.handler_output_position[0], objects.handler_output_position[1]))
                elif "door" in obj_tmp_renderer:
                    if "wood" in obj_tmp_renderer:
                        if "ns" in obj_tmp_renderer:
                            self.background_imagery.blit(self.obj_render_images.wood_door_base_ns, (objects.handler_output_position[0], objects.handler_output_position[1]))
                            if not (objects.handler_output_position[0], objects.handler_output_position[1]) in objects.open_doors:
                                self.background_imagery.blit(self.obj_render_images.wood_door_ns, (objects.handler_output_position[0], objects.handler_output_position[1]))
                        elif "ew" in obj_tmp_renderer:
                            self.background_imagery.blit(self.obj_render_images.wood_door_base_ew, (objects.handler_output_position[0], objects.handler_output_position[1]))
                            if not (objects.handler_output_position[0], objects.handler_output_position[1]) in objects.open_doors:
                                self.background_imagery.blit(self.obj_render_images.wood_door_ew, (objects.handler_output_position[0], objects.handler_output_position[1]))
                elif "wall" in obj_tmp_renderer:
                    if "wood" in obj_tmp_renderer:
                        self.background_imagery.blit(self.obj_render_images.wood_wall, (objects.handler_output_position[0], objects.handler_output_position[1]))
                    elif "marble" in obj_tmp_renderer:
                        self.background_imagery.blit(self.obj_render_:images.marble_wall, (objects.handler_output_position[0], objects.handler_output_position[1]))
                elif "power_station" in obj_tmp_renderer:
                    self.background_imagery.blit(self.obj_render_images.power_station, (objects.handler_output_position[0], objects.handler_output_position[1]))
                elif "nails" in obj_tmp_renderer:
                    self.background_imagery.blit(self.obj_render_images.nails, (objects.handler_output_position[0], objects.handler_output_position[1]))
                elif "meatuara_ns" in obj_tmp_renderer:
                    tmp = obj_tmp_renderer.split(" ")
                    self.moving_objects.blit(self.obj_render_images.meatuara_ns, (objects.handler_output_position[0], objects.handler_output_position[1] + int(tmp[3])))
        """
        self.background_imagery.blit(object_surface, (0,0))
        return self.background_imagery

firstTimeObjectBlit = True

def prepare_object_blit(id, block):
    global firstTimeObjectBlit, object_surface_done
    if firstTimeObjectBlit:
        global obj_render_images
        obj_render_images = Objects()
        firstTimeObjectBlit = False
    else:
        if "wire" in id:
            if "electric" in id:
                i = objects.get_wire_direction(block)
                if "refill" in id:
                    object_surface.blit(obj_render_images.wire_electric_insulated_refill, block)
                elif i == "ns":
                    object_surface.blit(obj_render_images.wire_electric_insulated_ns, block)
                elif i == "ew":
                    object_surface.blit(obj_render_images.wire_electric_insulated_ew, block)
                elif i == "es":
                    object_surface.blit(obj_render_images.wire_electric_insulated_es, block)
                elif i == "ne":
                    object_surface.blit(obj_render_images.wire_electric_insulated_ne, block)
                elif i == "nw":
                    object_surface.blit(obj_render_images.wire_electric_insulated_nw, block)
                elif i == "sw":
                    object_surface.blit(obj_render_images.wire_electric_insulated_sw, block)
                elif "refill" in id:
                    object_surface.blit(obj_render_images.wire_electric_insulated_refill, block)
        elif "door" in id:
            if "wood" in id:
                if "ns" in id:
                    object_surface.blit(obj_render_images.wood_door_base_ns, block)
                    if not block in objects.open_doors:
                        object_surface.blit(obj_render_images.wood_door_ns, block)
                elif "ew" in id:
                    object_surface.blit(obj_render_images.wood_door_base_ew, block)
                    if not block in objects.open_doors:
                        object_surface.blit(obj_render_images.wood_door_ew, block)
        elif "wall" in id:
            if "wood" in id:
                object_surface.blit(obj_render_images.wood_wall, block)
            elif "marble" in id:
                object_surface.blit(obj_render_images.marble_wall, block)
            elif "stone" in id:
                object_surface.blit(obj_render_images.stone_wall, block)
        elif "power_station" in id:
            object_surface.blit(obj_render_images.power_station, block)
        elif "nails" in id:
            object_surface.blit(obj_render_images.nails, block)
        elif "meatuara_ns" in id:
            tmp = id.split(" ")
            object_surface.blit(obj_render_images.meatuara_ns, (block[0] + int(tmp[2]), block[1] + int(tmp[3])))
        if "box" in id: # The box block can be occupied by more than one object, so it get an if rather than a elif.
            if "wood" in id:
                tmp = id.split(" ")
                object_surface.blit(obj_render_images.wood_box, (block[0] + int(tmp[1]), block[1] + int(tmp[2])))