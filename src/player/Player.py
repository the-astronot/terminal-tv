from cv2 import perspectiveTransform
from src.io.FileReader import FileReader
from src.player.Directory import Directory
##########
import os
import sys
import time
import math


class Player:

	button_offset = 2

	def __init__(self, path_to_files):
		self.termx, self.termy = os.get_terminal_size()
		self.home_dir = Directory(path_to_files,"",True)
		self.cursor = 0
		self.loaded = False
		self.play = False

	def queue(self, video):
		self.video = video
		self.termx = self.video.x
		self.termy = self.video.y + self.button_offset
		self.spf = self.video.spf
		self.last_frame_time = 0
		# Add a check to see if the terminal
		# is full screen or not
		# Dont resize if full screen and video
		# is smaller than video requires
		print("\x1b[8;{0};{1}t".format(self.termy,self.termx))
		print("\033[2J\033[0;0H",end="")
		start_frame = ""
		for _ in range(self.termy-self.button_offset):
			start_frame += "#"*self.termx + "\n"
		start_frame += "|[P] Play/Pause\t|\t[S] Stop|"
		print(start_frame)
		print("\033[1;0H",end="")
		self.loaded = True

	def play_pause(self):
		self.play = not self.play
		self.last_frame_time = time.time()

	def stop(self):
		self.play=False
		self.loaded=False
		self.video.file.close()
		self.last_frame_time = 0

	def render_selector(self):
		length = len(self.files[0])
		term_len = self.termy-1
		midway = math.floor(term_len/2)
		# Determine what to print
		if length < term_len:
			begin = 0
			end = length
		else:
			begin = self.cursor - midway
			end = begin + term_len
			while begin < 0:
				begin +=1
				end += 1
			while end > length:
				begin -=1
				end -= 1

		print("\033[1;0H",end="")
		for i in range(begin,end):
			if i == self.cursor:
				print("\033[K\033[30m\033[47m{0}\033[40m\033[37m".format(self.files[0][i]))
			else:
				print("\033[K\033[40m\033[37m{0}".format(self.files[0][i]))
		print("\033[K\033[40m\033[37m",end="")
		for i in range(0,term_len-length):
			print("\033[K")

	def update_files(self):
		self.files = self.home_dir.folder_array("")

	def increment_cursor(self):
		if self.cursor < len(self.files[0]):
			self.cursor+=1

	def decrement_cursor(self):
		if self.cursor > 0:
			self.cursor-=1

	def toggle(self):
		if isinstance(self.files[1][self.cursor],Directory):
			# Change the visibility of the directory
			print(self.files[1][self.cursor].display)
			self.files[1][self.cursor].toggle_visibility()
			print(self.files[1][self.cursor].display)
			self.update_files()
		else:
			# Queue the video
			fr = FileReader(self.files[1][self.cursor])
			self.queue(fr)

	def next_frame(self):
		if self.last_frame_time == 0:
			self.last_frame_time = time.time()
		text = self.video.read_frame()
		if text == "":
			self.stop()
			return
		curr_time = time.time()
		while(curr_time < self.last_frame_time+self.spf):
			time.sleep(.0002)
			curr_time = time.time()
		self.last_frame_time += self.spf
		print("\033[1;0H",end="")
		print(text,end="")


if __name__ == '__main__':
	filename = "Gorillaz_10.trm"
	fr = FileReader(filename)
	player = Player(os.getcwd())
	player.queue(fr)
	text = fr.read_frame()
	while text != "":
		print(text,end="")
		text = fr.read_frame()
		time.sleep(player.spf)
		print("\033[1;0H",end="")
	print("\033[2J\033[0;0H",end="")
	fr.file.close()
