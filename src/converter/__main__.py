from src.converter.config import run as runconfig
from src.converter.Converter import convert
import sys
import os
from dotenv import load_dotenv


def batch_convert(filename, delimiter):
	config_folder = os.path.join(os.path.dirname(__file__),"../../configs")
	media_drive = os.getenv("MEDIA_LOCATION")
	f = open(filename,"r")
	data = f.read()
	files = data.split("\n")
	defaults = ["","","",int(os.getenv("TERM_WIDTH")),int(os.getenv("FPS")),int(os.getenv("COLOR_OFFSET"))]
	for file in files:
		if file[0] != '#':
			job_data = file.split(delimiter)
			assert(len(job_data)==6)
			if len(job_data) != 0:
				# Data layout
				# video_path+name, dest_path, episode_name, termx, fps, color_offset
				for x in range(3,6):
					if job_data[x] == "":
						job_data[x] = defaults[x]
				config_file = os.path.join(config_folder,"config{}.conf".format(job_data[5]))
				if not os.path.exists(config_file):
					print("CONFIG NOT FOUND...\nGENERATING CONFIG")
					runconfig(int(job_data[5]),config_file,False)
					print("CONFIG GENERATED")
				color_dict = get_colors(config_file)
				convert(media_drive,job_data[0],job_data[2],job_data[1],int(job_data[3]),int(job_data[4]),color_dict)
				print()
			

def get_colors(config_file):
	color_dict = {}
	f = open(config_file,"r")
	text = f.read()
	for item in text.split("\n"):
		data = item.split("-")
		if len(data) > 1:
			color_dict[data[0]] = data[1]
	return color_dict


if __name__ == '__main__':
	load_dotenv()
	assert(len(sys.argv) > 1)
	filename = sys.argv[1]
	delimiter = os.getenv('DELIMITER')
	if len(sys.argv) == 3:
		delimiter = sys.argv[2]
	batch_convert(filename,delimiter)
