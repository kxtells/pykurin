#!/usr/bin/python
#######################
# Main pykurin entrance
# @author: Jordi Castells Sala
#
#
#######################

import os,sys
#Change directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Add libraries to the path
libp = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lib"))
sys.path.append(libp)

#pykurin libraries
import functions as BF
import cAnimSpriteFactory
import cCustomFont
import cInputKeys
from cPal import cPal
from cLevel import cLevel
from cAnimSprite import cAnimSprite
from cStatus import cStatus
from cMenu import cMenu
from cLevelList import cLevelList
from cSettings import cSettings
from cTransition import cTransition
from colors import *
import math

#3rd party libraries
import pymunk
from pymunk import Vec2d
import pygame

pygame.init()

size = WIDTH, HEIGHT = 640, 480
FPS = 45



###########################################################################################

########  ######## ######## #### ##    ## #### ######## ####  #######  ##    ##  ######
##     ## ##       ##        ##  ###   ##  ##     ##     ##  ##     ## ###   ## ##    ##
##     ## ##       ##        ##  ####  ##  ##     ##     ##  ##     ## ####  ## ##
##     ## ######   ######    ##  ## ## ##  ##     ##     ##  ##     ## ## ## ##  ######
##     ## ##       ##        ##  ##  ####  ##     ##     ##  ##     ## ##  ####       ##
##     ## ##       ##        ##  ##   ###  ##     ##     ##  ##     ## ##   ### ##    ##
########  ######## ##       #### ##    ## ####    ##    ####  #######  ##    ##  ######

############################################################################################

clock = pygame.time.Clock ()
window = pygame.display.set_mode(size)
icon   = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_caption("PYKURIN Beta")
pygame.display.set_icon(icon)

### Create the pymunk space
space = pymunk.Space()
#space.gravity = Vec2d(0.0, 0.0)

#EXAMPLE STATIC LINES
### Static line
#static_body = pymunk.Body()


INPUT_KEYS = cInputKeys.cInputKeys()
TRANSITION = cTransition(window)

###
#
# Font loading
#
###
FONT = pygame.font.Font("ttf/Tusj.ttf", 25)
TIMERFONT = pygame.font.Font("ttf/NATWR.ttf", 55)

#######################################
#
# BASIC SPRITE LOADING
#
#######################################
#sprite factory
SPRITE_FAC = cAnimSpriteFactory.cAnimSpriteFactory()

#Goal Text
imgset = BF.load_and_slice_sprite(300,150,'goal_text.png');
gtext_sprite = cAnimSprite(imgset)
gtext_sprite.move(800,250)

#timer bg
imgset = BF.load_and_slice_sprite(250,123,'timer_bg.png');
bg_timer_image = imgset[0]

#New Record Text
imgset = BF.load_and_slice_sprite(230,100,'newrecord.png');
newrecord_sprite = cAnimSprite(imgset,1)
newrecord_sprite.move(450,150)

#Lives sprite
imgsetlives = BF.load_and_slice_sprite(192,64,'livemeter.png');

#Custom Numbers
imgset_numbers = BF.load_and_slice_sprite(50,50,'numbers.png');
number_gen = cCustomFont.cCustomFont(imgset_numbers)

#Locked sprite
locked_sprite = pygame.image.load('sprites/locked.png')
openlock_sprite = pygame.image.load('sprites/openlock.png')

#LevelDone
tick_sprite = pygame.image.load('sprites/tick.png')


#######################################
#
# STATUS and SETTINGS CREATION
#
#######################################
#Status load
status = cStatus(imgsetlives,WIDTH,HEIGHT)
settings = cSettings()

#First Base Load
stick = cPal(0,0,20)
#Add stick to the physics simulator
#space.add(stick.body, stick.shape)

#General arrays with Sprites
BASIC_SPRITES=[]
ANIM_SPRITES=[]

BASIC_SPRITES.append(status.level)
BASIC_SPRITES.append(stick)


#######################################
#
# GAME MENUS CREATION
#
#######################################
# Level Selection Menu
#level_list = cLevelList("levels/training")
level_list = cLevelList()

levels_menu = cMenu(level_list.get_levelnames(),0,black,red)
levels_menu.set_background("backgrounds/squared_paper_lsel.png")
levels_menu.background_scroll = True

packlist = cLevelList()
packlist.load_packdir('levelpacks')
packs_menu = cMenu(packlist.get_packnames(),0,black,red)
packs_menu.set_background("backgrounds/squared_paper_psel.png")
packs_menu.background_scroll = True


#Game Over Menu
gover_menu_texts = 'Try again' , 'Return to level Select' , 'Main Menu'
gover_menu = cMenu(gover_menu_texts,0,black,red)
gover_menu.set_background("backgrounds/piece_paper.png")

#Pause Over Menu
pause_menu_texts = 'Continue', 'Restart Level' , 'Return to level Select' , 'Main Menu'
pause_menu = cMenu(pause_menu_texts,0,black,red)
pause_menu.set_background("backgrounds/piece_paper.png")


#Records Menu
records_menu_texts = 'Next Level', 'Repeat' , 'Level Select'
records_menu = cMenu(records_menu_texts,0,black,red)
records_menu.set_background("backgrounds/records_screen.png")

