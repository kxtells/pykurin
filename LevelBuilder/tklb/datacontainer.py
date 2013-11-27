from pygame import Rect
from pygame import image
from ConfigParser import SafeConfigParser
import uuid
import os
import shutil

class LevelContainer:
    BASHER      = 0
    BOUNCER     = 1
    LIVES       = 2
    GOALS       = 3
    STICKS      = 4
    BASHER_END  = 5

    IMAGE       = 0
    COLIMAGE    = 1
    BGIMAGE     = 2

    selecteditem = None


    #File Metadata
    background_filename = None
    uuid = None

    #working data
    last_error = None

    def __init__(self):
        """Loads all the needed common images"""
        self.base_pykurin_directory = None
        self.current_level_filename = None
        self.img_filename = None
        self.background_filename = None
        self.collision_filename= None
        self.bashers = []
        self.bouncers = []
        self.lives = []
        self.goals = []
        self.sticks = []
        self.bashers_end = []
        self.title = None

        #By default it is not assigned to a LevelPack. But on save it should, or
        #there is no place to be saved!
        self.lvlpack = None

        #References to everything
        self.items = [self.bashers, self.bouncers, self.lives, self.goals, self.sticks, self.bashers_end]

        #LEGACY
        self.items_pack = [self.bashers,self.bouncers,self.lives,self.goals,self.sticks,self.bashers_end]

    def set_pykurindir(self,path):
        self.base_pykurin_directory = path

    def get_pykurindir(self):
        return self.base_pykurin_directory

    def set_image(self,imagepath):
        self.img_filename = imagepath

    def get_image_fname(self):
        return self.img_filename

    def get_background_fname(self):
        return self.background_filename

    def get_colision_fname(self):
        return self.collision_filename

    def get_background_fname(self):
        return self.background_filename

    def set_bg_image(self, imagepath):
        self.background_filename = imagepath

    def set_col_image(self,imagepath):
        self.collision_filename  = imagepath

    def set_current_level_filename(self,text):
        self.current_level_filename = text

    def get_current_level_filename(self):
        return self.current_level_filename

    def set_last_error(self,text):
        self.last_error = text

    def get_levelpack(self):
        return self.lvlpack

    def set_levelpack(self, levelpack):
        assert isinstance(levelpack, LevelPackContainer)
        self.lvlpack = levelpack

    def get_last_error(self):
        if last_error==None:
            return "OK"
        else:
            return self.last_error

    def get_image(self):
        return self.image

    def get_bgimage(self):
        return self.bgimage

    def get_colimage(self):
        return self.colimage

    def get_title(self):
        return self.title

    def get_basepath(self):
        return self.base_pykurin_directory

    def set_title(self,text):
        self.title = text


    def set_uuid(self,uuid):
        self.uuid = uuid

    def generate_uuid(self):
        self.uuid = uuid.uuid4()

    #
    # Object Handling
    #
    def remove_item(self, itype, index):
        del self.items[itype][index]
        #A basher needs to remove also its end
        if itype == self.BASHER:
            del self.items[self.BASHER_END][index]

    def move_item(self, itype, index, nx, ny):
        self.items[itype][index] = Rect(nx,ny,0,0)

    def add_item(self,ident,mx,my):
        #if ident==0:
        #   return True
        if ident == self.BASHER: #basher
            self.bashers.append(Rect(mx,my,64,64))
            return len(self.bashers) - 1
        if ident == self.BASHER_END:
            self.bashers_end.append(Rect(mx,my,0,0)) #where basher moves
            return len(self.bashers_end) - 1
        elif ident == self.BOUNCER: #bouncer
            self.bouncers.append(Rect(mx,my,32,32))
            return len(self.bouncers) - 1
        elif ident == self.LIVES: #lives
            self.lives.append(Rect(mx,my,32,32))
            return len(self.lives) - 1
        elif ident == self.GOALS: #Goal
            if len(self.goals)<1: #only one goal ma friend
                self.goals.append(Rect(mx,my,100,100))
                return len(self.goals) - 1
        elif ident == self.STICKS: #Start
            if len(self.sticks)<1: #only one goal ma friend
                self.sticks.append(Rect(mx,my,64,64))
                return len(self.sticks) - 1

    #
    # Checkers
    #
    def isItemSelected(self):
        return self.selecteditem != None

    def isBgDefined(self):
        return self.background_filename != None

    def isColisionDefined(self):
        return self.collision_filename != None

    def isGoalDefined(self):
        return len(self.goals) > 0

    def isStartDefined(self):
        return len(self.sticks) > 0

    def isImageDefined(self):
        return self.img_filename !=None

    def isTitleDefined(self):
        return self.title !=None

    def isSaveable(self):
        """
            Checks if the current datacontainer can be saved, that means, that
            all the needed parameters are defined.
            Note that isSaveable=True does not mean that the level will run
            correctly with pykurin. For that, you also need to check if the
            data is in the pykurin directory. isAllDataInPykurinDirectory
            Returns True or False + an explanation of what is missing
        """
        ret = True
        text = ""
        if not self.isBgDefined():
            ret = False
            text += " - Background Image\n"

        if not self.isColisionDefined():
            ret = False
            text += " - Colision Image\n"

        if not self.isStartDefined():
            ret = False
            text += " - Start\n"

        if not self.isGoalDefined():
            ret = False
            text += " - Goal\n"

        if not self.isImageDefined():
            ret = False
            text += " - Base Image\n"

        if not self.isTitleDefined():
            ret = False
            text += " - Title\n"

        if not ret:
            text = "I cannot let you proceed my friend \nYour level is Missing some stuff:\n"+text

        return ret,text

    def isPykurinDirectory(self, dirpath):
        """Returns True if dirpath is a pykurin directory. (contains
        all what is expected from it). If not, returns False and a list
        of what failed
        """

        if not dirpath: return

        dirlist = os.listdir(dirpath)
        expected = ["pykurin.py", "levels", "backgrounds", "sticks", "sprites",
                "levelpacks"]

        for exp in expected:
            if exp not in dirlist:
                return False

        return True

    def isAllDataInPykurinDirectory(self):
        """Checks if all the data is relative to the set pykurin directory.
            All the levels must store their data in that directory, if not,
            pykurin won't run correctly.
            If the level has also a levelpack assigned it will check if all
            the data is in the levelpack directory.
        """
        pdir = self.get_pykurindir()

        if self.get_levelpack():
            lpdir = self.get_levelpack().get_dirname()
        else:
            lpdir = ""

        tdir  = os.path.join(pdir,"levels",lpdir)
        isall = True
        data  = []

        #Background always on the same place
        if pdir not in self.get_background_fname():
            isall = False
            data.append(self.get_background_fname())

        #Levels and colisions go to their own levelpackdir
        if tdir not in self.get_colision_fname():
            isall = False
            data.append(self.get_colision_fname())
        if tdir not in self.get_image_fname():
            isall = False
            data.append(self.get_image_fname())

        return isall, data

    def get_last_autogenfile(self, directory):
        """When creating new files, follow the convention:
            backgrounds/bgX.ext (X increases over time)
            levels/levelname.ext
            levels/levelnamecol.ext
        """
        pass

    def copyOutsidersToPykurinDirectory(self):
        """
            Check all the files defined that are outise the pykurin directory
            and creates a copy inside the directory (if it is possible)
            This will modify the datacontainer to point to the new files
            inside the pykurin directory.

            Will raise the Exceptions up, to be catched and presented.
        """
        pdir  = self.get_pykurindir()
        #Create a filename without special characters from the title
        filen = ''.join(e for e in self.get_title() if e.isalnum())
        operations = []

        if self.get_levelpack():
            lpdir = self.get_levelpack().get_dirname()
        else:
            lpdir = ""

        tdir  = os.path.join(pdir,"levels",lpdir)


        if pdir not in self.get_background_fname():
            origin  = self.get_background_fname()
            fname   = os.path.basename(origin)
            dest    = os.path.join(pdir,"backgrounds", fname)
            shutil.copyfile(origin, dest)
            self.set_bg_image(dest)
            operations.append("CP %s -> %s" %(origin, dest))

        #Levels and colisions go th the levelpack dir
        if tdir not in self.get_image_fname():
            origin  = self.get_image_fname()
            fn, ext = os.path.splitext(origin)
            dest    = os.path.join(pdir,"levels",lpdir,"%s%s"%(filen,ext))
            shutil.copyfile(origin, dest)
            self.set_image(dest)
            operations.append("CP %s -> %s" %(origin, dest))
        if tdir not in self.get_colision_fname():
            origin  = self.get_colision_fname()
            fn, ext = os.path.splitext(origin)
            dest    = os.path.join(pdir,"levels",lpdir,"%sCOL%s"%(filen,ext))
            shutil.copyfile(origin, dest)
            self.set_col_image(dest)
            operations.append("CP %s -> %s" %(origin, dest))

        return operations


    def load_from_file(self,full_path,xpadding=0,ypadding=0):
        """
            Load the datacontainer from a file.
        """
        #clear_everything()
        parser = SafeConfigParser()
        parser.read(full_path)

        imagefile = parser.get('options','background')
        colfilename = parser.get('options','collision')
        bgfilename = parser.get('options','background2')
        title = parser.get('options','name')
        uuid = parser.get('options','uuid')

        self.title = title
        self.uuid = uuid

        part = full_path.rpartition('/')
        part2 = imagefile.rpartition('/')

        colfilename = self.get_pykurindir()+"/"+colfilename
        self.set_image(os.path.join(self.get_pykurindir(), imagefile))
        self.set_bg_image(os.path.join(self.get_pykurindir(), bgfilename))
        self.set_col_image(os.path.join(self.get_pykurindir(), colfilename))


        #Fill the things
        self.retrieve_bouncer_list(parser,xpadding,ypadding)
        self.retrieve_lives_list(parser,xpadding,ypadding)
        self.retrieve_end(parser,xpadding,ypadding)
        self.retrieve_start(parser,xpadding,ypadding)
        self.retrieve_bashers_list(parser,xpadding,ypadding)

        #everything went as expected, save current editing filename
        self.current_level_filename = full_path

    def retrieve_bashers_list(self,parser,xp,yp):

        del self.bashers[:]
        del self.bashers_end[:]

        try:
            for b in parser.items('bashers'):
                #FORMAT: 490,200:490,350;1
                basher, basher_end_tmp = b
                basher_end = basher_end_tmp.partition(";")[0]
                bx,t,by = basher.partition(",")
                bex,t,bey = basher_end.partition(",")

                self.bashers.append(Rect(int(bx)+xp,int(by)+yp,0,0))
                self.bashers_end.append(Rect(int(bex)+xp,int(bey)+yp,0,0))
        except:
            pass

    def retrieve_bouncer_list(self,parser,xp,yp):
        del self.bouncers[:]
        try:
            for b in parser.items('bouncers'):
                bx,by = b
                self.bouncers.append(Rect(int(bx)+xp,int(by)+yp,32,32))
        except:
            pass

    def retrieve_lives_list(self,parser,xp,yp):
        del self.lives[:]
        try:
            for b in parser.items('recovers'):
                bx,by = b
                self.lives.append(Rect(int(bx)+xp,int(by)+yp,32,32))
        except:
            pass

    def retrieve_start(self,parser,xp,yp):
        del self.sticks[:]
        gx = int(parser.get('options','startx'))
        gy = int(parser.get('options','starty'))
        self.sticks.append(Rect(int(gx)+xp,int(gy)+yp,64,64))

    def retrieve_end(self,parser,xp,yp):
        del self.goals[:]
        gx = int(parser.get('options','endx'))
        gy = int(parser.get('options','endy'))
        self.goals.append(Rect(int(gx)+xp,int(gy)+yp,100,100))


    def clear_everything(self):
        image = None
        bashers =[]
        bouncers = []
        lives = []
        goals = []

        selecteditem = None

    def save_to_file(self,filepath,xpadding=0,ypadding=0):
        """
            Save the current datacontainer to a specified file in the expected
            format.

            The format is simply a .text configuration file with various
            sections
        """
        if len(self.sticks)!=1: return False, "Need a start Stick Position"
        if len(self.goals)!=1:  return False, "Need a GOAL Position"
        if not self.get_pykurindir(): return False, "There is no base pykurin directory set"

        f = open(filepath, 'w')
        f.write("[options]\n");
        f.write("name:"+self.title+"\n")

        colimgtuple = self.collision_filename.rpartition('levels')
        imgtuple = self.img_filename.rpartition('levels')
        colimg = colimgtuple[1]+colimgtuple[2]
        img = imgtuple[1]+imgtuple[2]
        bg = "backgrounds/"+self.background_filename.rpartition("/")[-1]
        f.write("collision:"+colimg+"\n")
        f.write("background:"+img+"\n")
        f.write("background2:"+bg+"\n")

        stickx = self.sticks[0][0] -xpadding
        sticky = self.sticks[0][1] -ypadding
        print stickx, sticky
        f.write("startx:"+str(stickx)+"\n")
        f.write("starty:"+str(sticky)+"\n")
        goalx = self.goals[0][0] -xpadding
        goaly = self.goals[0][1] -ypadding
        f.write("endx:"+str(goalx)+"\n")
        f.write("endy:"+str(goaly)+"\n")
        f.write("stick:sticks/stick.png\n") #default value at the moment

        #How to generate a UUID from python easily?
        if self.uuid == None:
            self.generate_uuid()
        f.write("uuid:"+str(self.uuid)+"\n")

        f.write("[bouncers]\n")
        for b in self.bouncers:
            bx = b[0] -xpadding
            by = b[1] -ypadding
            f.write(str(bx)+":"+str(by)+"\n")

        f.write("[recovers]\n")
        for b in self.lives:
            bx = b[0] -xpadding
            by = b[1] -ypadding
            f.write(str(bx)+":"+str(by)+"\n")

        f.write("[bashers]\n")

        for i,b in enumerate(self.bashers):
            #FORMAT: 490,200:490,350;1
            be = self.bashers_end[i]

            bx = b.center[0] -xpadding
            by = b.center[1] -ypadding
            bex = be.center[0] -xpadding
            bey = be.center[1] -ypadding

            f.write(str(bx)+","+str(by)+":"+str(bex)+","+str(bey)+";1\n")
        f.write("[flies]\n")
        f.close()

        return True,""

