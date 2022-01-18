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
from multiprocessing import Process


frames = []
images = []
current_frame = 0
posted_frame = -1


def prep_convert(filename, dest, term_width, fps_set,dict):
	video = Video(filename)
	file = os.path.basename(filename).replace(".mkv",".trm")
	audio_filename = os.path.join(dest,file.replace(".trm",""))
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
	term_height = int(height/float(y_redux))
	divide_convert(interval,term_width,term_height,filename,sec_per_frame,total_frames,dest,file,dict)


def load_image(base,interval,filename,x_redux,y_redux,o_interval,dict):
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
		c_frame.reduce_to_bytes(dict)
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
	video.vidcap.release()
	return c_frame.x, c_frame.y


def calc_completion(frame_num,total_frames):
	percentage = (frame_num/float(total_frames))*100.0
	print("{:.2f}% Complete ".format(percentage),end="")


def quick_convert(interval,x_redux,y_redux,filename,sec_per_frame,total_frames,dest,file,dict):
	global frames
	global current_frame
	num_threads = 5
	loaders = []
	start_time  = time.time()
	for i in range(num_threads):
		l = threading.Thread(target=load_image,args=[interval*i,interval*num_threads,filename,x_redux,y_redux,interval,dict])
		loaders.append(l)
	for thread in loaders:
		thread.start()
	active = True
	x,y = get_x_and_y(filename,x_redux,y_redux)
	filewriter = FileWriter(os.path.join(dest,file),x,y,sec_per_frame)
	frame_num = 0
	while active:
		while len(frames)>0:
			filewriter.add_bytes(frames[0])
			frames.pop(0)
			frame_num += 1
			calc_completion(frame_num, total_frames)
			end_time = time.time()
			print("{:.3f} FPS".format(frame_num/(end_time-start_time)), end="\r")
		active = False
		for thread in loaders:
			if thread.isAlive():
				active = True
				break
	# CLOSE EVERYTHING UP
	filewriter.end_file()
	cv2.destroyAllWindows()


def load_frame(filename,interval):
	global images
	video = Video(filename)
	while True:
		success, image = video.get_frame(interval)
		if not success:
			break
		images.append(image)
		while len(images) > 10:
			time.sleep(.1)
	video.vidcap.release()


def convert_frame(i,x_redux,y_redux,dict,total_frames,num_threads):
	global images
	global current_frame
	global posted_frame
	while current_frame != total_frames:
		if current_frame % num_threads == i and len(images) > 0:
			this_frame = current_frame
			imagep = ImageP(images[0])
			images.pop(0)
			current_frame += 1
			frame = Frame(imagep,x_redux,y_redux)
			frame.reduce_to_bytes(dict)
			while this_frame != posted_frame + 1:
				time.sleep(.001)
			frames.append(frame)
			posted_frame +=1
		else:
			time.sleep(.001)


def modified_convert(interval,x_redux,y_redux,filename,sec_per_frame,total_frames,dest,file,dict):
	global frames
	global current_frame
	num_threads = 5
	converters = []
	start_time  = time.time()
	loader = threading.Thread(target=load_frame,args=[filename,interval])
	loader.start()
	for i in range(num_threads):
		c = Process(target=convert_frame,args=[i,x_redux,y_redux,dict,total_frames,num_threads])
		converters.append(c)
	for thread in converters:
		thread.start()
	active = True
	x,y = get_x_and_y(filename,x_redux,y_redux)
	filewriter = FileWriter(os.path.join(dest,file),x,y,sec_per_frame)
	frame_num = 0
	while active:
		while len(frames)>0:
			filewriter.add_bytes(frames[0])
			frames.pop(0)
			frame_num += 1
			calc_completion(frame_num, total_frames)
			end_time = time.time()
			print("{:.3f} FPS".format(frame_num/(end_time-start_time)), end="\r")
		active = False
		for thread in converters:
			if thread.is_alive():
				active = True
				break
	# CLOSE EVERYTHING UP
	filewriter.end_file()
	cv2.destroyAllWindows()


def divide_and_conquer(begin,end,interval,filename,i,term_width,term_height,dict):
	video = Video(filename)
	video.vidcap.set(cv2.CAP_PROP_POS_FRAMES,begin*interval)
	fw = FileWriter("temp{}.trm".format(i),0,0,0)
	for _ in range(begin,end):
		success, frame = video.get_frame(interval)
		if success:
			image = ImageP(frame,term_width,term_height)
			c_frame = Frame(image)
			c_frame.reduce_to_bytes(dict)
			fw.add_bytes(c_frame)
	fw.end_file()


def divide_convert(interval,term_width,term_height,filename,sec_per_frame,total_frames,dest,file,dict):
	num_threads = 5
	converters = []
	jump = math.floor(total_frames/num_threads)
	extras = total_frames % num_threads
	begin = 0
	for i in range(num_threads):
		end = begin + jump
		if extras > 0:
			end += 1
			extras -= 1
		c = Process(target=divide_and_conquer,args=[begin,end,interval,filename,i,term_width,term_height,dict])
		converters.append(c)
		begin = end
	for thread in converters:
		thread.start()
	filewriter = FileWriter(os.path.join(dest,file),term_width,term_height,sec_per_frame)
	for thread in converters:
		thread.join()
	for x in range(num_threads):
		file = "temp{}.trm".format(x)
		f = open(file,"rb")
		f.seek(8)
		frame_data = f.read(term_width*term_height)
		while frame_data:
			filewriter.file.write(frame_data)
			frame_data = f.read(term_width*term_height)
		f.close()
	filewriter.end_file()
	cv2.destroyAllWindows()