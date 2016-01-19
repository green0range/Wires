#! /usr/bin/python2

# lib imports
from pygame import *
from threading import Thread
import os
import shutil
# other py's import
import graphics
import objects

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
        if mf != "":
            self.ma.import_map(m=mf)
        else: self.ma.import_map(m=mf)
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
        while True:
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

    def backgroundrenderloop(self):
        global step
        while True:
            # Map rendering
            self.root.blit(self.ma.render(), (0,0))

            #graphics.object_surface

            player_img_dat = self.player.render()
            img = self.select_player_images((player_img_dat[0]))
            self.root.blit(img, player_img_dat[1])
            display.flip()
            '''# Display updates
            if step > 1000:
                step = 0
            else: # quality/ frame rate/ lag control
                rur = int(1000/render_update_rate)
                doupdate = False
                for i in range(0, 1000, rur): # updates on variable step percentage.
                    if i == step:
                        doupdate = True
                        break
                    else:
                        doupdate = False
                if doupdate:
                    display.flip()'''

    def objectsloop(self):
        if len(objects.handler_input_all) == objects.map_w * objects.map_h -1:
            self.h.main_loop()

# handles player, movement, keypresses, etc.
game_timer = time.Clock()
class GameThread(Thread):
    global gw, game_timer
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global gw, game_timer
        while True:
            gw.mainloop()
            game_timer.tick(50)

object_timer = time.Clock()

class ObjectsThread(Thread):
    global object_timer
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global object_timer
        while True:
            gw.objectsloop()
            object_timer.tick(100)

# Renders everything
class RenderThread(Thread):
    global gw
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global gw
        while True:
            gw.backgroundrenderloop()

class Scripts(Thread):
    def __init__(self, path):
        self.path = path
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        first = True
        while True:
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
    global gw, screen, fullscreen
    screen = s
    fullscreen = full
    gw = GameWindow(mf=mf)
    GameThread()
    ObjectsThread()
    RenderThread()
    Scripts(mf)
    while not stop:
        pass