from ConfigParser import SafeConfigParser
import pygame
from cAnimSprite import cAnimSprite
import functions as BF
import cBouncer

class cLevel:
	
	def __init__(self,file):
		parser = SafeConfigParser()
		parser.read(file)

		self.name 	= parser.get('options','name')
		self.startx 	= int(parser.get('options','startx'))
		self.starty 	= int(parser.get('options','starty'))
		self.imgcol 	= pygame.image.load(parser.get('options','collision')).convert_alpha();
		self.image 	= pygame.image.load(parser.get('options','background')).convert_alpha();
		self.bg 	= pygame.image.load(parser.get('options','background2')).convert_alpha();
		self.mask       = pygame.mask.from_surface(self.imgcol);
		self.rect	= self.image.get_rect();
		self.stick      = parser.get('options','stick')
		self.uuid	= parser.get('options','uuid')

                #Load the Goal sprite
		goal_images     =  BF.load_and_slice_sprite(100,100,'goal.png');
                self.goal_sprite     =  cAnimSprite(goal_images,5)
                gx = int(parser.get('options','endx'))
                gy = int(parser.get('options','endy'))
                self.goal_sprite.move(gx,gy)
                
		#MONSTERS LOADING
		self.bouncers	=  self.retrieve_bouncer_list(parser)

	def stick_collides(self,stick):
                """
                        Check if a given stick collides with one of the
                        level walls
                """
                tmask = pygame.mask.from_surface(self.imgcol.subsurface(stick.rect))

                col = stick.mask.overlap(tmask,(0,0))
                
                if col == None: return 0,0,0
                else: return 1,col[0]+stick.rect.x,col[1]+stick.rect.y
		
		return 0,i,j

	def stick_in_goal(self,stick):
                """
                    Check if the stick collides with the level goal    
                """
                return stick.rect.colliderect(self.goal_sprite.rect)

	def retrieve_bouncer_list(self,parser):
		bouncer_list = []
		for b in parser.items('bouncers'):
			bx,by = b
			rot = 0
			newbouncer = cBouncer.cBouncer(int(bx),int(by),rot)
			bouncer_list.append(newbouncer)

		return bouncer_list