class LevelPackContainer:
    def __init__(self, name=None, dirname=None, icon=None, levels2open=None, pykurindir=None,
                 file=None):
        self.base_pykurin_directory = pykurindir

        if file:
            self.load(file)
            return

        self.name        = name

        #Contains
        self.dirname     = dirname
        self.icon        = icon
        self.levels2open = levels2open

    #Getters
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_dirname(self):
        return self.dirname

    def set_dirname(self, dname):
        if not dname.isalnum():
            return False, "Directory should be only letters and numbers"
        self.dirname = dname
        return True

    def get_icon(self):
        return self.icon

    def set_icon(self, icon):
        self.icon = icon

    def get_levels2open(self):
        return self.levels2open

    def set_levels2open(self, num):
        self.levels2open = num

    def get_pykurindir(self):
        return self.base_pykurin_directory

    def set_pykurindir(self, newdir):
        self.base_pykurin_directory = newdir

    def directoryExists(self):
        return os.path.isdir(os.path.join(self.get_pykurindir(), "levels", self.dirname))

    #SAVE
    def save(self, filepath):
        """ Save the file directly, not checking where is it being saved,
            or if it makes sense in the pykurin executable
        """

        f = open(filepath, 'w')
        f.write("[options]\n");

        f.write("name:"+str(self.name)+"\n")
        f.write("basedir:"+"levels"+"/"+str(self.dirname)+"\n")
        f.write("icon:"+str(self.icon)+"\n")
        f.write("levels2open:"+str(self.levels2open)+"\n")

    def load(self, filepath):

        parser = SafeConfigParser()
        parser.read(filepath)

        self.name        = str(parser.get('options','name'))
        self.icon        = str(parser.get('options','icon'))
        self.levels2open = int(parser.get('options','levels2open'))

        #Get just the basedirname, not the partial path (levels)
        bdir = str(parser.get('options','basedir'))
        self.dirname = bdir.rstrip("/").rpartition("/")[-1]

