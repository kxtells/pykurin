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

#some colors definitions
black = 0, 0, 0
yellow = 255, 255, 0
green = 0,255,0


clock = pygame . time . Clock ()
window = pygame.display.set_mode(size)


#First Base Load
level = cLevel("levels/lvl2.prop")
stick = cPal(level.startx,level.starty,0);
level_list = cLevelList("levels")

#HitWall sprite
imgset = BF.load_and_slice_sprite(32,32,'explosion.png');
tsprite = cAnimSprite(imgset)

#Lives sprite
imgsetlives = BF.load_and_slice_sprite(192,64,'livemeter.png');

#General arrays with Sprites
BASIC_SPRITES=[]
ANIM_SPRITES=[]

BASIC_SPRITES.append(level)
BASIC_SPRITES.append(stick)
ANIM_SPRITES.append(tsprite)

#Status load
status = cStatus(imgsetlives)


#
# Levels Menu
#
levels_menu = cMenu(level_list.get_levelnames(),0,yellow,green)


#
#Game Over Menu
#
gover_menu_texts = 'Try again' , 'Exit game'
gover_menu = cMenu(gover_menu_texts,0,yellow,green)


#Main Key Handler
def key_handler(event):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: stick.move_down();
                elif event.key == pygame.K_UP: stick.move_up();
                elif event.key == pygame.K_LEFT: stick.move_left();
                elif event.key == pygame.K_RIGHT: stick.move_right();
        #Inverse to stop the movement
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
                elif event.key == pygame.K_RETURN: game_over_menu_selection()

#Level Menu Handler
def key_level_menu_handler(event,menu):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN: menu.menu_down();
                elif event.key == pygame.K_UP: menu.menu_up();
                elif event.key == pygame.K_RETURN: level_menu_selection();

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
        level = cLevel("levels/lvl2.prop")
        stick.__init__(level.startx,level.starty,0);
        status.reset_lives()
        
        status.GAME_STAT = 0


def game_over_menu_selection():
        #Try again. Reload everything and return to game mode
        if gover_menu.current == 0:
                load_level(1)


        #Exit Application
        elif gover_menu.current == 1:
                pygame.quit()
                sys.exit()

def level_menu_selection():
        print "aa"
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
        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 14)
        # apply it to text on a label
        title           = myfont.render("Debug", 1, yellow)
        stickpos        = myfont.render("Stick:"+str(stick.rect.center), 1, yellow)
        stickcollides   = myfont.render("collides:"+str(colides), 1, yellow)
        # put the label object on the screen at point x=100, y=100
        window.blit(title, (0, 0))
        window.blit(stickpos, (0, 20))
        window.blit(stickcollides, (0, 40))



#A fancy rotozoom for the stick death
def fancy_stick_death_animation():
        scale = 1
        while scale < 10:
                
                window.fill(black)
                update_scene()
                stick.fancy_rotation_death(5,scale)
                scale+=0.1
                pygame.display.update()
                clock.tick(100)
                

#updates all the needed images/sprites
def update_scene():
        for o in BASIC_SPRITES:
                window.blit(o.image,o.rect)
        
        for s in ANIM_SPRITES:
                if s.draw:
                        window.blit(s.image,s.rect)
                        s.update(pygame.time.get_ticks())
        
        #LifeBar status
        window.blit(status.lifebar_image,status.lifebar_rect)

def game_over_screen():
        
        window.fill(black)
        stick.fancy_rotation_death(0,10)
        update_scene()
        stick.rotate(1)
        game_over_menu()


def level_selection_screen():
        window.fill(black)
        level_select_menu()

#
# Draw the level selection Screen
#
# @TODO MAKE IT WORK
def level_select_menu():
        '''
                level_select_menu:
                This menu moves all the entries up and down leaving
                the selected one always centered
        '''
        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 30)
        
        x = 200
        y = 200
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
        window.fill(black)
        update_scene()
        stick.rotate(5)
        stick.movement()


def main():
        #Main Game Function
        while 1:
                for event in pygame.event.get(): event_handler(event)
                
                #Playing Level
                if status.GAME_STAT == 0:
                        playing_screen()
                        
                        colision,cx,cy = level.stick_collides(stick);
                
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
                clock.tick(100) 


if __name__ == '__main__': main()  
