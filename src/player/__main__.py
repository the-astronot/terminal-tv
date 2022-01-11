################################################################################
##  Terminal_TV PLayer                                                        ##
####  author: jormungandr                                                   ####
####  exec: python3 -m src.player                                           ####
####  created: 01/09/22                                                     ####
################################################################################
# Imports from src
from src.player.Player import Player
from src.player.Directory import Directory
from src.io.FileReader import FileReader
from src.io.KBHit import KBHit
# Other Libraries
import time
import os
import sys
import threading
import getch as gh



# Dealing with user input
def accept_input(player):
	player.update_files()
	loop = True
	while(loop):
		if player.loaded == False:
			player.render_selector()
		loop = on_press(get_key(),player)

def on_press(key, player):
	global index
	#print(key)
	if key == "w":
		player.decrement_cursor()
	elif key == "s":
		player.increment_cursor()
	elif key == "\n":
		player.toggle()
	elif key == "p":
		player.play_pause()
	elif key == "q":
		print("\033[2J\033[H",end="")
		return False
	return True

def get_key():
    first_char = gh.getch()
    if first_char == '\x1b':
        return {'[A': 'up', '[B': 'down', '[C': 'right', '[D': 'left'}[gh.getch() + gh.getch()]
    else:
        return first_char

# Main loop
def main(player):
	kb = KBHit()
	player.update_files()
	player.render_selector()
	loop = True
	while(loop):
		if player.play and player.loaded:
			player.next_frame()
		if kb.kbhit():
			loop = on_press(kb.getch(),player)
			if player.loaded == False:
				player.render_selector()
	player.stop()
	kb.set_normal_term()

	
if __name__ == '__main__':
	print("\033[2J",end="")
	player = Player(os.getcwd())
	main(player)
