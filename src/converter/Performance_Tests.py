from src.converter.Converter import convert

import threading
import time
import os
import cv2


filename = "videos/Gorillaz.mkv"


def get_frames(filename, interval):
	global frame_num
	video = cv2.VideoCapture(filename)
	while True:
		success, frame = video.read()
		video.set(cv2.CAP_PROP_POS_FRAMES,interval*frame_num)
		if not success:
			break
		frame_num += 1



if __name__ == '__main__':
	interval = 2
	frame_num = 0
	start = time.time()
	load = threading.Thread(target=get_frames,args=[filename,interval])
	load1 = threading.Thread(target=get_frames,args=[filename,interval])
	load2 = threading.Thread(target=get_frames,args=[filename,interval])
	load.start()
	load1.start()
	load2.start()
	while True:
		end = time.time()
		print("{} FPS".format(frame_num/(end-start)),end="\r")
		if not load.is_alive():
			break
