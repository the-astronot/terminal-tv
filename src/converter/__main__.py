from converter.Video import Video
from converter.Frame import Frame
from converter.ImageP import ImageP
from converter.Character import Character
from converter.Printer import Printer




if __name__ == '__main__':
	filename = "Gorillaz.mp4"
	interval = 24
	video = Video(filename)
	video.strip_audio("../../audio/{}".format(filename.strip(".mkv")))
	success = True
	while(success):
		success, image = video.get_frame(interval)
