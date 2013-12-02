import pygame
import pymunk

class cPal(pygame.sprite.Sprite):
	"""The 'stick' class.. the player"""
	__MOV_SPEED = 6;
	__ROT_SPEED = 1;
	__BACK_TICKS = 12;
	_JUMP_LENGTH = 5;
	__TURBO_MULTIPLIER = 2;

	def __init__(self,x,y,rot,stickpath="sticks/stick.png"):
		pygame.sprite.Sprite.__init__(self)

		self.image      = pygame.image.load(stickpath).convert_alpha()
		self.baseImage  = pygame.image.load(stickpath).convert_alpha()
		self.mask       = pygame.mask.from_surface(self.image);

		self.rect = self.image.get_rect();

		self.movx = 0;
		self.movy = 0;

		#Rotation Direction
		self.rot = rot;
		self.clockwise = False

		#Backwards move
		self.tbackwards = False
		self.tbackwards_ticks = self.__BACK_TICKS

		self.rect.x,self.rect.y = x,y

		#Movement Flags
		self.fmove = True
		self.turbo = False
		self.path  = []
		self.directions  = []

		#PYMUNK
		#Fixed vecspace for the default stick
		self.mass      		= 10
		self.VecSpace  		= [(-31,-4), (31,-4), (31,4), (-31,4)]
		self.moment    		= pymunk.moment_for_poly(self.mass, self.VecSpace)
		self.body      		= pymunk.Body(self.mass, self.moment)
		self.body.elasticity= 0.95
		self.shape     		= pymunk.Poly(self.body, self.VecSpace)
		self.body.position  = (self.rect.x + self.rect.width/2, self.rect.y + self.rect.width/2)
		self.body.angle 	= self.rot

		self.shape.collision_type = 0 #stick collision type

    #Loads a new stick Image
	def load_stick_image(self,imagepath):
		self.image      = pygame.image.load(imagepath).convert_alpha()
		self.baseImage  = pygame.image.load(imagepath).convert_alpha()
		self.mask       = pygame.mask.from_surface(self.image);
		self.rect = self.image.get_rect();


	#Rotate function. Called continuously
	def rotate(self,amount=__ROT_SPEED):
		"""
			rotate an image while keeping its center in the specified
			amount attribute in degrees.

			self.tbackwards defines a temporal inverse rotation
		"""
		#if self.clockwise: self.clockwise_rotation(amount)
		#else: self.counterclockwise_rotation(amount)

		#self.rect = self.image.get_rect(center=self.rect.center)
		#self.mask = pygame.mask.from_surface(self.image)
		##ROTATING ANGLE... TODO
		if self.clockwise:
			self.body.angle += float(amount)/50
		else:
			self.body.angle += float(-amount)/50

	def clockwise_rotation(self,amount):
		if self.tbackwards:            	#Check if temporal backwards rotation is set
			self.rot -= amount + 2  	#When rotating back has to be faster
			self.tbackwards_ticks -= 1
		else:
			self.rot -= amount

		if self.tbackwards_ticks == 0:
			self.tbackwards = False
			self.tbackwards_ticks = self.__BACK_TICKS
			self.flip_rotation()

		if self.rot <= 0: self.rot = 360;

		self.image = pygame.transform.rotate(self.baseImage, self.rot)

	def counterclockwise_rotation(self,amount):
		if self.tbackwards:             	#Check if temporal backwards rotation is set
			self.rot += amount + 2  	#When rotating back has to be faster
			self.tbackwards_ticks -= 1
		else:
			self.rot += amount

		if self.tbackwards_ticks == 0:
			self.tbackwards = False
			self.tbackwards_ticks = self.__BACK_TICKS
			self.flip_rotation()

		if self.rot >= 360: self.rot = 0;

		self.image = pygame.transform.rotate(self.baseImage, self.rot)

	#
	# Moving Functions
	#
	def move_left(self):
		if self.fmove: self.movx -= cPal.__MOV_SPEED;
	def move_right(self):
		if self.fmove: self.movx += cPal.__MOV_SPEED;
	def move_up(self):
		if self.fmove: self.movy -= cPal.__MOV_SPEED;
	def move_down(self):
		if self.fmove: self.movy += cPal.__MOV_SPEED;

	def movement_record(self):
		self.path.append(self.rect)

	def direction_record(self):
		self.directions.append((self.movx*cPal.__TURBO_MULTIPLIER,self.movy*cPal.__TURBO_MULTIPLIER))

	def previous_direction(self, pused=10):
		if len(self.path) < pused:
			return 0,0
		else:
			maximum = pused*self.__MOV_SPEED*self.__TURBO_MULTIPLIER
			lastxy  = [(movx,movy) for movx,movy in self.directions[-pused:]]
			lastxy.reverse()

			cx = lastxy[0][0]
			cy = lastxy[0][1]
			cumx = 0
			cumy = 0
			for x,y in lastxy:
				cumx += x
				cumy += y

			cumx = (cumx / maximum) * 10
			cumy = (cumy / maximum) * 10
			return cumx, cumy

	def previous_movement(self, pused=5):
		if len(self.path) < pused:
			return 0,0
		else:
			lastxy = [(rect.x,rect.y) for rect in self.path[-pused:]]
			lastxy.reverse()
			cx = lastxy[0][0]
			cy = lastxy[0][1]
			cumx = 0
			cumy = 0
			for x,y in lastxy:
				cumx += cx - x
				cumy += cy - y
				cx    = x
				cy    = y

			return cumx, cumy

	def movement(self):
		"""Move the Stick Rectangle"""
		if self.fmove:
			if self.turbo:
				movx = self.movx*cPal.__TURBO_MULTIPLIER
				movy = self.movy*cPal.__TURBO_MULTIPLIER
				#self.rect = self.rect.move(movx,movy);
				#Move stick
				#self.body.position += (movx, movy)

				#With Impulses, body does not stop
				self.body.apply_impulse((movx/2, movy/2),(0,0))

				#With forces. Not working as I would like
				#self.body.apply_force((self.movx/20, self.movy/20),(0,0))
			else:
				#self.rect = self.rect.move(self.movx,self.movy);
				#Move stick
				#self.body.position += (self.movx, self.movy)

				#With Impulses, body does not stop
				self.body.apply_impulse((self.movx/2, self.movy/2),(0,0))

				#With forces. Not working as I would like
				#self.body.apply_force((movx/20, movy/20),(0,0))
				#print pymunk.Vec2d(self.movx,self.movy)

		self.movement_record()
		self.direction_record()

	def enable_disable_movement(self):
		"""sets the movement flag"""
		if self.fmove: self.fmove = False
		else: self.fmove = True

	#
	# Colision Back Rotation and jump back
	#
	def flip_rotation_tmp(self,nframes=__BACK_TICKS):
		"""
			Flips the rotation temporally for a specified number
			of frames
		"""
		if self.clockwise: self.clockwise = False
		else: self.clockwise = True

		if self.tbackwards: self.tbackwards = False
		else: self.tbackwards = True


		self.tbackwards_ticks = nframes
		#self.tbackwards = True

	def flip_rotation(self):
		"""
			Flips the rotation
		"""
		if self.clockwise: self.clockwise = False
		else: self.clockwise = True

	def rotate_back(self):
		self.rotate(amount=-10)

	#
	# @TODO: This function NEEDS REVISION.. Seems that some cases don't work properly
	def jump_back(self, cx=0, cy=0, multiplier=1):
		dx,dy = self.previous_direction()
		if dx==0 and dy==0:
			self.jump_back_static(cx, cy, multiplier)
		else:
			self.rect = self.rect.move(-dx*multiplier,-dy*multiplier);

	def jump_back_static(self,cx=0,cy=0,multiplier=1):
		"""
			The stick Jumps Back to avoid further colisions
			cx and xy are the MAP points of collision.

			The jump back is decided by quadrants of stick collision
			To decide which direction to jump
			Q1|Q3
			------
			Q2|Q4

		"""
		#JUMP directions
		#jx = 0
		#jy = 0
		jx = cPal._JUMP_LENGTH * -(self.movx)
		jy = cPal._JUMP_LENGTH * -(self.movy)
		#Check colision position of stick (which quadrant)
		sx = cx - self.rect.x
		sy = cy - self.rect.y
		sxc = self.rect.width/2
		syc = self.rect.height/2
		ax = abs(sx - sxc)
		ay = abs(sy - syc)
		#print str(ax)+".."+str(ay)

		if sx < sxc and sy < syc :     #Q1 Top Left
			jx += cPal._JUMP_LENGTH
			jy += cPal._JUMP_LENGTH
		elif sx < sxc and sy > syc:     #Q2 Bottom Left
			jx += cPal._JUMP_LENGTH
			jy += -cPal._JUMP_LENGTH
		elif sx > sxc and sy < syc:     #Q3 Top Right
			jx += -cPal._JUMP_LENGTH
			jy += cPal._JUMP_LENGTH
		else:                           #Q4 Bottom Right
			jx += -cPal._JUMP_LENGTH
			jy += -cPal._JUMP_LENGTH

		#New easy jumpbacj
		# @TODO: If you move counter direction when bashing a wall you can get past it
		# The idea is that with the time penalty, even with that situation there's no
		# clear wining
		#



		self.rect = self.rect.move(jx*multiplier,jy*multiplier);

	#Movement to reproduce when death
	def fancy_rotation_death(self,amount,scale):
		self.rot += amount

		if self.rot >= 360: self.rot = 0;

		self.image = pygame.transform.rotozoom(self.baseImage, self.rot,scale)
		self.rect = self.image.get_rect(center=self.rect.center)

	def move_towards_position(self,ox,oy):
		"""
			ox,oy is the position to reach
		"""

		if (self.rect.x <= ox+5 and self.rect.x >= ox-5) \
		   and (self.rect.y <= oy+5 and self.rect.y >= oy-5):
			return True

		if self.rect.x > ox:
			self.movx = -1
		else:
			self.movx = 1

		if self.rect.y > oy:
			self.movy = -1
		else:
			self.movy = 1


		return False

	def turbo_on(self):
		self.turbo = True

	def turbo_off(self):
		self.turbo = False

	def collides(self,monster):
		"""
			Checks if the stick collides with a specific monster
		"""
		if self.rect.colliderect(monster.rect):
			#Here need to pix perfect collision

			col = pygame.sprite.collide_mask(self,monster)
			if col == None: return False,0,0
			else:
				return True,col[0]+self.rect.x,col[1]+self.rect.y

		else: return False,0,0