class LevelPackList:
    """ A LevelPackList of the Levels currently defined in the pykurin directory.
        Used to maintain the packs and all under them.
    """
    def __init__(self, pykurinpath = None):
        self.lpackfiles  = []
        self.lpacks      = []
        self.pykurinpath = pykurinpath

        self.lpackdelete = []

        if not pykurinpath:
            return None

        lpacksdir = os.path.abspath(os.path.join(pykurinpath,"levelpacks"))
        for lpfile in os.listdir(lpacksdir):
            name, ext = os.path.splitext(lpfile)
            if ext != ".lvlpack":continue

            self.lpackfiles.append(lpfile)

        self.lpackfiles.sort()
        for lpfile in self.lpackfiles:
            fpath = os.path.join(lpacksdir, lpfile)
            self.lpacks.append(LevelPackContainer(file=fpath,
                                                  pykurindir=self.pykurinpath))

    def get_pykurindir(self):
        return self.pykurinpath

    def sync(self):
        """ Sync the packs to the levelpacks directory. Delete the packs marked
            for delete.

            Returns True and a Log of what files changed
        """
        errlog = []

        lpacksdir = os.path.abspath(os.path.join(self.pykurinpath,"levelpacks"))
        levelsdir = os.path.abspath(os.path.join(self.pykurinpath,"levels"))

        for idx,lp in enumerate(self.lpacks):
            try:
                fname = os.path.abspath(os.path.join(lpacksdir, self.lpackfiles[idx]))
                dname = os.path.abspath(os.path.join(lpacksdir, self.lpackfiles[idx]))
                lp.save(fname)
                errlog.append("SAVED: %s"%fname)
                if not lp.directoryExists():
                    newdir = os.path.abspath(os.path.join(levelsdir, lp.get_dirname()))
                    os.mkdir(newdir)
                    errlog.append("CREATED: %s"%newdir)
            except Exception as e:
                errlog.append("ERROR creating: %s"%e)
                continue

        for fname in self.lpackdelete:
            try:
                fname = os.path.abspath(os.path.join(lpacksdir, fname))
                os.unlink(fname)
                errlog.append("DELETED: %s"%fname)
            except Exception as e:
                errlog.append("ERROR deleting: %s"%e)
                continue

        return True, errlog

    def addPack(self, filename=None, name=None, dirname=None,
                      icon=None, levels2open=0):
        """
            Creates a new LevelPack, and returns a pointer to that new
            instance
        """

        if not filename:
            filename = "%s-levelpack.lvlpack"%(len(self.lpackfiles)+1)

        if not name:
            name    = "levelpack-%s"%(len(self.lpackfiles)+1)

        if not dirname:
            dirname = "levelpack-%s"%(len(self.lpackfiles)+1)

        ncont = LevelPackContainer(name = name, dirname=dirname, icon=icon,
                                  levels2open=levels2open,
                                  pykurindir=self.get_pykurindir())

        self.lpackfiles.append(filename)
        self.lpacks.append(ncont)
        pack = zip(self.lpackfiles, self.lpacks)
        pack.sort()
        self.lpackfiles = [f for f,p in pack]
        self.lpacks     = [p for f,p in pack]

        return ncont

    def removePackIdx(self, index):
        """ Remove pack from list. Marked for removal on sync"""
        self.lpackdelete.append(self.lpackfiles[index])
        del self.lpackfiles[index]
        del self.lpacks[index]

        return True

    def removePack(self, pack):
        """ Remove pack from list. Marked for removal on sync"""
        try:
            index = self.lpacks.index(pack)
        except:
            return False

        self.lpackdelete.append(self.lpackfiles[index])
        del self.lpackfiles[index]
        del self.lpacks[index]

        return True

    def getPackByName(self, name):
        pack = None

        names = [l.get_name() for l in self.lpacks]
        try:
            nameindex = names.index(name)
            return self.lpacks[nameindex]
        except ValueError as ve:
            return None

    def get_packs(self):
        """ Return a list with filename,LevelPackContainer"""
        return zip(self.lpackfiles, self.lpacks)
