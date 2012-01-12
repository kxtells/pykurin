import pygame

class cMenu:
	def __init__(self,text_options,default,color,selcolor):
		self.current = default
		self.options = text_options
		self.color = color
		self.select_color = selcolor
		self.background = None
		self.background_scroll = False

		#Attributes to Bind possible functions
		self.action_function = None
		self.event_function = None

	def menu_up(self):
		self.current -= 1
		if self.current < 0: self.current = len(self.options)-1
	
	def menu_down(self):
		self.current += 1
		if self.current > len(self.options)-1: self.current = 0

	def set_background(self,path):
		self.background	= pygame.image.load(path)
