#######################
# Main pykurin entrance
# @author: Jordi Castells Sala
#
#
#######################

import sys, pygame
import functions as BF
from cPal import cPal
from cLevel import cLevel
from cAnimSprite import cAnimSprite
from cStatus import cStatus
from cMenu import cMenu
from cLevelList import cLevelList

pygame.init()

size = width, height = 800, 600

#DEBUG
COLLISION=True

#some colors definitions
black = 0, 0, 0
yellow = 255, 255, 0
green = 0,255,0
white = 255,255,255


clock = pygame.time.Clock ()
window = pygame.display.set_mode(size)

#####
# SPRITE LOADING
#####
#HitWall sprite
imgset = BF.load_and_slice_sprite(32,32,'explosion.png');
tsprite = cAnimSprite(imgset)

#Lives sprite
imgsetlives = BF.load_and_slice_sprite(192,64,'livemeter.png');


#####
# STATUS CREATION
#####
#Status load
status = cStatus(imgsetlives)


#First Base Load
status.level = cLevel("levels/lvl000001.prop")
stick = cPal(status.level.startx,status.level.starty,0);

#General arrays with Sprites
BASIC_SPRITES=[]
ANIM_SPRITES=[]

BASIC_SPRITES.append(status.level)
BASIC_SPRITES.append(stick)
ANIM_SPRITES.append(tsprite)


#####
# MENUS CREATION
#####

# Level Selection Menu
level_list = cLevelList("levels")
levels_menu = cMenu(level_list.get_levelnames(),0,yellow,green)
levels_menu.set_background("backgrounds/levelsel.png")

#Game Over Menu
gover_menu_texts = 'Try again' , 'Return to level Select' , 'Exit game'
gover_menu = cMenu(gover_menu_texts,0,yellow,green)


#Debug Options
def key_debug_actions(event):
#the global var collision may be modified
        global COLLISION

        if event.key == pygame.K_F1:
                if COLLISION: COLLISION = False
                else: COLLISION = True
                
#Main Key Handler
def key_handler(event):
        
        
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: stick.move_down();
                elif event.key == pygame.K_UP: stick.move_up();
                elif event.key == pygame.K_LEFT: stick.move_left();
                elif event.key == pygame.K_RIGHT: stick.move_right();

                #Debug Handlers
                key_debug_actions(event)
        
        elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN: stick.move_up();
                elif event.key == pygame.K_UP: stick.move_down();
                elif event.key == pygame.K_LEFT: stick.move_right();
                elif event.key == pygame.K_RIGHT: stick.move_left();

        #print event

#Game Over Menu Handler
def key_menu_handler(event,menu):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: menu.menu_down();
                elif event.key == pygame.K_UP: menu.menu_up();
                elif event.key == pygame.K_RETURN: game_over_menu_selection();

#Level Menu Handler
def key_level_menu_handler(event,menu):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: menu.menu_down();
                elif event.key == pygame.K_UP: menu.menu_up();
                elif event.key == pygame.K_RETURN: load_level(levels_menu.current+1)

#
# MAIN ENTRANCE FOR 
#Event Handler
#
#
def event_handler(event):
        """ 
                Different handlers for different events in different status
                0 - Gaming screen
                1 - Game Over screen
        """
        if event.type == pygame.QUIT: pygame.quit();sys.exit()
        
        #Gaming
        if status.GAME_STAT == 0:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_handler(event)
        
        #Game Over Screen
        elif status.GAME_STAT == 1:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_menu_handler(event,gover_menu)

        #Game Over Screen
        elif status.GAME_STAT == 2:
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP: key_level_menu_handler(event,levels_menu)



def load_level(level_num):
        print "levels/lvl"+str(level_num).zfill(6)+".prop"
        status.level = cLevel("levels/lvl"+str(level_num).zfill(6)+".prop")
        stick.__init__(status.level.startx,status.level.starty,0);
        
        status.reset_lives()
        status.GAME_STAT = 0
        status.current_level = level_num
        status.reset_timer()

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

def level_menu_selection():
        status.GAME_STAT = 0

