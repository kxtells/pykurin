from Tkinter import *
import datacontainer
import tkFileDialog, tkSimpleDialog, tkMessageBox
from tksimplestatusbar import StatusBar

import os

#
#
# Generic Dialog functions
#
#

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

def save_file_chooser(naming, ftype=".prop"):
	try:
		somefile = tkFileDialog.asksaveasfilename(filetypes=[(naming, ftype)])
		return somefile
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


#
#
# MAIN LEVEL EDITOR SCREEN
#
#
class PykurinLevelEditorUI(Frame):

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
        menu.add_command(label="Edit")

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Objects", menu=menu)
        menu.add_command(label="Start")
        menu.add_command(label="Finish")
        menu.add_command(label="Bouncer")
        menu.add_command(label="Lifeup")
        menu.add_command(label="Basher")

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Test", menu=menu)
        menu.add_command(label="Run Level", command=self.run_level)



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

        #Bind Center click to pan
        self.canvas.bind("<B2-Motion>", self.pan_motion)
        self.canvas.bind("<Button-2>", self.pan_start)

        #Bind clicking to select
        self.canvas.bind("<Button-1>", self.canvas_left_click)
        self.canvas.bind("<B1-Motion>", self.canvas_left_click_motion)
        self.canvas.bind("<ButtonRelease-1>", self.canvas_left_click_release)

        #Bind clicking to select
        self.canvas.bind("<Delete>", self.delete_item)

        #PAN
        self.panx  = 0
        self.pany  = 0
        self.ppx   = None
        self.ppy   = None

        #Selected item
        self.sitem = None

        #ID dictionary between GUI and datacontainer
        self.dataids = {}

    def get_item_type(self, itemid):
        return self.dataids[itemid][0]

    def isBasher(self, itemid):
        return self.get_item_type(itemid) == self.DC.BASHER

    def isBasherEnd(self, itemid):
        return self.get_item_type(itemid) == self.DC.BASHER_END


    #
    # Running a level
    #
    def run_level(self):
        """Run the current level by the specified pykurin base dir"""
        bdir = self.DC.get_base_dir()
        pykurinexe = os.path.join(bdir,"pykurin.py")
        fname = self.DC.get_current_level_filename()

        os.system("/usr/bin/python %s %s" % (pykurinexe, fname))

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
        #Once clicked, give keyboard focus to canvas (in case it wasn't set)
        self.canvas.focus_set()

        x = event.x
        y = event.y

        #Delete all selections
        for item in self.canvas.find_withtag("selection"):
            self.canvas.delete(item)

        #Create a new selection
        self.select_item(x,y)

    def select_item(self, x, y):
        """Selects an item, setting the sitem attribute"""
        c = self.canvas
        items = self.canvas.find_overlapping(x-2,y-2,x+2,y+2)

        #Just interested in the selectable items
        pitems = []

        for i in items:
            if "select" in c.gettags(i):
                pitems.append(i)

        self.sitem = None
        if pitems:
            self.sitem = pitems[0]

        print self.sitem, "Is now selected"

        if self.sitem:
            c.create_rectangle(c.bbox(self.sitem), tags=("pan","selection"),
                                                   outline="red", width=2)

    #
    # Item moving
    #
    def canvas_left_click_motion(self, event):
        """This motion is responsible mainly for the movement of the items"""
        if not self.sitem:
            return

        #If item selected Move that item
        self.canvas.coords(self.sitem, (event.x, event.y))

        #Move the selection
        for item in self.canvas.find_withtag("selection"):
            self.canvas.coords(item, self.canvas.bbox(self.sitem))

        #Basher needs a little bit more of work
        if self.isBasher(self.sitem) :
            self.update_basher_arrow(self.sitem)
        if self.isBasherEnd(self.sitem):
            basher_id = self.dataids[self.sitem][2]
            self.update_basher_arrow(basher_id)

    def canvas_left_click_release(self, event):
        print "lc release"

    def update_basher_arrow(self, basherid):
        basher_line   = self.dataids[basherid][3]
        basher_end    = self.dataids[basherid][2]
        basher_coords = self.canvas.bbox(basherid)
        end_coords    = self.canvas.bbox(basher_end)

        bwidth        = abs(basher_coords[0] - basher_coords[2])
        bheight       = abs(basher_coords[1] - basher_coords[3])

        ewidth        = abs(end_coords[0] - end_coords[2])
        eheight       = abs(end_coords[1] - end_coords[3])

        lbbox         = ( basher_coords[0] + bwidth  / 2,
                          basher_coords[1] + bheight / 2,
                          end_coords[0]    + ewidth  / 2,
                          end_coords[1]    + eheight / 2
                        )

        print lbbox
        self.canvas.coords(basher_line, lbbox)



