import pygame

class cCustomFont:
	
	def __init__(self,custom_number_images):
		self.custom_numbers = custom_number_images

	def parse_number(self,number):
		numstr = str(number)
		images = []

		for i in numstr:
			images.append(self.custom_numbers[int(i)])

		return images

	def get_doubledots(self):
		return self.custom_numbers[-1]
