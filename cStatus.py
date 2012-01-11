import pygame
from cLevel import cLevel
import time

class cStatus:
	"""All the status information to show to the player"""
	def __init__(self,lives_images,width,height,fps=60):
		self.lives=3
		self.lifebar_img_arr = lives_images
		self.lifebar_image = self.lifebar_img_arr[self.lives]
		self.lifebar_rect = self.lifebar_image.get_rect()

		self.lifebar_rect.x = width - self.lifebar_rect.width
		#Contains the game status
		#__GAME_STAT
		#	0 - Playing with the stick on a level
		#	1 - Game over on a level
		#	2 - Level Selection
		#       3 - Goal SCREEN
		self.GAME_STAT = 2

                # Substatus is used on different screens to move to different sub status
                # (for example, goal screen has 3 status:
                #       - Move to center
                #       - Show screen with results
                #       - Show Options
                #
                # This has to be managed by outer functions
		self.SUBSTAT = 0
	
		#
		# Level Information
		#
		self.level = cLevel("levels/lvl000001.prop") #loads the default level
		self.current_level = 1
		
		#
		# Stick Information
		#

                #
                # Elapsed Time Information
                #
                self.start_time = time.time()

                #
                # Listen KeyStrokes
                #
                self.LISTEN_KEYS = True

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

	def get_elapsed_time(self):
                return time.time() - self.start_time

        def reset_timer(self):
                self.start_time = time.time()

        def enable_disable_keyboard(self):
                if self.LISTEN_KEYS: self.LISTEN_KEYS = False
                else: self.LISTEN_KEYS = True

        def is_keyboard_enabled(self):
                return self.LISTEN_KEYS
