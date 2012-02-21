import sys, pygame
from colors import *
from icons import *
from Tkinter import *
import tkFileDialog, tkSimpleDialog, tkMessageBox
import menubar
import datacontainer


MB = menubar.menubar()
SB = menubar.subbar()
DC = datacontainer.datacontainer()
TKroot = Tk()
TKroot.withdraw()

pygame.init()

#Map screen movement
move_screen = False
move_object = False
pad_x = 0
pad_y = 0

#create the screen
w = 800
h = 600
window =  pygame.display.set_mode((w, h)) 

#
menu_height = 64

pygame.display.flip()


def clear_paddings():
	global pad_x
	global pad_y
	pad_x = pad_y = 0

##########################
                            
 ###    ###      #    #   # 
 #  #   #  #    # #   #   # 
 #  #   #  #   #   #  # # # 
 #  #   ###    #####  # # # 
 #  #   #  #   #   #  ## ## 
 ###    #  #   #   #  #   # 

############################
def draw_feedback_on_icons():
	"""
		Basic idea is to draw colors under the icons
		showing if something is already defined or not
	"""
	w = 50
	h = 10
	r = (MB.LOADCOL*MB.separator,51,w,h)
	if DC.isColisionDefined():
		pygame.draw.rect(window, green, pygame.Rect(r))
	else:
		pygame.draw.rect(window, red, pygame.Rect(r))
	
	r = (MB.LOADBG*MB.separator,51,w,h)
	if DC.isBgDefined():
		pygame.draw.rect(window, green, pygame.Rect(r))
	else:
		pygame.draw.rect(window, red, pygame.Rect(r))
	
	r = (MB.GOAL*MB.separator,51,w,h)
	if DC.isGoalDefined():
		pygame.draw.rect(window, green, pygame.Rect(r))
	else:
		pygame.draw.rect(window, red, pygame.Rect(r))

	r = (MB.STICK*MB.separator,51,w,h)
	if DC.isStartDefined():
		pygame.draw.rect(window, green, pygame.Rect(r))
	else:
		pygame.draw.rect(window, red, pygame.Rect(r))


def draw_menu():
	"""
		Draws the ontop menu with the various icons
	"""
	r = (0,0,w,menu_height)
	pygame.draw.rect(window, gray, pygame.Rect(r))

	for i,icon in enumerate(MB.icons):
		window.blit(icon,MB.rects[i])

	if MB.selectedicon != None:
		window.blit(selectmask,MB.rects[MB.selectedicon])
	
	draw_feedback_on_icons()


def draw_image():
	"""
		Draws the level image
	"""
	if DC.image != None:
		window.blit(DC.image,DC.image.get_rect().move(pad_x,menu_height+pad_y))

def draw_subbar():
	"""
		Draws the little subbar on the bottom of the screen
		with the level title, the last error and cursor coordinates
	"""
	r = (0,580,w,20)
	myfont = pygame.font.SysFont("Arial", 14)

	pygame.draw.rect(window, white, pygame.Rect(r))
	
	pstring = ""
	if len(DC.get_title())>32: pstring = "..."

	title = myfont.render(DC.get_title()[0:32]+pstring, 1, black)
	cursor = myfont.render(SB.get_cursor_text(), 1, black)
	window.blit(title, (0, 580))
	window.blit(cursor, (740, 580))



def draw_objects():
	"""
		Draw all the objects and other information
		about them that just will appear here in the
		editor
	"""
	for bouncer_rect in DC.bouncers:
		window.blit(bouncer_img,bouncer_rect.move(pad_x,pad_y))
	
	for lives_rect in DC.lives:
		window.blit(lives_img,lives_rect.move(pad_x,pad_y))

	for goals_rect in DC.goals:
		window.blit(goal_img,goals_rect.move(pad_x,pad_y))

	for sticks_rect in DC.sticks:
		window.blit(stick_img,sticks_rect.move(pad_x,pad_y))
	
	for i,basher_rect in enumerate(DC.bashers):
		brect_moved = basher_rect.move(pad_x,pad_y)
		r = DC.bashers_end[i].move(pad_x,pad_y)

		#draw basher_movement line
		p1 = brect_moved.center[0] , brect_moved.center[1]
		p2 = r.center[0] , r.center[1]
		pygame.draw.line(window, red, p1, p2)

		#draw the basher
		window.blit(basher_img,brect_moved)
		
		#draw the last point of basher movement
		pygame.draw.rect(window,red,r)

