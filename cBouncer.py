import cMonster
import pygame

class cBouncer(cMonster.cMonster):

	def __init__(self,x,y,rot):
		cMonster.cMonster.__init__(self,x,y,rot)
		self.image      = pygame.image.load("sprites/bouncer.png").convert_alpha()
		self.baseImage  = pygame.image.load("sprites/bouncer.png").convert_alpha()
		self.rect	= self.image.get_rect().move(x,y)
		self.mask       = pygame.mask.from_surface(self.image);
	
	def onCollision(self,stick):
		stick.flip_rotation()
