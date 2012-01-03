from ConfigParser import SafeConfigParser
import pygame

class cLevel:
	
	def __init__(self,file):
		parser = SafeConfigParser()
		parser.read(file)

		self.name 	=  parser.get('options','name')
		self.startx 	=  int(parser.get('options','startx'))
		self.starty 	=  int(parser.get('options','starty'))
		self.imgcol 	=  pygame.image.load(parser.get('options','collision'));
		self.image 	=  pygame.image.load(parser.get('options','background'));
		self.mask       =  pygame.mask.from_surface(self.imgcol);
		self.rect	=  self.image.get_rect();
                

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
