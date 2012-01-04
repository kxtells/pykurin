import os
import glob
from ConfigParser import SafeConfigParser

class cLevelList:
	levelfiles = []
	levelnames = []

	def __init__(self,path):
		
		for infile in glob.glob( os.path.join(path, '*.prop') ):
			self.levelfiles.append(infile)
		
		self.levelfiles.sort()
		
		for infile in self.levelfiles:
			self.levelnames.append(self.get_level_name_from_file(infile))

		print self.levelfiles
		print self.levelnames

	def load_list_of_levels(self,path):
		'''
		load_list_of_levels:
			returns a list of all the levels in the levels directory
		'''
	
		for infile in glob.glob (os.path.join(path,'*.prop')):
			self.levelfiles.append(infile)
	

	def get_level_name_from_file(self,path):
		parser = SafeConfigParser()
		parser.read(path)
		return parser.get('options','name')

	def get_levelnames(self):
		return self.levelnames
