# This file was copied from one of my other projects, Project-Pixel, 
# that turns images into pixel art
# Author: jormungandr

from PIL import Image
import math

class ImageP:
	
	def __init__(self, filename):
		self.original = filename
		self.o_image = Image.open(self.original)
		self.o_pixels = self.o_image.load()
		self.width, self.height = self.o_image.size
		#self.new_image = Image.new(mode="RGB",size=(self.width,self.height))
		#self.new_pixels = self.new_image.load()
		self.rgb_vals = []

	def save_modified_relative(self, filename):
		self.new_image.save("../{}.jpg".format(filename))

	def get_average(self, index0, index1, index2, index3):
		num_pixels = 0.0
		r_sum = 0.0
		g_sum = 0.0
		b_sum = 0.0
		for i in range(index0, index1):
			for j in range(index2, index3):
				triple = self.o_pixels[i,j]
				r_sum += triple[0]
				g_sum += triple[1]
				b_sum += triple[2]
				num_pixels += 1.0
		averages = (0,0,0)
		r_avg = math.floor((r_sum/num_pixels)+.5)
		g_avg = math.floor((g_sum/num_pixels)+.5)
		b_avg = math.floor((b_sum/num_pixels)+.5)
		averages = (r_avg,g_avg,b_avg)
		return averages

	def pixel_reduce(self, pixels_per_chunk):
		self.rgb_vals = []
		averages = ()
		for x in range(0,self.width,pixels_per_chunk):
			column = []
			for y in range(0,self.height,pixels_per_chunk):
				averages = self.get_average(x,min(x+pixels_per_chunk,self.width),y,min(y+pixels_per_chunk,self.height))
				print(averages)
				column.append(averages)
			self.rgb_vals.append(column)

	def palette_reduce(self, palette_size):
		pass

"""	
	def modify_file_from_array(self, chunk_size):
		print(len(self.rgb_vals), len(self.rgb_vals[0]))
		width = len(self.rgb_vals)*chunk_size
		height = len(self.rgb_vals[-1])*chunk_size
		print(width,height)
		self.new_image = Image.new(mode="RGB",size=(width,height))
		self.new_pixels = self.new_image.load()
		for i in range(len(self.rgb_vals)):
			for j in range(len(self.rgb_vals[0])):
				for x in range(i*chunk_size,(i+1)*chunk_size):
					for y in range(j*chunk_size,(j+1)*chunk_size):
						self.new_pixels[x,y] = self.rgb_vals[i][j]
		self.save_modified()
"""
