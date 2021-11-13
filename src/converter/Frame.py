import math
from Character import Character
from ImageP import ImageP
from Printer import Printer

class Frame:

	red_array = [127.5,0,0]
	green_array = [0,127.5,0]
	blue_array = [0,0,127.5]
	white_array = [127.5,127.5,127.5]
	black_array = [0,0,0]
	g_hi = [255,255,255]
	g_lo = [0,0,0]
	color_arrays = [red_array,green_array,blue_array,white_array,black_array]
	color_names = ["red","grn","blu","wht","blk"]

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
		#for _ in self.characters:
			#print("[",end='')
			#for _ in self.characters[0]:
				#print("0",end='')
			#print("")
		for i in range(num_rows):
			for j in range(num_cols):
				base = [0,0,0]
				red = rgb_vals[i][j][0]
				p_red = red/255.0
				green = rgb_vals[i][j][1]
				p_green = green/255.0
				blue = rgb_vals[i][j][2]
				p_blue = blue/255.0
				white = (red+green+blue)/3.0
				p_white = (p_red+p_green+p_blue)/3.0
				p_black = 1 - p_white
				#std_dev = math.sqrt((math.pow(red-white,2)+math.pow(green-white,2)+math.pow(blue-white,2))/3.0)
				#p_std_dev = (math.pow(p_white-p_red,2)+math.pow(p_white-p_green,2)+math.pow(p_white-p_blue,2))/3.0
				#print("{0}:{1}:{2:}:{3:.1f}->{4:.3f}".format(red,green,blue,white,std_dev))
				#print("{0:.3f}:{1:.3f}:{2:.3f}:{3:.3f}:{4:.3f}->{5:.5f}".format(p_red,p_green,p_blue,p_white,p_black,std_dev))
				#if(std_dev < 20):
					#self.characters[i][j].bg = "wht"
				highest_color = 2
				highest_val = blue
				if green > highest_val:
					highest_color = 1
					highest_val = green
				if red > highest_val:
					highest_color = 0
					highest_val = red
				base[highest_color] = 127.5
				bg,fg,char = self.get_closest(base, colors[highest_color], [red,green,blue])
				self.characters[i][j].assign_fg_bg(fg,bg)
				self.characters[i][j].char = char

	def get_closest(self, base, main_color, comp):
		low_dist = 255
		secondary = ""
		char = "."
		x = 0
		for array in self.color_arrays:
			c_array = [base[0]+array[0],base[1]+array[1],base[2]+array[2]]
			print(c_array,"->",comp)
			value = math.sqrt(math.pow(c_array[0]-comp[0],2)+math.pow(c_array[1]-comp[1],2)+math.pow(c_array[2]-comp[2],2))
			if value < low_dist:
				low_dist = value
				secondary = self.color_names[x]
			x+=1
		# Check Gray
		value0 = math.sqrt(math.pow(self.white_array[0]-comp[0],2)+math.pow(self.white_array[1]-comp[1],2)+math.pow(self.white_array[2]-comp[2],2))
		value1 = math.sqrt(math.pow(self.g_lo[0]-comp[0],2)+math.pow(self.g_lo[1]-comp[1],2)+math.pow(self.g_lo[2]-comp[2],2))
		value2 = math.sqrt(math.pow(self.g_hi[0]-comp[0],2)+math.pow(self.g_hi[1]-comp[1],2)+math.pow(self.g_hi[2]-comp[2],2))
		if value0 < low_dist:
			low_dist = value0
			main_color = "blk"
			secondary = "wht"
			char = "M"
		if value1 < low_dist:
			low_dist = value1
			main_color = "blk"
			secondary = "wht"
			char = "."
		if value2 < low_dist:
			low_dist = value2
			main_color = "wht"
			secondary = "blk"
			char = "."
		return main_color,secondary,char


if __name__ == '__main__':
	#filename = "PinkFloyd"
	filename = "Initial_D"
	image = "../../images/{}.jpg".format(filename)
	processor = ImageP(image)
	o_x, o_y = processor.width, processor.height
	chunk_x = math.ceil(o_x/80.0)
	chunk_y = math.ceil(o_y/24.0)
	c_frame = Frame(processor,chunk_x,chunk_y)
	c_frame.reduce_to_two()
	printer = Printer()
	for y in range(len(c_frame.characters[0])):
		for x in range(len(c_frame.characters)):
			fg, bg = c_frame.characters[x][y].get_fg_bg()
			printer.change_fg(fg)
			printer.change_bg(bg)
			printer.print_char(c_frame.characters[x][y].char)
		print()
