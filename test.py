#######################
# Main pykurin entrance
# @author: Jordi Castells Sala
#
#
#######################

import sys, pygame
import functions as BF
import cAnimSpriteFactory
import cCustomFont
from cPal import cPal
from cLevel import cLevel
from cAnimSprite import cAnimSprite
from cStatus import cStatus
from cMenu import cMenu
from cLevelList import cLevelList

pygame.init()

size = width, height = 640, 480

#DEBUG
DEBUG_COLLISION=False
DEBUG_DEATH=False

#some colors definitions
black = 0, 0, 0
yellow = 255, 255, 0
green = 0,255,0
blue = 0,0,150
red = 255,0,0
white = 255,255,255


clock = pygame.time.Clock ()
window = pygame.display.set_mode(size,pygame.DOUBLEBUF)
icon   = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_caption("PYKURIN Alpha")
pygame.display.set_icon(icon)
#######################################
#
# BASIC SPRITE LOADING
#
#######################################
#sprite factory
SPRITE_FAC = cAnimSpriteFactory.cAnimSpriteFactory()


tsprite = SPRITE_FAC.get_explosion_sprite()

#Goal Text
imgset = BF.load_and_slice_sprite(300,150,'goal_text.png');
gtext_sprite = cAnimSprite(imgset)
gtext_sprite.move(800,300)

#New Record Text
imgset = BF.load_and_slice_sprite(230,100,'newrecord.png');
newrecord_sprite = cAnimSprite(imgset,1)
newrecord_sprite.move(450,150)
print imgset

#Lives sprite
imgsetlives = BF.load_and_slice_sprite(192,64,'livemeter.png');


#Custom Numbers
imgset_numbers = BF.load_and_slice_sprite(50,50,'numbers.png');
number_gen = cCustomFont.cCustomFont(imgset_numbers)


#######################################
#
# STATUS CREATION
#
#######################################
#Status load
status = cStatus(imgsetlives,width,height)

#First Base Load
status.level = cLevel("levels/lvl000001.prop")
stick = cPal(status.level.startx,status.level.starty,0);

#General arrays with Sprites
BASIC_SPRITES=[]
ANIM_SPRITES=[]

BASIC_SPRITES.append(status.level)
BASIC_SPRITES.append(stick)
ANIM_SPRITES.append(tsprite)


#######################################
#
# GAME MENUS CREATION
#
#######################################
# Level Selection Menu
level_list = cLevelList("levels")
levels_menu = cMenu(level_list.get_levelnames(),0,blue,red)
levels_menu.set_background("backgrounds/squared_paper_title.png")
levels_menu.background_scroll = True

#Game Over Menu
gover_menu_texts = 'Try again' , 'Return to level Select' , 'Exit game'
gover_menu = cMenu(gover_menu_texts,0,blue,red)
gover_menu.set_background("backgrounds/piece_paper.png")

#Pause Over Menu
pause_menu_texts = 'Continue', 'Restart Level' , 'Return to level Select' , 'Exit game'
pause_menu = cMenu(pause_menu_texts,0,blue,red)
pause_menu.set_background("backgrounds/piece_paper.png")


#Records Menu
records_menu_texts = 'Next Level', 'Repeat' , 'Return to level Select'
records_menu = cMenu(records_menu_texts,0,blue,red)
records_menu.set_background("backgrounds/records_screen.png")

#######################################
#
# KEY HANDLERS
#
#######################################
#Debug Options
def key_debug_actions(event):
#the global var collision may be modified
        global DEBUG_COLLISION
        global DEBUG_DEATH

        if event.key == pygame.K_F1:
                if DEBUG_COLLISION: DEBUG_COLLISION = False
                else: DEBUG_COLLISION = True
        elif event.key == pygame.K_F2:
                if DEBUG_DEATH: DEBUG_DEATH = False
                else: DEBUG_DEATH = True
                
#Main Key Handler For the GAMING STATUS
def key_handler(event):
        #Do not listen keystrokes is keyboard is disabled
        if not status.is_keyboard_enabled(): return
        
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

        #print event

#Game Over Menu Handler
def key_menu_handler(event,menu):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: menu.menu_down();
                elif event.key == pygame.K_UP: menu.menu_up();
                elif event.key == pygame.K_RETURN: menu.action_function()
		else:
			if menu.event_function != None: menu.event_function(event)