#Records Menu
main_menu_texts = 'Main Game', 'Settings' , 'Say Goodbye'
main_menu = cMenu(main_menu_texts,0,black,red)
main_menu.set_background("backgrounds/squared_paper_maintitle.png")

#Settings Menu
settings_menu_texts = ['Player Name: '+str(settings.get_username()), 'Fullscreen', 'Go Back' ]
settings_menu = cMenu(settings_menu_texts,0,black,red)
settings_menu.set_background("backgrounds/squared_paper_settings.png")

INPUT_KEYS_BG = pygame.image.load("backgrounds/squared_paper_wun.png")

#
# Function to update the settings menu
#
def update_settings_menu_texts():
	#default fullscreens for settings menu
	if settings.get_fullscreen():
		settings_menu.options[1] = "Fullscreen: ON"
	else:
		settings_menu.options[1] = "Fullscreen: OFF"

	settings_menu.options[0] = "Player Name: "+str(settings.get_username())


update_settings_menu_texts()


#####################################################################

########  ######   ######  ########  ######## ######## ##    ##
##       ##    ## ##    ## ##     ## ##       ##       ###   ##
##       ##       ##       ##     ## ##       ##       ####  ##
######    ######  ##       ########  ######   ######   ## ## ##
##             ## ##       ##   ##   ##       ##       ##  ####
##       ##    ## ##    ## ##    ##  ##       ##       ##   ###
##        ######   ######  ##     ## ######## ######## ##    ##

######################################################################

def set_fullscreen():
	"""
		Set a fullscreen
	"""
	pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)

def toggle_fullscreen():
	"""
		Change between fullscreen and windowed
		Modifies the texts on settings menu
	"""
	fullscreen = settings.get_fullscreen()
	if not fullscreen:
		set_fullscreen()
		fullscreen = True
	else:
		pygame.display.set_mode(size)
		fullscreen = False

	settings.set_fullscreen(fullscreen)
	fullscreen = settings.get_fullscreen()

	#modify the settings_menu text
	if fullscreen: text = ' ON'
	else: text = ' OFF'
	settings_menu.options[1] = "Fullscreen:"+text

#default fullscreens for settings menu
if settings.get_fullscreen(): set_fullscreen()


##########################################################

######## ##     ## ######## ##    ## ########  ######
##       ##     ## ##       ###   ##    ##    ##    ##
##       ##     ## ##       ####  ##    ##    ##
######   ##     ## ######   ## ## ##    ##     ######
##        ##   ##  ##       ##  ####    ##          ##
##         ## ##   ##       ##   ###    ##    ##    ##
########    ###    ######## ##    ##    ##     ######

###########################################################

#Debug Options
def key_debug_actions(event):
#the global var collision may be modified
	if event.key == pygame.K_F1:
		status._DEBUG_PYMUNK = not status._DEBUG_PYMUNK
	elif event.key == pygame.K_F2:
		status._DEBUG_PYMUNKLEVEL = not status._DEBUG_PYMUNKLEVEL
	elif event.key == pygame.K_f:
		stick.flip_rotation()
	elif event.key == pygame.K_F12:
		print level_list.levelfiles
		print level_list.levelsuuid

#Main Key Handler For the GAMING STATUS
def key_handler(event):

	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_DOWN: stick.move_down();
		elif event.key == pygame.K_UP: stick.move_up();
		elif event.key == pygame.K_LEFT: stick.move_left();
		elif event.key == pygame.K_RIGHT: stick.move_right();
		elif event.key == pygame.K_LCTRL: stick.turbo_on();

		#Pause Button
		elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p: status.pause_game()

		#Debug Handlers
		key_debug_actions(event)

	elif event.type == pygame.KEYUP:
		if event.key == pygame.K_DOWN: stick.move_up();
		elif event.key == pygame.K_UP: stick.move_down();
		elif event.key == pygame.K_LEFT: stick.move_right();
		elif event.key == pygame.K_RIGHT: stick.move_left();
		elif event.key == pygame.K_LCTRL: stick.turbo_off();

#Game Over Menu Handler
def key_menu_handler(event,menu):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: menu.menu_down();
                elif event.key == pygame.K_UP: menu.menu_up();
                elif event.key == pygame.K_RETURN: menu.action_function()
		else:
			if menu.event_function != None: menu.event_function(event)


def input_name_keyhandler(event):
	"""
		Input handler when reading a username
	"""
	if event.key == pygame.K_ESCAPE:
		TRANSITION.setActive()
		status.set_game_status(cStatus._STAT_SETTINGS)

	if INPUT_KEYS.process_keystroke(event): #process the keystrokes, and if keystroke is ENTER finish
		if INPUT_KEYS.sanitize_input():
			TRANSITION.setActive()
			settings.set_username(INPUT_KEYS.text)
			update_settings_menu_texts()
			status.set_game_status(cStatus._STAT_SETTINGS)



#Specific Pause menu handler
# (for giving the change to exit the menu without selecting)
def pause_menu_events(event):
	if event.key == pygame.K_ESCAPE or event.key == pygame.K_p: status.unpause_game()

