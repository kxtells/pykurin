#
#
# Dialog to handle Level related information such as name, start and end position,
# base pykurin path etc.
#
#
from Tkinter import *

class tkLevelDialog(Toplevel):

    def __init__(self, parent, title = None, modal=True, datacontainer=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
        self.DC = datacontainer


        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))


        Label(self, text="Name:").grid(row=0)
        Label(self, text="Background:").grid(row=1)
        Label(self, text="Background2:").grid(row=2)
        Label(self, text="Collisions:").grid(row=3)
        Label(self, text="Stick:").grid(row=4)

        self.leveltitle = StringVar()
        self.leveltitle.set(self.DC.get_title())
        self.e0 = Entry(self, textvariable = self.leveltitle)


        self.background = StringVar()
        self.background.set(self.DC.get_image_fname())
        self.e1 = Entry(self, textvariable = self.background)

        self.background2 = StringVar()
        self.background2.set(self.DC.get_background_fname())
        self.e2 = Entry(self, textvariable = self.background2)


        self.collision = StringVar()
        self.collision.set(self.DC.get_colision_fname())
        self.e3 = Entry(self, textvariable = self.collision)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)
        #self.e4.grid(row=4, column=1)

        if modal:
            self.wait_window(self)
