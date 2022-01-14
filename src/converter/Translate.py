colors = [30,34,32,36,31,35,33,37]
chars = [':','n','B','@']

def translate(fg_val,bg_val,char_val):
	fg = colors[fg_val]
	bg = colors[bg_val]+10
	char = chars[char_val]
	return "\033[{0}m\033[{1}m{2}\033[0m".format(fg,bg,char)