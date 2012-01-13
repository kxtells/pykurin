import pygame
import os
import glob
import shelve


_MAX_SAVED_RECORDS = 5

#Function to load a sprite set and slice it
def load_and_slice_sprite(w,h,filename):
	'''
	load_and_slice_sprite:
		All the sprites are positioned in a horitzontal file
		All the frames have the same size (w,h)
	'''

	images = []
	master_image = pygame.image.load(os.path.join('sprites', filename))
	master_w,master_h = master_image.get_size()

	for i in xrange(int(master_w/w)):
		images.append(master_image.subsurface((i*w,0,w,h)).convert_alpha())

	return images

def save_record(levelfile,username,newtime):
	"""
		Saves the new record into the proper shelve and returns
		the record list and an index showing the current player record.
		if the record is not on the top 5 the returned index is -1
	"""
	#data pack
	newdata = (newtime,username)
	
	db = shelve.open("db/"+levelfile)
	
	dbrecords = []
	#recover data if exists
	if db.has_key("records"):
		dbrecords = db["records"]

	#check if a data drop is needed
	if len(dbrecords) < _MAX_SAVED_RECORDS:
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

	print dbrecords,user_index
	return dbrecords,user_index

def load_records(levelfile):
	print "LOAD RECORD"
