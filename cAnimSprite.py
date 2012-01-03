# Basic class definition courtesy of Nicolas Crovatti (http://shinylittlething.com/2009/07/21/pygame-and-animated-sprites/)
#
#

import pygame

class cAnimSprite(pygame.sprite.Sprite):

	def __init__(self,images,fps=10):
		pygame.sprite.Sprite.__init__(self)
		self._images = images
		
		#Track start time and update time
		self._start = pygame.time.get_ticks()
		self._delay = 1000/fps
		self._last_update = 0
		self._frame = 0
		self.image = images[0]
		self.rect = self.image.get_rect()
		self.draw = True

		#Update to the first image
		self.update(pygame.time.get_ticks())

	def update(self,time):
		if time - self._last_update > self._delay:
			self._frame+=1
			if self._frame >= len(self._images): self._frame = 0;self.draw = False
			self.image = self._images[self._frame]
			self._last_update = time

        #Change the sprite position
	def move(self,x,y):
		self.rect.x = x-self.rect.width/2
		self.rect.y = y-self.rect.height/2

        #Incremental move by amount
	def incr_move(self,incrx,incry):
                self.rect.x += incrx
                self.rect.y += incry

        def out_of_screen(self,width=800,height=600):
                """
                        Checks if the sprite is out of the screen
                """
                x = self.rect.x
                y = self.rect.y
                w = self.rect.width
                h = self.rect.height
                
                if x + w < 0 or \
                   y + h< 0 or \
                   x > width or \
                   y > height:
                           return True

                return False
