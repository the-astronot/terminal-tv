import math

def progress_bar(current,maximum,width):
	color = "\033[32m"
	normal = "\033[37m"
	fraction = min(current/float(maximum),1.0)
	amount = math.floor(fraction*width)
	return color + " [" + "="*amount + "_"*(width-amount) + "] " + normal