#Collision game handling
# - show collision sprite
# - Move stick back a little bit giving time to react
def colision_handler(cx,cy):
        tsprite.move(cx,cy)
        tsprite.draw = True
        stick.flip_rotation_tmp()
        
        if status.decrease_lives(): fancy_stick_death_animation()



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
        title           = myfont.render("Debug", 1, yellow)
        stickpos        = myfont.render("Stick:"+str(stick.rect.center), 1, yellow)
        stickcollides   = myfont.render("collides:"+str(colides), 1, yellow)
        fps             = myfont.render("FPS:"+str(clock.get_fps()),1,yellow)

        elapsed_time    = myfont.render("TIME:"+timestr,1,yellow)
        
        # put the label object on the screen at point x=100, y=100
        window.blit(title, (0, 0))
        window.blit(stickpos, (0, 20))
        window.blit(stickcollides, (0, 40))
        window.blit(fps, (0, 60))
        window.blit(elapsed_time, (0, 80))

        if COLLISION == False:
                colisionOnOff   = myfont.render("COLLISION OFF",1,yellow)
                window.blit(colisionOnOff, (400, 0))


#A fancy rotozoom for the stick death
def fancy_stick_death_animation():
        scale = 1
        while scale < 10:
                
                window.fill(white)
                update_scene()
                stick.fancy_rotation_death(5,scale)
                scale+=0.1
                pygame.display.update()
                clock.tick(30)
                

#updates all the needed images/sprites
def update_scene():
        #for o in BASIC_SPRITES:
        window.blit(status.level.image,status.level.rect)
        window.blit(stick.image,stick.rect)
        
        for s in ANIM_SPRITES:
                if s.draw:
                        window.blit(s.image,s.rect)
                        s.update(pygame.time.get_ticks())
        
        #LifeBar status
        window.blit(status.lifebar_image,status.lifebar_rect)

def game_over_screen():
        
        window.fill(white)
        stick.fancy_rotation_death(0,10)
        update_scene()
        stick.rotate(1)
        game_over_menu()


def level_selection_screen():
        window.fill(white)
        level_select_menu()

#
# Draw the level selection Screen
#
# @TODO THE LEVELS MUST BE ORDERED
def level_select_menu():
        '''
                level_select_menu:
                This menu moves all the entries up and down leaving
                the selected one always centered
        '''

        if levels_menu.background != None:
                window.blit(levels_menu.background,levels_menu.background.get_rect())

        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 30)
        
        #center - (number of lower levels)
        
        y = 300 - (levels_menu.current * 50)
        x = 200
        #y = 200
        color = yellow

        for index,me in enumerate(levels_menu.options):
                if levels_menu.current == index: color = levels_menu.select_color
                else: color = gover_menu.color

                render_font = myfont.render(me, 1, color) 
                window.blit(render_font, (x, y))
                y += 50

#
#Draw the game over menu
#
def game_over_menu():
        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 30)
        
        x = 200
        y = 200
        color = yellow

        for index,me in enumerate(gover_menu.options):
                if gover_menu.current == index: color = gover_menu.select_color
                else: color = gover_menu.color

                render_font = myfont.render(me, 1, color) 
                window.blit(render_font, (x, y))
                y += 50

#
# Draws everything of the playing level screen
#
def playing_screen():
        window.fill(white)
        update_scene()
        stick.rotate(3)
        stick.movement()


def main():
        #Main Game Function
        while 1:
                for event in pygame.event.get(): event_handler(event)
                
                #Playing Level
                if status.GAME_STAT == 0:

                        #Debug Purposes
                        if COLLISION:
                                colision,cx,cy = status.level.stick_collides(stick);
                                if colision: colision_handler(cx,cy)
                        
                        playing_screen()                        
        
                        debug_onscreen(colision)
                
                #Game Over
                elif status.GAME_STAT == 1: 
                        game_over_screen()
                
                #Level Selection
                elif status.GAME_STAT == 2:
                        level_selection_screen()
                
                
                pygame.display.update()
                clock.tick(30) 


if __name__ == '__main__': main()  
