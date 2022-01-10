# CLASS: FILEREADER
# AUTHOR: JORMUNGANDR
#####################
# MY IMPORTS
from src.converter.Frame import Frame
from src.converter.Translate import translate
# IMPORTS
import os
import sys
import time
import struct


# CLASS DEF
class FileReader:

	colors = ["red","ylw","grn","cyn","blu","mag","wht","blk"]
	values = ['100','110','010','011','001','101','111','000']

	def __init__(self, filename):
		self.filename = filename
		self.file = open(self.filename,"rb")
		self.x = int.from_bytes(self.file.read(2),byteorder="big")
		self.y = int.from_bytes(self.file.read(2),byteorder="big")
		self.spf = struct.unpack('>f',self.file.read(4))[0]-.095

	def read_frame(self):
		text = ""
		for y in range(self.y):
			for _ in range(self.x):
				byte = self.file.read(1)
				if not byte:
					return ""
				byte_val = int.from_bytes(byte,byteorder="big")
				fg_val = 0
				bg_val = 0
				ch_val = 0
				for i in range(3):
					if byte_val >= 2**(7-i):
						fg_val += 2**(2-i)
						byte_val -= 2**(7-i)
				for i in range(3,6):
					if byte_val >= 2**(7-i):
						bg_val += 2**(5-i)
						byte_val -= 2**(7-i)
				for i in range(6,8):
					if byte_val >= 2**(7-i):
						ch_val += 2**(7-i)
						byte_val -= 2**(7-i)
				text += translate(fg_val,bg_val,ch_val)
			text += "\n"
		return text.strip("\n")


if __name__ == '__main__':
	print("\033[2J\033[0;0H",end="")
	filereader = FileReader("Gorillaz_10.txt")
	text = filereader.read_frame()
	while text != "":
		print(text,end="")
		text = filereader.read_frame()
		time.sleep(filereader.spf)
		print("\033[1;0H",end="")
	print("\033[2J\033[0;0H",end="")
	filereader.file.close()
	
