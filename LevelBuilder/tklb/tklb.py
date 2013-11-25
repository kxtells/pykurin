from Tkinter import *
import datacontainer
import tkFileDialog, tkSimpleDialog, tkMessageBox
from tksimplestatusbar import StatusBar

from lbdialogs import tkLevelDialog

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

        #The Menu bar
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
        menu.add_command(label="Edit", command=self.e_edit_level_attributes)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Test", menu=menu)
        menu.add_command(label="Run Level", command=self.run_level)

        # The toolbar to create things
        toolbar = Frame(self.master)

        self.buttons = []

        b = Button(toolbar, text="Bouncer", width=6, command=lambda: self.button(self.DC.BOUNCER,0))
        b.pack(side=LEFT, padx=2, pady=2)
        self.buttons.append(b)

        b = Button(toolbar, text="lifeup", width=6, command=lambda: self.button(self.DC.LIVES,1))
        b.pack(side=LEFT, padx=2, pady=2)
        self.buttons.append(b)

        b = Button(toolbar, text="basher", width=6, command=lambda: self.button(self.DC.BASHER,2))
        b.pack(side=LEFT, padx=2, pady=2)
        self.buttons.append(b)

        #Contains the currently pressed button. Not the index but the type of the item to create
        #DC.BASHER (for example)
        self.buttonpressed = None
        toolbar.pack(side=TOP, fill=X)


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

		#Window title
        self.changeWindowTitle("TK pykurin Level builder")

    def get_item_type(self, itemid):
        return self.dataids[itemid][0]

    def isBasher(self, itemid):
        return self.get_item_type(itemid) == self.DC.BASHER

    def isBasherEnd(self, itemid):
        return self.get_item_type(itemid) == self.DC.BASHER_END

    def changeWindowTitle(self, title):
        self.master.wm_title(title)

    #
    # Toolbar selection handling
    #
    def unsunken_all(self):
        for b in self.buttons:
            b.config(relief=RAISED)

    def isButtonPressed(self):
        return self.buttonpressed != None

    def button(self, code, buttonid):
        self.unsunken_all()
        if self.buttonpressed == code:
            self.buttons[buttonid].config(relief=RAISED)
            self.buttonpressed = None
        else:
            self.buttons[buttonid].config(relief=SUNKEN)
            self.buttonpressed = code

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
    # Item selection and creating
    #
    def canvas_left_click(self, event):
        """ May select/unselect an Item.
            If any creation tool is active may create one of the selected items

        """
        if self.isButtonPressed():
            self.adding_item_to_canvas(event)
        else:
            self.selecting_items(event)

    def selecting_items(self, event):
        #Once clicked, give keyboard focus to canvas (in case it wasn't set)
        self.canvas.focus_set()

        x = event.x
        y = event.y

        #Delete all selections
        for item in self.canvas.find_withtag("selection"):
            self.canvas.delete(item)

        #Create a new selection
        self.select_item(x,y)


    def adding_item_to_canvas(self, event):
        if self.buttonpressed == self.DC.BASHER:
            self._create_basher(event.x, event.y, new=True)
        elif self.buttonpressed == self.DC.BOUNCER:
            self._create_bouncer(event.x, event.y, new=True)
        elif self.buttonpressed == self.DC.LIVES:
            self._create_lives(event.x, event.y, new=True)

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
        bbox  = self.canvas.bbox(self.sitem)
        w     = abs(bbox[0] - bbox[2])
        h     = abs(bbox[1] - bbox[3])
        self.canvas.coords(self.sitem, (event.x -w/2, event.y -h/2))

        #Move the selection
        for item in self.canvas.find_withtag("selection"):
            self.canvas.coords(item, self.canvas.bbox(self.sitem))

        #Basher needs a little bit more of work
        if self.isBasher(self.sitem) :
            self.update_basher_arrow(self.sitem)
        if self.isBasherEnd(self.sitem):
            basher_id = self.dataids[self.sitem][2]
            self.update_basher_arrow(basher_id)

    def unpan_bbox(self, bbox):
        """Return a bbox without the panning movements"""
        return (bbox[0] - self.panx, bbox[1] - self.pany, bbox[2] - self.panx, bbox[3] - self.pany)

    def canvas_left_click_release(self, event):
        if not self.sitem:
            return

        itype = self.dataids[self.sitem][0]
        iid   = self.dataids[self.sitem][1]
        bbox  = self.unpan_bbox(self.canvas.bbox(self.sitem))

        self.DC.move_item(itype, iid, bbox[0], bbox[1])

    def update_basher_arrow(self, basherid):
        """Update the arrow representing the path of the BASHER.
            This needs updating everytime the basher or basher end changes
            position
        """
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

        self.canvas.coords(basher_line, lbbox)

    #
    # Remove items
    #
    def delete_item(self, event):
        """Deletes the current selected item"""
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
        """ Creates a new level with no file associated to it """
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


    def e_edit_level_attributes(self):
        d = tkLevelDialog(self.master, datacontainer=self.DC)
    #
    # Item Creation
    #
    def _create_bouncer(self, x, y, dcid=None, new=False):
        canvas = self.canvas
        dc     = self.DC
        if new:
            dcid = dc.add_item(self.DC.BOUNCER, x, y)

        id = canvas.create_image((x, y),
                            image=dc.get_bouncer_image(), anchor=NW,
                            tags=("select", "move", "bouncer", "delete", "pan"))

        self.dataids[id] = (dc.BOUNCER, dcid)

    def _create_lives(self, x, y, dcid=None, new=False):
        canvas = self.canvas
        dc     = self.DC

        if new:
            dcid = dc.add_item(self.DC.LIVES, x, y)


        id = canvas.create_image((x, y),
                            image=dc.get_live_image(), anchor=NW,
                            tags=("select", "move", "delete", "lives", "pan"))

        self.dataids[id] = (dc.LIVES, dcid)


    def _create_basher(self, x, y, rx=None, ry=None, dcid=None, new=False):
        """
            Create a basher to add to the canvas and Datacontainer.
            By default the basher is only created in the canvas, to be
            saved in the datacontainer the new flag has to be set to true
        """
        canvas = self.canvas
        dc     = self.DC

        if not rx:
            rx = x + 100
        if not ry:
            ry = y

        #If its new, it can't have an dcid. Create and get the dcid first
        if new:
            dcid = dc.add_item(self.DC.BASHER, x, y)
            dc.add_item(self.DC.BASHER_END, rx, ry)


        idl = canvas.create_line(0,0,0,0,tags = ("pan"))

        ids = canvas.create_image((rx, ry),
                            image=dc.get_basher_goto_image(), anchor=NW,
                            tags=("select", "move", "pan", "basher"))

        idb = canvas.create_image((x, y),
                            image=dc.get_basher_image(), anchor=NW,
                            tags=("select", "move", "pan"))


        self.dataids[idb] = (dc.BASHER, dcid, ids, idl)
        self.dataids[ids] = (dc.BASHER_END, dcid, idb, idl)
        self.dataids[idl] = (-1, dcid)

        self.update_basher_arrow(idb)


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
            self._create_bouncer(r.x, r.y, dcid=idx)

        for idx,r in enumerate(dc.lives):
            self._create_lives(r.x, r.y, dcid=idx)

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

            self.dataids[id] = (dc.STICKS, idx)

        for idx,r in enumerate(dc.bashers):
            r1 = r
            r2 = dc.bashers_end[idx]
            self._create_basher(r1.x, r1.y, rx=r2.x, ry=r2.y, dcid=idx)

        # Draw the 0,0 cross
        canvas.create_line(10, 0, -10, 0, fill="red", tags=("pan"))
        canvas.create_line(0, 10, 0, -10, fill="red", tags=("pan"))


root = Tk()

app = PykurinLevelEditorUI(root)
app.pack()

#show_disclaimer()
root.mainloop()
