################################################################################
##  Terminal_TV Directory                                                     ##
####  author: jormungandr                                                   ####
####  exec: none                                                            ####
####  created: 01/09/22                                                     ####
################################################################################
import os
import sys
import getch as gh


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
		self.folders.append(Directory(os.path.join(self.path,foldername),foldername,False))

	def add_file(self,filename):
		self.files.append(filename)

	def toggle_visibility(self):
		if self.display:
			self.display = False
		else:
			self.display = True

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
		name_array = []
		obj_array = []
		if self.display:
			for folder in self.folders:
				if (len(self.files)==0 and folder==self.folders[-1]):
					name_array.append(indent+"└─ {}".format(folder.name))
					next_indent = indent + "   "
				else:
					name_array.append(indent+"├─ {}".format(folder.name))
					next_indent = indent + "│  "
				obj_array.append(folder)
				name_array+=folder.folder_array(next_indent)[0]
				obj_array+=folder.folder_array(next_indent)[1]
			for file in self.files:
				if file == self.files[-1]:
					name_array.append(indent+"└─ {}".format(file))
				else:
					name_array.append(indent+"├─ {}".format(file))
				obj_array.append(os.path.join(self.path,file))
		return name_array, obj_array

