import pygame
import pymunk
import os
import glob
import sys



#Function to load a sprite set and slice it
def load_and_slice_sprite(w,h,filename):
	'''
	load_and_slice_sprite:
		All the sprites are positioned in a horitzontal file
		All the frames have the same size (w,h)
	'''

	images = []
	master_image = pygame.image.load(os.path.join('sprites', filename))
	master_w,master_h = master_image.get_size()

	for i in xrange(int(master_w/w)):
		images.append(master_image.subsurface((i*w,0,w,h)).convert_alpha())

	return images

def print_mask(mask):
	w,h = mask.get_size()
	for y in range(h):
		for x in range(w):
			sys.stdout.write(str(mask.get_at((x,y))))

		sys.stdout.write("\n")
	sys.stdout.write("---------------------------\n")

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+480

def rect_to_pymunkBB(rect):
	return pymunk.BB(rect.left, rect.bottom, rect.right, rect.top)

def pymunkBB_to_rect(bb):
	return pygame.Rect(bb.right,bb.top,bb.top-bb.bottom,bb.right - bb.left,)

def vertices_from_BB(bb, shrink=0):
	""" Get vertices from Bounding Box. Shrink gives the ability to reduce the
	size of the vertices to adjust collision
	"""
	l = bb.left
	r = bb.right
	t = bb.top
	b = bb.bottom
	s = shrink
	return [(t+s,l+s),(t+s,r-s),(b-s,r-s),(b-s,l+s)]
