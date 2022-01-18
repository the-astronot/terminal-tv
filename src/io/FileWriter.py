# CLASS: FILEWRITER
# AUTHOR: JORMUNGANDR
#####################
# MY IMPORTS
from src.converter.Frame import Frame
# IMPORTS
import os
import sys
import struct


# CLASS DEF
class FileWriter:

	colors = ["red","ylw","grn","cyn","blu","mag","wht","blk"]
	values = ['100','110','010','011','001','101','111','000']

	def __init__(self, filename, x, y, spf):
		self.filename = filename
		f = open(self.filename,"w")
		f.close()
		self.file = open(self.filename,"wb")
		self.file.write((x).to_bytes(2,byteorder="big"))
		self.file.write((y).to_bytes(2,byteorder="big"))
		self.file.write(struct.pack('>f',spf))

	def add_frame(self, frame):
		for y in range(len(frame.characters[0])):
			for x in range(len(frame.characters)):
				byte = ''
				fg, bg = frame.characters[x][y].get_fg_bg()
				char = frame.characters[x][y].char
				for i in range(8):
					if fg == self.colors[i]:
						byte += self.values[i]
						break
				for i in range(8):
					if bg == self.colors[i]:
						byte += self.values[i]
						break
				if char == ':':
					byte += '00'
				elif char == 'n':
					byte += '01'
				elif char == 'B':
					byte += '10'
				elif char == '@':
					byte += '11'
				#print(byte)
				byte_val = 0
				for i in range(8):
					if byte[7-i] == '1':
						byte_val += 2**i
				self.file.write((byte_val).to_bytes(1,byteorder="big"))

	def add_bytes(self, frame):
		for byte in frame.bytes:
			byte_val = 0
			for i in range(8):
				if byte[7-i] == '1':
					byte_val += 2**i
			self.file.write((byte_val).to_bytes(1,byteorder="big"))
	
	def end_file(self):
		self.file.close()
