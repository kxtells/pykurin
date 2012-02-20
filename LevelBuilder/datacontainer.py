from pygame import Rect
from pygame import image
from ConfigParser import SafeConfigParser
import uuid

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
	image = None
	bashers = []
	bouncers = []
	lives = []
	goals = []
	sticks = []
	bashers_end = []

	items_pack = [bashers,bouncers,lives,goals,sticks,bashers_end]
	selecteditem = None

	colimg_filename = None
	img_filename = None
	background_filename = None
	title = "NO TITLE"
	uuid = None
	
	def set_image(self,imagepath):
		self.image = image.load(imagepath)
		
		#store only the last part
		#part = imagepath.rpartition('/')
		#self.img_filename = "levels/"+part[-1]
		self.img_filename = imagepath

	def get_image(self,img):
		return self.image

	def get_title(self):
		return self.title

	def set_title(self,text):
		self.title = text

	def set_col_image(self,imagepath):
		self.colimg_filename = imagepath

	def set_bg_image(self,imagepath):
		self.background_filename = imagepath

	def set_uuid(self,uuid):
		self.uuid = uuid
	
	def generate_uuid(self):
		self.uuid = uuid.uuid4()

	def add_item(self,ident,mx,my):
		if ident==0:
			return True
		elif ident == 1: #basher
			print "addbasher"
			self.bashers.append(Rect(mx-32,my-32,64,64))
			self.bashers_end.append(Rect(mx-8 -64,my-8 -64,16,16)) #where basher moves
		elif ident == 2: #bouncer
			print "addbouncer"
			self.bouncers.append(Rect(mx-16,my-16,32,32))
		elif ident == 3: #lives
			print "addlives"
			self.lives.append(Rect(mx-16,my-16,32,32))
		elif ident == 4: #lives
			print "addgoal"
			if len(self.goals)<1: #only one goal ma friend
				self.goals.append(Rect(mx-50,my-50,100,100))
		elif ident == 5: #lives
			print "addstart"
			if len(self.sticks)<1: #only one goal ma friend
				self.sticks.append(Rect(mx-32,my-32,64,64))							
	
	def move_current_item(self,mx,my):
		if self.selecteditem == None: return False
		print self.selecteditem
		ident = self.selecteditem[0]
		obj = self.selecteditem[1]
		
		if ident == 0: #basher
			self.items_pack[ident][obj] = Rect(mx-32,my-32,64,64)
		elif ident == 1 or ident == 2: #bouncer and lives
			self.items_pack[ident][obj] = Rect(mx-16,my-16,32,32)
		elif ident==3:
			self.items_pack[ident][obj] = Rect(mx-50,my-50,100,100)
		elif ident==4:
			self.items_pack[ident][obj] = Rect(mx-32,my-32,64,64)
		elif ident==5:
			self.items_pack[ident][obj] = Rect(mx-8,my-8,16,16)							

	def touched_item(self,mx,my):
		touched = None

		for i,items_arr in enumerate(self.items_pack):
			for j,item_rect in enumerate(items_arr):
				if item_rect.contains((mx-2,my-2,4,4)):
					touched = i,j						
		

		self.selecteditem = touched

		return self.selecteditem!=None
	
	def touched_selected_item(self,mx,my):
		if self.selecteditem==None: return
		ident = self.selecteditem[0]
		obj = self.selecteditem[1]

		return self.items_pack[ident][obj].contains((mx-2,my-2,4,4))

	def unselect_item(self):
		self.selecteditem = None

	def get_selected_square(self):
		if self.selecteditem == None: 
			return None
		else:
			st = self.selecteditem[0]
			si = self.selecteditem[1]
			return self.items_pack[st][si]
	
	def delete_selected_item(self):
		if self.selecteditem != None:
			st = self.selecteditem[0]
			si = self.selecteditem[1]
			self.items_pack[st].pop(si)

			#basher is a double item, so we have to delete that
			if st == 0: #it's a basher
				self.items_pack[5].pop(si)
			elif st == 5: #it's the end of a basher
				self.items_pack[5].pop(si)

			self.selecteditem = None


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

	
	#
	#
	# Load Parser from file
	# Multiple functions to do so
	#
	#
	def load_from_file(self,full_path,xpadding=0,ypadding=64):
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

		#print imagefile
		part = full_path.rpartition('/')
		part2 = imagefile.rpartition('/')
		imagepath =  part[0]+"/"+part2[2]
		self.set_image(imagepath)

		#Fill the things
		self.retrieve_bouncer_list(parser,xpadding,ypadding)
		self.retrieve_lives_list(parser,xpadding,ypadding)
		self.retrieve_end(parser,xpadding,ypadding)
		self.retrieve_start(parser,xpadding,ypadding)
		self.retrieve_bashers_list(parser,xpadding,ypadding)
	
	def retrieve_bashers_list(self,parser,xp,yp):

		del self.bashers[:]
		del self.bashers_end[:]
		print "retrieving"
				
		try:
			for b in parser.items('bashers'):
				#FORMAT: 490,200:490,350;1
				basher, basher_end_tmp = b
				basher_end = basher_end_tmp.partition(";")[0]
				bx,t,by = basher.partition(",")
				bex,t,bey = basher_end.partition(",")

				self.bashers.append(Rect(int(bx)-32+xp,int(by)-32+yp,64,64))
				self.bashers_end.append(Rect(int(bex)-8+xp,int(bey)-8+yp,16,16))	
		except:
			pass

	def retrieve_bouncer_list(self,parser,xp,yp):
		del self.bouncers[:]
		try:
			for b in parser.items('bouncers'):
				bx,by = b
				self.bouncers.append(Rect(int(bx)-16+xp,int(by)-16+yp,32,32))
		except:
			pass
	
	def retrieve_lives_list(self,parser,xp,yp):
		del self.lives[:]
		try:
			for b in parser.items('recovers'):
				bx,by = b
				self.lives.append(Rect(int(bx)-16+xp,int(by)-16+yp,32,32))
		except:
			pass
	
	def retrieve_start(self,parser,xp,yp):
		del self.sticks[:]
		gx = int(parser.get('options','startx'))
		gy = int(parser.get('options','starty'))		
		self.sticks.append(Rect(int(gx)-32+xp,int(gy)-32+yp,64,64))
	
	def retrieve_end(self,parser,xp,yp):
		del self.goals[:]
		gx = int(parser.get('options','endx'))
		gy = int(parser.get('options','endy'))		
		self.goals.append(Rect(int(gx)-50+xp,int(gy)-50+yp,100,100))

	
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
	def save_to_file(self,filepath,xpadding=0,ypadding=64):
		if len(self.sticks)!=1: return False,"Need a start Stick Position"
		if len(self.goals)!=1: return False,"Need a GOAL Position"

		f = open(filepath, 'w')
		f.write("[options]\n");
		f.write("name:"+self.title+"\n")
		
		colimg = "levels/"+self.colimg_filename.rpartition("/")[-1]
		img = "levels/"+self.img_filename.rpartition("/")[-1]
		bg = "backgrounds/"+self.background_filename.rpartition("/")[-1]
		f.write("collision:"+colimg+"\n")
		f.write("background:"+img+"\n")
		f.write("background2:"+bg+"\n")

		stickx = self.sticks[0][0] +32 -xpadding
		sticky = self.sticks[0][1] +32 -ypadding
		f.write("startx:"+str(stickx)+"\n")
		f.write("starty:"+str(sticky)+"\n")
		goalx = self.goals[0][0] +50 -xpadding
		goaly = self.goals[0][1] +50 -ypadding
		f.write("endx:"+str(goalx)+"\n")
		f.write("endy:"+str(goaly)+"\n")
		f.write("stick:sticks/stick.png\n") #default value at the moment

		#How to generate a UUID from python easily?
		if self.uuid == None:
			self.generated_uuid()
		f.write("uuid:"+str(self.uuid)+"\n")

		f.write("[bouncers]\n")
		for b in self.bouncers:
			bx = b[0] +16 -xpadding
			by = b[1] +16 -ypadding
			f.write(str(bx)+":"+str(by)+"\n")

		f.write("[recovers]\n")
		for b in self.lives:
			bx = b[0] +16 -xpadding
			by = b[1] +16 -ypadding
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