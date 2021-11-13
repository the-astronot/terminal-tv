

class Character:
	char = "."
	fg, bg = "wht", "blk"
	
	def __init__(self):
		pass

	def assign_fg_bg(self, fg, bg):
		self.fg = fg
		self.bg = bg

	def get_fg_bg(self):
		return self.fg,self.bg
