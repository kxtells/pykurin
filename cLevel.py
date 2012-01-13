from ConfigParser import SafeConfigParser
import pygame
from cAnimSprite import cAnimSprite
import functions as BF
import cBouncer
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
                self.goal_sprite     =  cAnimSprite(goal_images,5)
                gx = int(parser.get('options','endx'))
                gy = int(parser.get('options','endy'))
                self.goal_sprite.move(gx,gy)
                
		#MONSTERS LOADING
		self.bouncers	=  self.retrieve_bouncer_list(parser)

		#
		# Record Storage between status
		# Read the records once and temprary store them here
		# By default empty, only load records when finishing level
		#
		self.records = []
		self.player_record_index = -1

	def stick_collides(self,stick):
                """
                        Check if a given stick collides with one of the
                        level walls
                """
                tmask = pygame.mask.from_surface(self.imgcol.subsurface(stick.rect))

                col = stick.mask.overlap(tmask,(0,0))
                
                if col == None: return 0,0,0
                else: return 1,col[0]+stick.rect.x,col[1]+stick.rect.y
		
		return 0,i,j

	def stick_in_goal(self,stick):
                """
                    Check if the stick collides with the level goal    
                """
                return stick.rect.colliderect(self.goal_sprite.rect)

	def retrieve_bouncer_list(self,parser):
		bouncer_list = []
		for b in parser.items('bouncers'):
			bx,by = b
			rot = 0
			newbouncer = cBouncer.cBouncer(int(bx),int(by),rot)
			bouncer_list.append(newbouncer)

		return bouncer_list

	
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
