import functions as BF
from cAnimSprite import cAnimSprite
import random

class cAnimSpriteFactory():
	explosions = []
	boings = []
	ouchs = []
	livesup = []
	fireworks = []

	all_sprites = [explosions,boings,ouchs,livesup,fireworks]
	sprite_fps = [20,10,10,10,10]

	# Sprite id definitions
	EXPLOSION = 0
	BOING = 1
	OUCH = 2
	LIVES = 3
	FIREWORK = 4

	def __init__(self):
		"""
			Load all the possible sprites at the beginning :-)
		"""

		for x in range(6):
			explosion_imgset = BF.load_and_slice_sprite(32,32,'explosion'+str(x)+'.png');
			self.explosions.append(explosion_imgset)

		for x in range(4):
			boing_imgset = BF.load_and_slice_sprite(100,50,'boing'+str(x)+'.png');
			self.boings.append(boing_imgset)

		for x in range(3):
			imgset = BF.load_and_slice_sprite(100,50,'ouch'+str(x)+'.png');
			self.ouchs.append(imgset)

		for x in range(1):
			imgset = BF.load_and_slice_sprite(100,50,'livesup'+str(x)+'.png');
			self.livesup.append(imgset)

		for x in range(1):
			imgset = BF.load_and_slice_sprite(75,75,'firework'+str(x)+'.png');
			self.fireworks.append(imgset)

	def create_sprite(self,x=-5000,y=-5000,spritetype=0):
		"""
			Get a random imageset for a spritetype
			create a Animation Sprite and return it
		"""
		rand = random.randint(0,len(self.all_sprites[spritetype])-1)
		tsprite = cAnimSprite(self.all_sprites[spritetype][rand],self.sprite_fps[spritetype])
		tsprite.move(x,y) #out of view
		tsprite.draw = True
		return tsprite

	def get_sprite_by_id(self,x=-5000,y=-5000,id=0):
		"""
			Function to call from outside
		"""
		return self.create_sprite(x,y,id)

