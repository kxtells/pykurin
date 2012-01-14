from pygame import time

class cMonster:
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
		self.anim.update(time.get_ticks())

	def isMonster(self):
		return True

	def logic_update(self):
		return False
