import subprocess
import posixpath
import time
import shutil
import os

def cmus_sync(play_cmus,play_phone,phone):
	a = set()
	b = set()

	#adds every element of the source playlist
	with open(play_cmus,"r") as source:
		for line in source:
			a.add(line.rstrip('\n'))	
		if '' in a:
			a.remove('')

	#adds every element of the dest playlist
	with open(play_phone,"r") as dest:
		for line in dest:	
			b.add(line.rstrip('\n'))
		if '' in b:
			b.remove('')

	#these items should be added to dest
	add = a-b
	#these items should be removed from dest
	remove = b-a
	
	remove_songs(remove,phone)
	add_songs(add,phone)


	shutil.copy(play_cmus,play_phone)
	
def remove_songs(remove,phone):
	
	# let the user know we're removing
	print("Removing...")
	# print the 0% progress, each '#' symbolises 2% 
	print("["+(" "*50)+"]"+" 0%   ",end='\r')
	
	if len(remove) != 0:
		# ppi = procent per item
		ppi = (100/float(len(remove)))
		# prp = progress procent
		prp = ppi	
		# remove the files
		for item in remove:
			# the path /Artist/Album/Song
			path_elem = []
			# number of '#' in progress
			prog = int(prp/2)
			# add the directories and song name
			path = item
			
			# get the artist/album/song path
			for i in range(3):
				dirs = posixpath.split(path)
				path_elem.append(dirs[1])
				path = dirs[0]	
			
			artist = phone + "/" + path_elem[2]
			album = artist + "/" + path_elem[1]
			song = album + "/" + path_elem[0]
			
			os.remove(song)
			# if the album dir is empty we want to remove it
			if os.listdir(album) == []:
				os.rmdir(album)
				# same goes for the artist dir
				if os.listdir(artist) == []:
					os.rmdir(artist)

			# print current progress
			print(("["+("#"*prog)+(" "*(50-prog))+"]"+" "+str(round(prp))+"%   "),end='\r')
			prp += ppi

	# print that we're done
	print(("["+("#"*50)+"]"+" 100%   "))
	if len(remove) == 1:
		print ("Done. Removed: %s song\n"%(len(remove)))
	else:
		print ("Done. Removed: %s songs\n"%(len(remove)))



def add_songs(add, phone):

	# let the user know we're removing
	print("Adding...")
	# print the 0% progress, each '#' symbolises 2% 
	print("["+(" "*50)+"]"+" 0%   ",end='\r')
	
	if len(add) != 0:
		# ppi = procent per item
		ppi = (100/float(len(add)))
		# prp = progress procent
		prp = ppi	
		# remove the files
		for item in add:
			# the path /Artist/Album/Song
			path_elem = []
			# number of '#' in progress
			prog = int(prp/2)
			# add the directories and song name
			path = item

			# get the artist/album/song path
			for i in range(3):
				dirs = posixpath.split(path)
				path_elem.append(dirs[1])
				path = dirs[0]	

			artist = phone + "/" + path_elem[2]
			album = artist + "/" + path_elem[1]
			song = album + "/" + path_elem[0]
			
			
			# check if artist dir exists
			if posixpath.exists(artist):
				# checks if album dir exits
				if posixpath.exists(album):
					# copy song to album dir
					shutil.copy(item,song)
				else:
					# create album dir
					os.makedirs(album)
					# copy song to album dir
					shutil.copy(item,song)
			else:
				# create artist dir
				os.makedirs(artist)
				# create album dir
				os.makedirs(album)
				# copy song to album dir
				shutil.copy(item,song)

			# print current progress
			print(("["+("#"*prog)+(" "*(50-prog))+"]"+" "+str(round(prp))+"%   "),end='\r')
			prp += ppi

	# print that we're done
	print(("["+("#"*50)+"]"+" 100%   "))
	if len(add) == 1:
		print ("Done. Added: %s song\n"%(len(add)))
	else:
		print ("Done. Added: %s songs\n"%(len(add)))

if __name__=='__main__':
	play_cmus = play_phone = phone = ""
	#start time for program
	start_time = time.time()	
	
	with open("/home/sam/.cmus_sync","r") as f:
		#checks specific files of the config for paths.
		for i,line in enumerate(f):
			if i == 1:
				play_cmus = line.rstrip('\n')
	
			if i == 4:
				play_phone = line.rstrip('\n')

			if i == 7:
				phone = line.rstrip('\n')
	
	# prints the paths from the config file
	print("\nMusic destination: %s"%(phone))
	print("Source playlist: %s"%(play_cmus))
	print("Phone playlist: %s\n"%(play_phone))
	
	cmus_sync(play_cmus, play_phone, phone)
	#end time for program
	print("--- %s seconds ---" % (round((time.time() - start_time),3)))
