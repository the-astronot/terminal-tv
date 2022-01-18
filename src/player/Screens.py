################################################################################
##  Terminal_TV Screens                                                       ##
####  author: jormungandr                                                   ####
####  exec: none                                                            ####
####  created: 01/13/22                                                     ####
################################################################################
# Imports from src
from src.player.Progress_Bar import progress_bar
# Library Imports
import math


def print_selector(files,cursor,term_len):
	length = len(files[0])
	midway = math.floor(term_len/2)
	# Determine what to print
	if length < term_len:
		begin = 0
		end = length
	else:
		begin = cursor - midway
		end = begin + term_len
		while begin < 0:
			begin +=1
			end += 1
		while end > length:
			begin -=1
			end -= 1
	# Gross Printing Logic
	print("\033[H",end="")
	for i in range(begin,end):
		if i == cursor:
			print("\033[K\033[30m\033[47m{0}\033[40m\033[37m".format(files[0][i]))
		else:
			print("\033[K\033[40m\033[37m{0}".format(files[0][i]))
	print("\033[K\033[40m\033[37m",end="")
	for i in range(0,term_len-length):
		print("\033[K")


def print_starter(termx,termy,b_offset,frame_num,max_frames):
	wipe_screen(termy)
	# Resize screen
	print("\033[8;{0};{1}t".format(termy,termx))
	wipe_screen(termy)
	start_frame = ""
	for _ in range(termy-b_offset):
		start_frame += "#"*termx + "\n"
	start_frame += progress_bar(frame_num, max_frames, termx-4) + "\n"
	start_frame += "|[Q] Quit\t|[Space] Play/Pause\t|[E] Eject\t|[A] Rewind\t|[D] Fast_Forward\t|"
	print(start_frame,end="")
	print("\033[H",end="")


def print_frame(text, frame_num, max_frames, width):
	print("\033[H",end="")
	print(text)
	print(progress_bar(frame_num,max_frames,width))
	print("|[Q] Quit\t|[Space] Play/Pause\t|[E] Eject\t|[A] Rewind\t|[D] Fast_Forward\t|",end="")


def print_pickup(termy,termx,ptime,cursor):
	midway = math.floor((termy-2)/2)
	continue_text = "Continue at {}".format(ptime)
	restart_text = "Restart Media"
	wipe_screen(termy)
	for _ in range(midway):
		print("\033[K")
	if cursor == 0:
		print("\033[K\033[30m\033[47m{0}".format(continue_text.center(termx)))
		print("\033[K\033[40m\033[37m{0}".format(restart_text.center(termx)))
	else:
		print("\033[K\033[40m\033[37m{0}".format(continue_text.center(termx)))
		print("\033[K\033[30m\033[47m{0}\033[40m\033[37m".format(restart_text.center(termx)))


def wipe_screen(termy):
	print("\033[H",end="")
	for _ in range(termy):
		print("\033[K")
	print("\033[H",end="")
