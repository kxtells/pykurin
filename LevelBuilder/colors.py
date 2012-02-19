#
# Colors definitions
#
import random

black = 0, 0, 0
yellow = 255, 255, 0
green = 0,255,0
blue = 0,0,150
red = 255,0,0
white = 255,255,255
orange = 255,174,0
purple = 145,0,145
lblue = (164,180,255)
gray = (125,125,125)

COLOR_ARRAY = [purple,green,blue,red,orange,(0,107,31),(164,180,255)]
def random_color():
	return COLOR_ARRAY[random.randint(0,len(COLOR_ARRAY)-1)]
	