#Specific Pause menu handler
# (for giving the change to exit the menu without selecting)
def pause_menu_events(event):
	if event.key == pygame.K_ESCAPE or event.key == pygame.K_p: status.unpause_game()

#
# MAIN ENTRANCE FOR EVENT HANDLING 
#
def event_handler(event):
        """ 
                Different handlers for different events in different status
        	Check cStatus class for status definitions
	"""
        if event.type == pygame.QUIT: pygame.quit();sys.exit()
        
        #Gaming
        if status.GAME_STAT == cStatus._STAT_GAMING:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_handler(event)
        
        #Game Over Screen
        elif status.GAME_STAT == cStatus._STAT_GAMEOVER:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,gover_menu)

        #PAUSE Screen
        elif status.GAME_STAT == cStatus._STAT_PAUSE:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,pause_menu)

	#Select level Screen
        elif status.GAME_STAT == cStatus._STAT_LEVELSEL:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,levels_menu)

	#Records level Screen
        elif status.GAME_STAT == cStatus._STAT_LEVELRECORD:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,records_menu)



#######################################
#
# SPECIFIC MENU FUNCTIONS AND BINDINGS
#
#######################################

#Load a Specific Level (needed for level menu function)
# @TODO : Maybe better in another place or python file
def load_level(level_num):
        status.level = cLevel(level_list.levelfiles[level_num])
        stick.__init__(status.level.startx,status.level.starty,0,status.level.stick);
        #stick.load_stick_image(status.level.stick)
        
        status.reset_lives()
        status.GAME_STAT = cStatus._STAT_GAMING 
	status.SUBSTAT = 0
        status.current_level = level_num
        status.reset_timer()

#Records menu selection function
def records_menu_selection():
	if records_menu.current == 0:
		status.current_level += 1
                load_level(status.current_level)

	elif records_menu.current == 1:
                load_level(status.current_level)
	
	elif records_menu.current == 2:
		status.GAME_STAT = cStatus._STAT_LEVELSEL

#Game over menu selection function
def game_over_menu_selection():
        #Try again. Reload everything and return to game mode
        if gover_menu.current == 0:
                load_level(status.current_level)

        #Return to Level Select Menu
        elif gover_menu.current == 1:
                status.GAME_STAT = 2
        
        #Exit Application
        elif gover_menu.current == 2:
                pygame.quit()
                sys.exit()

#Level Menu Selection Function
def level_menu_selection():
        load_level(levels_menu.current)
        status.GAME_STAT = 0

#Pause Menu selection Function
def pause_menu_selection():
        #Continue, change to game mode
        if pause_menu.current == 0:
		status.unpause_game()

	#Reset Level
        elif pause_menu.current == 1:
                load_level(status.current_level)
	
	#Return to Level Select Menu
        elif pause_menu.current == 2:
                status.GAME_STAT = 2
        
        #Exit Application
        elif pause_menu.current == 3:
                pygame.quit()
                sys.exit()

#MENU BINDINGS
gover_menu.action_function = game_over_menu_selection
levels_menu.action_function = level_menu_selection
pause_menu.action_function = pause_menu_selection
records_menu.action_function = records_menu_selection

pause_menu.event_function = pause_menu_events



#######################################
#
# GAME HANDLERS
#
#######################################


#Collision game handling
def colision_handler(cx,cy):
        """
                All actions triggered by a colision
                 - add a collision sprite to print
                 - Change stick rotation direction for a time
                 - Make the stick jump back
        """   
        
	#Create a 'collision' animated sprite
	tsprite = SPRITE_FAC.get_explosion_sprite(cx,cy)
	ANIM_SPRITES.append(tsprite)        


	#Move the Stick back from the collision place
	stick.jump_back(cx,cy)
        stick.flip_rotation_tmp()

	#Only if not in debug mode or invincible mode
        if not DEBUG_DEATH:
		if not status.invincible:
			status.set_invincible()
                	if status.decrease_lives(): fancy_stick_death_animation()


def item_colisions():
	for i,m in enumerate(status.level.items):
		if stick.collides(m):
			if not status.invincible:
				m.col_anim.draw = True
				ANIM_SPRITES.append(m.col_anim)
				m.onCollision(stick) #different monster handlers
				status.set_invincible()
				tsprite = SPRITE_FAC.get_boing_sprite(m.rect.center[0],m.rect.center[1])
				ANIM_SPRITES.append(tsprite)
				#stick.jump_back()

