from pygame import time
from pygame import mask
import pygame
import pymunk
from cAnimSpriteFactory import cAnimSpriteFactory as SF

class cMonster(pygame.sprite.Sprite):
	"""
		Superclass for monsters and items. Controlling basic
	"""
	def __init__(self,x=0,y=0,rot=0):
		self.x = x
		self.y = y
		self.rot = rot

		self.damages_on_touch = True
		self.x = 0
		self.y = 0
		self.rot = 0
		self.image = None
		self.rect = None
		self.baseImage = None
		self.mask = None
		self.anim = None
		self.col_anim = None
		self.delete_on_colision = False

		#
		# This is the sprite that will be created on collision
		# It is identified by an ID from cAnimSpriteFactory
		self.col_sprite = SF.OUCH

		#pymunk shape
		#Each subclass should define a shape that fits with its image to process
		#collisions
		self.shape = None
		self.body  = None

		#Impulse force
		self.impforce = 30

	def onCollision(self, stick, status, cpos):
		"""OnCollision function gets three parameters:
			stick: Instance of cPal
			status: Instances of cStatus
			cpos: Pymunk world coordinate position of the collision
		"""
		self.col_anim.draw = True

	def onCollisionImpulseStickAway(self, stick, status, cpos):
		"""Generic function to impulse the stick away from the monster"""

		#Impulse the stick away from the bouncer
		cxi = cpos.x - self.body.position.x
		cyi = cpos.y - self.body.position.y

		impx = impy = 0
		if cxi < 0:
			impx = -self.impforce
		else:
			impx = self.impforce

		if cyi < 0:
			impy = -self.impforce
		else:
			impy = self.impforce

		stick.body.apply_impulse((impx, impy),(0,0))

	#Function to call on draw update
	def draw_update(self):
		if self.col_anim.draw == False:
			return self.anim.update(time.get_ticks())
		else:
			return self.col_anim.update(time.get_ticks())


	def isMonster(self):
		return True

	def logic_update(self):
		return False

	def onWallCollision(self):
		return False


	def collides(self,monster):
		"""
			Checks if the monster collides with a specific monster
		"""
		if self.rect.colliderect(monster.rect):
			#Here need to pix perfect collision
 			trectmonst = self.rect.clip(monster.rect).move(-monster.rect.x,-monster.rect.y)
 			trectstick = self.rect.clip(monster.rect).move(-self.rect.x,-self.rect.y)

			tmonstmask = mask.from_surface(monster.image.subsurface(trectmonst))
 			tcurrentmask = mask.from_surface(self.image.subsurface(trectstick))

			col = tcurrentmask.overlap(tmonstmask,(0,0))
                	if col == None: return False,0,0
                	else: return True,col[0]+self.rect.x,col[1]+self.rect.y

		else: return False,0,0
