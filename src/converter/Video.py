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
		#while(interval >=0 ):
			#success, image = self.vidcap.read()
			#interval -= 1
		self.vidcap.set(cv2.CAP_PROP_POS_FRAMES,self.curr_frame_num)
		self.curr_frame_num += interval
		return self.vidcap.read()

	def strip_audio(self,audiofilename):
		subprocess.call(["ffmpeg","-y","-i",self.filename,"{}.mp3".format(audiofilename)], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
		

if __name__ == '__main__':
	vidjya = Video("../../videos/Bojack_Horseman_S01E01.mkv")
	interval=24
	for x in range(60):
		cv2.imwrite("../../images/BH/{}.png".format(x+1),vidjya.get_frame(interval)[1])
	vidjya.vidcap.release()
	vidjya.strip_audio("../../audio/BH")
