import functions as BF
from cAnimSprite import cAnimSprite
import random

class cAnimSpriteFactory():
	explosions = []
	boings = []

	def __init__(self):
		for x in range(6): 
			explosion_imgset = BF.load_and_slice_sprite(32,32,'explosion'+str(x)+'.png');
			self.explosions.append(explosion_imgset)

		for x in range(1): 
			boing_imgset = BF.load_and_slice_sprite(100,50,'boing'+str(x)+'.png');
			self.boings.append(boing_imgset)
	
	def get_explosion_sprite(self,x=-5000,y=-5000):
		"""
			Get a random imageset for a explosion
			create a Animation Sprite and return it
		"""
		rand = random.randint(0,len(self.explosions)-1)
		tsprite = cAnimSprite(self.explosions[rand],20)
		tsprite.move(x,y) #out of view
		tsprite.draw = True
		return tsprite
	
	def get_boing_sprite(self,x=-5000,y=-5000):
		"""
			Get a random imageset for a Boing
			create a Animation Sprite and return it
		"""
		rand = random.randint(0,len(self.boings)-1)
		tsprite = cAnimSprite(self.boings[rand],20)
		tsprite.move(x,y) #out of view
		tsprite.draw = True
		return tsprite
