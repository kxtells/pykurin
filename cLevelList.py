import os
import glob
from ConfigParser import SafeConfigParser

class cLevelList:
	levelfiles = []
	levelnames = []

	def __init__(self,path):
		"""
			Loads the .prop files in the proper path
		"""		
		for infile in glob.glob( os.path.join(path, '*.prop') ):
			self.levelfiles.append(infile)
		
		self.levelfiles.sort()
		
		for infile in self.levelfiles:
			self.levelnames.append(self.get_level_name_from_file(infile))


	def get_level_name_from_file(self,path):
		parser = SafeConfigParser()
		parser.read(path)
		return parser.get('options','name')

	def get_levelnames(self):
		return self.levelnames
