from pygame import time
from pygame import mask
import pygame

class cMonster(pygame.sprite.Sprite):
	"""
		Superclass for monsters and items. Controlling basic
	"""
	damages_on_touch = True
	x = 0
	y = 0
	rot = 0
	image = None
	rect = None
	baseImage = None
	mask = None
	anim = None
	col_anim = None
	delete_on_colision = False

	def __init__(self,x=0,y=0,rot=0):
		self.x = x
		self.y = y
		self.rot = rot


	def onCollision(self,stick,status):
		"""
			Default on colision handling.
			Decreases the player lives
		"""
		if not status._DEBUG_DEATH: status.decrease_lives()


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