#Also used by settings menu
def level_menu_events(event):
	if event.key == pygame.K_ESCAPE:
		status.set_game_status(cStatus._STAT_PACKSEL)
		TRANSITION.setActive()

#Also used by settings menu
def pack_menu_events(event):
	if event.key == pygame.K_ESCAPE:
		status.set_game_status(cStatus._STAT_MAINMENU)
		TRANSITION.setActive()

#
# MAIN ENTRANCE FOR EVENT HANDLING
#
def event_handler(event):
	"""
		Different handlers for different events in different status
		Check cStatus class for status definitions
	"""
	if event.type == pygame.QUIT: pygame.quit();sys.exit()

	#if transition ongoing do not listen the events
	if TRANSITION.isActive(): return

	#Gaming
	if status.GAME_STAT == cStatus._STAT_GAMING:
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_handler(event)

	#Game Over Screen
	elif status.GAME_STAT == cStatus._STAT_GAMEOVER:
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,gover_menu)

	#PAUSE Screen
	elif status.GAME_STAT == cStatus._STAT_PAUSE:
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,pause_menu)

	#Select PACK Screen
	elif status.GAME_STAT == cStatus._STAT_PACKSEL:
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,packs_menu)

	#Select level Screen
	elif status.GAME_STAT == cStatus._STAT_LEVELSEL:
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,levels_menu)

	#Records level Screen
	elif status.GAME_STAT == cStatus._STAT_LEVELRECORD:
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,records_menu)

	#MAIN Menu Screen
	elif status.GAME_STAT == cStatus._STAT_MAINMENU:
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,main_menu)

	#SETTINGS Menu Screen
	elif status.GAME_STAT == cStatus._STAT_SETTINGS:
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,settings_menu)

	#TEXT INPUT
	elif status.GAME_STAT == status._STAT_NEWNAME:
		if event.type == pygame.KEYDOWN: input_name_keyhandler(event)



####################################################

##     ## ######## ##    ## ##     ##  ######
###   ### ##       ###   ## ##     ## ##    ##
#### #### ##       ####  ## ##     ## ##
## ### ## ######   ## ## ## ##     ##  ######
##     ## ##       ##  #### ##     ##       ##
##     ## ##       ##   ### ##     ## ##    ##
##     ## ######## ##    ##  #######   ######

######################################################


def create_space(level):
	"""Modify the global space, to be updated according to the levels.
		Right now, the levels do not have space configurations, but it might
		have it in the future
	"""
	global space

	space = pymunk.Space(iterations=10)
	#Stop the movement each step
	space.damping = 0.9
	#Use no gravity
	space.gravity = Vec2d(0.0, 0.0)

	#Add the level collision vectors
	space.add(stick.body, stick.shape) 		#Stick
	space.add(status.level.level_segments) 	#Level

	#Items
	for item in level.items:
		if item.shape:
			#Items are always static
			space.add(item.shape)

	#Monsters
	for monster in level.monsters:
		if monster.shape:
			#Items are always static
			space.add(monster.shape)

	#Monsters

	#Collision Handlers

	space.add_collision_handler(0, 1,
			begin=None,
			pre_solve=None,
			post_solve=col_stick_level,
			separate=None)

	space.add_collision_handler(0, 2,
			begin=None,
			pre_solve=None,
			post_solve=col_stick_item,
			separate=None)

	space.add_collision_handler(0, 3,
			begin=None,
			pre_solve=None,
			post_solve=col_stick_monster,
			separate=None)

def load_level_filename(level_fname):
	"""Load level from a filename."""
	status.level = cLevel(level_fname)
	stick.__init__(status.level.startx,status.level.starty,0,status.level.stick);
	#stick.load_stick_image(status.level.stick)

	status.reset_lives()
	status.set_game_status(cStatus._STAT_GAMING)
	status.SUBSTAT = 0
	status.reset_timer()
	status.clear_penalty_seconds()

	create_space(status.level)

#Load a Specific Level (needed for level menu function)
# @TODO : Maybe better in another place or python file
def load_level(level_num):
	load_level_filename(level_list.levelfiles[level_num])
	status.current_level = level_num

def load_levellist_with_pack(pack_num):
	"""
		Fills the level menu with the levels of a packlist
	"""

	basedir = packlist.get_pack_basedir(pack_num)
	#levels_menu references to level list so just modify level list
	#and set level_menu current to 0
	level_list.load_leveldir(basedir)
	levels_menu.reload_options(level_list.get_levelnames())
	levels_menu.set_current(0)

#Records menu selection function
def records_menu_selection():
	if records_menu.current == 0:
		status.current_level += 1
		if level_list.level_exists(status.current_level):
			load_level(status.current_level)
		else:
			status.set_game_status(cStatus._STAT_PACKSEL)


	elif records_menu.current == 1:
		load_level(status.current_level)

	elif records_menu.current == 2:
		levels_menu.set_current(status.current_level)
		status.set_game_status(cStatus._STAT_LEVELSEL)

	TRANSITION.setActive()

