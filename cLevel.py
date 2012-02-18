from ConfigParser import SafeConfigParser
import pygame
from cAnimSprite import cAnimSprite
import functions as BF
import cItemBouncer
import cItemRecoverLives
import cMonsterBasher
import cMonsterFlie
import shelve

class cLevel:
	_MAX_SAVED_RECORDS = 5
	
	def __init__(self,file):
		parser = SafeConfigParser()
		parser.read(file)

		self.name 	= parser.get('options','name')
		self.startx 	= int(parser.get('options','startx'))
		self.starty 	= int(parser.get('options','starty'))
		self.imgcol 	= pygame.image.load(parser.get('options','collision')).convert_alpha();
		self.image 	= pygame.image.load(parser.get('options','background')).convert_alpha();
		self.bg 	= pygame.image.load(parser.get('options','background2')).convert_alpha();
		self.mask       = pygame.mask.from_surface(self.imgcol);
		self.rect	= self.image.get_rect();
		self.stick      = parser.get('options','stick')
		self.uuid	= parser.get('options','uuid')

                #Load the Goal sprite
		goal_images     =  BF.load_and_slice_sprite(100,100,'goal.png');
                self.goal_sprite=  cAnimSprite(goal_images,5)
                gx = int(parser.get('options','endx'))
                gy = int(parser.get('options','endy'))
                self.goal_sprite.move(gx,gy)
                
		#ITEMS LOADING
		bouncers	=  self.retrieve_bouncer_list(parser)
		recovers	=  self.retrieve_recover_list(parser)
		self.items		=  []
		self.items += bouncers
		self.items += recovers


		#MONSTERS LOADING
		bashers = self.retrieve_basher_list(parser)
		flies = self.retrieve_flies_list(parser)
		self.monsters = []
		self.monsters += bashers
		self.monsters += flies

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
	def stick_collides(self,stick):
                """
                        Check if a given stick collides with one of the
                        level walls
                """
		i,j = 0,0
		try:
			tmask = pygame.mask.from_surface(self.imgcol.subsurface(stick.rect))

                	col = stick.mask.overlap(tmask,(0,0))
                
                	if col == None: return False,0,0
                	else: return True,col[0]+stick.rect.x,col[1]+stick.rect.y
		
		except: 
			pass

		return False,i,j

	def stick_in_goal(self,stick):
                """
                    Check if the stick center is within the level goal    
                """
		scx = stick.rect.center[0]
		scy = stick.rect.center[1]
		stick_center_rect = (scx-10,scy-10,10,10)
		return self.goal_sprite.rect.contains(stick_center_rect)
		#return stick.rect.colliderect(self.goal_sprite.rect)

	############################
	#
	# Retrieve specific data
	#
	############################
	def retrieve_bouncer_list(self,parser):
		bouncer_list = []
		try:
			for b in parser.items('bouncers'):
				bx,by = b
				rot = 0
				newbouncer = cItemBouncer.cItemBouncer(int(bx),int(by),rot)
				bouncer_list.append(newbouncer)
		except:
			pass

		return bouncer_list

	def retrieve_recover_list(self,parser):
		recover_list = []
		try:
			for r in parser.items('recovers'):
				rx,ry = r
				newrecover = cItemRecoverLives.cItemRecoverLives(int(rx),int(ry))
				recover_list.append(newrecover)

		except:
			pass
		
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
	
	def save_record(self,username,newtime):
		"""
			Saves the new record into the proper shelve
			loads the records into the class attributes self.records and self.player_record_index
			returns a tuple with the results
		"""
		#data pack
		newdata = (newtime,username)
		
		db = shelve.open("db/"+self.uuid)
		
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
		print user_index
		return dbrecords,user_index

	def load_records(self):
		"""
			Return a tuple (record,name) for a level
		"""
		db = shelve.open("db/"+self.uuid)
		
		dbrecords = []
		#recover data if exists
		if db.has_key("records"):
			dbrecords = db["records"]
	
		self.records = dbrecords

		return dbrecords


