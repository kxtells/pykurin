import shelve

class cSettings:
	#by default nothing loaded, when asked and not loaded it will load the settings file
	username = None
	fullscreen = None
	settings_file = "db/settings.set"

	#def __init__(self,file):
		

	def get_username(self):
		if self.username == None:
			self.load_settings_file()
		
		return self.username


	def load_settings_file(self):
		"""
			Loads the settings file and
			fills all the settings
		"""
		try:
			s = open(self.settings_file, 'r');s.close() #file exists check, if not, an exception raises
			db = shelve.open(self.settings_file)
			self.username = db["username"]
			self.fullscreen = db["fullscreen"]
			db.close()
		except:
			self.load_default_settings()


	def save_settings_file(self):
		"""
			Saves the settings class into a settings file
		"""
		db = shelve.open(self.settings_file)
		db["username"] = self.username
		db["fullscreen"] = self.fullscreen
		db.close()


	def load_default_settings(self):
		"""
			Loads all the settings to a default value in case
			the settings file is not found, then saves the
			new settings file
		"""
		self.fullscreen = False
		self.username = "DummyName"
		self.save_settings_file()
	
