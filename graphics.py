from pygame import *
from os import path
import objects

tile_w = 0
tile_h = 0
screen_size = (800, 600)

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
            path.join("assets", "terrain", "wood_floor.jpg")
        ]
        export_list = []
        for i in range (0, len(import_list)):
            tmp = image.load(import_list[i]).convert()
            export_list.append(transform.scale(tmp, (tile_w, tile_h)))
        tmp = 0
        # Convert to easier naming system
        self.wood_floor = export_list[0]
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
            path.join("assets", "objects", "wood_door_w.png"),
            path.join("assets", "objects", "wood_door_n.png"),
            path.join("assets", "objects", "wood_door_e.png"),
            path.join("assets", "objects", "wood_door_s.png"),
            path.join("assets", "objects", "wood_wall.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_es.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_ew.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_ne.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_ns.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_nw.png"),
            path.join("assets", "objects", "wires", "wire_electrical_insulated_sw.png")
        ]
        export_list = []
        for i in range (0, len(import_list)):
            tmp = image.load(import_list[i]).convert_alpha()
            export_list.append(transform.scale(tmp, (tile_w, tile_h)))
        tmp = 0
        # Convert to easier naming system
        self.wood_door_w = export_list[0]
        self.wood_door_n = export_list[1]
        self.wood_door_e = export_list[2]
        self.wood_door_s = export_list[3]
        self.wood_wall = export_list[4]
        self.wire_electric_insulated_es = export_list[5]
        self.wire_electric_insulated_ew = export_list[6]
        self.wire_electric_insulated_ne = export_list[7]
        self.wire_electric_insulated_ns = export_list[8]
        self.wire_electric_insulated_nw = export_list[9]
        self.wire_electric_insulated_sw = export_list[10]
        # Clear export list to save space
        export_list = 0

class PlayerImg:
    def __init__(self):
        self.north = image.load(path.join("assets", "objects", "player", "north.png")).convert_alpha()
        self.east = image.load(path.join("assets", "objects", "player", "east.png")).convert_alpha()
        self.south = image.load(path.join("assets", "objects", "player", "south.png")).convert_alpha()
        self.west = image.load(path.join("assets", "objects", "player", "west.png")).convert_alpha()

# This class imports map files, separates data, and then perpares for rendering. The import_map
# function must be called once first, and then for every new map. The render function runs off'
# data prepared in the import_map function, and should be looped after the import is called.
# It does not full render the images but sorts out all their coordinates, which are then returned
# to the caller with the terrain image for full rendering. This can be done by bliting the return
# value. Objects are passed to the object handle after being read from the map file. Meta data
# about the map, such as title, author and description can also be gained with the get_info function.
class MapImports:
    def __init__(self, screen):
        self.screen = screen
        self.background_imagery = Surface(screen)
    def import_map(self, m=(path.join("assets", "maps", "testmap.wrm")), want_meta=False):
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
        # Extracts data from beyond start point marker
        try:
            self.map_h = int(f_raw[height_point + 1])
            self.map_w = int(f_raw[width_point + 1])
            area = self.map_h * self.map_w
            self.terrain = []
            for i in range(0, area):
                self.terrain.append(f_raw[terrain_point+1+i])
            self.objects = []
            for i in range(0, area):
                self.objects.append(f_raw[object_point+1+i])
            self.object_handler = objects.Handler(self.objects)  # Creates object handler here
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
        self.obj_render_images = Objects()

    def render(self):
        # Terrain rendering starts at top left tile then left -> right -> Next line repeat. Until all is rendered.
        # This relies on being constantly repeated in another function. It forwards all object render data from
        # the object controller. Yeah, it's pass the parcel in here.
        restart = False
        while not restart:
            self.terrain_counter += 1
            self.x_counter += (self.screen[0]/self.map_w)
            if self.x_counter >= self.screen[0]-3:
                self.x_counter = 0
                self.y_counter += (self.screen[1]/self.map_h)
            if self.y_counter >= self.screen[1]-3:
                self.x_counter = -(self.screen[0]/self.map_w)
                self.y_counter = 0
                self.terrain_counter = -1
                restart = True
            if not restart:
                self.object_render_control = self.object_handler.main_loop(block=(self.x_counter, self.y_counter), counter=self.terrain_counter)
                if self.terrain[self.terrain_counter] == "wood_floor":
                    self.background_imagery.blit(self.t.wood_floor, (self.x_counter, self.y_counter))

                obj_tmp_renderer = self.object_handler.main_loop(block=(self.x_counter, self.y_counter), counter=self.terrain_counter)
                if "door" in obj_tmp_renderer:
                    if "wood" in obj_tmp_renderer:
                        if "_n" in obj_tmp_renderer:
                            self.background_imagery.blit(self.obj_render_images.wood_door_n, (self.x_counter, self.y_counter))
                        if "_e" in obj_tmp_renderer:
                            self.background_imagery.blit(self.obj_render_images.wood_door_e, (self.x_counter, self.y_counter))
                        if "_s" in obj_tmp_renderer:
                            self.background_imagery.blit(self.obj_render_images.wood_door_s, (self.x_counter, self.y_counter))
                        if "_w" in obj_tmp_renderer:
                            self.background_imagery.blit(self.obj_render_images.wood_door_w, (self.x_counter, self.y_counter))
                if "wall" in obj_tmp_renderer:
                    self.background_imagery.blit(self.obj_render_images.wood_wall, (self.x_counter, self.y_counter))
                if "wire" in obj_tmp_renderer:
                    i = objects.get_wire_direction((self.x_counter, self.y_counter))
                    if i == "ns":
                        self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_ns, (self.x_counter, self.y_counter))
                    elif i == "ew":
                        self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_ew, (self.x_counter, self.y_counter))
                    elif i == "es":
                        self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_es, (self.x_counter, self.y_counter))
                    elif i == "ne":
                        self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_ne, (self.x_counter, self.y_counter))
                    elif i == "nw":
                        self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_nw, (self.x_counter, self.y_counter))
                    elif i == "sw":
                        self.background_imagery.blit(self.obj_render_images.wire_electric_insulated_sw, (self.x_counter, self.y_counter))
        return self.background_imagery




                # self.object_render_control