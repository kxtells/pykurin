from icons import *

class menubar:
	#this order is fucking important because this program is not general :-P
	icons = [bashericon,bouncericon,livesicon,goalicon,stickicon,openicon,colimgicon,bgimgicon,loadicon,saveicon]
	rects = []


	BASHER = 0
	BOUNCER = 1
	LIVES = 2

	GOAL = 3
	STICK = 4
	LOADIMG = 5
	LOADCOL = 6
	LOADBG = 7
	LOAD = 8 #reminder where's loadiocn
	SAVE = 9 #reminder where's loadiocn

	item_icon_num = 5
	menu_height = 64
	separator = 64
	selectedicon = None

	def __init__(self):

		for i,icon in enumerate(self.icons):
			self.rects.append(icon.get_rect())
			self.rects[i].move_ip(self.menu_height*i,0)

	def click_action(self,mx,my):
		"""
			Returns an index to the clicked icon.
			if out of menubar, simply returns -1
		"""
		if my > 64: return -1

		for i,icon_rect in enumerate(self.rects):
			if icon_rect.contains((mx-2,my-2,4,4)): #if touched icon

				if i == self.selectedicon: 
					self.selectedicon = None #if already selected, unselect
				
				elif i<5: #not opening files
					self.selectedicon = i
				
				return i
	
	def unselect_icon(self):
		self.selectedicon = None
	
	def get_height(self):
		return self.menu_height

	def get_separator(self):
		return self.separator
	

class subbar(menubar):
	icons = []
	rects = []
	cx = 0
	cy = 0

	TITLE = 1

	def __init__(self):
		self.a = "a2"
	
	def touched_bar(self,mx,my):
		if my > 580: 
			if mx < 100:
				return self.TITLE
		else: return None
	
	def set_cursor(self,x,y):
		self.cx = x
		self.cy = y
	
	def get_cursor_text(self):
		return str(self.cx)+":"+str(self.cy)



