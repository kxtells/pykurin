import shelve

class cSettings:
	#by default nothing loaded, when asked and not loaded it will load the settings file
	username = None
	fullscreen = None
	settings_file = "db/settings.set"
	loaded = False
	cleared_levels_uuid_list = []

	#def __init__(self,file):
		

	def get_username(self):
		if self.username == None:
			self.load_settings_file()
		return self.username

	def get_fullscreen(self):
		if self.fullscreen == None:
			self.load_settings_file()
		return self.fullscreen

	def set_username(self,newname):
		self.load_settings_file()
		self.username = newname
		self.save_settings_file()

	def set_fullscreen(self,newbool):
		self.load_settings_file()
		self.fullscreen = newbool
		self.save_settings_file()

	def total_levels_cleared(self):
		return len(self.cleared_levels_uuid_list)

	def isLevelCompleted(self,uuid):
		return uuid in self.cleared_levels_uuid_list

	def add_cleared_level(self,uuid):
		"""
			Adds a levels to the cleared list if is not already there
		"""
		if not uuid in self.cleared_levels_uuid_list:
			self.cleared_levels_uuid_list.append(uuid)
			self.save_settings_file()

	def load_settings_file(self):
		"""
			Loads the settings file and
			fills all the settings
		"""
		if self.loaded: return #if already loaded, no need to open files to load

		try:
			s = open(self.settings_file, 'r');s.close() #file exists check, if not, an exception raises
			db = shelve.open(self.settings_file)
			self.username = db["username"]
			self.fullscreen = db["fullscreen"]
			self.cleared_levels_uuid_list = db["clearedlevelslist"]
			db.close()
			self.loaded = True
		except:
			self.load_default_settings()


	def save_settings_file(self):
		"""
			Saves the settings class into a settings file
		"""
		db = shelve.open(self.settings_file)
		db["username"] = self.username
		db["fullscreen"] = self.fullscreen
		db["clearedlevelslist"] = self.cleared_levels_uuid_list
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
	
