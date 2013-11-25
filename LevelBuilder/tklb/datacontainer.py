from pygame import Rect
from pygame import image
from ConfigParser import SafeConfigParser
import uuid

from PIL import Image, ImageTk

class datacontainer:
    #
    # basher = 0
    # bouncer = 1
    # lives = 2
    # goals = 3
    # sticks = 4
    #
    #
    #

    BASHER      = 0
    BOUNCER     = 1
    LIVES       = 2
    GOALS       = 3
    STICKS      = 4
    BASHER_END  = 5

    selecteditem = None


    #File Metadata
    colimg_filename = None
    img_filename = None
    background_filename = None
    title = None
    uuid = None

    #working data
    last_error = None

    def __init__(self):
        """Loads all the needed common images"""
        self.__load_images()

        self.base_pykurin_directory = None
        self.current_level_filename = None
        self.image = None
        self.bgimage = None
        self.bashers = []
        self.bouncers = []
        self.lives = []
        self.goals = []
        self.sticks = []
        self.bashers_end = []

        #References to everything
        self.items = [self.bashers, self.bouncers, self.lives, self.goals, self.sticks, self.bashers_end]

        #LEGACY
        self.items_pack = [self.bashers,self.bouncers,self.lives,self.goals,self.sticks,self.bashers_end]

    def __load_images(self):
        """Loads the basic set of icons"""
        images = {}
        timage = Image.open("icons/basher.png")
        images["basher"] = ImageTk.PhotoImage(timage)

        timage = Image.open("icons/basher_goto_icon.png")
        images["basher_goto"] = ImageTk.PhotoImage(timage)

        timage = Image.open("icons/bouncer.png")
        images["bouncer"] = ImageTk.PhotoImage(timage)

        timage = Image.open("icons/goalimage.png")
        images["goal"] = ImageTk.PhotoImage(timage)

        timage = Image.open("icons/lives.png")
        images["live"] = ImageTk.PhotoImage(timage)

        timage = Image.open("icons/stick.png")
        images["stick"] = ImageTk.PhotoImage(timage)

        self.images = images

    def set_base_dir(self,path):
        self.base_pykurin_directory = path

    def get_base_dir(self):
        return self.base_pykurin_directory

    def set_image(self,imagepath):
        image = Image.open(imagepath)
        self.image = ImageTk.PhotoImage(image)
        self.img_filename = imagepath

    def set_bg_image(self, imagepath):
        image = Image.open(imagepath)
        self.bgimage= ImageTk.PhotoImage(image)
        self.background_filename = imagepath

    def set_current_level_filename(self,text):
        self.current_level_filename = text

    def get_current_level_filename(self):
        return self.current_level_filename

    def set_last_error(self,text):
        self.last_error = text

    def get_last_error(self):
        if last_error==None:
            return "OK"
        else:
            return self.last_error

    def get_image(self):
        return self.image

    def get_bgimage(self):
        return self.bgimage

    def get_title(self):
        return self.title

    def get_basepath(self):
        return self.base_pykurin_directory

    def set_title(self,text):
        self.title = text

    def set_col_image(self,imagepath):
        self.colimg_filename = imagepath

    def set_uuid(self,uuid):
        self.uuid = uuid

    def generate_uuid(self):
        self.uuid = uuid.uuid4()

    #
    # Image Getters
    #
    def get_basher_image(self):
        return self.images["basher"]

    def get_basher_goto_image(self):
        return self.images["basher_goto"]

    def get_bouncer_image(self):
        return self.images["bouncer"]

    def get_live_image(self):
        return self.images["live"]

    def get_stick_image(self):
        return self.images["stick"]

    def get_goal_image(self):
        return self.images["goal"]

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
        return self.colimg_filename != None

    def isGoalDefined(self):
        return len(self.goals) > 0

    def isStartDefined(self):
        return len(self.sticks) > 0

    def isImageDefined(self):
        return self.image !=None

    def isTitleDefined(self):
        return self.title !=None

    def isSaveable(self):
        """
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

    #
    #
    # Load Parser from file
    # Multiple functions to do so
    #
    #
    def load_from_file(self,full_path,xpadding=0,ypadding=0):
        #clear_everything()
        parser = SafeConfigParser()
        parser.read(full_path)

        #print full_path
        imagefile = parser.get('options','background')
        self.img_filename = imagefile
        colfilename = parser.get('options','collision')
        self.colimg_filename = colfilename
        bgfilename = parser.get('options','background2')
        self.background_filename = bgfilename
        title = parser.get('options','name')
        self.title = title
        uuid = parser.get('options','uuid')
        self.uuid = uuid

        part = full_path.rpartition('/')
        part2 = imagefile.rpartition('/')

        imagepath =  part[0]+"/"+part2[2]
        bgimagepath = self.base_pykurin_directory+"/"+self.background_filename
        self.set_image(imagepath)
        self.set_bg_image(bgimagepath)


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

    #
    #
    # Save to file
    #
    #
    def save_to_file(self,filepath,xpadding=0,ypadding=0):
        if len(self.sticks)!=1: return False, "Need a start Stick Position"
        if len(self.goals)!=1:  return False, "Need a GOAL Position"
        if not self.base_pykurin_directory: return False, "There is no base pykurin directory set"

        f = open(filepath, 'w')
        f.write("[options]\n");
        f.write("name:"+self.title+"\n")

        colimgtuple = self.colimg_filename.rpartition('levels')
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
