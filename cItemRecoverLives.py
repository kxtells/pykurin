import cMonster
import pygame
from cAnimSprite import cAnimSprite
from cAnimSpriteFactory import cAnimSpriteFactory as SF
import functions as BF
import pymunk

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

		self.anim     		= cAnimSprite(anim_images,10)
		self.col_anim  		= cAnimSprite(col_anim_images,20)
		self.anim.rect  	= self.rect
		self.col_anim.rect  = self.rect
		self.col_sprite 	= SF.LIVES

		#Status sets
		self.col_anim.draw = False
		#Only Usable once
		self.delete_on_colision = True

		#pymunk shape
		self.body = pymunk.Body() #static
		self.body.position += (x + 16,y + 16) #Add half of size
		self.radius  = 17
		self.shape = pymunk.Circle(self.body, self.radius, (0,0))
		self.shape.elasticity = 0.9

		self.shape.collision_type = 2

	def onCollision(self,stick,status):
		super(cItemRecoverLives, self).onCollision(stick,status)
		status.reset_lives()

	def isMonster(self):
		return False
