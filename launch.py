import root
import Tkinter
import tkFileDialog
import os
import webbrowser

Screen = (500,500)
Full = True

# Open storyline maps
def story():
    story_path = os.path.join("assets", "maps", "working_map", "1.wrm") # TODO: change back to story after testing
    root.import_pack("/home/william/Documents/Wires/repo/wires/assets/maps/story.zip")
    root.start(mf=story_path)#, s=Screen, full=Full)
    w.destroy()

# Open mapo from file system
def fs():
    initdir = os.path.join("assets", "maps")
    file = tkFileDialog.askopenfilename(initialdir=initdir, filetypes=[('Wires Map', '.wrm'), ('Wires Map Pack (Zipped)', '.zip')])
    root.start(mf=file)#, s=Screen, full=Full)
    w.destroy()

def github():
    print "Going to https://github.com/green0range/Wires/"
    webbrowser.open_new("https://github.com/green0range/Wires/")

def show_license():
    f = open(os.path.join("assets", "license.txt"), "r")
    txt = f.read()
    f.close()
    lw = Tkinter.Tk()
    scroll = Tkinter.Scrollbar(lw)
    scroll.pack(side="right", fill="y")
    can_license = Tkinter.Canvas(lw, yscrollcommand=scroll.set, width=715)
    can_license.create_text((0,0), text=txt, width=710, anchor="nw")
    can_license.pack(side="left", fill="both")
    scroll.config(command=can_license.yview)
    # , text=txt, yscrollcommand=scroll.set).grid(row=0, column=0)
    Tkinter.mainloop()

w = Tkinter.Tk()

#Import images
logo = Tkinter.PhotoImage(file=os.path.join("assets", "Marketing", "Logo png.png"))

# Create widgets
lbl_logo = Tkinter.Label(w, image=logo).grid(row=0, columnspan=3)
# 1st column
btn_story = Tkinter.Button(w, text="Story Mode", command=story).grid(row=1, column=0, sticky='w', pady=2)
btn_online = Tkinter.Button(w, text="Online Maps").grid(row=2, column=0, sticky='w', pady=2)
btn_fs = Tkinter.Button(w, text="Open FS Map", command=fs).grid(row=3, column=0, sticky='w', pady=2)
#2nd column
lbl_credits = Tkinter.Label(w, text="                       Credits:").grid(row=1, column=1, sticky='w', pady=2)
lbl_dev = Tkinter.Label(w, text="Development: William Satterthwaite").grid(row=2, column=1, sticky='w', pady=2)
lbl_soft = Tkinter.Label(w, text="Software: Python, pygame, Tkinter").grid(row=3, column=1, sticky='w', pady=2)
# 3rd Column
btn_web = Tkinter.Button(w, text="Website").grid(row=1, column=2, sticky='e', pady=2)
btn_github = Tkinter.Button(w, text="Github", command=github).grid(row=2, column=2, sticky='e', pady=2)
btn_license = Tkinter.Button(w, text="License", command=show_license).grid(row=3, column=2, sticky='e', pady=2)

w.mainloop()