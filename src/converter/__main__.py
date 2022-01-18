from src.converter.Converter import convert
from src.converter.Quick_Converter import *
import os


if __name__ == '__main__':
	filename = "videos/S01E01_Space_Pilot_3000.mkv"
	#dest = "example_filesystem/tv_shows/scooby_doo/"
	## Comparison
	#filename = "videos/S01E01_Yesterday's_Jam.mkv"
	#dest = "example_filesystem/test/"
	#filename = "videos/Initial_D_S01E02.mkv"
	dest = "example_filesystem/test/"
	term_width = 160
	fps = 15
	dict = {}
	f = open("src/converter/config.txt","r")
	text = f.read()
	for item in text.split("\n"):
		data = item.split("-")
		if len(data) > 1:
			dict[data[0]] = data[1]
	convert(filename,dest,term_width,fps,dict)
