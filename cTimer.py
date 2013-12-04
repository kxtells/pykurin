"""
	Class timer for timed events.

	Has to be periodically updated.

	When the timer reaches zero, it returns True
"""
import time

class cTimer:
	def __init__(self, seconds, function=None):
		self.seconds  = seconds
		self.function = function
		self.start    = time.time()

	def update(self):
		""" Returns true when the timer finished. False otherwise"""
		ctime = time.time()
		if ctime - self.start > self.seconds:
			if self.function:
				self.function()

			return True

		return False

"""
A timer to handle the blinking of something. The parameter function
is called each "blink" seconds passed with one boolean parameter
to represent the blinking status.
onfinish function is called when the timer ends
"""
class cTimerBlink:
	def __init__(self, seconds, blink, onchange=None, onfinish=None):
		self.seconds  = seconds
		self.blink    = blink
		self.onchange = onchange
		self.onfinish = onfinish
		self.bstat    = True
		self.start    = time.time()

	def update(self):
		""" Returns true when the timer finished. False otherwise"""
		ctime = time.time()
		tdiff = ctime - self.start
		if tdiff > self.seconds:
			if self.onfinish:
				self.onfinish()
			return True
		elif int(tdiff % self.blink) == 0:
			self.bstat = not self.bstat
			if self.onchange:
				self.onchange(self.bstat)

		return False
