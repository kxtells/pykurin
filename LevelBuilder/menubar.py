from icons import *

class menubar:
	#this order is fucking important because this program is not general :-P
	icons = [openicon,bashericon,bouncericon,livesicon,goalicon,stickicon,colimgicon,bgimgicon,loadicon,saveicon]
	rects = []

	GOAL = 4
	STICK = 5
	LOADBG = 6
	LOADCOL = 7
	LOAD = 8 #reminder where's loadiocn
	SAVE = 9 #reminder where's loadiocn

	separator = 64

	selectedicon = None

	def __init__(self):

		for i,icon in enumerate(self.icons):
			self.rects.append(icon.get_rect())
			self.rects[i].move_ip(self.separator*i,0)

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
				
				elif i!=0 and i!=self.LOAD and i!=self.SAVE and i!=self.LOADCOL and i!=self.LOADBG: #not opening files
					self.selectedicon = i
				
				return i



