import pygame

class cCustomFont:
	
	def __init__(self,custom_number_images):
		self.custom_numbers = custom_number_images

	def parse_number(self,number):
		numstr = str(number)
		images = []

		for i in numstr:
			if i == ":":
				continue
			else:
				images.append(self.custom_numbers[int(i)])

		return images
