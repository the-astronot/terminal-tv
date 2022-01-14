# My files
from src.converter.Video import Video
from src.converter.Frame import Frame
from src.converter.ImageP import ImageP
from src.converter.Printer import Printer
from src.io.FileWriter import FileWriter
# Libraries
import cv2
import math
import os


def convert(filename, dest, term_width, fps_set):
	video = Video(filename)
	file = os.path.basename(filename).replace(".mkv",".trm")
	audio_filename = os.path.join(dest,file.strip(".trm"))
	if not os.path.exists(audio_filename+".mp3"):
		print("Beginning Stripping Audio...")
		video.strip_audio(audio_filename)
		print("Finishing Stripping Audio")
	# Getting video dimensions
	print("Getting Video Dimensions")
	width = video.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = video.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	fps = video.vidcap.get(cv2.CAP_PROP_FPS)
	frames = video.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
	print("[Width] = {0}\n[Height] = {1}\n[FPS] = {2}".format(width,height,fps))
	# User set dimensions
	fps_set = min(fps_set,fps)
	# Working out other vals
	interval = math.ceil(fps/fps_set)
	#total_frames = float(frames/interval)
	sec_per_frame = float(interval/fps)
	# Sets image reduction levels
	x_redux = math.ceil(width/float(term_width))
	y_redux = math.ceil(x_redux*2.2)
	# BEGIN PROCESSING
	success, image = video.get_frame(interval)
	imagep = ImageP(image)
	c_frame = Frame(imagep,x_redux,y_redux)
	c_frame.reduce_to_two()
	filewriter = FileWriter(os.path.join(dest,file),c_frame.x,c_frame.y,sec_per_frame)
	filewriter.add_frame(c_frame)
	# PROCESS UNTIL EOF
	frame_count = 1
	while(success):
		print("{:.2f}% Complete".format(float(frame_count/total_frames)*100),end="\r")
		success, image = video.get_frame(interval)
		if not success:
			break
		imagep = ImageP(image)
		c_frame = Frame(imagep,x_redux,y_redux)
		c_frame.reduce_to_two()
		filewriter.add_frame(c_frame)
		frame_count += 1
	# CLOSE EVERYTHING UP
	filewriter.end_file()
	video.vidcap.release()
	cv2.destroyAllWindows()
