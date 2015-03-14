import subprocess
import ntpath
import time

def cmus_sync(play_cmus,play_phone,phone):
	a = set()
	b = set()
	rmindex = addindex = 1
	with open(play_cmus,"r") as source:
		for line in source:
			a.add(line.rstrip('\n'))	
		if '' in a:
			a.remove('')
		source.seek(0)
	

	with open(play_phone,"r") as dest:
		for line in dest:	
			b.add(line.rstrip('\n'))
		if '' in b:
			b.remove('')
		dest.seek(0)

	add = a-b
	remove = b-a

	if remove != {}:
		if len(remove) != 0:	
			pro = (100/float(len(remove)))
			pr = pro
		print ("Removing...")
		print("["+(" "*20)+"]"+" 0%   ",end='\r')
		for item in remove:
			pro5 = int(pr/5)
			name = ntpath.basename(item)
			phonepath = phone+"/"+name
			print(("["+("#"*pro5)+(" "*(20-pro5))+"]"+" "+str(round(pr,1))+"%   "),end='\r')
			subprocess.call(["rm","-r",phonepath])
			pr += pro	
		else:
			print(("["+("#"*20)+"]"+" 100%   "))
			if len(remove) == 1:
				print ("Done. Removed: %s song"%(len(remove)))
			else:
				print ("Done. Removed: %s songs"%(len(remove)))

	if add !={}:
		if len(add) != 0:	
			pro = (100/float(len(add)))
			pr = pro
		print ("Adding...")
		print("["+(" "*20)+"]"+" 0%   ",end='\r')
		for item in add:
			#add new files to phone
			pro5 = int(pr/5)
			name = ntpath.basename(item)
			print(("["+("#"*pro5)+(" "*(20-pro5))+"]"+" "+str(round(pr,1))+"%   "),end='\r')
			subprocess.call(["rsync",item,phone])
			pr += pro	
		else:
			print(("["+("#"*20)+"]"+" 100%  "))
			if len(add) == 1:
				print("Done. Added: %s new song"%(len(add)))		
			else:
				print("Done. Added: %s new songs"%(len(add)))		


	subprocess.call(["cp","-r",play_cmus,play_phone])
	



if __name__=='__main__':
	play_cmus = play_phone = phone = ""
	start_time = time.time()	
	with open("cmus_sync.conf","r") as f:
		for i,line in enumerate(f):
			if i == 1:
				play_cmus = line.rstrip('\n')
	
			if i == 4:
				play_phone = line.rstrip('\n')

			if i == 7:
				phone = line.rstrip('\n')

	cmus_sync(play_cmus, play_phone, phone)
	print("--- %s seconds ---" % (round((time.time() - start_time),3)))
