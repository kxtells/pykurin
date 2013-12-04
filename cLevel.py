from ConfigParser import SafeConfigParser
import pygame
from cAnimSprite import cAnimSprite
import functions as BF
import cItemBouncer
import cItemRecoverLives
import cMonsterBasher
import cMonsterFlie
import shelve
import pygame
import pymunk
import os

class cLevel(pygame.sprite.Sprite):
	_MAX_SAVED_RECORDS = 5

	def __init__(self, file, load=True):
		"""Creates an instance of a Level to be run. By default it will load
			everything to be used as the playing level.

			if load is set to false, only the records and metadata is loaded,
			but no image is processed.
		"""
		parser = SafeConfigParser()
		parser.read(file)

		self.name 	= parser.get('options','name')
		self.startx = int(parser.get('options','startx'))
		self.starty = int(parser.get('options','starty'))
		self.stick  = parser.get('options','stick')
		self.uuid	= parser.get('options','uuid')
		self.imgcol = None
		self.image  = None
		self.bg     = None
		self.mask   = None
		self.rect	= None
		self.goal_sprite = None
		self.items  = []
		self.monsters = []

		if load:
			self.imgcol	= pygame.image.load(parser.get('options','collision')).convert_alpha();
			self.image 	= pygame.image.load(parser.get('options','background')).convert_alpha();
			self.bg 	= pygame.image.load(parser.get('options','background2')).convert_alpha();
			self.mask   = pygame.mask.from_surface(self.imgcol);
			self.rect	= self.image.get_rect();

			#Load the Goal sprite
			gx = int(parser.get('options','endx'))
			gy = int(parser.get('options','endy'))
			goal_images     =  BF.load_and_slice_sprite(100,100,'goal.png');
			self.goal_sprite=  cAnimSprite(goal_images,5)
			self.goal_sprite.move(gx + 50,gy + 50) #need the +50 not sure why [TODO]

			#ITEMS LOADING
			bouncers	=  self.retrieve_bouncer_list(file)
			recovers	=  self.retrieve_recover_list(file)
			self.items	=  []
			self.items += bouncers
			self.items += recovers


			#MONSTERS LOADING
			bashers = self.retrieve_basher_list(file)
			#flies = self.retrieve_flies_list(parser)
			flies = []
			self.monsters = []
			self.monsters += bashers
			self.monsters += flies

			#PYMUNK SEGMENT
			self.level_segments = []
			self.generate_pymunk_vectors()

		#
		# Record Storage between status
		# Read the records once and temprary store them here
		# By default empty, only load records when finishing level
		#
		self.records = []
		self.player_record_index = -1


		#Specific status settings
		try:
			self.start_lives = parser.get('options','start_lives')
		except:
			self.start_lives = 3 #cannot include cStatus
			pass


	############################
	#
	# Stick Positioning
	#
	############################
	def stick_in_goal(self,stick):
                """
                    Check if the stick center is within the level goal
                """
		scx,scy = stick.body.position
		stick_center_rect = (scx-10,scy-10,10,10)
		return self.goal_sprite.rect.contains(stick_center_rect)

	############################
	#
	# Retrieve specific data
	#
	############################
	def retrieve_bouncer_list(self,fname):
		""" Get a bouncer list from a .prop file."""
		with open(fname) as f:
			content = f.readlines()

		bouncers = content[content.index('[bouncers]\n')+1:content.index('[recovers]\n')]
		bouncer_list = []
		for dat in bouncers:
			bl	= dat.rstrip("\n").split(":")
			bx	= bl[0]
			by	= bl[1]
			rot = 0
			newbouncer = cItemBouncer.cItemBouncer(int(bx),int(by),rot)
			bouncer_list.append(newbouncer)

		return bouncer_list

	def retrieve_recover_list(self,fname):
		""" Get a bouncer list from a .prop file."""
		with open(fname) as f:
			content = f.readlines()

		bouncers = content[content.index('[recovers]\n')+1:content.index('[bashers]\n')]
		recover_list = []
		for dat in bouncers:
			rl = dat.rstrip("\n").split(":")
			rx = rl[0]
			ry = rl[1]
			newrecover = cItemRecoverLives.cItemRecoverLives(int(rx),int(ry))
			recover_list.append(newrecover)

		return recover_list

	def retrieve_basher_list(self,parser):
		basher_list = []
		try:
			for b in parser.items('bashers'):
				scoord,ecoord = b
				sx = scoord.partition(',')[0]
				sy = scoord.partition(',')[2]
				ex = ecoord.partition(',')[0]
				ey = ecoord.partition(',')[2].partition(';')[0]
				speed = ecoord.partition(',')[2].partition(';')[2]
				newbasher = cMonsterBasher.cMonsterBasher(int(sx),int(sy),int(ex),int(ey),int(speed))
				basher_list.append(newbasher)
		except:
			pass

		return basher_list

	def retrieve_basher_list(self,fname):
		""" Get a bouncer list from a .prop file."""
		with open(fname) as f:
			content = f.readlines()

		bashers = content[content.index('[bashers]\n')+1:content.index('[flies]\n')]
		basher_list = []
		for dat in bashers:
			bash_n_speed = dat.rstrip("\n").split(";")
			bl = bash_n_speed[0].split(":")
			borig = bl[0].split(",")
			bend  = bl[1].split(",")
			speed = int(bash_n_speed[1])
			sx= borig[0]
			sy= borig[1]
			ex = bend[0]
			ey = bend[1]

			newbasher = cMonsterBasher.cMonsterBasher(int(sx),int(sy),int(ex),int(ey),int(speed))
			basher_list.append(newbasher)

		return basher_list

	def retrieve_flies_list(self,parser):
		flies_list = []
		try:
			for b in parser.items('flies'):
				sx,sy = b
				newflie = cMonsterFlie.cMonsterFlie(int(sx),int(sy))
				flies_list.append(newflie)
		except:
			pass

		return flies_list


	############################
	#
	# Interfacing with record files
	#
	############################

	def save_record(self, username, newtime, isperfect):
		"""
			Saves the new record into the proper shelve
			loads the records into the class attributes self.records and self.player_record_index
			returns a tuple with the results
		"""
		#data pack
		newdata = (newtime, username, isperfect)

		db = shelve.open(os.path.join("db", self.uuid))

		dbrecords = []
		#recover data if exists
		if db.has_key("records"):
			dbrecords = db["records"]

		#check if a data drop is needed
		if len(dbrecords) < cLevel._MAX_SAVED_RECORDS:
			dbrecords.append(newdata)
		else:
			dbrecords.sort()
			worsttime = dbrecords[-1][0]
			if newtime < worsttime:
				dbrecords.pop()
				dbrecords.append(newdata)

		dbrecords.sort()

		db["records"] = dbrecords

		user_index = -1
		for i,val in enumerate(dbrecords):
			if dbrecords[i][0] == newtime and dbrecords[i][1] == username:
				user_index = i

		db.close()

		self.records = dbrecords
		self.player_record_index = user_index
		return dbrecords,user_index

	def load_records(self):
		"""
			Return a tuple (record,name) for a level
		"""
		db = shelve.open(os.path.join("db/",self.uuid))

		dbrecords = []
		#recover data if exists
		if db.has_key("records"):
			dbrecords = db["records"]

		self.records = dbrecords

		return dbrecords

	def get_uuid(self):
		return self.uuid


	############################
	#
	# Search objects
	#
	############################
	def get_item_by_shape(self, shape):
		"""Returns a specific item instance by its shape definition"""
		for item in self.items:
			if item.shape == shape:
				return item

		return None

	def get_monster_by_shape(self, shape):
		"""Returns a specific monster instance by its shape definition"""
		for monster in self.monsters:
			if monster.shape == shape:
				return monster

		return None



	############################
	#
	# Pymunk collisions map
	#
	############################

	def generate_pymunk_vectors(self):
		""" This function generates a list of pymunk vectors representing the
			Collisions of the Level. It does so with the following algorithm.

			VERY CRUDE APPROACH, JUST FOR TESTING
			This is a classic edge detection problem, Right now I generate
			a crude list of horizontal and vertical vectors. Create lines
		"""
		mask = self.mask
		w,h = mask.get_size()

		#Two list of start,end values
		#horizontal = [[(0,0),(0,0)] for i in range(h)]
		#vertical   = [[(0,0),(0,0)] for i in range(h)]
		horizontal = []

		inline= False
		start = None
		end   = None
		for r in range(w):
			for c in range(h):
				val = mask.get_at((r,c))
				if inline:
					#We found a line and we are following it
					if val:
						continue
					else:
						#Line finished
						end = (r,c)
						horizontal.append([start,end])
						inline = False
				else:
					#We are searching for a start of a line
					if val:
						start = (r,c)
						inline = True
					else:
						continue

		#Generate the pymunk lines
		self.level_segments = []
		static_body = pymunk.Body()
		for f in horizontal:
			nseg = pymunk.Segment(static_body, f[0], f[1], 0.0)
			nseg.collision_type = 1
			#Segment elasticity, to create bounce... so far no good
			nseg.elasticity = 0.95
			self.level_segments.append(nseg)
