import pygame
from cLevel import cLevel

class cStatus:
	"""All the status information to show to the player"""
	def __init__(self,lives_images,fps=10):
		self.lives=3
		self.lifebar_img_arr = lives_images
		self.lifebar_image = self.lifebar_img_arr[self.lives]
		self.lifebar_rect = self.lifebar_image.get_rect()

		self.lifebar_rect.x = 608
		#Contains the game status
		#__GAME_STAT
		#	0 - Playing with the stick on a level
		#	1 - Game over on a level
		#	2 - Level Selection
		self.GAME_STAT = 2
	
		#
		# Level Information
		#
		self.level = cLevel("levels/lvl1.prop") #loads the default level
		self.current_level = 1
		
		#
		# Stick Information
		#


	def decrease_lives(self):
		""" 
			decreases the number of lives left
			changes the sprite of current lives
			and setting the GAME OVER status if necessary
	
			returns True/False representing a Gameover to
			trigger possible animations
		"""
		self.lives -= 1
		self.lifebar_image = self.lifebar_img_arr[self.lives]
	
		if self.lives <= 0: 
			self.GAME_STAT = 1
			return True

		return False
	
	def reset_lives(self):
		self.lives = 3
		self.lifebar_image = self.lifebar_img_arr[self.lives]
