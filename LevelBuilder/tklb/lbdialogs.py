#
#
# Dialog to handle Level related information such as name, start and end position,
# base pykurin path etc.
#
#
from Tkinter import *

from common_dialogs import *

import os
import difflib
import tempfile

class tkLevelDialog(Toplevel):
    def __init__(self, parent, title = None, modal=True, datacontainer=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.DC = datacontainer


        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))


        Label(self, text="Name:").grid(row=0)
        Label(self, text="Level Image:").grid(row=1)
        Label(self, text="Static Background:").grid(row=2)
        Label(self, text="Collisions Image:").grid(row=3)
        Label(self, text="Stick:").grid(row=4)

        self.leveltitle = StringVar()
        self.leveltitle.set(self.DC.get_title())
        self.e0 = Entry(self, textvariable = self.leveltitle, width=50)


        self.image = StringVar()
        self.image.set(self.DC.get_image_fname())
        self.e1 = Entry(self, textvariable = self.image, width=50,
                        state=DISABLED, relief=RIDGE)

        self.background2 = StringVar()
        self.background2.set(self.DC.get_background_fname())
        self.e2 = Entry(self, textvariable = self.background2, width=50,
                       state=DISABLED, relief=RIDGE)

        self.collision = StringVar()
        self.collision.set(self.DC.get_colision_fname())
        self.e3 = Entry(self, textvariable = self.collision, width=50,
                       state=DISABLED, relief=RIDGE)

        self.bviewfile = Button(self, text="View File", width=6,
                              command=lambda: self.view_file())

        self.bdifffile = Button(self, text="Diff File", width=6,
                              command=lambda: self.diff_file())

        #If theres no original file, theres no diff or view
        if not self.DC.get_current_level_filename():
            self.bviewfile.config(state=DISABLED)
            self.bdifffile.config(state=DISABLED)


        self.bframe  = Frame(self)
        self.bok     = Button(self.bframe, text="OK", width=6, command=lambda: self.finish())
        #self.bapply  = Button(self.bframe, text="Apply", width=6, command=lambda: self.apply())
        self.bcancel = Button(self.bframe, text="Cancel", width=6, command=lambda: self.cancel())

        self.fchooser1 = Button(self, text="F", width=1,
                                command=lambda: self.fchooser(self.DC.IMAGE))
        self.fchooser2 = Button(self, text="F", width=1,
                                command=lambda: self.fchooser(self.DC.BGIMAGE))
        self.fchooser3 = Button(self, text="F", width=1,
                                command=lambda: self.fchooser(self.DC.COLIMAGE))
        #bcancel= Button(toolbar, text="Cancel", width=6, command=self.cancel())
        #bapply.pack(side=LEFT, padx=2, pady=2)
        #self.buttons.append(b)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)
        #self.e4.grid(row=4, column=1)
        self.bviewfile.grid(row=5, column=0)
        self.bdifffile.grid(row=6, column=0)

        self.bframe.grid(row=7, column=0, columnspan=3)
        self.bok.grid(row=0, column=0)
        #self.bapply.grid(row=0, column=1)
        self.bcancel.grid(row=0, column=2)
        self.fchooser1.grid(row=1, column=2)
        self.fchooser2.grid(row=2, column=2)
        self.fchooser3.grid(row=3, column=2)

        if modal:
            self.wait_window(self)

    def apply(self):
        if self.e1.get() != "None":
            self.DC.set_image(self.e1.get())
        if self.e2.get() != "None":
            self.DC.set_bg_image(self.e2.get())
        if self.e3.get() != "None":
            self.DC.set_col_image(self.e3.get())
        if self.e0.get() != "None":
            self.DC.set_title(self.e0.get())

    def finish(self):
        self.apply()
        self.destroy()

    def cancel(self):
        self.destroy()

    def fchooser(self, which):
        """
            File chooser for the Image, static background and Collision
        """
        filename = open_image_chooser("Image chooser",
                                    self.DC.get_basepath());
        if not filename:
            return

        if which == self.DC.IMAGE:
            self.image.set(filename)
        elif which == self.DC.BGIMAGE:
            self.background2.set(filename)
        elif which == self.DC.COLIMAGE:
            self.collision.set(filename)

    def view_file(self):
        fname = self.DC.get_current_level_filename()
        tkTextViewer(self.parent, title="FILE %s"%os.path.basename(fname),
                filename=fname)

    def diff_file(self):
        fname  = self.DC.get_current_level_filename()
        tfil   = tempfile.NamedTemporaryFile()
        tfname = tfil.name

        with open (fname, "r") as datafile:
            lines1=datafile.readlines()

        self.DC.save_to_file(tfname)
        with open (tfname, "r") as datafile:
            lines2=datafile.readlines()


        difflines=difflib.unified_diff(lines1, lines2,
                                      fromfile=fname, tofile=tfname)
        tkTextViewer(self.parent, title="FILE %s"%os.path.basename(fname),
                textdata="".join(difflines))



"""
    Basic class to present big amount of text together.
    Useful for presenting logs or small files

    tkTextViewer(master, textdata="lala")
"""
class tkTextViewer(Toplevel):
    def __init__(self, parent, title = None, modal=True, textdata="", filename=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.text   = textdata
        if filename:
            try:
                with open (filename, "r") as datafile:
                    data=datafile.readlines()
                    self.text = "".join(data)
            except:
                self.text = "ERROR READING FILE: %s" % filename


        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))


        self.TW = Text(self)
        self.TW.insert(INSERT, self.text)

        self.bok = Button(self, text="OK", width=6, command=lambda: self.finish())

        #self.TW.grid(row=0, column=0)
        #self.bok.grid(row=1, column=0)
        self.TW.pack()
        self.bok.pack()



        if modal:
            self.wait_window(self)

    def finish(self):
        self.destroy()