def settings_menu_selection():
	if settings_menu.current == 0:
		status.set_game_status(cStatus._STAT_NEWNAME)

	elif settings_menu.current == 1:
		toggle_fullscreen()


	elif settings_menu.current == 2:
		status.set_game_status(cStatus._STAT_MAINMENU)

	TRANSITION.setActive()

#Game over menu selection function
def game_over_menu_selection():
    #Try again. Reload everything and return to game mode
	if gover_menu.current == 0:
		load_level(status.current_level)

        #Return to Level Select Menu
	elif gover_menu.current == 1:
		levels_menu.set_current(status.current_level)
		status.set_game_status(cStatus._STAT_LEVELSEL)

        #Return to Main Menu
	elif gover_menu.current == 2:
		status.set_game_status(cStatus._STAT_MAINMENU)

	TRANSITION.setActive()

#Level Menu Selection Function
def level_menu_selection():
	load_level(levels_menu.current)
	status.set_game_status(cStatus._STAT_GAMING)
	TRANSITION.setActive()

#Level Menu Selection Function
def pack_menu_selection():
	if packlist.isPackOpen(packs_menu.current,settings.total_levels_cleared()):
		load_levellist_with_pack(packs_menu.current)
		status.set_game_status(cStatus._STAT_LEVELSEL)
		TRANSITION.setActive()
	else:
		print "pack not opened yet"

#Pause Menu selection Function
def pause_menu_selection():
	#Continue, change to game mode
	if pause_menu.current == 0:
		status.unpause_game()

	#Reset Level
	elif pause_menu.current == 1:
		load_level(status.current_level)
		TRANSITION.setActive()
	#Return to Level Select Menu
	elif pause_menu.current == 2:
		levels_menu.set_current(status.current_level)
		status.set_game_status(cStatus._STAT_LEVELSEL)
		TRANSITION.setActive()

	#Return to Main Menu
	elif pause_menu.current == 3:
		status.set_game_status(cStatus._STAT_MAINMENU)
		TRANSITION.setActive()

def main_menu_selection():
        #Go to level selection to start the game
	if main_menu.current == 0:
		status.set_game_status(cStatus._STAT_PACKSEL)

	#Settings
	elif main_menu.current == 1:
		update_settings_menu_texts()
		status.set_game_status(cStatus._STAT_SETTINGS)

	#Exit
	elif main_menu.current == 2:
		pygame.quit()
		sys.exit()

	TRANSITION.setActive()

#MENU BINDINGS
gover_menu.action_function = game_over_menu_selection
levels_menu.action_function = level_menu_selection
pause_menu.action_function = pause_menu_selection
records_menu.action_function = records_menu_selection
main_menu.action_function = main_menu_selection
settings_menu.action_function = settings_menu_selection
packs_menu.action_function = pack_menu_selection

levels_menu.event_function = level_menu_events #return to packs menu on escape
settings_menu.event_function = pack_menu_events #return to main menu on escape
packs_menu.event_function = pack_menu_events #return to main menu on escape
pause_menu.event_function = pause_menu_events


###################################################

##        #######   ######   ####  ######
##       ##     ## ##    ##   ##  ##    ##
##       ##     ## ##         ##  ##
##       ##     ## ##   ####  ##  ##
##       ##     ## ##    ##   ##  ##
##       ##     ## ##    ##   ##  ##    ##
########  #######   ######   ####  ######

###################################################

#PYMUNK COLLISION HANDLING
def col_stick_level(who, arbiter):
	cpos = arbiter.contacts[0].position
	tsprite = SPRITE_FAC.get_sprite_by_id(cpos.x,cpos.y,SPRITE_FAC.EXPLOSION)
	ANIM_SPRITES.append(tsprite)

	if not status.invincible:
		#Add 3 seconds to the total time
		status.add_seconds(3)
		status.set_invincible()
		status.decrease_lives()


def col_stick_item(who, arbiter):
	ishape = arbiter.shapes[1] #shape of the item
	item = status.level.get_item_by_shape(ishape)
	item.onCollision(stick, status)

	cpos = arbiter.contacts[0].position
	tsprite = SPRITE_FAC.get_sprite_by_id(cpos.x, cpos.y, item.col_sprite)
	ANIM_SPRITES.append(tsprite)

def col_stick_monster(who, arbiter):
	ishape = arbiter.shapes[1] #shape of the item
	monster= status.level.get_monster_by_shape(ishape)
	monster.onCollision(stick, status)

	cpos = arbiter.contacts[0].position
	tsprite = SPRITE_FAC.get_sprite_by_id(cpos.x, cpos.y, item.col_sprite)
	ANIM_SPRITES.append(tsprite)

def monster_logic():
	for m in status.level.monsters:
		m.logic_update()
		if status.level.stick_collides(m)[0]:
			m.onWallCollision()

###################################################################

########  ########     ###    ##      ## #### ##    ##  ######
##     ## ##     ##   ## ##   ##  ##  ##  ##  ###   ## ##    ##
##     ## ##     ##  ##   ##  ##  ##  ##  ##  ####  ## ##
##     ## ########  ##     ## ##  ##  ##  ##  ## ## ## ##   ####
##     ## ##   ##   ######### ##  ##  ##  ##  ##  #### ##    ##
##     ## ##    ##  ##     ## ##  ##  ##  ##  ##   ### ##    ##
########  ##     ## ##     ##  ###  ###  #### ##    ##  ######

