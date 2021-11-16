import math
import os
from Character import Character
from ImageP import ImageP
from Printer import Printer

class Frame:
	'''
	red_array = [127.5,0,0]
	yellow_array = [127.5,127.5,0]
	green_array = [0,127.5,0]
	cyan_array = [0,127.5,127.5]
	blue_array = [0,0,127.5]
	magenta_array = [127.5,0,127.5]
	white_array = [127.5,127.5,127.5]
	black_array = [0,0,0]
	'''
	red_arrays = [[100,15,15],[150,25,25],[60,5,5]]
	yellow_arrays = [[150,150,50],[150,110,0],[100,90,15],[200,150,50],[90,100,20],[60,60,5],[35,70,5]]
	green_arrays = [[110,150,10],[25,150,25],[15,100,15],[100,200,50],[5,60,5]]
	cyan_arrays = [[25,150,150],[15,100,100],[50,200,200],[5,80,80]]
	blue_arrays = [[25,25,150],[15,15,100],[50,50,200],[5,5,60]]
	magenta_arrays = [[150,25,150],[110,15,110],[200,50,200]]
	white_arrays = [[150,150,150],[200,200,200],[105,105,105]]
	black_arrays = [[15,15,15]]
	chars = [".",":","v","n","d","B","g","@"]
	g_hi = [255,255,255]
	g_lo = [0,0,0]
	color_arrays = [red_arrays,yellow_arrays,green_arrays,cyan_arrays,blue_arrays,magenta_arrays,white_arrays,black_arrays]
	color_names = ["red","ylw","grn","cyn","blu","mag","wht","blk"]

	def __init__(self, image,reduction_x, reduction_y):
		# image is of type ImageP
		self.image = image
		self.image.pixel_reduce(reduction_x, reduction_y)

	def reduce_to_two(self):
		colors = ["red","grn","blu"]
		rgb_vals = self.image.rgb_vals
		num_rows = len(rgb_vals)
		num_cols = len(rgb_vals[0])
		self.characters = [[Character() for _ in range(num_cols)] for _ in range(num_rows)]
		
		for i in range(num_rows):
			for j in range(num_cols):
				base = [0,0,0]
				mids = [0,0,0]
				red = rgb_vals[i][j][0]
				green = rgb_vals[i][j][1]
				blue = rgb_vals[i][j][2]
				white = (red+green+blue)/3.0
				black = 255-white
				
				highest_color = 2
				second_highest = 2
				highest_val = blue
				if green > highest_val:
					second_highest = highest_color
					highest_color = 1
					highest_val = green
				else:
					second_highest = 1
				if red > highest_val:
					second_highest = highest_color
					highest_color = 0
					highest_val = red
				elif red > rgb_vals[i][j][second_highest]:
					second_highest = 0
				base[highest_color] = 127.5
				mids[highest_color] = 127.5
				mids[second_highest] = 127.5
				bg,fg,char = self.get_closest(base, colors[highest_color], mids, [red,green,blue])
				self.characters[i][j].assign_fg_bg(fg,bg)
				self.characters[i][j].char = char


	def get_closest(self, base, main_color, mids, comp):
		low_dist = 255
		x = 0
		y = 0
		char = "."
		comparison = 30
		if (abs(abs(comp[0])-abs(comp[1])) < comparison) and (abs(abs(comp[0])-abs(comp[2])) < comparison) and (abs(abs(comp[1])-abs(comp[2])) < comparison):
			black_val = math.sqrt(math.pow(15-comp[0],2)+math.pow(15-comp[1],2)+math.pow(15-comp[2],2))
			white_val = math.sqrt(math.pow(200-comp[0],2)+math.pow(200-comp[1],2)+math.pow(200-comp[2],2))
			if white_val > black_val:
				main_color = "blk"
				best_color = [15,15,15]
				best_value = black_val
				#secondary = "wht"
				#secondary_value = math.sqrt(math.pow(215-comp[0],2)+math.pow(215-comp[1],2)+math.pow(215-comp[2],2))
			else:
				main_color = "wht"
				best_color = [200,200,200]
				best_value = white_val
				#secondary = "blk"
				#secondary_value = math.sqrt(math.pow(215-comp[0],2)+math.pow(215-comp[1],2)+math.pow(215-comp[2],2))
		else:
			for color in self.color_arrays:
				for shade in color:
					value = math.sqrt(math.pow(min(shade[0],255)-comp[0],2)+math.pow(min(shade[1],255)-comp[1],2)+math.pow(min(shade[2],255)-comp[2],2))
					if value < low_dist:
						low_dist = value
						main_color = self.color_names[x]
						best_color = shade
				x+=1
			best_value = low_dist
		low_dist = 255
		for color in self.color_arrays:
			for shade in color:
				value = math.sqrt(math.pow(min(best_color[0]+shade[0],255)-comp[0],2)+math.pow(min(best_color[1]+shade[1],255)-comp[1],2)+math.pow(min(best_color[2]+shade[2],255)-comp[2],2))
				if value < low_dist and (self.color_names[y]!= main_color):
					low_dist = value
					secondary = self.color_names[y]
					second_best = shade
			y+=1
		secondary_value = low_dist
		ratio = best_value/(secondary_value+1)
		for x in range(8):
			if ratio > math.pow(x,1.5)*.1+.7:
				char = self.chars[x]
	
		return main_color,secondary,char


if __name__ == '__main__':
	filename = "Initial_D"
	#filename = "takumi"
	#filename = "The_Great_Wave"
	#filename = "mind_fuzz"
	image = "../../images/{}.jpg".format(filename)
	processor = ImageP(image)
	o_x, o_y = processor.width, processor.height
	cols,rows = os.get_terminal_size()
	print(cols,rows)
	chunk_x = math.ceil(o_x/float(cols))
	chunk_y = math.ceil(o_y/float(rows-1))
	c_frame = Frame(processor,chunk_x,chunk_y)
	c_frame.reduce_to_two()
	printer = Printer()
	for y in range(len(c_frame.characters[0])):
		for x in range(len(c_frame.characters)):
			fg, bg = c_frame.characters[x][y].get_fg_bg()
			printer.change_fg(fg)
			printer.change_bg(bg)
			printer.option = c_frame.characters[x][y].option
			printer.print_char(c_frame.characters[x][y].char)
		print()
	printer.reset()
