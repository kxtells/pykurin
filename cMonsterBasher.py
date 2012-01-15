import cMonster
import pygame
from cAnimSprite import cAnimSprite
import functions as BF

class cMonsterBasher(cMonster.cMonster):
	movx = 0
	movy = 0
	speed = 1

	def __init__(self,x,y,ex,ey,speed):
		cMonster.cMonster.__init__(self,x,y)
		self.image      = pygame.image.load("sprites/basher_col.png").convert_alpha()
		self.baseImage  = pygame.image.load("sprites/basher_col.png").convert_alpha()
		self.rect	= self.image.get_rect().move(x,y)
		self.mask       = pygame.mask.from_surface(self.image);
		
		anim_images     = BF.load_and_slice_sprite(64,64,'basher_nanim.png');
		col_anim_images = BF.load_and_slice_sprite(64,64,'basher_colanim.png');
                
		self.anim     	= cAnimSprite(anim_images,5)
		self.col_anim  	= cAnimSprite(col_anim_images,5)
		self.anim.rect  = self.rect
		self.col_anim.rect  = self.rect

		#Status sets
		self.col_anim.draw = False

		#
		self.startx = x
		self.starty = y
		self.endx = ex
		self.endy = ey
		self.going_to_end = True
		self.speed = speed

	#Function to call on logic update
	def logic_update(self):
		x = self.rect.x
		y = self.rect.y


		if self.startx == self.endx:
			self.movx = 0
		else:
			self.update_x_movement()

		if self.starty == self.endy:
			self.movy = 0
		else:
			self.update_y_movement()

		self.rect = self.rect.move(self.movx,self.movy)
		self.check_and_set_direction()

	def check_and_set_direction(self):
		x = self.rect.x
		y = self.rect.y

		#if (x < xmin and x < xmax) or (y > ymin and y > ymax):
		#	self.flip_direction()
		
		if self.going_to_end:
			if (x == self.endx + self.speed/2 and y == self.endy + self.speed/2) \
			or (x == self.endx + self.speed/2 and y == self.endy - self.speed/2) \
			or (x == self.endx - self.speed/2 and y == self.endy + self.speed/2) \
			or (x == self.endx - self.speed/2 and y == self.endy - self.speed/2):
				self.going_to_end = False
		else:
			if (x == self.startx + self.speed/2 and y == self.starty + self.speed/2) \
			or (x == self.startx + self.speed/2 and y == self.starty - self.speed/2) \
			or (x == self.startx - self.speed/2 and y == self.starty + self.speed/2) \
			or (x == self.startx - self.speed/2 and y == self.starty - self.speed/2): 
				self.going_to_end = True
	
	def flip_direction(self):
		if self.going_to_end: self.going_to_end = False
		else: self.going_to_end = True


	def update_x_movement(self):
		x = self.rect.x
		y = self.rect.y
		if self.going_to_end:
			if self.x < self.endx:
				self.movx = self.speed
			else:
				self.movx = -self.speed
		else:
			if self.x < self.startx:
				self.movx = self.speed
			else:
				self.movx = -self.speed

	def update_y_movement(self):
		x = self.rect.x
		y = self.rect.y
		if self.going_to_end:
			if y < self.endy:
				self.movy = self.speed
			else:
				self.movy = -self.speed
		else:
			if y < self.starty:
				self.movy = self.speed
			else:
				self.movy = -self.speed
