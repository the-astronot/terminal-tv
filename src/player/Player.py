from src.io.FileReader import FileReader
##########
import os
import sys
import time

class Player:

	button_offset = 2

	def __init__(self):
		self.termx, self.termy = os.get_terminal_size()

	def queue(self, video):
		self.video = video
		self.termx = self.video.x
		self.termy = self.video.y + self.button_offset
		self.spf = self.video.spf
		# Add a check to see if the terminal
		# is full screen or not
		# Dont resize if full screen and video
		# is smaller than video requires
		print("\x1b[8;{0};{1}t".format(self.termy,self.termx))
		print("\033[2J\033[0;0H",end="")
		start_frame = ""
		for _ in range(self.termy-self.button_offset):
			start_frame += "#"*self.termx + "\n"
		start_frame += "|[P] Play\t|\t[S] Stop|"
		print(start_frame)
		print("\033[1;0H",end="")
		time.sleep(1)
		self.play = True

	def play(self):
		self.play = True

	def pause(self):
		self.play = False

if __name__ == '__main__':
	filename = "Gorillaz_10.txt"
	fr = FileReader(filename)
	player = Player()
	player.queue(fr)
	text = fr.read_frame()
	while text != "":
		print(text,end="")
		text = fr.read_frame()
		time.sleep(player.spf)
		print("\033[1;0H",end="")
	print("\033[2J\033[0;0H",end="")
	fr.file.close()
