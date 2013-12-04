"""
	Class timer for timed events.

	Has to be periodically updated.

	When the timer reaches zero, it
"""
import time

class cTimer:
	def __init__(self, seconds, function=None):
		self.seconds  = seconds
		self.function = function
		self.start    = time.time()

	def update(self):
		ctime = time.time()
		if ctime - self.start > self.seconds:
			if self.function:
				self.function()

			return True

		return False

