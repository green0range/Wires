#! /usr/bin/python2

# lib imports
from pygame import *
from threading import Thread
import os
import shutil
# other py's import
import graphics
import objects
from time import sleep

init()

fullscreen = False
render_update_rate = 10
stop = False
screen = (1200, 750) # TODO: make launcher /w screen size parameter

class GameWindow:
    global screen, stop
    step = 0
    def __init__(self, mf=""):
        global step
        global screen
        step = 0
        if fullscreen:
            d = display.Info()  # dynamic scren sizing
            screen = (d.current_w, d.current_h)
            self.root = display.set_mode(screen, FULLSCREEN)
        else:
            self.root = display.set_mode(screen, 0, 32)
        self.ma = graphics.MapImports(screen)
        self.ma.import_map(m=mf)
        self.object_images = graphics.Objects()
        self.player = objects.Player()
        self.player_images = graphics.PlayerImg()
        self.clock = time.Clock()
        self.h = objects.Handler()
    def select_object_images(self, obj_id):
        if obj_id == "wood_door_w":
            return self.object_images.wood_door_w
        if obj_id == "wood_door_n":
            return self.object_images.wood_door_n
        if obj_id == "wood_door_e":
            return self.object_images.wood_door_e
        if obj_id == "wood_door_s":
            return self.object_images.wood_door_s
        if obj_id == "wood_wall":
            return self.object_images.wood_wall
    def select_player_images(self, obj_id):
        if obj_id == "north":
            return self.player_images.north
        if obj_id == "east":
            return self.player_images.east
        if obj_id == "south":
            return self.player_images.south
        if obj_id == "west":
            return self.player_images.west

    def mainloop(self):
        global stop
        # Quit events
        for e in event.get():
            if e.type == QUIT:
                quit()
                stop = True
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    quit()
                    stop = True
        self.player.move(key.get_pressed())
        if objects.player_request != "":
            if "location_update" in objects.player_request:
                i = objects.player_request.split(" ")
                self.player.x = int(i[1])
                self.player.y = int(i[2])
                objects.player_request = ""

    def backgroundrenderloop(self):
        global step
        # Map rendering
        self.root.blit(self.ma.render(), (0,0))

        #graphics.object_surface

        player_img_dat = self.player.render()
        img = self.select_player_images((player_img_dat[0]))
        self.root.blit(img, player_img_dat[1])
        display.flip()

    def objectsloop(self):
        if len(objects.handler_input_all) == objects.map_w * objects.map_h -1:
            self.h.main_loop()

level_count = 0
level_order = []
level_current = 0
level_gotonext = False

def next_level():
    global stop, level_current, level_order, level_gotonext
    level_current += 1
    if level_current > level_count:
        print "level complete. No next level. Quiting..."
        print level_current
        print level_order
        stop = True
    else:
        stop = True
        level_gotonext = True

def import_pack(path):
    global level_count, level_order
    import zipfile
    zf = zipfile.ZipFile(path, "r")
    zf.extractall(os.path.join("assets", "maps", "working_map"))
    zf.close()
    f = open(os.path.join("assets", "maps", "working_map", "wiresconfig"), "r")
    config_raw = f.read()
    f.close()
    config = config_raw.split("\n")
    for i in range(0, len(config)):
        if config[i] == '!LEVELNUMBER:':
            level_count = int(config[i+1])
        elif config[i] == "!ORDER:":
            print "dfgdfg"
            for j in range(i+1, i+1+level_count):
                level_order.append(config[j])
                print level_order

# handles player, movement, keypresses, etc.
game_timer = time.Clock()
class GameThread(Thread):
    global gw, game_timer, stop
    def __init__(self):
        print "start main thread"
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global gw, game_timer
        while True:
            gw.mainloop()

object_timer = time.Clock()

class ObjectsThread(Thread):
    global object_timer, stop
    def __init__(self):
        print "start object thread"
        objects.first_time = True
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global object_timer
        while not stop:
            gw.objectsloop()
            object_timer.tick(100)

# Renders everything
class RenderThread(Thread):
    global gw, stop
    def __init__(self):
        print "start render thread"
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global gw
        while not stop:
            gw.backgroundrenderloop()

class Scripts(Thread):
    global stop
    def __init__(self, path):
        self.path = path
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        first = True
        while not stop:
            if first:
                if graphics.script !="":
                    i = self.path.split("\\")
                    e = self.path.split("/")
                    if len(e) > len(i):
                        e.pop()
                        shutil.copyfile(os.path.join("/".join(e), graphics.script), "map_script.py")
                        import map_script
                        map_script.rootdir = "/".join(e)
                    else:
                        i.pop() # TODO: TEST ON WINDOWS
                        os.rename(os.path.join("".join(i), graphics.script), "map_script.py")
                        import map_script
                        map_script.rootdir = "".join(i)
                    map_script.init()
                    first = False



def start(s=screen, full=False, mf=""):
    global gw, screen, fullscreen, stop, level_gotonext, level_order, level_current
    screen = s
    fullscreen = full
    gw = GameWindow(mf=mf)
    GameThread()
    ObjectsThread()
    RenderThread()
    Scripts(mf)
    close = False
    i=0
    while not close:
        if stop:
            i +=1
            if i > 100: # Delays the shut down of gw, letting rendering threads shutdown properly without crashing.
                if level_gotonext:
                    graphics.script = ""
                    gw.ma.import_map(m=os.path.join("assets", "maps", "working_map", level_order[level_current]))
                    level_gotonext = False
                    stop = False
                    objects.solid = []
                    ObjectsThread()
                    RenderThread()
                    objects.update_player_location((1,1))
                    Scripts(os.path.join("assets", "maps", "working_map", level_order[level_current]))
                else:
                    close = True