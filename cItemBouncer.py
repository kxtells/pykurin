import cMonster
import pygame
from cAnimSprite import cAnimSprite
import functions as BF

class cItemBouncer(cMonster.cMonster):
	BSPRITEFAC = 1 #this is a little dirty. References the value assigned in cAnimSpriteFactory
	def __init__(self,x,y,rot):
		cMonster.cMonster.__init__(self,x,y,rot)
		self.image      = pygame.image.load("sprites/bouncer.png").convert_alpha()
		self.rect	= self.image.get_rect().move(x,y)
		self.mask       = pygame.mask.from_surface(self.image);
		
		anim_images     = BF.load_and_slice_sprite(32,32,'bouncer_nanim.png');
		col_anim_images = BF.load_and_slice_sprite(32,32,'bouncer_anim.png');
                
		self.anim     	= cAnimSprite(anim_images,5)
		self.col_anim  	= cAnimSprite(col_anim_images,20)
		self.anim.rect  = self.rect
		self.col_anim.rect  = self.rect

		#Status sets
		self.col_anim.draw = False

	def onCollision(self,stick,status):
		stick.flip_rotation()

	def isMonster(self):
		return False
