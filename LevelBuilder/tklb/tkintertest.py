from Tkinter import *

class AppUI(Frame):

    def __init__(self, master=None):
    Frame.__init__(self, master, relief=SUNKEN, bd=2)

    self.menubar = Menu(self)

    menu = Menu(self.menubar, tearoff=0)
    self.menubar.add_cascade(label="File", menu=menu)
    menu.add_command(label="New Level")
    menu.add_command(label="Open Level")
    menu.add_command(label="Save Level")
    menu.add_command(label="Save Level As")
    menu.add_command(label="Exit")

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


    try:
        self.master.config(menu=self.menubar)
    except AttributeError:
        # master is a toplevel window (Python 1.4/Tkinter 1.63)
        self.master.tk.call(master, "config", "-menu", self.menubar)

    self.canvas = Canvas(self, bg="gray", width=800, height=600,
                 bd=0, highlightthickness=0)
    self.canvas.pack()


root = Tk()

app = AppUI(root)
app.pack()

root.mainloop()
