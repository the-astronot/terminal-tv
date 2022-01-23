# My files
from src.converter.Video import Video
from src.converter.Frame import Frame
from src.converter.ImageP import ImageP
from src.converter.Printer import Printer
from src.io.FileWriter import FileWriter
from src.io.Episode import Episode
# Libraries
import cv2
import math
import os
import time


def convert(media_drive,filename,episode_name,dest,term_width,fps_set,dict):
	# Getting all of the names out of the way
	# Video Name -> Based of Current Dir -> fine
	# Episode_Name -> based on input and media drive -> append
	rel_episode_name = os.path.join(dest,episode_name) + ".dtrm"
	episode_name = os.path.join(media_drive,rel_episode_name)
	# Relative audioname -> derived from ep_name -> fine
	rel_audio_name = rel_episode_name.replace(".dtrm",".mp3")
	# Full audioname -> append
	audio_name = os.path.join(media_drive,rel_audio_name)
	# All folders on path to episode
	folders = os.path.dirname(episode_name)
	# File to save terminal file to

	# Open Video File
	video = Video(filename)
	# Create any required folders
	try:
		os.makedirs(folders)
	except OSError:
		pass
	# Create episode
	episode = Episode(episode_name)
	episode.read_episode()
	# Save path for terminal file
	file = os.path.join(folders,(os.path.basename(filename)).replace(".mkv","").replace(".mp4","")+"_{}.trm".format(len(episode.files)))
	# Strip audio
	if episode.audio_file == "":
		print("Beginning Stripping Audio...")
		video.strip_audio(audio_name)
		episode.audio_file = rel_audio_name
		print("Finishing Stripping Audio")
	# Getting video dimensions
	print("Getting Video Dimensions")
	width = video.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = video.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	fps = video.vidcap.get(cv2.CAP_PROP_FPS)
	frames = video.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
	print("[Width] = {0}\n[Height] = {1}\n[FPS] = {2:.3f}".format(width,height,fps))
	# User set dimensions
	fps_set = min(fps_set,fps)
	# Working out other vals
	interval = math.ceil(fps/fps_set)
	total_frames = int(frames/interval)
	sec_per_frame = float(float(interval)/float(fps))
	print("[Interval] = {1}\n[Sec/Frame] = {0:.5f}".format(sec_per_frame,interval))
	# Sets image reduction levels
	x_redux = width/float(term_width)
	y_redux = (x_redux*2)
	term_height = int(height/float(y_redux))
	# BEGIN PROCESSING
	start_time = time.time()
	filewriter = FileWriter(file,term_width,term_height,sec_per_frame)
	# PROCESS UNTIL EOF
	frame_count = 0
	while(frame_count < total_frames):
		success, image = video.get_frame(interval)
		if not success:
			break
		imagep = ImageP(image,term_width,term_height)
		c_frame = Frame(imagep)
		c_frame.reduce_to_bytes(dict)
		filewriter.add_bytes(c_frame)
		frame_count += 1
		end_time = time.time()
		print("{:.2f}% Complete {:.3f} FPS".format(float(frame_count/total_frames)*100,frame_count/(end_time-start_time)),end="\r")
	# CLOSE EVERYTHING UP
	episode.add_file(file,term_width)
	filewriter.end_file()
	episode.write_episode()
	video.vidcap.release()
	cv2.destroyAllWindows()
