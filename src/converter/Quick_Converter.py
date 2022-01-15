# My files
from src.converter.Video import Video
from src.converter.Frame import Frame
from src.converter.ImageP import ImageP
from src.io.FileWriter import FileWriter
# Libraries
import cv2
import math
import os
import threading
import random
import time


frames = []
current_frame = 0


def prep_convert(filename, dest, term_width, fps_set):
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
	print("[Width] = {0}\n[Height] = {1}\n[FPS] = {2}\n[Frames] = {3}".format(width,height,fps,frames))
	# User set dimensions
	fps_set = min(fps_set,fps)
	# Working out other vals
	interval = math.ceil(fps/fps_set)
	total_frames = float(frames/interval)
	sec_per_frame = float(interval/fps)
	print("[FPS_Set] = {0}\n[Interval] = {1}\n[Sec/Frame] = {2}".format(fps_set,interval,sec_per_frame))
	# Sets image reduction levels
	x_redux = math.ceil(width/float(term_width))
	y_redux = math.ceil(x_redux*2.2)
	quick_convert(interval,x_redux,y_redux,filename,sec_per_frame,total_frames,dest,file)


def load_image(base,interval,filename,x_redux,y_redux,o_interval):
	global frames
	global current_frame
	video = Video(filename)
	success, image = video.get_frame(base)
	ticking = base
	while True:
		success, image = video.get_frame(interval)
		if not success:
			break
		imagep = ImageP(image)
		c_frame = Frame(imagep,x_redux,y_redux)
		c_frame.reduce_to_two()
		while True:
			if ticking == current_frame:
				frames.append(c_frame)
				current_frame += o_interval
				break
			time.sleep(random.uniform(.001,.1))
		ticking += interval
	video.vidcap.release()


def get_x_and_y(filename,x_redux,y_redux):
	video = Video(filename)
	success, image = video.get_frame(0)
	imagep = ImageP(image)
	c_frame = Frame(imagep,x_redux,y_redux)
	c_frame.reduce_to_two()
	video.vidcap.release()
	return c_frame.x, c_frame.y


def calc_completion(frame_num,total_frames):
	percentage = (frame_num/float(total_frames))*100.0
	print("{:.2f}% Complete".format(percentage),end="\r")


def quick_convert(interval,x_redux,y_redux,filename,sec_per_frame,total_frames,dest,file):
	global frames
	global current_frame
	num_threads = 5
	loaders = []
	start_time  = time.time()
	for i in range(num_threads):
		l = threading.Thread(target=load_image,args=[interval*i,interval*num_threads,filename,x_redux,y_redux,interval])
		loaders.append(l)
	for thread in loaders:
		thread.start()
	active = True
	x,y = get_x_and_y(filename,x_redux,y_redux)
	filewriter = FileWriter(os.path.join(dest,file),x,y,sec_per_frame)
	frame_num = 0
	while active:
		while len(frames)>0:
			filewriter.add_frame(frames[0])
			frames.pop(0)
			frame_num += 1
			calc_completion(frame_num, total_frames)
			end_time = time.time()
			print("{} FPS".format(frame_num/(end_time-start_time)), end="")
		active = False
		for thread in loaders:
			if thread.isAlive():
				active = True
				break
	# CLOSE EVERYTHING UP
	filewriter.end_file()
	cv2.destroyAllWindows()