###################################################################

#Debug information
def debug_onscreen(colides):
        #TIMING
        seconds         = int(status.get_elapsed_time())
        millis          = str(seconds - status.get_elapsed_time()).partition(".")[2]
        timestr         = str(seconds)+":"+millis[0:3]

        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 14)
        # apply it to text on a label
        title           = myfont.render("Debug", 1, red)
        stickpos        = myfont.render("Stick:"+str(stick.rect.center), 1, red)
        stickcollides   = myfont.render("collides:"+str(colides), 1, red)
        stickinvincib   = myfont.render("invincib:"+str(status.invincible), 1, red)
        fps             = myfont.render("FPS:"+str(clock.get_fps()),1,red)
        elapsed_time    = myfont.render("TIME:"+timestr,1,red)
        levels_cleared  = myfont.render("LEVELS:"+str(settings.total_levels_cleared()),1,red)

        # put the label objects on the screen
        window.blit(title, (0, 0))
        window.blit(stickpos, (0, 20))
        window.blit(stickcollides, (0, 40))
        window.blit(stickinvincib, (0, 60))
        window.blit(fps, (0, 80))
        window.blit(elapsed_time, (0, 100))
        window.blit(levels_cleared, (0, 120))

        if status._DEBUG_COLLISION == True:
                colisionOnOff   = myfont.render("COLLISION OFF",1,red)
                window.blit(colisionOnOff, (400, 0))
        if status._DEBUG_DEATH == True:
                deathOnOff      = myfont.render("DEATH OFF",1,red)
                window.blit(deathOnOff, (400, 20))


def draw_transition():
	TRANSITION.draw_transition()
	return
	if TRANSITION.isActive():
		if TRANSITION.isDrawBG():
			window.blit(TRANSITION.getBG(),TRANSITION.getBG().get_rect())

		if TRANSITION.getType() == TRANSITION.SQUARES:
			for r in TRANSITION.getRects():
				pygame.draw.rect(window,black,r)
		elif TRANSITION.getType() == TRANSITION.CIRCLE:
			pygame.draw.circle(window, black, (WIDTH/2,HEIGHT/2), TRANSITION.getRadius())
		TRANSITION.logic_update()

#Updates all the needed images/sprites for goal Screen
def update_scene_goal():
        window.blit(gtext_sprite.image,gtext_sprite.rect)
        gtext_sprite.update(pygame.time.get_ticks())

#
#@TODO: THis has to be beautiful
#
def update_scene_records():
	records = status.level.records
	player_index = status.level.player_record_index

	# pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 25)

	for i,r in enumerate(records):
		player = r[1]
		time = r[0]

		seconds         = int(time)
        	millis          = str(seconds - time).partition(".")[2]
        	timestr         = str(seconds)+":"+millis[0:3]

		if player_index == i:
			timefont	= FONT.render(timestr, 1, black,yellow)
			namefont	= FONT.render(player, 1, black,yellow)
		else:
			timefont	= FONT.render(timestr, 1, black)
			namefont	= FONT.render(player, 1, black)



		window.blit(namefont, (150, 50*(i+3)))
		window.blit(timefont, (50, 50*(i+3)))

	if player_index > -1:
        	window.blit(newrecord_sprite.image,newrecord_sprite.rect)
                newrecord_sprite.update(pygame.time.get_ticks())


def get_window_offset():
	"""Get the offset to apply"""
	pos = stick.body.position
	dx = -(pos.x-WIDTH/2)
	dy = -(pos.y-HEIGHT/2)
	return int(dx),int(dy)


#updates all the needed images/sprites
def update_scene():
	"""
		Blits all the Gaming sprites:
		 - status.level , goal_sprite, ANIM_SPRITES, stick, lifebar
		 - Possible level monsters

		Also deletes sprites from ANIM_SPRITES if their draw flag is false
	"""
	window.fill(white)

	window.blit(status.level.bg,status.level.bg.get_rect())

	#Scroll Follows Rect
	#dx = -(stick.rect.center[0]-WIDTH/2)
	#dy = -(stick.rect.center[1]-HEIGHT/2)

	#Scroll Follows Nothing
	#dx = dy = 0

	#scroll follows pymunk shape
	dx,dy = get_window_offset()

	#print bb,"--",stick.rect,"(",bb.top,bb.left,bb.right - bb.left,bb.top-bb.bottom,")"


	rect = BF.pymunkBB_to_rect(stick.shape.bb)
	window.blit(status.level.image,status.level.rect.move(dx,dy))

	window.blit(status.level.goal_sprite.image,status.level.goal_sprite.rect.move(dx,dy))
	status.level.goal_sprite.update(pygame.time.get_ticks())


	#Items InGame
	for i,m in enumerate(status.level.items):
		if m.col_anim.draw == False:
			window.blit(m.anim.image,m.rect.move(dx,dy))
			m.draw_update()
		else:
			window.blit(m.col_anim.image,m.rect.move(dx,dy))
			if m.draw_update() and m.delete_on_colision:
				status.level.items.remove(m)

     	#Monsters
	for i,m in enumerate(status.level.monsters):
		if m.col_anim.draw == False:
			window.blit(m.anim.image,m.rect.move(dx,dy))
			m.draw_update()
		else:
			window.blit(m.col_anim.image,m.rect.move(dx,dy))
			if m.draw_update() and m.delete_on_colision:
				status.level.monsters.remove(m)


	for i,s in enumerate(ANIM_SPRITES):
		if s.draw:
			window.blit(s.image,s.rect.move(dx,dy))
			s.update(pygame.time.get_ticks())
		else:
			ANIM_SPRITES.pop(i) #If draw is false, delete the reference

	#Paint Stick according to pymunk's body position
	#Looks a little bit hacky
	angle_degrees 	 = -math.degrees(stick.body.angle) + 180
	rotated_logo_img = pygame.transform.rotate(stick.baseImage, angle_degrees)
	offset = Vec2d(rotated_logo_img.get_size()) / 2.
	offset += (-dx, -dy)
	p = stick.body.position - offset
	window.blit(rotated_logo_img, p)

	#window.blit(stick.image,rect.move(dx,dy))

