################################################################################
##  Terminal_TV Episode                                                       ##
####  author: jormungandr                                                   ####
####  exec: none                                                            ####
####  created: 01/19/22                                                     ####
################################################################################
import os


class Episode:
	def __init__(self,e_name):
		self.e_name = e_name
		self.files = []
		self.file_sizes = []
		self.time = 0
		self.audio_file = ""

	def get_closest(self,x,direction=None):
		closest = -1
		second_closest = -1
		sep = 1000
		sep2 = 2000
		if direction == None:
			for i in range(len(self.file_sizes)):
				if abs(self.file_sizes[i]-x) < sep:
					closest = i
					sep = abs(self.file_sizes[i]-x)
		elif direction == 0:
			# Go higher
			for i in range(len(self.file_sizes)):
				if abs(self.file_sizes[i]-x) < sep and self.file_sizes[i]>=x:
					second_closest = closest
					sep2 = sep
					closest = i
					sep = self.file_sizes[i]-x
				elif abs(self.file_sizes[i]-x) < sep2 and self.file_sizes[i]>=x:
					second_closest = i
					sep2 = abs(self.file_sizes[i]-x)
			if second_closest != -1:
				closest = second_closest
		else:
			# Go lower
			for i in range(len(self.file_sizes)):
				if abs(self.file_sizes[i]-x) < sep and self.file_sizes[i]<=x:
					second_closest = closest
					sep2 = sep
					closest = i
					sep = abs(self.file_sizes[i]-x)
				elif abs(self.file_sizes[i]-x) < sep2 and self.file_sizes[i]<=x:
					second_closest = i
					sep2 = abs(self.file_sizes[i]-x)
			if second_closest != -1:
				closest = second_closest
		return closest

	def add_file(self,filename,size,audio_file=None):
		self.files.append(filename)
		self.file_sizes.append(size)
		if audio_file != None:
			self.audio_file = audio_file

	def remove_file(self,index):
		self.files.pop(index)
		self.file_sizes.pop(index)
		if len(self.files) == 0:
			self.audio_file = ""

	def read_episode(self):
		if os.path.exists(self.e_name):
			f = open(self.e_name,"r")
			text = f.read()
			data = text.split("\n#####\n")
			self.files = data[0].split("\n")
			self.file_sizes = data[1].split("\n")
			for i in range(len(self.file_sizes)):
				self.file_sizes[i] = int(self.file_sizes[i])
			self.time = float(data[2])
			self.audio_file = data[3]
			f.close()

	def write_episode(self):
		f = open(self.e_name,"w+")
		for file in self.files:
			f.write("{}\n".format(file))
		f.write("#####\n")
		for file_size in self.file_sizes:
			f.write("{}\n".format(file_size))
		f.write("#####\n")
		f.write("{}\n".format(self.time))
		f.write("#####\n")
		f.write("{}".format(self.audio_file))
		f.close()

	def add_audio(self,audio_file):
		self.audio_file = audio_file
