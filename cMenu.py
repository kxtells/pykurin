import pygame

class cMenu:
	def __init__(self,text_options,default,color,selcolor):
		self.current = default
		self.options = text_options
		self.color = color
		self.select_color = selcolor
		self.background = None
		self.background_scroll = False
		self.font_size = 20

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

	def set_font_size(self,num):
		self.font_size = num

	def get_font_size(self):
		return self.font_size

	def set_current(self,num):
		if num > len(self.options): return False
		else: self.current = num
		return True

	def reload_options(self, text_options):
		self.options = text_options