#        arrow_startx = r1.x + r1.w/2
#        arrow_starty = r1.y + r1.h/2
#        arrow_endx   = r2.x + 5
#        arrow_endy   = r2.y + 5
#
#        idl = canvas.create_line(arrow_startx,
#                           arrow_starty,
#                           arrow_endx,
#                           arrow_endy,
#                           tags = ("pan")
#                           )
#
#
#        self.canvas.coords(basher_line, bcoords)

    #
    # Remove items
    #
    def delete_item(self, event):
        if not self.sitem:
            print "No item selected"
            return

        itype = self.dataids[self.sitem][0]
        if itype == self.DC.BASHER:
            dcid = self.dataids[self.sitem][1]

            # Canvas ids of the other basher parts
            rectid = self.dataids[self.sitem][2]
            lineid = self.dataids[self.sitem][3]

            #delete from canvas
            self.canvas.delete(self.sitem)
            self.canvas.delete(rectid)
            self.canvas.delete(lineid)

            self.DC.remove_item(itype, dcid)

        else:
            dcid = self.dataids[self.sitem][1]
            #Delete from the container
            self.DC.remove_item(itype, dcid)

            self.canvas.delete(self.sitem)

        self.__update_dataids_after_remove(itype, dcid)


    #
    # Handling references to data ids
    #
    def __update_dataids_after_remove(self, itype, dcid):
        """Update all the indexes after the removal of one
        of the objects.
            This is kind of ugly because the ids of datacontainer
            are just the indexes. So removing one object from there
            implies invalidating most of the indexes here.
        """
        for tkid,dcdata in self.dataids.items():
            dtype = dcdata[0]
            if dtype == itype:
                if dcdata[1] > dcid:
                    if itype == self.DC.BASHER:
                        self.dataids[tkid] = (itype, dcdata[1] - 1,
                                              dcdata[2], dcdata[3])
                    else:
                        self.dataids[tkid] = (itype, dcdata[1] - 1)

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

    def __f_save(self, fname):
        """Try to save the level to the specified filename"""
        if fname:
            ret, msg = self.DC.save_to_file(fname)
            if ret:
                popup_message("SUCCESS","%s saved" % fname)
            else:
	            tkMessageBox.showerror("ERROR","File %s NOT saved\n %s" % (fname, msg))
        else:
	        tkMessageBox.showerror("Invalid Filename %s" % fname)

    def f_save_level(self):
        fname = self.DC.get_current_level_filename()
        if not fname:
            self.f_save_level_as()
        else:
            self.__f_save(fname)

    def f_save_level_as(self):
        fname = save_file_chooser("Save As")
        self.__f_save(fname)

    def f_exit(self):
        self.master.destroy()

    def _create_canvas_with_DC(self):
        """
            Create a canvas from the DC.
        """
        canvas = self.canvas
        dc     = self.DC
        canvas.delete(ALL)
        self.panx = self.pany = 0

        canvas.create_image((0,0),
                                image=dc.get_bgimage(), anchor=NW)
        canvas.create_image((0,0),
                            image=dc.get_image(), anchor=NW,
                            tags = ("pan"))

        #Filled with pygame RECTS
        for idx,r in enumerate(dc.bouncers):
            id = canvas.create_image((r.x, r.y),
                                image=dc.get_bouncer_image(), anchor=NW,
                                tags=("select", "move", "bouncer", "delete", "pan"))

            self.dataids[id] = (dc.BOUNCER, idx)

        for idx,r in enumerate(dc.lives):
            id = canvas.create_image((r.x, r.y),
                                image=dc.get_live_image(), anchor=NW,
                                tags=("select", "move", "delete", "lives", "pan"))

            self.dataids[id] = (dc.LIVES, idx)

        for idx,r in enumerate(dc.goals):
            id = canvas.create_image((r.x, r.y),
                                image=dc.get_goal_image(), anchor=NW,
                                tags=("select", "move", "goal", "pan"))

            self.dataids[id] = (dc.GOALS, idx)

        for idx,r in enumerate(dc.sticks):
            id = canvas.create_image((r.x, r.y),
                                image=dc.get_stick_image(), anchor=NW,
                                tags=("select", "move", "stick", "pan")
                                )

            self.dataids[id] = (dc.GOALS, idx)

        for idx,r in enumerate(dc.bashers):
            r1 = r
            r2 = dc.bashers_end[idx]

            arrow_startx = r1.x + r1.w/2
            arrow_starty = r1.y + r1.h/2
            arrow_endx   = r2.x + 5
            arrow_endy   = r2.y + 5
            idl = canvas.create_line(arrow_startx,
                               arrow_starty,
                               arrow_endx,
                               arrow_endy,
                               tags = ("pan")
                               )

            ids = canvas.create_image((arrow_endx-5, arrow_endy-5),
                                image=dc.get_basher_goto_image(), anchor=NW,
                                tags=("select", "move", "pan", "basher"))

            idb = canvas.create_image((r1.x, r1.y),
                                image=dc.get_basher_image(), anchor=NW,
                                tags=("select", "move", "pan"))

            self.dataids[idb] = (dc.BASHER, idx, ids, idl)
            self.dataids[ids] = (dc.BASHER_END, idx, idb, idl)
            self.dataids[idl] = (-1, idx)

        # Draw the 0,0 cross
        canvas.create_line(10, 0, -10, 0, fill="red", tags=("pan"))
        canvas.create_line(0, 10, 0, -10, fill="red", tags=("pan"))

root = Tk()

app = PykurinLevelEditorUI(root)
app.pack()

#show_disclaimer()
root.mainloop()