def draw_selection():
	"""
		In the case that there's an object selected
		draws a red Line in its perimeter to highlight
		the selection
	"""
	item = DC.get_selected_square()

	if item != None:
		x1 = item[0] + pad_x
		y1 = item[1] + pad_y
		w = item[2]
		h = item[3]
		p1 = (x1,y1)
		p2 = (x1,y1+h)
		p3 = (x1+w,y1+h)
		p4 = (x1+w,y1)
		#pygame.draw.rect(window,red, item)
		pygame.draw.lines(window, red, True, [p1,p2,p3,p4])


################################################################

 #####  #  #          #####  #  #   ###    #  #    ##     ##   
   #    # #             #    #  #    #     ## #   #  #   #  #  
   #    ##              #    ####    #     # ##   #       #    
   #    # #             #    #  #    #     #  #   # ##     #   
   #    #  #            #    #  #    #     #  #   #  #   #  #  
   #    #  #            #    #  #   ###    #  #    ##     ##   

#################################################################
                                                               
def open_file_chooser(naming,ftype="*"):
	try:
		somefile = tkFileDialog.askopenfilename(filetypes=[(naming, ftype)],multiple=False)
		return somefile
	except:
		return None

def save_file_chooser(naming,ftype=".prop"):
	try:
		somefile = tkFileDialog.asksaveasfilename(filetypes=[(naming, ftype)])
		return somefile
	except:
		return None		

def input_text_dialog(title,question):
	return tkSimpleDialog.askstring(title, question)

def popup_message(title,text):
	return tkMessageBox.showinfo(title,text)

def popup_message_yesnocancel(title,text):
	return tkMessageBox.askyesnocancel(title,text)
		

############################################
#
#
                                                                                                                              
   #     ##    #####  ###     ##    #  #           ##     ##    #  #   #####  ###     ##    #      #      ####   ###     ##   
  # #   #  #     #     #     #  #   ## #          #  #   #  #   ## #     #    #  #   #  #   #      #      #      #  #   #  #  
 #   #  #        #     #     #  #   # ##          #      #  #   # ##     #    #  #   #  #   #      #      ###    #  #    #    
 #####  #        #     #     #  #   #  #          #      #  #   #  #     #    ###    #  #   #      #      #      ###      #   
 #   #  #  #     #     #     #  #   #  #          #  #   #  #   #  #     #    #  #   #  #   #      #      #      #  #   #  #  
 #   #   ##      #    ###     ##    #  #           ##     ##    #  #     #    #  #    ##    ####   ####   ####   #  #    ##   
                                                                                                                            
#
#
############################################

def action_set_title():
	"""
		Opens a basic input dialog, and if the user presses OK 
		saves a new name for the level
	"""
	try:
		newtitle = input_text_dialog("Level Title","Level title")
		if newtitle != None:
			DC.set_title(newtitle)
	except:
		pass

def action_openbackgroundimage():
	"""
		Opens a file chooser and sets the background image with it
		NOTE: The background image does not appear in PLB, it's simply
		the background draw for pykurin.
	"""
	try:
		filepath = open_file_chooser("image");
		if filepath != None:			
			DC.set_bg_image(filepath)
	except:
		pass

def action_openimage():
	"""
		Opens a file chooser and sets the level image with it.
	"""
	try:
		filepath = open_file_chooser("image");
		if filepath != None:
			DC.set_image(filepath)

	except:
		pass

def action_opencolisionimage():
	"""
		Opens a file chooser and sets the colison image with it.
	"""
	try:
		filepath = open_file_chooser("image");
		if filepath != None:			
			DC.set_col_image(filepath)

	except:
		pass

def action_openprop():
	"""
		Opens a file chooser to load a properties image
	"""
	try:
		filepath = open_file_chooser("Properties",".prop");
		if filepath != None:
			clear_paddings()			
			DC.load_from_file(filepath,xpadding=0,ypadding=menu_height)

	except:
		pass

