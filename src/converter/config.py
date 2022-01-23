import math


class Color:
	def __init__(self,r,g,b,name,number=None):
		self.r = r
		self.g = g
		self.b = b
		self.name = name
		self.number = number

class Char:
	def __init__(self,name,val,number=None):
		self.name = name
		self.val = val
		self.number = number

class Pixel:
	def __init__(self,fg,bg,char):
		self.fg = fg
		self.bg = bg
		self.char = char
		self.r = fg.r*char.val + bg.r*(1-char.val)
		self.g = fg.g*char.val + bg.g*(1-char.val)
		self.b = fg.b*char.val + bg.b*(1-char.val)


def run(color_booster,config_file,display):
	f = open(config_file,"w+")
	colors = []
	colors.append(Color(255,0,0,"RED","100"))
	colors.append(Color(255,255,0,"YLW","110"))
	colors.append(Color(0,255,0,"GRN","010"))
	colors.append(Color(0,255,255,"CYN","011"))
	colors.append(Color(0,0,255,"BLU","001"))
	colors.append(Color(255,0,255,"MAG","101"))
	colors.append(Color(0,0,0,"BLK","000"))
	colors.append(Color(255,255,255,"WHT","111"))
	chars = []
	chars.append(Char(":",.100,"00")) # .063 Real
	chars.append(Char("n",.200,"01"))	# .145 Real
	chars.append(Char("B",.300,"10")) # .224 Real
	chars.append(Char("@",.400,"11")) # .300 Real
	possibilities = []
	for bg in colors:
		for fg in colors:
			for char in chars:
				possibilities.append(Pixel(fg,bg,char))
				#r_comb = fg.r*char.val + bg.r*(1-char.val)
				#g_comb = fg.g*char.val + bg.g*(1-char.val)
				#b_comb = fg.b*char.val + bg.b*(1-char.val)
				#print("FG: {0}, BG: {1}, Char: {2} --> ({3},{4},{5})".format(fg.name,bg.name,char.name,r_comb,g_comb,b_comb))
	for r in range(0,256,8):
		for g in range(0,256,8):
			for b in range(0,256,8):
				lowest_dist = 255
				best = None
				for p in possibilities:
					dist = math.sqrt((p.r-r)**2+(p.g-g)**2+(p.b-b)**2)
					if p.r != p.g and p.r != p.b: # Color Booster
						dist -= color_booster
					if dist < lowest_dist:
						lowest_dist = dist
						best = p
				if display:
					print("({0},{1},{2}) --> ({3},{4},{5}) --> ({6},{7},{8})".format(r,g,b,best.r,best.g,best.b,best.fg.name,best.bg.name,best.char.name))
				line = "{0:03d}{1:03d}{2:03d}-{3}{4}{5}\n".format(int(r/8),int(g/8),int(b/8),best.fg.number,best.bg.number,best.char.number)
				f.write(line)
	f.close()



if __name__ == '__main__':
	color_booster = 15
	run(color_booster,"config.txt",True)