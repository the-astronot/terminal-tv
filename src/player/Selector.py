################################################################################
##  Terminal_TV Selector                                                      ##
####  author: jormungandr                                                   ####
####  exec: none                                                            ####
####  created: 01/09/22                                                     ####
################################################################################
import os
import sys
#from pynput import keyboard
import getch as gh


class Selector:
	def __init__(self, path):
		self.home = path
		#self.player = player
		self.branch_name = ""
		self.branch = []
		self.home_dir = Directory(path,"",True)

	def display_tree(self):
		for x in self.branch:
			print(x)


class Directory:
	def __init__(self,path,name,display):
		self.path = path
		self.name = name
		self.display = display
		self.folders = []
		self.files = []
		for file in os.listdir(self.path):
			if os.path.isfile(os.path.join(self.path,file)):
				self.add_file(file)
			else:
				self.add_folder(file)

	def add_folder(self, foldername):
		self.folders.append(Directory(os.path.join(self.path,foldername),foldername,True))

	def add_file(self,filename):
		self.files.append(filename)

	def toggle_visibility(self):
		self.display = not self.display

	def print_folder(self, indent):
		if self.display:
			for folder in self.folders:
				if (len(self.files)==0 and folder ==self.folders[-1]):
					print(indent+"└─ {}".format(folder.name))
					next_indent = indent + "   "
				else:
					print(indent+"├─ {}".format(folder.name))
					next_indent = indent + "│  "
				folder.print_folder(next_indent)
			for file in self.files:
				if file == self.files[-1]:
					print(indent+"└─ {}".format(file))
				else:
					print(indent+"├─ {}".format(file))

	def folder_array(self, indent):
		array = []
		if self.display:
			for folder in self.folders:
				if (len(self.files)==0 and folder==self.folders[-1]):
					array.append(indent+"└─ {}".format(folder.name))
					next_indent = indent + "   "
				else:
					array.append(indent+"├─ {}".format(folder.name))
					next_indent = indent + "│  "
				array+=folder.folder_array(next_indent)
			for file in self.files:
				if file == self.files[-1]:
					array.append(indent+"└─ {}".format(file))
				else:
					array.append(indent+"├─ {}".format(file))
		return array


def on_press(key):
	global index
	print(key)
	if key == "up":
		index+=1
		print(index)
	elif key == "down":
		index-=1
		print(index)


def get_key():
    first_char = gh.getch()
    if first_char == '\x1b':
        return {'[A': 'up', '[B': 'down', '[C': 'right', '[D': 'left'}[gh.getch() + gh.getch()]
    else:
        return first_char


index=0

if __name__ == '__main__':
	
	sel = Selector(os.getcwd())
	sel.display_tree()
	array = sel.home_dir.folder_array("")
	for element in array:
		print(element)
	while True:
		on_press(get_key())
	

