from Tkinter import *
import datacontainer
import tkFileDialog, tkSimpleDialog, tkMessageBox
from tksimplestatusbar import StatusBar

import os

def open_file_chooser(naming, ftype="*", basepath = None):
    if not basepath:
        basepath = '.'

    somefile = tkFileDialog.askopenfilename(filetypes=[(naming, ftype)],
            initialdir=basepath,
            multiple=False)
    return somefile or u''

def open_dir_chooser(naming,ftype="*"):
	try:
		somedir = tkFileDialog.askdirectory(title=naming,mustexist=True)
		return somedir
	except:
		return None

def popup_message(title,text):
    return tkMessageBox.showinfo(title,text)

def show_disclaimer():
    """
        Show a disclaimer saying that this software is shit
    """
    popup_message("BorinotGames Note","This program is provided AS IS :-P\n\
It is just a helper utility, don't expect to be beautiful or bug free in Exotic cases")


class AppUI(Frame):

    def __init__(self, master=None):

        self.DC = datacontainer.datacontainer()
        Frame.__init__(self, master, relief=SUNKEN, bd=2)

        self.menubar = Menu(self)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="New Level",     command=self.f_new_level)
        menu.add_command(label="Open Level",    command=self.f_open_level)
        menu.add_command(label="Save Level",    command=self.f_save_level)
        menu.add_command(label="Save Level As", command=self.f_save_level_as)
        menu.add_command(label="Exit",          command=self.f_exit)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=menu)
        menu.add_command(label="As Game")
        menu.add_command(label="Collisions")

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Level", menu=menu)
        menu.add_command(label="Cut")
        menu.add_command(label="Copy")
        menu.add_command(label="Paste")

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Objects", menu=menu)
        menu.add_command(label="Start")
        menu.add_command(label="Finish")
        menu.add_command(label="Bouncer")
        menu.add_command(label="Lifeup")
        menu.add_command(label="Basher")

        # Status bar with the x y information
        self.statusbar = StatusBar(self.master)
        self.statusbar.pack(side=BOTTOM, fill=X)

        while self.DC.base_pykurin_directory == None:
            bdir = open_dir_chooser("Choose Pykurin Base Directory")
            self.DC.set_base_dir(bdir)

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(master, "config", "-menu", self.menubar)

        self.canvas = Canvas(self, bg="gray", width=800, height=600,
                     bd=0, highlightthickness=0)
        self.canvas.pack()

        #Bind Mouseover on Canvas
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.canvas.bind("<B2-Motion>", self.pan_motion)
        self.canvas.bind("<Button-2>", self.pan_start)

        self.canvas.bind("<Button-1>", self.canvas_left_click)
        self.canvas.bind("<B1-Motion>", self.canvas_left_click_motion)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_left_click_release)

        #PAN
        self.panx  = 0
        self.pany  = 0
        self.ppx   = None
        self.ppy   = None

        #Selected item
        self.sitem = None

        #ID dictionary between GUI and datacontainer
        self.dataids = {}

    #
    # Panning
    #
    def mouse_motion(self, event):
        self.statusbar.set("%s : %s" % (event.x - self.panx, event.y - self.pany))

    def pan_start(self, event):
        self.ppx = event.x
        self.ppy = event.y

    def pan_motion(self, event):
        canvas = self.canvas
        px = self.ppx - event.x
        py = self.ppy - event.y

        self.panx -= px
        self.pany -= py

        #Pan the objects tagged as PAN.
        for item in canvas.find_withtag("pan"):
            canvas.move(item, -px, -py)

        self.pan_start(event)


    #
    # Item selection
    #
    def canvas_left_click(self, event):
        x = event.x
        y = event.y
        c = self.canvas
        items = self.canvas.find_overlapping(x-2,y-2,x+2,y+2)

        #Just interested in the movable items
        pitems = []
        for i in items:
            if "select" in c.gettags(i):
                pitems.append(i)

        self.sitem = pitems[0]

    def canvas_left_click_motion(self, event):
        print event

    def canvas_left_click_release(self, event):
        print event

    #
    # LEVEL LOADING AND SAVING
    #
    def f_new_level(self):
        print "NEW LEVEL"
        pass

    def f_open_level(self):
        """
            Opens a file chooser to load a properties image
        """
        filepath = open_file_chooser("Properties",
                                    ".prop",
                                    self.DC.get_basepath());
        if os.path.isfile(filepath):
            #clear_paddings()
            self.DC.load_from_file(filepath)

        self._create_canvas_with_DC()

    def f_save_level(self):
        pass

    def f_save_level_as(self):
        pass

    def f_exit(self):
        self.master.destroy()

    def _create_canvas_with_DC(self):
        """
            Create a canvas from the DC.
        """
        canvas = self.canvas
        canvas.delete(ALL)
        self.panx = self.pany = 0

        canvas.create_image((0,0),
                                image=self.DC.get_bgimage(), anchor=NW)
        canvas.create_image((0,0),
                            image=self.DC.get_image(), anchor=NW,
                            tags = ("pan"))

        #Filled with pygame RECTS
        for r in self.DC.bouncers:
            canvas.create_image((r.x, r.y),
                                image=self.DC.get_bouncer_image(), anchor=NW,
                                tags=("select", "move", "bouncer", "delete", "pan"))

        for r in self.DC.lives:
            canvas.create_image((r.x, r.y),
                                image=self.DC.get_live_image(), anchor=NW,
                                tags=("select", "move", "delete", "lives", "pan"))

        for r in self.DC.goals:
            canvas.create_image((r.x, r.y),
                                image=self.DC.get_goal_image(), anchor=NW,
                                tags=("select", "move", "goal", "pan"))

        for r in self.DC.sticks:
            canvas.create_image((r.x, r.y),
                                image=self.DC.get_stick_image(), anchor=NW,
                                tags=("select", "move", "stick", "pan")
                                )

        for i,r in enumerate(self.DC.bashers):
            r1 = r
            r2 = self.DC.bashers_end[i]

            arrow_startx = r1.x + r1.w/2
            arrow_starty = r1.y + r1.h/2
            arrow_endx   = r2.x
            arrow_endy   = r2.y
            canvas.create_line(arrow_startx,
                               arrow_starty,
                               arrow_endx,
                               arrow_endy,
                               tags = ("pan")
                               )

            canvas.create_rectangle(arrow_endx-5, arrow_endy-5,
                                    arrow_endx+5, arrow_endy+5,
                                    tags=("select", "move", "delete", "basher",
                                          "pan"))
            canvas.create_image((r1.x, r1.y),
                                image=self.DC.get_basher_image(), anchor=NW,
                                tags=("select", "move", "pan"))

        # Draw the 0,0 cross
            canvas.create_line(10, 0, -10, 0, fill="red", tags=("pan"))
            canvas.create_line(0, 10, 0, -10, fill="red", tags=("pan"))

root = Tk()

app = AppUI(root)
app.pack()

#show_disclaimer()
root.mainloop()
