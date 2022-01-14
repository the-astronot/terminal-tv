from src.converter.Converter import convert
from src.converter.Quick_Converter import *
import os


if __name__ == '__main__':
	#filename = "videos/Initial_D_S01E01.mkv"
	#dest = "example_filesystem/tv_shows/initial_d"
	filename = "videos/Gorillaz.mkv"
	dest = "example_filesystem"
	term_width = 120
	fps = 10
	prep_convert(filename,dest,term_width,fps)
