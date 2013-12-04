import pygame

class cInputKeys():
	"""
		Class to control the key input, also store
		temporary (while the game is on) the last name
		stored
	"""
	MAXCHARS = 10

	def __init__(self):
		self.text = ""
		self.error_texts = []

	def get_error(self):
		return self.error_texts

	def clear_error(self):
		self.error_texts = []

	def sanitize_input(self):
		"""
			Called when the user presser intro.
			returns True or False depending if the string is acceptable
			if not, sets self.error_text
		"""
		if len(self.text)<3:
			self.error_texts = ['At least three letters on your name']
			return False

		if not all(ord(c) < 128 for c in self.text):
			self.error_texts = ['Invalid characters, sorry for that' , 'But it makes my life easier']
			return False

		return True


	def process_keystroke(self,event):
		"""
			Keeps increasing the text with the input keys
			Returns True when the player decided that the name is ok
			False otherwise
		"""
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
				self.text = self.text[:-1]
			elif event.key == pygame.K_RETURN:
				return True
			else:
				if event.key in cInputKeys.CHARACTERS:
					if len(self.text) < cInputKeys.MAXCHARS:
						self.text += event.unicode

		return False
	#
	# Brute force to check acceptable events
	#
	CHARACTERS = [ \
	pygame.K_a, \
	pygame.K_b, \
	pygame.K_c, \
	pygame.K_d, \
	pygame.K_e, \
	pygame.K_f, \
	pygame.K_g, \
	pygame.K_h, \
	pygame.K_i, \
	pygame.K_j, \
	pygame.K_k, \
	pygame.K_l, \
	pygame.K_m, \
	pygame.K_n, \
	pygame.K_o, \
	pygame.K_p, \
	pygame.K_q, \
	pygame.K_r, \
	pygame.K_s, \
	pygame.K_t, \
	pygame.K_u, \
	pygame.K_v, \
	pygame.K_w, \
	pygame.K_x, \
	pygame.K_y, \
	pygame.K_z, \
	]
