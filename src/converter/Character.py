

class Character:
	colors = []
	values = []
	fg, bg = "wht", "blk"
	# Colors - 0 : White
	#				 - 1 : Black
	# 			 - 2 : Red
	#				 - 3 : Green
	#				 - 4 : Blue
	def __init__(self, char):
		self.char = char

	def assign_color(self,color_num, color_val):
		self.colors.append(color_num)
		self.values.append(color_val)

	def assign_fg_bg(self, fg, bg):
		self.fg = fg
		self.bg = bg