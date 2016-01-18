import root
import Tkinter
import tkFileDialog
import os

def story():
    root.start()#(s=(1000, 1000), full=True)
    w.destroy()

def fs():
    initdir = os.path.join("assets", "maps")
    file = tkFileDialog.askopenfilename(initialdir=initdir, filetypes=[('Wires Map', '.wrm'), ('Wires Map Pack (Zipped)', '.zip')])
    root.start(mf=file)

w = Tkinter.Tk()
btn_story = Tkinter.Button(w, text="Story Mode", command=story).pack()
btn_online = Tkinter.Button(w, text="Find Map(s) (packs) online").pack()
btn_fs = Tkinter.Button(w, text="Open from file system", command=fs).pack()
w.mainloop()