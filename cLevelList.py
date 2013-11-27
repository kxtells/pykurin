import os
import glob
from ConfigParser import SafeConfigParser

class cLevelList:
	def __init__(self):
		self.levelfiles = []
		self.levelnames = []
		self.levelsuuid = []

		self.packfiles = []
		self.packnames = []
		self.packdirs = []
		self.packscoretoopen = []

	def load_leveldir(self,path):
		"""
			Loads the .prop files in the proper path
		"""
		del self.levelfiles[:]
		del self.levelnames[:]
		del self.levelsuuid[:]

		levelfiles = []
		levelnames = []
		levelsuuid = []
		for infile in glob.glob(os.path.join(path, '*.prop') ):
			levelfiles.append(infile)

		levelfiles.sort()

		for infile in levelfiles:
			levelnames.append(self.get_level_name_from_file(infile))
			levelsuuid.append(self.get_specific_option(infile,'uuid'))

		tmp = zip(levelnames, levelfiles, levelsuuid)
		tmp.sort()
		self.levelfiles = [lf for ln,lf,lu in tmp]
		self.levelnames = [ln for ln,lf,lu in tmp]
		self.levelsuuid = [lu for ln,lf,lu in tmp]

	def load_packdir(self,path):
		"""
			Loads the .prop files in the proper path
		"""
		del self.packfiles[:]
		del self.packnames[:]

		for infile in glob.glob( os.path.join(path, '*.lvlpack') ):
			self.packfiles.append(infile)

		self.packfiles.sort()

		for infile in self.packfiles:
			self.packnames.append(self.get_specific_option(infile,'name'))
			self.packdirs.append(self.get_specific_option(infile,'basedir'))
			self.packscoretoopen.append(int(self.get_specific_option(infile,'levels2open')))

	def get_level_name_from_file(self,path):
		parser = SafeConfigParser()
		parser.read(path)
		return parser.get('options','name')

	def get_specific_option(self,path,option):
		parser = SafeConfigParser()
		parser.read(path)
		return parser.get('options',option)


	def get_levelnames(self):
		return self.levelnames

	def get_packnames(self):
		return self.packnames

	def get_pack_basedir(self,id):
		return self.packdirs[id]

	def isPackOpen(self,id,total):
		return self.packscoretoopen[id] <= total

	def level_exists(self,lnum):
		return lnum>0 and lnum < len(self.levelfiles)

	def level_uuid(self,lnum):
		return self.levelsuuid[lnum]
