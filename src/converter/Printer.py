

class Printer:
	def __init__(self):
		self.fg = 37
		self.bg = 40
		self.option = ""

	def change_fg(self,new_color):
		colors = ["blk","red","grn","ylw","blu","mag","cyn","wht"]
		codes = [30,31,32,33,34,35,36,37]
		for color_num in range(len(colors)):
			if colors[color_num] == new_color:
				self.fg = codes[color_num]
	def change_bg(self,new_color):
		colors = ["blk","red","grn","ylw","blu","mag","cyn","wht"]
		codes = [40,41,42,43,44,45,46,47]
		for color_num in range(len(colors)):
			if colors[color_num] == new_color:
				self.bg = codes[color_num]
	def toggle_bold(self,boolean):
		if boolean:
			self.option = "1:"
		else:
			self.option = ""

	def reset(self):
		self.fg = 37
		self.bg = 40
		self.option = ""
	
	def print_char(self, char):
		print("\033[{0}{1}m\033[{2}m{3}\033[0m".format(self.option,self.fg,self.bg,char),end="")


if __name__ == '__main__':
	# Test
	printer = Printer()
	for x in range(20):
		printer.print_char("M")
	print()
	printer.change_bg("blu")
	for x in range(20):
		printer.print_char("M")
	print()
	printer.toggle_bold(True)
	for x in range(20):
		printer.print_char("M")
	print()
	printer.toggle_bold(False)
	printer.change_fg("grn")
	printer.change_bg("wht")
	for x in range(20):
		printer.print_char("M")
	print()
	printer.reset()
	printer.change_bg("red")
	printer.change_fg("blk")
	for x in range(20):
		printer.print_char("!")
	print()