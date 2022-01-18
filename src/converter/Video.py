import os
import subprocess
import cv2
from src.converter.Frame import Frame
from src.converter.ImageP import ImageP

class Video:
	def __init__(self, filename):
		self.filename = filename
		self.vidcap = cv2.VideoCapture(self.filename)
		self.curr_frame_num = 0
	
	def get_frame(self,interval):
		for _ in range(interval-1):
			self.vidcap.read()
		self.curr_frame_num += interval
		return self.vidcap.read()

	def strip_audio(self,audiofilename):
		subprocess.call(["ffmpeg","-y","-i",self.filename,"{}.mp3".format(audiofilename)], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
		