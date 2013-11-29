#
#
# Dialog to handle Level related information such as name, start and end position,
# base pykurin path etc.
#
#
from Tkinter import *

from common_dialogs import *

import icons
import datacontainer

import os
import difflib
import tempfile
import icons

BUTTON_SIZE = 70
BUTTON_COMPOUND= LEFT


class tkLevelDialog(Toplevel):
    C_IMAGE         = 0
    C_BACKGROUND    = 1
    C_COLLISION     = 2
    C_LEVELPACK     = 3

    def __init__(self, parent, title = None, modal=True, levelcontainer=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.DC = levelcontainer
        self.LPL = datacontainer.LevelPackList(self.DC.get_pykurindir())
        self.ICONS = icons.icons_from_dir()


        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))


        Label(self, text="Name:").grid(row=0)
        Label(self, text="Level Image:").grid(row=1)
        Label(self, text="Static Background:").grid(row=2)
        Label(self, text="Collisions Image:").grid(row=3)
        Label(self, text="Level Pack:").grid(row=4)
        Label(self, text="Stick:").grid(row=5)

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

        self.lpack = StringVar()
        if self.DC.get_levelpack():
            self.lpack.set(self.DC.get_levelpack().get_name())
        else:
            self.lpack.set("No level Pack")

        lnames = [lp.get_name() for lfn,lp in self.LPL.get_packs()]
        self.e4 = OptionMenu(self, self.lpack, *lnames)

        self.bviewfile = Button(self, text="View File", width=6,
                              command=lambda: self.view_file())

        self.bdifffile = Button(self, text="Diff File", width=6,
                              command=lambda: self.diff_file())

        #If theres no original file, theres no diff or view
        if not self.DC.get_current_level_filename():
            self.bviewfile.config(state=DISABLED)
            self.bdifffile.config(state=DISABLED)


        ICONS = icons.icons_from_dir()
        self.bframe  = Frame(self)
        self.bok     = Button(self.bframe, image=self.ICONS["tick24"], compound=BUTTON_COMPOUND,
                              text="OK", width=BUTTON_SIZE, command=lambda: self.finish())
        #self.bapply  = Button(self.bframe, text="Apply", width=6, command=lambda: self.apply())
        self.bcancel = Button(self.bframe, image=self.ICONS["cross24"], compound=BUTTON_COMPOUND,
                              text="CANCEL", width=BUTTON_SIZE, command=lambda: self.cancel())

        self.fchooser1 = Button(self, image=ICONS["edit16"],
                                command=lambda: self.fchooser(self.C_IMAGE))
        self.fchooser2 = Button(self, image=ICONS["edit16"],
                                command=lambda: self.fchooser(self.C_BACKGROUND))
        self.fchooser3 = Button(self, image=ICONS["edit16"],
                                command=lambda: self.fchooser(self.C_COLLISION))
        #self.fchooser4 = Button(self, image=ICONS["edit16"],
        #                        command=lambda: self.levelpacksDialog())
        #bcancel= Button(toolbar, text="Cancel", width=6, command=self.cancel())
        #bapply.pack(side=LEFT, padx=2, pady=2)
        #self.buttons.append(b)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)
        self.e4.grid(row=4, column=1)

        self.fchooser1.grid(row=1, column=2)
        self.fchooser2.grid(row=2, column=2)
        self.fchooser3.grid(row=3, column=2)
        #self.fchooser4.grid(row=4, column=2)

        self.bviewfile.grid(row=5, column=0)
        self.bdifffile.grid(row=6, column=0)

        self.bframe.grid(row=7, column=0, columnspan=3)
        self.bok.grid(row=0, column=0)
        #self.bapply.grid(row=0, column=1)
        self.bcancel.grid(row=0, column=2)

        self.grab_set()
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
        lvlpackname = self.lpack.get()
        lvlpack     = self.LPL.getPackByName(lvlpackname)
        if lvlpack:
            self.DC.set_levelpack(lvlpack)

    def finish(self):
        self.apply()
        self.destroy()

    def cancel(self):
        self.destroy()

    def levelpacksDialog(self):
        tkLevelPacksList(self.parent, title="Level Packs Selector",
                        pykurindir=self.DC.get_pykurindir())

    def fchooser(self, which):
        """
            File chooser for the Image, static background and Collision
        """
        filename = open_image_chooser("Image chooser",
                                    self.DC.get_basepath());
        if not filename:
            return

        if which == self.C_IMAGE:
            self.image.set(filename)
        elif which == self.C_BACKGROUND:
            self.background2.set(filename)
        elif which == self.C_COLLISION:
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
                textdata="".join(difflines),
                isdiff=True)



