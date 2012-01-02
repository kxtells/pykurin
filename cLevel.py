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
		self.rect	=  self.image.get_rect();

	def stick_collides(self,stick):
		arr_px_stick            = pygame.surfarray.array_alpha(stick.image);
                arr_px_background       = pygame.surfarray.array_alpha(self.imgcol.subsurface(stick.rect));

		width = stick.rect.width
		height = stick.rect.height
	
		for i in range(width):
    			for j in range(height):
				val = arr_px_stick[i][j]
				bgval = arr_px_background[i][j]
				if val==255 and bgval==255:
					return 1,i+stick.rect.x,j+stick.rect.y
		
		return 0,i,j
