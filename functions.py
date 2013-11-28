import pygame
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
