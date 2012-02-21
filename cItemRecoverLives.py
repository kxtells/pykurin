import cMonster
import pygame
from cAnimSprite import cAnimSprite
import functions as BF

class cItemRecoverLives(cMonster.cMonster):
	BSPRITEFAC = 3 #this is a little dirty. References the value assigned in cAnimSpriteFactory
	def __init__(self,x,y):
		cMonster.cMonster.__init__(self,x,y,0)
        #Get the base circle because i
		self.image      = pygame.image.load("sprites/circle_col.png").convert_alpha()
		self.baseImage  = pygame.image.load("sprites/circle_col.png").convert_alpha()
		self.rect	    = self.image.get_rect().move(x,y)
		self.mask       = pygame.mask.from_surface(self.image);
		
		anim_images     = BF.load_and_slice_sprite(32,32,'recover_lives_anim.png');
		col_anim_images = BF.load_and_slice_sprite(32,32,'recover_lives_anim.png');
                
		self.anim     	= cAnimSprite(anim_images,10)
		self.col_anim  	= cAnimSprite(col_anim_images,20)
		self.anim.rect  = self.rect
		self.col_anim.rect  = self.rect

		#Status sets
		self.col_anim.draw = False
		#Only Usable once
    		self.delete_on_colision = True

	def onCollision(self,stick,status):
		status.reset_lives()
	
	def isMonster(self):
		return False
