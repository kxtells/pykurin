from pygame import Rect, image, transform, draw
from random import randint
from colors import *

class cTransition:
	background = None
	draw_background = True

	#transition T1
	rects = []
	active = False
	growing = True
	rw = 15
	rh = 15
	window = None
	ttype = 1

	#Transition t2
	radius = 0
	step = 10

	#Trans Types
	SQUARES = 1
	CIRCLE = 2
	TOTALTYPES = 2

	def __init__(self,window):

		rw = self.rw
		rh = self.rh
		rx = 0
		ry = 0
		width = window.get_width()
		height = window.get_height()
		self.window = window

		for x in range(0,width,rw):
			for y in range(0,height,rh):
				self.rects.append(Rect(x,y,0,0))


	def isActive(self):
		return self.active
	
	def isGrowing(self):
		return self.growing		
	
	def isDrawBG(self):
		if self.draw_background == None: 
			return False
		else:
			return self.draw_background	

	def setActive(self):
		width = self.window.get_width()
		height = self.window.get_height()
		self.background = image.frombuffer(image.tostring(self.window,"RGB"),(width,height),"RGB")
		self.ttype = randint(1,self.TOTALTYPES)
		self.active = True
	
	def setInactive(self):
		self.active = False

	def setBackground(self,bg):
		self.background = bg

	def setDrawBackground(self,bg):
		self.draw_background = bg

	def setGrowing(self,boolval):
		self.growing = boolval

	#
	# GETTERS
	#
	def getBG(self):
		return self.background

	def getRects(self):
		return self.rects

	def getType(self):
		return self.ttype

	def getRadius(self):
		return self.radius		

	#
	# LOGIC
	#
	def logic_update(self):
		if self.isActive():
			if self.ttype==1:
				self.logic_update_1()
			elif self.ttype==2:
				self.logic_update_2()
	
	def logic_update_1(self):
		if self.isGrowing():
			for f in self.rects: f.inflate_ip(1,1)
			fr_curr_width = self.rects[0][2]
			if fr_curr_width == self.rw: 
				self.setGrowing(False)
				self.setDrawBackground(False)
		else:
			for f in self.rects: f.inflate_ip(-1,-1)					
	
			fr_curr_width = self.rects[0][2]
			if fr_curr_width == 0:
				self.setInactive()
				self.setGrowing(True)
				self.setDrawBackground(True)									

	def logic_update_2(self):
		width = self.window.get_width()
		height = self.window.get_height()
		if self.isGrowing():
			self.radius += self.step
			if self.radius >= max(width/2,height/2):
				self.setGrowing(False)
				self.setDrawBackground(False)
		else:
			self.radius -= self.step
			if self.radius <= 0:
				self.setInactive()
				self.setGrowing(True)
				self.setDrawBackground(True)



	def draw_transition(self):
		if self.isActive():
			if self.isDrawBG():
				self.window.blit(self.getBG(),self.getBG().get_rect())
			
			if self.getType() == self.SQUARES:
				for r in self.getRects():
					draw.rect(self.window,black,r)
			elif self.getType() == self.CIRCLE:
				width = self.window.get_width()
				height = self.window.get_height()
				draw.circle(self.window, black, (width/2,height/2), self.getRadius())
			
			self.logic_update()