"""
    Basic class to present big amount of text together.
    Useful for presenting logs or small files

    tkTextViewer(master, textdata="lala")
"""
class tkTextViewer(Toplevel):
    def __init__(self, parent, title = None, modal=True, textdata="",
                filename=None, isdiff=False, islog=False):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.ICONS = icons.icons_from_dir()

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


        self.textframe = Frame(self)
        self.TW = Text(self.textframe)
        self.TW.insert(INSERT, self.text)
        scrollbar = Scrollbar(self.textframe)
        self.TW.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.TW.yview)



        if isdiff:
            self._colorize_diff()
        elif islog:
            self._colorize_log()

        self.bok = Button(self, text="OK", image=self.ICONS["tick24"], compound=BUTTON_COMPOUND,
                          width=BUTTON_SIZE, command=lambda: self.finish())

        #self.TW.grid(row=0, column=0)
        #self.bok.grid(row=1, column=0)
        self.textframe.pack()
        scrollbar.pack(side=RIGHT, fill=Y)
        self.TW.pack()
        self.bok.pack()

        self.grab_set()
        self.wait_window(self)

    def finish(self):
        self.destroy()

    def _colorize_diff(self):
        """
            Colorizes a UNIFIED DIFF.
        """
        for linenum, line in enumerate(self.text.split("\n")):
            cline = linenum+1

            if len(line) == 0 :
                continue

            if line.startswith("-"):
                self.TW.tag_add("rem","%s.0" % cline, "%s.%s" %(cline, len(line)))
            elif line.startswith("+"):
                self.TW.tag_add("add","%s.0" % cline, "%s.%s" %(cline, len(line)))
            elif line.startswith("@@"):
                self.TW.tag_add("info","%s.0" % cline, "%s.%s" %(cline, len(line)))

        self.TW.tag_config("rem",   background="#fdf6e3", foreground="#d33682")
        self.TW.tag_config("add",   background="#fdf6e3", foreground="#859900")
        self.TW.tag_config("info",  background="#fdf6e3", foreground="#b58900")

    def _colorize_log(self):
        """
            Colorizes a UNIFIED DIFF.
        """
        for linenum, line in enumerate(self.text.split("\n")):
            cline = linenum+1

            if len(line) == 0 :
                continue

            if line.startswith("ERROR"):
                self.TW.tag_add("ERROR","%s.0" % cline, "%s.%s" %(cline, len(line)))
            elif line.startswith("DELETE"):
                self.TW.tag_add("DELETE","%s.0" % cline, "%s.%s" %(cline, len(line)))
            elif line.startswith("SAVE"):
                self.TW.tag_add("SAVE","%s.0" % cline, "%s.%s" %(cline, len(line)))
            elif line.startswith("COPY"):
                self.TW.tag_add("COPY","%s.0" % cline, "%s.%s" %(cline, len(line)))

        self.TW.tag_config("ERROR",  background="#fdf6e3", foreground="#d33682")
        self.TW.tag_config("SAVE",   background="#fdf6e3", foreground="#859900")
        self.TW.tag_config("DELETE", background="#fdf6e3", foreground="#b58900")
        self.TW.tag_config("COPY",   background="#fdf6e3", foreground="#b58900")




