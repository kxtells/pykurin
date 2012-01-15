import cMonster
import pygame
from cAnimSprite import cAnimSprite
import functions as BF

class cMonsterBasher(cMonster.cMonster):

	def __init__(self,x,y,ex,ey):
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
		self.movx = 1
		self.movy = 0
		self.startx = x
		self.starty = y 
		self.endx = ex
		self.endy = ey
		self.going_to_end = True

	#Function to call on logic update
	def logic_update(self):
		x = self.rect.x
		y = self.rect.y


		if self.going_to_end:
			if x < self.endx:
				self.movx = 1
			else:
				self.movx = -1
	
			if y < self.endy:
				self.movy = 1
			else:
				self.movy = -1
		else:
			if x < self.startx:
				self.movx = 1
			else:
				self.movx = -1
	
			if y < self.starty:
				self.movy = 1
			else:
				self.movy = -1

		if self.going_to_end:
			if x >= self.endx and y >= self.endy: 
				self.movx = 0
				self.movy = 0
				self.going_to_end = False
		else:
			if x <= self.startx and y <= self.endy: 
				self.movx = 0
				self.movy = 0
				self.going_to_end = True

		self.rect = self.rect.move(self.movx,self.movy)


