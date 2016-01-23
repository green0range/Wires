import root
import Tkinter
import tkFileDialog
import os

def story():
    story_path = os.path.join("assets", "maps", "working_map", "1.wrm") # TODO: change back to story after testing
    root.import_pack("/home/william/Documents/Wires/repo/wires/assets/maps/story.zip")
    root.start(mf=story_path)#(s=(1000, 1000), full=True)
    w.destroy()

def fs():
    initdir = os.path.join("assets", "maps")
    file = tkFileDialog.askopenfilename(initialdir=initdir, filetypes=[('Wires Map', '.wrm'), ('Wires Map Pack (Zipped)', '.zip')])
    root.start(mf=file)
    w.destroy()

w = Tkinter.Tk()
btn_story = Tkinter.Button(w, text="Story Mode", command=story).pack()
btn_online = Tkinter.Button(w, text="Find Map(s) (packs) online").pack()
btn_fs = Tkinter.Button(w, text="Open from file system", command=fs).pack()
w.mainloop()