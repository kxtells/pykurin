from ConfigParser import SafeConfigParser
import pygame
from cAnimSprite import cAnimSprite
import functions as BF
import cItemBouncer
import cItemRecoverLives
import cMonsterBasher
import cMonsterFlie
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
		print "load_settings"
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
		print "default_settings"
		self.fullscreen = False
		self.username = "DummyName"
		self.save_settings_file()
	

	############################
	#
	# Interfacing with record files
	#
	############################
	
	def save_record(self,username,newtime):
		"""
			Saves the new record into the proper shelve
			loads the records into the class attributes self.records and self.player_record_index
			returns a tuple with the results
		"""
		#data pack
		newdata = (newtime,username)
		
		db = shelve.open("db/"+self.uuid)
		
		dbrecords = []
		#recover data if exists
		if db.has_key("records"):
			dbrecords = db["records"]
	
		#check if a data drop is needed
		if len(dbrecords) < cLevel._MAX_SAVED_RECORDS:
			dbrecords.append(newdata)
		else:
			dbrecords.sort()
			worsttime = dbrecords[-1][0]
			if newtime < worsttime:
				dbrecords.pop()
				dbrecords.append(newdata)
		
		dbrecords.sort()
	
		db["records"] = dbrecords
	
		user_index = -1
		for i,val in enumerate(dbrecords):
			if dbrecords[i][0] == newtime and dbrecords[i][1] == username:
				user_index = i
	
		db.close()

		self.records = dbrecords
		self.player_record_index = user_index
		print user_index
		return dbrecords,user_index

	def load_records(self):
		"""
			Return a tuple (record,name) for a level
		"""
		db = shelve.open("db/"+self.uuid)
		
		dbrecords = []
		#recover data if exists
		if db.has_key("records"):
			dbrecords = db["records"]
	
		self.records = dbrecords

		return dbrecords


