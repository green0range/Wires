# This file is not part of or needed by the game. However, it is used to create maps for the game, both in development,
# and (hopefully) community maps.

# It only handles basic tile placement. Custom objects/ scripts can be added latter, but this will take care of
# the boring things.

# Map packs do not have a tool, but contain a bundle of maps, with a config telling the game how there are to be put
# together, there will be documentation explaining this.

from Tkinter import *
from os import path
import time
import tkFileDialog

metadata = "Warning, WIRES map file. Modification may cause in game errors. Created with provided mapmaker tool.\n!META:\n"
size = (0,0)
placements = []

class New:
    global metadata,size
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("New Map")
        # Labels
        self.lbl_title = Label(self.root, text="Title:").grid(row=0, column=0, sticky="w")
        self.lbl_descript = Label(self.root, text="Description:").grid(row=1, column=0, sticky="w")
        self.lbl_author = Label(self.root, text="Author:").grid(row=3, column=0,sticky="w")
        self.lbl_width = Label(self.root, text="Width (tiles)").grid(row=4, column=0,sticky="w")
        self.lbl_height = Label(self.root, text="Height (tiles)").grid(row=5, column=0,sticky="w")
        # Text/ entries
        self.ent_title = Entry(self.root)
        self.ent_title.grid(row=0, column=1)
        self.txt_descript = Text(self.root, width=40, height=4)
        self.txt_descript.grid(row=2, column=0, columnspan=2)
        self.ent_author = Entry(self.root)
        self.ent_author.grid(row=3, column=1)
        self.ent_width = Entry(self.root)
        self.ent_width.grid(row=4, column=1)
        self.ent_height = Entry(self.root)
        self.ent_height.grid(row=5, column=1)
        # Buttons
        self.btn_cancel = Button(self.root, text="Cancel", command=self.root.destroy).grid(row=6, column=0, sticky="w")
        self.btn_create = Button(self.root, text="Create", command=self.create).grid(row=6, column=1, sticky="e")
        mainloop()

    def create(self):
        # Prepare metadata. Always end in \n
        global metadata, size
        descript = self.txt_descript.get(0.0, END)
        descript_list = descript.split("\n")
        descript_line_count = len(descript_list)
        metadata += "!TITLE:\n" + self.ent_title.get() + "\n"
        metadata += "!DESCRuntimeError: Too early to create imageRIPTION:\n" + descript + "\n"
        metadata += "!DESCRIPTIONLENGTH:\n" + str(descript_line_count) + "\n"
        metadata += "!AUTHOR:\n" + self.ent_author.get() + "\n"
        metadata += "!DATESTAMP:\n" + str(time.time()) + "\n" # Unix time
        try:
            size = (int(self.ent_width.get()), int(self.ent_height.get()))
            self.root.destroy()
            m = Mapmaker()
        except ValueError:
            print "Error, invalid size. Exiting..."
            self.root.destroy()
'''
class Image_import:
    def __init__(self):
        self.import_list = [
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
            path.join("assets", "objects", "meatuara_ns.png")
        ]
        export_list = []
        for i in range (0, len(self.import_list)):
            export_list.append(Image.open(self.import_list[i]))
            #export_list.append(ImageTk.PhotoImage(tmp))
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
        '''

class Mapmaker:
    global size, placements, metadata
    def __init__(self):
        global size
        self.tilesize = 20
        self.root = Tk()
        self.can_map = Canvas(self.root, width=(self.tilesize*size[0]), height=(self.tilesize*size[1]))
        self.can_map.bind("<Button-1>", self.place)
        self.can_map.pack()
        self.selected = "wood_floor_(default)"
        for i in range(0, size[0]):
            self.can_map.create_line(i*self.tilesize, 0, i*self.tilesize, self.tilesize*size[1]+size[1])
        for i in range(0, size[1]):
            self.can_map.create_line(0, i*self.tilesize, self.tilesize*size[0]+size[0], i*self.tilesize)
        #items
        self.btn_marble_floor = Button(self.root, text="Marble floor", command=lambda item="marble_floor":self.select(item))
        self.btn_marble_floor.pack()
        self.btn_stone_floor = Button(self.root, text="Stone floor", command=lambda item="stone_floor":self.select(item))
        self.btn_stone_floor.pack()
        self.btn_wood_floor = Button(self.root, text="Wood floor", command=lambda item="wood_floor":self.select(item))
        self.btn_wood_floor.pack()
        self.btn_marble_wall = Button(self.root, text="Marble Wall", command=lambda item="marble_wall":self.select(item))
        self.btn_marble_wall.pack()
        self.btn_nails = Button(self.root, text="Nails", command=lambda item="nails":self.select(item))
        self.btn_nails.pack()
        self.btn_wood_wall = Button(self.root, text="Wood Wall", command=lambda item="wood_wall":self.select(item))
        self.btn_wood_wall.pack()
        self.btn_stone_wall = Button(self.root, text="Stone Wall", command=lambda item="stone_wall":self.select(item))
        self.btn_stone_wall.pack()
        self.btn_save = Button(self.root, text="Save", command=self.save)
        self.btn_save.pack()

        mainloop()

    def select(self, item):
        print "Selected:", item
        self.selected = item

    def place(self, event):
        global placements
        coordinates = (int(event.x/self.tilesize), int(event.y/self.tilesize))
        print "Placed", self.selected, "@", str(coordinates)
        placement = (self.selected, coordinates)
        coordinates = (coordinates[0], coordinates[1]+1) # Bug fix
        placements.append(placement)
        if "floor" in self.selected:
            self.can_map.create_rectangle(coordinates[0]*self.tilesize, coordinates[1]*self.tilesize, coordinates[0]*self.tilesize + self.tilesize,coordinates[1]*self.tilesize - self.tilesize,fill="grey")
        else:
            self.can_map.create_rectangle(coordinates[0]*self.tilesize, coordinates[1]*self.tilesize, coordinates[0]*self.tilesize + self.tilesize,coordinates[1]*self.tilesize - self.tilesize,fill="black")

    def save(self):
        global placements, size, metadata
        # Order terrain/object lists.
        terrian_ordered = []
        objects_ordered = []
        for i in range(0, size[0]*size[1]):
            terrian_ordered.append("wood_floor_(default)")
            objects_ordered.append("none")
        for i in range(0, len(placements)):
            x_order = placements[i][1][0]
            y_order = placements[i][1][1]
            order = y_order * size[0] + x_order
            if "floor" in placements[i][0]:
                terrian_ordered[order] = placements[i][0]
            else:
                objects_ordered[order] = placements[i][0]
        # format data into a string
        mapdata = "!MAPDATA:\n!HEIGHT:\n"
        mapdata += str(size[1]) + "\n!WIDTH:\n"
        mapdata += str(size[0]) + "\n!TERRAIN:\n"
        for i in range(0, len(terrian_ordered)):
            mapdata += terrian_ordered[i] + "\n"
        mapdata += "!OBJECT:\n"
        for i in range(0, len(terrian_ordered)):
            mapdata += objects_ordered[i] + "\n"
        data = metadata + mapdata
        # Write data to file
        f = open(tkFileDialog.asksaveasfilename(filetypes=[('Wires Map', '.wrm')]), "w")
        f.write(data)
        f.close()
        self.root.destroy()

w = New()

