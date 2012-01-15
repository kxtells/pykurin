import cMonster
import pygame
from cAnimSprite import cAnimSprite
import functions as BF
import random

class cMonsterFlie(cMonster.cMonster):

	def __init__(self,x,y):
		cMonster.cMonster.__init__(self,x,y)
		self.image      = pygame.image.load("sprites/flie_col.png").convert_alpha()
		self.rect	= self.image.get_rect().move(x,y)
		self.mask       = pygame.mask.from_surface(self.image);
		
		anim_images     = BF.load_and_slice_sprite(32,32,'flie_anim.png');
		col_anim_images = BF.load_and_slice_sprite(32,32,'flie_anim_death.png');
                
		self.anim     	= cAnimSprite(anim_images,30)
		self.col_anim  	= cAnimSprite(col_anim_images,10)
		self.anim.rect  = self.rect
		self.col_anim.rect  = self.rect

		#Status sets
		self.col_anim.draw = False
		self.delete_on_colision = True

		#
		self.movx = 1
		self.movy = 1
	
	#Function to call on logic update
	def logic_update(self):
		self.rect = self.rect.move(self.movx,self.movy)

	def onWallCollision(self):
		if self.movx<0: cmx=+1
		else: cmx=-1

		if self.movy<0: cmy=1
		else: cmy=-1

		self.movx = random.uniform(-2,2)*cmx	
		self.movy = random.uniform(-2,2)*cmy	


	def onCollision(self,stick,status):
		cMonster.cMonster.onCollision(self,stick,status)
		#status.level.monsters.remove(self)