#########
#
# DRAWING FUNCTIONS
#
##########

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
        
        # put the label objects on the screen
        window.blit(title, (0, 0))
        window.blit(stickpos, (0, 20))
        window.blit(stickcollides, (0, 40))
        window.blit(stickinvincib, (0, 60))
        window.blit(fps, (0, 80))
        window.blit(elapsed_time, (0, 100))

        if DEBUG_COLLISION == True:
                colisionOnOff   = myfont.render("COLLISION OFF",1,red)
                window.blit(colisionOnOff, (400, 0))
        if DEBUG_DEATH == True:
                deathOnOff      = myfont.render("DEATH OFF",1,red)
                window.blit(deathOnOff, (400, 20))


#Updates all the needed images/sprites for goal Screen
def update_scene_goal():
        window.blit(gtext_sprite.image,gtext_sprite.rect)
        gtext_sprite.update(pygame.time.get_ticks())

#@TODO: THis has to be beautiful
def update_scene_records():
	records = status.level.records
	player_index = status.level.player_record_index

	if player_index > -1:
        	window.blit(newrecord_sprite.image,newrecord_sprite.rect)
                newrecord_sprite.update(pygame.time.get_ticks())

	# pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 30)
	
	for i,r in enumerate(records):
		player = r[1]
		time = r[0]
		
		seconds         = int(time)
        	millis          = str(seconds - time).partition(".")[2]
        	timestr         = str(seconds)+":"+millis[0:3]
        	
		if player_index == i:
			bgcolor = yellow
		else:
			bgcolor = None

		timefont	= myfont.render(timestr, 1, blue,bgcolor)
		namefont	= myfont.render(player, 1, blue,bgcolor)
        	
		window.blit(namefont, (200, 50*(i+3)))
		window.blit(timefont, (100, 50*(i+3)))


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

        dx = -(stick.rect.center[0]-width/2)
        dy = -(stick.rect.center[1]-height/2)

        window.blit(status.level.image,status.level.rect.move(dx,dy))

        window.blit(status.level.goal_sprite.image,status.level.goal_sprite.rect.move(dx,dy))
        status.level.goal_sprite.update(pygame.time.get_ticks())
        
        for i,s in enumerate(ANIM_SPRITES):
                if s.draw:
                        window.blit(s.image,s.rect.move(dx,dy))
                        s.update(pygame.time.get_ticks())
		else:
			ANIM_SPRITES.pop(i) #If draw is false, delete the reference
			
	#Items InGame
	for i,m in enumerate(status.level.items):
                if m.col_anim.draw == False: 
			window.blit(m.anim.image,m.rect.move(dx,dy))
			m.anim.update(pygame.time.get_ticks())
        

	window.blit(stick.image,stick.rect.move(dx,dy))
        

#Updates all the gui sprites
def update_gui():
        #LifeBar status
        window.blit(status.lifebar_image,status.lifebar_rect)
        
	#TIMING
        seconds         = int(status.get_elapsed_time())
        millis          = str(seconds - status.get_elapsed_time()).partition(".")[2]

	seconds_images = number_gen.parse_number(int(seconds))
	millis_images = number_gen.parse_number(int(millis[0:2]))

	nw = seconds_images[0].get_rect().width

	#Bg Zeros (avoid a flickr)
	zero = number_gen.parse_number(0)[0]
	window.blit(pygame.transform.rotate(zero,-10),zero.get_rect().move((1+4)*nw,height-zero.get_rect().height - 15))
	
	#Trailing zeros
	while len(seconds_images) < 3:
		zero = number_gen.parse_number(0)[0]
		seconds_images.insert(0,zero)

	
	ddimg = number_gen.get_doubledots()
	window.blit(pygame.transform.rotate(ddimg,-10),ddimg.get_rect().move(len(seconds_images)*nw,height-ddimg.get_rect().height - 15))
	
	for i,s in enumerate(seconds_images):
		window.blit(pygame.transform.rotate(s,-10),s.get_rect().move(i*nw,height-s.get_rect().height - 15))

	for i,s in enumerate(millis_images):
		window.blit(pygame.transform.rotate(s,-10),s.get_rect().move((i+4)*nw,height-s.get_rect().height - 15))

