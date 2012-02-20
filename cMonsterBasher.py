import cMonster
import pygame
from cAnimSprite import cAnimSprite
import functions as BF

class cMonsterBasher(cMonster.cMonster):
	movx = 0
	movy = 0
	speed = 1

	def __init__(self,x,y,ex,ey,speed):
		cMonster.cMonster.__init__(self,x,y)
		self.image      = pygame.image.load("sprites/basher_col.png").convert_alpha()
		self.baseImage  = pygame.image.load("sprites/basher_col.png").convert_alpha()
		self.rect		= self.image.get_rect().move(x,y)
		self.mask       = pygame.mask.from_surface(self.image);
		
		anim_images     = BF.load_and_slice_sprite(64,64,'basher_nanim.png');
		col_anim_images = BF.load_and_slice_sprite(64,64,'basher_colanim.png');
                
		self.anim     	= cAnimSprite(anim_images,5)
		self.col_anim  	= cAnimSprite(col_anim_images,5)
		self.anim.rect  = self.rect
		self.col_anim.rect  = self.rect

		#Status sets
		self.col_anim.draw = False

		#
		self.movx = 1
		self.movy = 1
		self.startx = x
		self.starty = y
		self.endx = ex
		self.endy = ey
		self.going_to_end = True
		self.endxbigger = (self.endx > self.startx)
		self.endybigger = (self.endy > self.starty)
		self.speed = speed

		self.toendx , self.toendy = self.to_end_movement()

		#
		# Testing movement with interpolation
		#
		self.mov_points = []
		self.curr_point = 0
		self.interpolate_points_in_line(self.startx,self.starty,self.endx,self.endy)

	def logic_update_with_interpolated_points(self):
		currpos = self.mov_points[self.curr_point]
		if self.going_to_end:
			nextpos = self.mov_points[self.curr_point+1]
			self.curr_point+=1
			if self.curr_point == len(self.mov_points) -1: self.going_to_end = False #reached end
		else:
			nextpos = self.mov_points[self.curr_point-1]
			self.curr_point-=1
			if self.curr_point == 0: self.going_to_end = True #reached end
		
		mx = currpos[0] - nextpos[0]
		my = currpos[1] - nextpos[1]
		self.rect.move_ip(mx,my)

		pass
	
	def logic_update(self):
		self.logic_update_with_interpolated_points()
		#pass

	#Function to call on logic update
	def logic_update_version1(self):
		x = self.rect.center[0]
		y = self.rect.center[1]

		mx = my = 0


		if self.going_to_end:
			mx , my = self.toendx, self.toendy
		else:
			mx , my = -self.toendx, -self.toendy

		self.rect = self.rect.move(mx,my)
		self.check_and_set_direction()

	def check_and_set_direction(self):
		x = self.rect.x
		y = self.rect.y

		if self.going_to_end:
			if self.endxbigger and self.endybigger:
				if(self.x >= self.endx and self.y >= self.endy): self.going_to_end = False

			elif self.endxbigger and not self.endybigger:
				if(self.x >= self.endx and self.y <= self.endy): self.going_to_end = False

			elif not self.endxbigger and self.endybigger:
				if(self.x <= self.endx and self.y >= self.endy): self.going_to_end = False

			elif not self.endxbigger and not self.endybigger:
				if(self.x <= self.endx and self.y <= self.endy): self.going_to_end = False
		else:
			if self.endxbigger and self.endybigger:
				if(self.x <= self.endx and self.y <= self.endy): self.going_to_end = True

			elif self.endxbigger and not self.endybigger:
				if(self.x <= self.endx and self.y >= self.endy): self.going_to_end = True

			elif not self.endxbigger and self.endybigger:
				if(self.x >= self.endx and self.y <= self.endy): self.going_to_end = True

			elif not self.endxbigger and not self.endybigger:
				if(self.x >= self.endx and self.y >= self.endy): self.going_to_end = True
	
	def to_end_movement(self):
		mx = 0
		my = 0

		if self.startx < self.endx:
			mx = 1
		else:
			mx = -1
		if self.starty < self.endy:
			my = 1
		else:
			my = -1
		
		if self.startx == self.endx: mx = 0 # Need to check what happens when that is slightly different
		if self.starty == self.endy: my = 0 #
		
		return mx,my


	def interpolate_over_x(self,startx,starty,endx,endy):
		x = 0
		y = 0
		x0 = startx
		y0 = starty
		x1 = endx
		y1 = endy
		
		if startx > endx: rev = False
		else: rev = True

		maxx = max(startx,endx)
		minx = min(startx,endx)

		rang = range(minx,maxx)
		if rev: 
			for x in reversed(rang):
				#Linear Interpolation
				topfunc = (x-x0)*y1 - (x-x0)*y0
				downfunc = x1 - x0
				y = y0 + ((topfunc)/(downfunc))
				self.mov_points.append((x,y))
		else:
			for x in rang:
				#Linear Interpolation
				topfunc = (x-x0)*y1 - (x-x0)*y0
				downfunc = x1 - x0
				y = y0 + ((topfunc)/(downfunc))
				self.mov_points.append((x,y))

	def interpolate_over_y(self,startx,starty,endx,endy):
		x = 0
		y = 0
		x0 = startx
		y0 = starty
		x1 = endx
		y1 = endy
		
		if starty > endy: rev = False
		else: rev = True

		maxy = max(starty,endy)
		miny = min(starty,endy)

		rang = range(miny,maxy)
		if rev: 
			for y in reversed(rang):
				#Linear Interpolation
				topfunc = (y-y0)*x1 - (y-y0)*x0
				downfunc = y1 - y0
				x = x0 + ((topfunc)/(downfunc))
				self.mov_points.append((x,y))
		else:
			for y in rang:
				#Linear Interpolation
				topfunc = (y-y0)*x1 - (y-y0)*x0
				downfunc = y1 - y0
				x = x0 + ((topfunc)/(downfunc))
				self.mov_points.append((x,y))				
	
	def interpolate_points_in_line(self,startx,starty,endx,endy):
		x = 0
		y = 0
		x0 = startx
		y0 = starty
		x1 = endx
		y1 = endy

		diffx = max(startx,endx) - min(startx,endx)
		diffy = max(starty,endy) - min(starty,endy)

		if diffx > diffy:
			self.interpolate_over_x(startx,starty,endx,endy)
		else:
			self.interpolate_over_y(startx,starty,endx,endy)
		


