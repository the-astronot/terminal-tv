from Character import Character
from ImageP import ImageP
from Printer import Printer

class Frame:
	def __init__(self, image,reduction):
		# image is of type ImageP
		self.image = image
		self.image.pixel_reduce(reduction)

	def reduce_to_two(self):
		rgb_vals = self.image.rgb_vals
		num_rows = len(rgb_vals[0])
		num_cols = len(rgb_vals)
		self.characters = [[Character for _ in range(num_rows)] for _ in range(num_cols)]
		for _ in self.characters:
			print("[",end='')
			for _ in self.characters[0]:
				print(" 0 ",end='')
			print("]")
		for i in range(num_rows):
			for column in rgb_vals:
				pass

