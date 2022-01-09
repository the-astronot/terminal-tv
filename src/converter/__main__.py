# My files
from src.converter.Video import Video
from src.converter.Frame import Frame
from src.converter.ImageP import ImageP
from src.converter.Character import Character
from src.converter.Printer import Printer
from src.io.FileWriter import FileWriter
# Libraries
import cv2
import math


if __name__ == '__main__':
	filename = "videos/Gorillaz.mkv"
	filename = "videos/Bojack_Horseman_S01E01.mkv"
	video = Video(filename)
	printer = Printer()
	#video.strip_audio("audio/{}".format(filename.split("/")[-1].strip(".mkv")))
	# Getting video dimensions
	width = video.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = video.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	fps = video.vidcap.get(cv2.CAP_PROP_FPS)
	print("[Width] = {0}\n[Height] = {1}\n[FPS] = {2}".format(width,height,fps))
	# User set dimensions
	term_width = 200
	#interval = math.ceil(fps/2.0)
	interval = math.ceil(fps/10.0)
	sec_per_frame = float(interval/fps)
	# Sets image reduction levels
	x_redux = math.ceil(width/float(term_width))
	y_redux = math.ceil(x_redux*2.2)
	# BEGIN PROCESSING
	success, image = video.get_frame(interval)
	imagep = ImageP(image)
	c_frame = Frame(imagep,x_redux,y_redux)
	c_frame.reduce_to_two()
	filewriter = FileWriter("test.txt",c_frame.x,c_frame.y,sec_per_frame)
	filewriter.add_frame(c_frame)
	# PROCESS UNTIL EOF
	while(success):
		success, image = video.get_frame(interval)
		if not success:
			break
		imagep = ImageP(image)
		c_frame = Frame(imagep,x_redux,y_redux)
		c_frame.reduce_to_two()
		filewriter.add_frame(c_frame)
	# CLOSE EVERYTHING UP
	filewriter.end_file()
	video.vidcap.release()
	cv2.destroyAllWindows()