def update_pymunk_debug():
	# debug draw

	#print "Vel:",stick.body.velocity

	#scroll follows pymunk shape
	dx,dy = get_window_offset()

	#DRAW THE STICK
	ps = stick.shape.get_vertices()
	ps = [(p.x + dx, p.y +dy) for p in ps]
	ps += [ps[0]]
	pygame.draw.lines(window, yellow, False, ps, 2)
	pos = stick.body.position
	pygame.draw.circle(window, red, (int(pos.x)+dx,int(pos.y)+dy), 5, 2)

	#Draw the Items collision shape
	for item in status.level.items:
		if item.shape:
			ps = item.body.position + (dx,dy)
			p = (int(ps.x), int(ps.y))
			pygame.draw.circle(window, red, p, int(item.radius), 2)

	#Draw the monsters collision shape
	for monster in status.level.monsters:
		pos = monster.body.position
		#pygame.draw.rect(window, red, BF.pymunkBB_to_rect(monster.shape).move(dx + pos.x, dy + pos.y), 2)
		ps = monster.shape.get_vertices()
		ps = [(p.x + dx, p.y +dy) for p in ps]
		ps += [ps[0]]

		pygame.draw.lines(window, red , False, ps, 2)

	#TEXT
	# Display some text
	font = pygame.font.Font(None, 36)
	text = font.render("COLLISIONS", 2, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = window.get_rect().centerx
	window.blit(text, textpos)


	#If asked, draw the level collisions. HEAVY
	if status._DEBUG_PYMUNKLEVEL:
		#LOTS of lines, affects FPS
		for line in status.level.level_segments:
			body = line.body
			pv1 = body.position + line.a.rotated(body.angle)
			pv2 = body.position + line.b.rotated(body.angle)
			p1 = pv1.x + dx, pv1.y +dy
			p2 = pv2.x + dx, pv2.y +dy
			pygame.draw.lines(window, red, False, [p1,p2], 2)


def update_gui_timer_CF():
	"""
		Draw the timer using custom fonts
	"""

	#TIMING
	seconds         = int(status.get_elapsed_time())
	millis          = str(seconds - status.get_elapsed_time()).partition(".")[2]

	if seconds > 999:
		seconds = "999"
		millis = "00"

	seconds_images = number_gen.parse_number(int(seconds))
	millis_images = number_gen.parse_number(int(millis[0:2]))

	nw = seconds_images[0].get_rect().width

	#Bg Zeros (avoid a flickr)
	zero = number_gen.parse_number(0)[0]
	window.blit(pygame.transform.rotate(zero,-10),zero.get_rect().move((1+4)*nw,HEIGHT-zero.get_rect().height - 15))

	#Trailing zeros
	while len(seconds_images) < 3:
		zero = number_gen.parse_number(0)[0]
		seconds_images.insert(0,zero)


	ddimg = number_gen.get_doubledots()
	window.blit(pygame.transform.rotate(ddimg,-10),ddimg.get_rect().move(len(seconds_images)*nw,HEIGHT-ddimg.get_rect().height - 15))

	for i,s in enumerate(seconds_images):
		window.blit(pygame.transform.rotate(s,-10),s.get_rect().move(i*nw,HEIGHT-s.get_rect().height - 15))

	for i,s in enumerate(millis_images):
		window.blit(pygame.transform.rotate(s,-10),s.get_rect().move((i+4)*nw,HEIGHT-s.get_rect().height - 15))

def update_gui_timer_TTF():
	"""
		updates the timer using a TTF font
		@TODO::Check another font than the dafault font for menus,
		this font here, generates bouncing numbers not good
		for my eye
	"""
	window.blit(bg_timer_image,bg_timer_image.get_rect().move(0,400))
	time = round(status.get_elapsed_time(),2)
	ypad = 55
	xpad = 26

	if time > 999:
		time = "A Lot!"
		t=0
	else:
		#traling zeros space
		if time < 10:t = 2
		elif time < 100:t = 1
		else:t = 0

		for zero in range(t):
			timertxt = TIMERFONT.render(str("0"), 1, black)
			window.blit(timertxt, (10+zero*xpad, HEIGHT-ypad))

	timertxt = TIMERFONT.render(str(time), 1, black)
	window.blit(timertxt, (10+t*xpad, HEIGHT-ypad))

#Updates all the gui sprites
def update_gui():
	#LifeBar status
	window.blit(status.lifebar_image,status.lifebar_rect)

	#timer
	#update_gui_timer_CF()
	update_gui_timer_TTF()

#A fancy rotozoom for the stick death
def fancy_stick_death_animation():
        scale = 1
        while scale < 10:
                update_scene()
                stick.fancy_rotation_death(5,scale)
                scale+=0.2
                pygame.display.update()
                clock.tick(FPS)


##################################################################

 ######   ######  ########  ######## ######## ##    ##  ######
##    ## ##    ## ##     ## ##       ##       ###   ## ##    ##
##       ##       ##     ## ##       ##       ####  ## ##
 ######  ##       ########  ######   ######   ## ## ##  ######
      ## ##       ##   ##   ##       ##       ##  ####       ##
##    ## ##    ## ##    ##  ##       ##       ##   ### ##    ##
 ######   ######  ##     ## ######## ######## ##    ##  ######

##################################################################

#InGame menu Screen
def ingame_menu_screen(menu,rotate=True,x=200,y=200):
	"""
	 Paints a menu on screen while keeping the painting going behind.
	  - menu (the menu to print)
	  - rotate (keeps the stick rotating) --- True in fancy gameover, False in Pause
	"""
	update_scene()
	update_gui()
	if rotate: stick.rotate(1)
	draw_menu(menu,x,y)

#InGame menu Screen
def menu_screen(menu,rotate=True,x=200,y=200):
	"""
	 Paints a menu on screen
	  - menu (the menu to print)
	  - rotate (keeps the stick rotating) --- True in fancy gameover, False in Pause
	"""
	update_gui()
	if rotate: stick.rotate(1)
	draw_menu(menu,x,y)

#
# What to draw on screen for a newname
#
def newname_screen():
	window.fill(white)

	window.blit(INPUT_KEYS_BG,INPUT_KEYS_BG.get_rect())

	namefont    = FONT.render(INPUT_KEYS.text, 1, black)
	window.blit(namefont, (100, 200))

	for i,err in enumerate(INPUT_KEYS.get_error()):
		errorfont = FONT.render(err, 1, red)
		window.blit(errorfont, (100, 250+i*40))

#Game Over Screen


def level_selection_screen():
	level_select_menu()

def pack_selection_screen():
	pack_select_menu()

def goal_screen():
	"""
		Update screen when goal. Different situations to handle, controlled
		by status.SUBSTAT
			1 - Move the stick to the center of the goal
			2 - Do a fancy flip Screen animation
			3 - Show a screen with the results
			4 - Give options: Repeat or Next level
	"""
	update_scene()
	stick.rotate(25)

	if status.SUBSTAT == 0:
		#Move Stick to Goal center
		ox = status.level.goal_sprite.rect.center[0];
		oy = status.level.goal_sprite.rect.center[1];

		if not stick.move_towards_position(ox,oy):
			stick.movement()
			space.step(1)
		else:
			stick.enable_disable_movement()
			status.SUBSTAT = 1

	elif status.SUBSTAT == 1:
		#Goal Running there
		gtext_sprite.incr_move(-10,0)
		update_scene_goal()
		if gtext_sprite.out_of_screen():
			status.SUBSTAT = 2
			gtext_sprite.move(800,250) #return to begining

	elif status.SUBSTAT == 2:
		TRANSITION.setActive()
		status.SUBSTAT = 0     #reset to original
		status.set_game_status(cStatus._STAT_LEVELRECORD)

def records_screen():
	"""
		Show the records
	"""

	#Some Entering animation would be nice
	#if status.SUBSTAT == 0:
	status.SUBSTAT = 1 #Skip the first stat (saved for further animation)

	if status.SUBSTAT == 1:
		draw_menu(records_menu,WIDTH-200,HEIGHT-210)
		update_scene_records()

#
# Draw the level selection Screen
# @TODO: this is very specific for the level selection... but it's almost the same as the other menus, so maybe can be joined in draw menu with a flag?
#
def level_select_menu():
        '''
                level_select_menu:
                This menu moves all the entries up and down leaving
                the selected one always centered
        '''
	increment_px_y = 29

	if levels_menu.background != None:
		sy = 0
		if levels_menu.background_scroll == True:
			sy = levels_menu.current * increment_px_y
			window.blit(levels_menu.background,levels_menu.background.get_rect().move(0,-sy))

		y = 228 - (levels_menu.current * increment_px_y)
		x = 150
		color = yellow

		for index,me in enumerate(levels_menu.options):
			if levels_menu.current == index: color = levels_menu.select_color
			else: color = levels_menu.color

			if settings.isLevelCompleted(level_list.level_uuid(index)):
				window.blit(tick_sprite,tick_sprite.get_rect().move(x-20,y))

			render_font = FONT.render(me, 1, color)
			window.blit(render_font, (x, y))
			y += increment_px_y

def pack_select_menu():
        '''
                pack_select_menu:
                Actually does the same as level_select_menu
                But the idea is to do that a little bit different
        '''
	increment_px_y = 29

	if packs_menu.background != None:
		sy = 0
		if packs_menu.background_scroll == True:
			sy = packs_menu.current * increment_px_y
			window.blit(packs_menu.background,packs_menu.background.get_rect().move(0,-sy))

		y = 228 - (packs_menu.current * increment_px_y)
		x = 150
		color = yellow

		#assuming that lock and openlock are of the same size
		lock_rect = locked_sprite.get_rect();
		lock_rect_w = lock_rect[2]

		for index,me in enumerate(packs_menu.options):
			draw_lock = True
			if packs_menu.current == index:
					if packlist.isPackOpen(packs_menu.current,settings.total_levels_cleared()):
						color = packs_menu.select_color
						draw_lock = False
					else:
						color = dimred
			else:
				if packlist.isPackOpen(index,settings.total_levels_cleared()):
					color = packs_menu.color
					draw_lock = False
				else:
					color = gray

			if draw_lock:
				window.blit(locked_sprite,lock_rect.move(x-lock_rect_w,y))
			else:
				window.blit(openlock_sprite,lock_rect.move(x-lock_rect_w,y))




			render_font = FONT.render(me, 1, color)
			window.blit(render_font, (x, y))
			y += increment_px_y


#
# Draws a menu on screen
# - menu (the menu to draw)
#
def draw_menu(menu,sx=200,sy=160):

	if menu.background != None:
		window.blit(menu.background,menu.background.get_rect())

        x = sx
        y = sy

        for index,me in enumerate(menu.options):
                if menu.current == index: color = menu.select_color
                else: color = menu.color

                render_font = FONT.render(me, 1, color)
                window.blit(render_font, (x, y))
                y += 39

#
# Draws everything of the playing level screen
#
def playing_screen():
	update_scene()
	update_gui()
	stick.rotate()
	stick.movement()

	#DEBUG PYMUNK
	if status._DEBUG_PYMUNK:
		update_pymunk_debug()



def finish_level():
	settings.add_cleared_level(status.level.get_uuid())
	time = status.get_elapsed_time()
	status.set_game_status(cStatus._STAT_GOAL)
	records = status.level.save_record(settings.get_username(),time)



###############################################

##     ##    ###    #### ##    ##
###   ###   ## ##    ##  ###   ##
#### ####  ##   ##   ##  ####  ##
## ### ## ##     ##  ##  ## ## ##
##     ## #########  ##  ##  ####
##     ## ##     ##  ##  ##   ###
##     ## ##     ## #### ##    ##

###############################################
def gaming_status(debug=False):
	monster_logic()
	playing_screen()
	#debug_onscreen(colision)
	#Unset invincibility when needed
	status.unset_invincible_by_time()

	#check if goal
	if status.level.stick_in_goal(stick):
		if debug: return True
		finish_level()

	#check if dead
	if status.lives <= 0:
		if debug: return True
		fancy_stick_death_animation()

	#Game Over
	space.step(1)


def main_game():
        #Main Game Function
	while 1:
		for event in pygame.event.get(): event_handler(event)
		window.fill(white)

		#Playing Level
		if status.GAME_STAT == cStatus._STAT_GAMING:
			gaming_status()

		elif status.GAME_STAT == cStatus._STAT_GAMEOVER:
			stick.fancy_rotation_death(0,10)
			ingame_menu_screen(gover_menu,y=175)

			#Level Selection
		elif status.GAME_STAT == cStatus._STAT_LEVELSEL:
			level_selection_screen()

		elif status.GAME_STAT == cStatus._STAT_PACKSEL:
			pack_selection_screen()

		#Goal
		elif status.GAME_STAT == cStatus._STAT_GOAL:
			goal_screen()

		#After Goal, Level Records Screen
		elif status.GAME_STAT == cStatus._STAT_LEVELRECORD:
			records_screen()

		#Pause Menu
		elif status.GAME_STAT == cStatus._STAT_PAUSE:
			ingame_menu_screen(pause_menu,rotate=False,x=200,y=160)

		#Main Menu
		elif status.GAME_STAT == cStatus._STAT_MAINMENU:
			menu_screen(main_menu,rotate=False)

		#settings Menu
		elif status.GAME_STAT == cStatus._STAT_SETTINGS:
			menu_screen(settings_menu,rotate=False)

		elif status.GAME_STAT == cStatus._STAT_NEWNAME:
			newname_screen()

		draw_transition() #transition always on top

		pygame.display.update()
		clock.tick(FPS)

def main_debug(filename):
	load_level_filename(filename)
	status.set_game_status(cStatus._STAT_GAMING)
	finish = False
	status._DEBUG_DEATH = True
	status._DEBUG_COLLISION = True
	#space.add(stick.body, stick.shape)
	while not finish:
		for event in pygame.event.get(): event_handler(event)
		finish = gaming_status(debug=True)

		pygame.display.update()
		clock.tick(FPS)

def main():
	if len(sys.argv) > 1:
		main_debug(sys.argv[1])
	else:
		main_game()

if __name__ == '__main__': main()