def action_saveprop():
	"""
		To save the current level.
		If a filepath was already defined it asks for overwrite, if user
		does not want to overwrite, opens a file dialog
	"""
	try:
		filepath = DC.file_prop_path
		if filepath != None:
			ret = popup_message_yesnocancel("Overwrite","overwrite:"+filepath+"?")
			
			if ret: #yes
				DC.save_to_file(filepath)
			if ret == False: #No
				filepath = save_file_chooser("Provide FileName");
				if filepath != None:
					DC.save_to_file(filepath)
			else: #Cancel
				pass

		else:
			filepath = save_file_chooser("FileName");
			if filepath != None:
				DC.save_to_file(filepath)
				DB.set_file_prop_path(filepath)
			
	except:
		pass
	
###########################
#
#
#                                          
 ####   #  #   ####   #  #   #####   ##   
 #      #  #   #      ## #     #    #  #  
 ###    #  #   ###    # ##     #     #    
 #      ####   #      #  #     #      #   
 #       ##    #      #  #     #    #  #  
 ####    ##    ####   #  #     #     ##   
#
#
#
#
#
############################
def handle_event(evt):
	"""
		All the mouse events handling, firing ACTION CONTROLLERS
		and selecting/unelecting/deleting etc
	"""
	global move_screen
	global move_object
	global pad_x
	global pad_y


	#
	# Fantastic delete an object
	#
	if evt.type == pygame.KEYDOWN:
		if evt.key == pygame.K_DELETE:
			if DC.isItemSelected():
				DC.delete_selected_item()

	if evt.type == pygame.MOUSEBUTTONDOWN:
		x = evt.pos[0]
		y = evt.pos[1]

		#
		# Sub bar firing events
		#
		sub = SB.touched_bar(x,y)
		if sub!= None:
			if sub == SB.TITLE:
				action_set_title()

		#
		# UPPER MENU firing events or modifying status
		#
		action = MB.click_action(x,y) #if click action it will highlight that actin
		if action != None and action !=-1:
			if action == 0:
				action_openimage()
			if action == MB.LOAD:
				action_openprop()
			if action == MB.SAVE:
				action_saveprop()
			if action == MB.LOADCOL:
				action_opencolisionimage()
			if action == MB.LOADBG:
				action_openbackgroundimage()
		
		
		#
		# Canvas. 
		# Basically moving the screen and objects
		# or adding an object if a proper flag is set on MB
		#
		elif action == -1: #clicked on canvas
			if MB.selectedicon!=None: #there's an action to do 
				DC.add_item(MB.selectedicon,x-pad_x,y-pad_y)

			else: #no item selected on menu, let's work on the canvas
				#if DC.isItemSelected(): #is a item on canvas selected? do something
				if DC.touched_selected_item(x-pad_x,y-pad_y):
					move_object = True
						#DC.unselect_item()
				else:
					DC.unselect_item()
					#DC.move_current_item(x-pad_x,y-pad_y)
				#else: #nothing selected, you may be selecting or moving the screen!
				if not DC.touched_item(x-pad_x,y-pad_y):
					move_screen = True
				else:
					move_object = True
	
	if evt.type == pygame.MOUSEBUTTONUP:
		move_screen = False
		move_object = False
	
	if evt.type == pygame.MOUSEMOTION:
		x = evt.pos[0]
		y = evt.pos[1]
		
		SB.set_cursor(x-pad_x,y-pad_y-menu_height)

		if move_screen:
			pad_x+=evt.rel[0]
			pad_y+=evt.rel[1]
		if DC.isItemSelected() and move_object:
			DC.move_current_item(x-pad_x,y-pad_y)


############################################
#
#                           
 #   #    #    ###    #  #  
 ## ##   # #    #     ## #  
 # # #  #   #   #     # ##  
 # # #  #####   #     #  #  
 #   #  #   #   #     #  #  
 #   #  #   #  ###    #  #  
#
#
############################################
def show_disclaimer():
	"""
		Show a disclaimer saying that this software is shit
	"""
	
	popup_message("BorinotGames Note","This program is provided AS IS :-P\n\
It is just a helper utility, don't expect to be beautiful or bug free in Exotic cases")

def main():
	#show_disclaimer() #Add this on publication
	while True: 
		window.fill(gray)
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				sys.exit(0) 
			else:
				#print event
				handle_event(event)
	    
		
		draw_image()
		draw_objects()
		draw_selection()
		draw_menu()
		draw_subbar()
		pygame.display.flip()

if __name__ == '__main__': main()  