#A fancy rotozoom for the stick death
def fancy_stick_death_animation():
        scale = 1
        while scale < 10:
                update_scene()
                stick.fancy_rotation_death(5,scale)
                scale+=0.1
                pygame.display.update()
                clock.tick(30)

#InGame menu Screen
def ingame_menu_screen(menu,rotate=True):
	"""
	 Paints a menu on screen while keeping the painting going behind.
	  - menu (the menu to print)
	  - rotate (keeps the stick rotating) --- True in fancy gameover, False in Pause
	"""
	update_scene()
	update_gui()
	if rotate: stick.rotate(1)
	draw_menu(menu)

#Game Over Screen


def level_selection_screen():
        level_select_menu()


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
                ox = status.level.goal_sprite.rect.x;
                oy = status.level.goal_sprite.rect.y;

                if not stick.move_towards_position(ox,oy):
                        stick.movement()
                else:
                        stick.enable_disable_movement()
                        status.SUBSTAT = 1

        elif status.SUBSTAT == 1:
                #Goal Running there
                gtext_sprite.incr_move(-10,0)
                update_scene_goal()
                if gtext_sprite.out_of_screen():
                        status.SUBSTAT = 2
                        gtext_sprite.move(800,300) #return to begining

        elif status.SUBSTAT == 2:
                status.SUBSTAT = 0     #reset to original
        	status.GAME_STAT = cStatus._STAT_LEVELRECORD

def records_screen():
	"""
		Show the records
	"""
	
	#Some Entering animation would be nice
        #if status.SUBSTAT == 0:
	status.SUBSTAT = 1 #Skip the first stat (saved for further animation)
	
	if status.SUBSTAT == 1:
		draw_menu(records_menu,width-200,height-200)
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

        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 25)

        y = 285 - (levels_menu.current * increment_px_y)
        x = 150
        color = yellow

        for index,me in enumerate(levels_menu.options):
                if levels_menu.current == index: color = levels_menu.select_color
                else: color = levels_menu.color

                render_font = myfont.render(me, 1, color) 
                window.blit(render_font, (x, y))
                y += increment_px_y

#
# Draws a menu on screen 
# - menu (the menu to draw)
#
def draw_menu(menu,sx=200,sy=165):
        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 20)
        
	if menu.background != None:
		window.blit(menu.background,menu.background.get_rect())
        
        x = sx
        y = sy

        for index,me in enumerate(menu.options):
                if menu.current == index: color = menu.select_color
                else: color = menu.color

                render_font = myfont.render(me, 1, color) 
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


def finish_level():
        time = status.get_elapsed_time()
	status.GAME_STAT = cStatus._STAT_GOAL
	records = status.level.save_record('kxtells',time)

def main():
        #Main Game Function
        while 1:
                for event in pygame.event.get(): event_handler(event)
                window.fill(white)

                #Playing Level
		if status.GAME_STAT == cStatus._STAT_GAMING:

                        #Debug Purposes
                        if not DEBUG_COLLISION:
				#Level Colision
                                colision,cx,cy = status.level.stick_collides(stick);
                                if colision: colision_handler(cx,cy)
				#Monster colision
				item_colisions()
                        
                        playing_screen()                        
                        debug_onscreen(colision)
			#Unset invincibility when needed
			status.unset_invincible_by_time()

                        if status.level.stick_in_goal(stick): 
				finish_level()
                
                #Game Over
                elif status.GAME_STAT == cStatus._STAT_GAMEOVER: 
        		stick.fancy_rotation_death(0,10)
			ingame_menu_screen(gover_menu)
                
                #Level Selection
                elif status.GAME_STAT == cStatus._STAT_LEVELSEL:
                        level_selection_screen()

		#Goal
                elif status.GAME_STAT == cStatus._STAT_GOAL:
                        goal_screen()
                
		#After Goal, Level Records Screen
                elif status.GAME_STAT == cStatus._STAT_LEVELRECORD:
			records_screen()

		#Pause Menu
                elif status.GAME_STAT == cStatus._STAT_PAUSE: 
			ingame_menu_screen(pause_menu,rotate=False)
                
                
                pygame.display.update()
                clock.tick(30) 


if __name__ == '__main__': main()  