"""
    Frame to present the LevelPacks List And edit if necessary.
"""
class tkLevelPacksList(Toplevel):
    def __init__(self, parent, modal=True, pykurindir=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.LPL   = datacontainer.LevelPackList(pykurindir)
        self.ICONS = icons.icons_from_dir()

        self.title("Level Pack Manager")

        self.parent = parent
        self.LB = Listbox(self, width=50)

        self.bframe   = Frame(self)
        self.bok      = Button(self.bframe, text="OK", image=self.ICONS["tick24"],
                                compound=BUTTON_COMPOUND,  width=BUTTON_SIZE, command=lambda: self.finish())

        self.bcancel  = Button(self.bframe, text="CANCEL",image=self.ICONS["cross24"],
                                compound=BUTTON_COMPOUND, width=BUTTON_SIZE, command=lambda: self.cancel())

        self.bdel = Button(self, text="DELETE", width=BUTTON_SIZE, image=self.ICONS["trash24"],
                                compound=BUTTON_COMPOUND, command=lambda: self.deletepack())

        self.bnew = Button(self, text="ADDPACK", width=BUTTON_SIZE, image=self.ICONS["new24"],
                                compound=BUTTON_COMPOUND, command=lambda: self.addpack())

        self.bmod = Button(self, text="MODIFY", width=BUTTON_SIZE, image=self.ICONS["edit24"],
                                compound=BUTTON_COMPOUND, command=lambda: self.modify())

        self.LB.grid(row=0, column=0, rowspan=5)

        self.bframe.grid(row=6, columnspan=2)
        self.bok.grid(row=0, column=0)
        self.bcancel.grid(row=0, column=1)

        self.bnew.grid(row=1, column=1)
        self.bmod.grid(row=2, column=1)
        self.bdel.grid(row=3, column=1)

        self.__load_listbox()

        self.grab_set()
        self.wait_window(self)


    def finish(self):
        stat,errlog = self.LPL.sync()

        tkTextViewer(self.parent, title="LevelPack Changes",
                textdata="\n".join(errlog), islog=True)

        self.destroy()
        return

    def __load_listbox(self):
        self.LB.delete(0, END)

        self.levelpacks = []
        for fname,lpc in self.LPL.get_packs():
            self.LB.insert(END,"%s\t%s"%(lpc.get_name(), fname))
            self.levelpacks.append(lpc)

    def deletepack(self):
        items = map(int, self.LB.curselection())

        for idx in items:
            ret = self.LPL.removePack(self.levelpacks[idx])

        self.__load_listbox()

    def addpack(self):
        self.LPL.addPack()
        self.__load_listbox()

    def modify(self):
        items     = map(int, self.LB.curselection())
        sel_lpack = self.levelpacks[items[-1]]

        tkLevelPackEdit(self.parent, levelpack=sel_lpack)

        self.__load_listbox()

    def cancel(self):
        self.destroy()

"""
    Level Pack editor.
    Edit a specific LevelPack, changing the name and various attributes.

    Presents a list of which levels are assigned to this levelpack.
"""
class tkLevelPackEdit(Toplevel):
    def __init__(self, parent, modal=True, levelpack=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)


        self.parent = parent
        self.LP = levelpack
        self.ICONS = icons.icons_from_dir()


        self.listframe  = Frame(self)
        self.lb = Listbox(self.listframe, width=49)
        scrollbar = Scrollbar(self.listframe)
        self.lb.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lb.yview)


        self.title("MODIFY: %s"%self.LP.get_name())
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))


        Label(self, text="Name:").grid(row=0)
        Label(self, text="Directory Name:").grid(row=1)
        Label(self, text="Icon:").grid(row=2)
        Label(self, text="Levels to open:").grid(row=3)
        Label(self, text="Levels Assigned:").grid(row=4)

        self.packtitle = StringVar()
        self.packtitle.set(self.LP.get_name())
        self.e0 = Entry(self, textvariable = self.packtitle, width=50)

        self.dname = StringVar()
        self.dname.set(self.LP.get_dirname())
        self.e1 = Entry(self, textvariable = self.dname, width=50)

        self.icon = StringVar()
        self.icon.set(self.LP.get_icon())
        self.e2 = Entry(self, textvariable = self.icon, width=50)

        self.levels2open = StringVar()
        self.levels2open.set(self.LP.get_levels2open())
        self.e3 = Entry(self, textvariable = self.levels2open, width=50)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)


        self.bframe  = Frame(self)
        self.bok     = Button(self.bframe, text="OK", width=BUTTON_SIZE, image=self.ICONS["tick24"],
                                compound=BUTTON_COMPOUND, command=lambda: self.ok())
        self.bcancel = Button(self.bframe, text="Cancel", image=self.ICONS["tick24"],
                                compound=BUTTON_COMPOUND, width=BUTTON_SIZE, command=lambda: self.cancel())

        #self.lb.grid(row=4, column=1)
        self.listframe.grid(row=4, column=1)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.lb.pack()

        self.bframe.grid(row=5, column=0, columnspan=2)
        self.bok.grid(row=0, column=0)
        self.bcancel.grid(row=0, column=1)

        self._fill_listbox()

        self.grab_set()
        self.wait_window(self)

    def _fill_listbox(self):
        #FILL THE LISTBOX
        for file in self.LP.get_list_of_levels():
            fpath = os.path.join(self.LP.get_directory_fullpath(), file)
            lc = datacontainer.LevelContainer(pykurindir=self.LP.get_pykurindir())
            lc.load_from_file(fpath)
            self.lb.insert(END,"%s\t%s"%(lc.get_title(),file))


    def apply(self):
        if self.e0.get() != "None":
            self.LP.set_name(self.e0.get())
        dirname = self.e1.get()
        if dirname != "None":
            ok,err = self.LP.set_dirname(dirname)
            if not ok:
                error_message("ERROR","Set directory name %s: %s"%(dirname,err))
        if self.e2.get() != "None":
            self.LP.set_icon(self.e2.get())
        if self.e3.get() != "None":
            self.LP.set_levels2open(self.e3.get())


    def ok(self):
        #apply changes, sync and leave
        self.apply()
        self.destroy()
        pass

    def cancel(self):
        self.destroy()
