################################################################################
##  Terminal_TV Player                                                        ##
####  author: jormungandr                                                   ####
####  exec: none                                                            ####
####  created: 01/09/22                                                     ####
################################################################################
from src.player.Selector import Selector
import src.player.Screens as Screens
###########
import os
import time
import math
import vlc


class Player:

	button_offset = 2

	def __init__(self, path_to_files,audio_available):
		self.termx, self.termy = os.get_terminal_size()
		self.selector = Selector(path_to_files)
		self.loaded = False
		self.play = False
		self.audio_available = audio_available
		self.audio = None
		self.video = None
		self.audio_changed = False

	def queue(self, video, audio=None):
		self.video = video
		if audio and self.audio_available:
			self.audio = vlc.MediaPlayer(audio)
			self.audio.play()
			time.sleep(.5)
			self.audio.pause()
		self.termx = self.video.x
		self.termy = self.video.y + self.button_offset
		self.spf = self.video.spf
		self.last_frame_time = 0
		self.frame_num = 0
		# Add a check to see if the terminal
		# is full screen or not
		# Dont resize if full screen and video
		# is smaller than video requires
		Screens.print_starter(self.termx,self.termy,self.button_offset,self.frame_num,self.video.max_frames)
		self.loaded = True

	def queue_at_time(self,video,audio,time):
		pass

	def play_pause(self):
		self.play = not self.play
		if self.audio:
			self.audio_changed = True
		self.last_frame_time = time.time()

	def stop(self):
		# End current video, close files
		self.play=False
		self.loaded=False
		if self.audio:
			self.audio.stop()
		self.audio = None
		if self.video != None and self.video.file:
			self.video.file.close()
		self.last_frame_time = 0

	def render_selector(self):
		# Print the file selector
		term_len = self.termy-1
		Screens.print_selector(self.selector.files,self.selector.cursor,term_len)

	def increment_cursor(self):
		if self.selector.target == 0:
			self.selector.increment_main_cursor()
		else:
			self.selector.increment_backup_cursor()

	def decrement_cursor(self):
		if self.selector.target == 0:
			self.selector.decrement_main_cursor()
		else:
			self.selector.decrement_backup_cursor()
	
	def next_frame(self):
		if self.last_frame_time == 0:
			self.last_frame_time = time.time()
		text = self.video.read_frame()
		if text == "":
			self.stop()
			return
		curr_time = time.time()
		# Wait until its time for the frame
		while(curr_time < self.last_frame_time+self.spf):
			time.sleep(.0002)
			curr_time = time.time()
		# Try to keep on schedule
		self.last_frame_time += self.spf
		self.frame_num += 1
		Screens.print_frame(text,self.frame_num,self.video.max_frames, self.termx-4)

	def skip(self, time_interval):
		req_pause = self.play # Do I have to stop beforehand?
		time_val = 0
		if req_pause: # Pause
			self.play_pause()
			time.sleep(self.spf)
		num_frames = math.floor(time_interval/self.spf)
		self.frame_num += num_frames
		if self.audio:
			time_val = self.audio.get_time()
		if self.frame_num < 0:
			self.frame_num = 0
			time_val = 0
		elif self.frame_num >= self.video.max_frames-10:
			self.stop()
			return
		else:
			time_val += int(time_interval*1000)
		self.video.seek_frame(self.frame_num)
		if self.audio:
			self.audio.set_time(time_val)
		if req_pause: # Play again
			self.play_pause()
		else:
			self.next_frame()
