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

    def mouse_motion(self, event):
        self.statusbar.set("%s : %s" % (event.x, event.y))

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

    def f_save_level(self):
        pass

    def f_save_level_as(self):
        pass

    def f_exit(self):
        pass

root = Tk()

app = AppUI(root)
app.pack()

#show_disclaimer()
root.mainloop()
