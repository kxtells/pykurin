import pygame
from cLevel import cLevel
import time
from colors import *

class cStatus:
	"""All the status information to control the game"""
	_INVINCIBLE_TIME = 0.75
	_MAX_LIVES = 3

	"Games possible states"
	_STAT_GAMING = 0
	_STAT_GAMEOVER = 1
	_STAT_LEVELSEL = 2
	_STAT_GOAL = 3
	_STAT_PAUSE = 4
	_STAT_LEVELRECORD = 5
	_STAT_TITLESCREEN = 6 
	_STAT_GAMEMENU = 7
	_STAT_MAINMENU = 8
	_STAT_SETTINGS = 9
	_STAT_NEWNAME =10 

	"""Debug shit"""
	_DEBUG_COLLISION=False
	_DEBUG_DEATH=False
	


	level = None
	
	def __init__(self,lives_images,width,height,fps=60):
		self.lives=cStatus._MAX_LIVES
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
		#       4 - PAUSE SCREEN
		#self.GAME_STAT = cStatus._STAT_LEVELSEL
		self.GAME_STAT = cStatus._STAT_MAINMENU

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
		self.level;
		self.current_level = 1
		
		#
		# Stick Information
		#
		self.invincible = False
		self.invincible_start_time = 0

		#
		# Elapsed Time Information
		#
		self.start_time = time.time()
		self.pause_stime = time.time()
		self.pause_time_diff = 0
		self.penalty_seconds = 0

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
		self.lives = cStatus._MAX_LIVES
		self.lifebar_image = self.lifebar_img_arr[self.lives]

	def get_elapsed_time(self):
		if self.GAME_STAT == cStatus._STAT_PAUSE or self.GAME_STAT == self._STAT_GAMEOVER:
			return time.time() - self.start_time - (time.time() - self.pause_stime) + self.penalty_seconds
		else:
			return time.time() - self.start_time - self.pause_time_diff + self.penalty_seconds

	def reset_timer(self):
		print "reset"
		self.start_time = time.time()
		self.pause_stime = time.time()
		self.pause_time_diff = 0
		self.penalty_seconds = 0
	
	def enable_disable_keyboard(self):
		if self.LISTEN_KEYS: self.LISTEN_KEYS = False
		else: self.LISTEN_KEYS = True

	def is_keyboard_enabled(self):
		return self.LISTEN_KEYS

	def set_invincible(self):
		"""Sets the invincible flag and the start invincibility time if is not already set"""
		if self.invincible == False:
			self.invincible = True
			self.invincible_start_time = time.time()

	def unset_invincible_by_time(self):
		elapsed = time.time() - self.invincible_start_time
		if elapsed >= cStatus._INVINCIBLE_TIME: self.invincible = False

	
	def pause_game(self):
		"""
			HouseKeeping when paused
		"""
		self.GAME_STAT = cStatus._STAT_PAUSE
		self.pause_stime = time.time()
	
	def unpause_game(self):
		"""
			HouseKeeping unpausing the game
		"""
		self.GAME_STAT = cStatus._STAT_GAMING
		diff = time.time() - self.pause_stime
		self.pause_time_diff += diff

	def add_seconds(self,num):
		self.penalty_seconds += num

	
	def clear_penalty_seconds(self):
		self.penalty_seconds = 0

	def set_game_status(self,stat):
		self.GAME_STAT = stat
