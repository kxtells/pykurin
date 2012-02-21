from pygame import Rect, image

class cTransition:
	rects = []
	active = False
	growing = True
	background = None
	draw_background = True
	rw = 20
	rh = 20
	window = None
	ttype = 1

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
		self.active = True

	def setInactive(self):
		self.active = False

	def setBackground(self,bg):
		self.background = bg

	def setDrawBackground(self,bg):
		self.draw_background = bg

	def setGrowing(self,boolval):
		self.growing = boolval

	def getBG(self):
		return self.background

	def getRects(self):
		return self.rects

	def logic_update(self):
		if self.ttype==1:
			self.logic_update_1()
	
	def logic_update_1(self):
		if self.isActive():
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

								
		else:
			pass					
			
