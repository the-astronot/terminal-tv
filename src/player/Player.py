################################################################################
##  Terminal_TV Player                                                        ##
####  author: jormungandr                                                   ####
####  exec: none                                                            ####
####  created: 01/09/22                                                     ####
################################################################################
from src.player.Selector import Selector
from src.io.FileReader import FileReader
import src.player.Screens as Screens
###########
import os
import time
import math
import vlc


class Player:

	button_offset = 2

	def __init__(self, path_to_files,audio_available):
		self.path_to_files = path_to_files
		self.termx, self.termy = os.get_terminal_size()
		self.selector = Selector(path_to_files)
		self.loaded = False
		self.play = False
		self.audio_available = audio_available
		self.audio = None
		self.video = None
		self.audio_changed = False
		self.episode = None
	
	def queue(self, episode, index=None):
		self.episode = episode
		if index == None:
			index = episode.get_closest(self.termx)
			if index == -1:
				return
		self.episode_index = index
		self.video = FileReader(os.path.join(self.path_to_files,episode.files[index]))
		self.termx = self.video.x
		self.termy = self.video.y + self.button_offset
		self.spf = self.video.spf
		self.last_frame_time = 0
		self.frame_num = int(episode.time/self.spf)
		self.video.seek_frame(self.frame_num)
		if episode.audio_file != "" and self.audio_available and os.path.exists(os.path.join(self.path_to_files,episode.audio_file)):
			self.audio = vlc.MediaPlayer(os.path.join(self.path_to_files,episode.audio_file))
			self.audio.audio_set_volume(0)
			self.audio.play()
			time.sleep(.5)
			self.audio.pause()
			self.audio.set_time(int((self.frame_num*self.spf)*1000))
			self.audio.audio_set_volume(100)
		# Add a check to see if the terminal
		# is full screen or not
		# Dont resize if full screen and video
		# is smaller than video requires
		Screens.print_starter(self.termx,self.termy,self.button_offset,self.frame_num,self.video.max_frames)
		self.loaded = True

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
		# Save episode data
		if self.episode != None:
			if self.frame_num >= self.video.max_frames-(60/self.spf):
				self.episode.time = 0
			else:
				self.episode.time = self.spf*self.frame_num
			self.episode.write_episode()
		self.episode = None

	def render_selector(self):
		# Print the file selector
		term_len = self.termy-1
		if self.selector.target == 0:
			Screens.print_selector(self.selector.files,self.selector.cursor,term_len)
		else:
			Screens.print_pickup(term_len,self.termx,self.selector.episode.time,self.selector.backup_cursor)

	def increment_cursor(self):
		if self.selector.target == 0:
			self.selector.increment_main_cursor()
		else:
			self.selector.increment_backup_cursor(2)

	def decrement_cursor(self):
		if self.selector.target == 0:
			self.selector.decrement_main_cursor()
		else:
			self.selector.decrement_backup_cursor()
	
	def next_frame(self):
		if self.last_frame_time == 0:
			self.last_frame_time = time.time()
		curr_time = time.time()
		while curr_time > self.last_frame_time+(self.spf):
			# if lagging behind, skip frames
			# this tends to occur for larger videos
			self.frame_num += 1
			self.video.seek_frame(self.frame_num)
			self.last_frame_time += self.spf
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
		# Jump forward (pos) or backwards (neg)
		req_pause = self.play and self.audio # Do I have to stop beforehand?
		time_val = 0
		if req_pause: # Pause
			self.audio.pause()
			self.audio_changed = True
			#time.sleep(.5)
		num_frames = math.floor(time_interval/self.spf)
		self.frame_num += num_frames
		if self.frame_num < 0:
			self.frame_num = 0
			time_val = 0
		elif self.frame_num >= self.video.max_frames-10:
			self.audio_changed = False
			self.stop()
			return
		else:
			time_val = int(self.frame_num*self.spf*1000)
		self.video.seek_frame(self.frame_num)
		if self.audio:
			self.audio.set_time(time_val)
		self.next_frame()

	def change_resolution(self,direction):
		# Get next size if it exists, and queue it
		index = self.episode.get_closest(self.termx,direction)
		if index != self.episode_index:
			self.episode.time = self.frame_num*self.spf
			episode = self.episode
			self.stop()
			self.queue(episode,index)
