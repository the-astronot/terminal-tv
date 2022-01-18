################################################################################
##  Terminal_TV pLayer                                                        ##
####  author: jormungandr                                                   ####
####  exec: python3 -m src.player                                           ####
####  created: 01/09/22                                                     ####
################################################################################
# Imports from src
from src.player.Player import Player
from src.io.KBHit import KBHit
import src.player.Screens as Screens
# Other Libraries
import os
import time

# Check audio availability
# Very basic, basically just checking 
# whether I'm using WSL or not
if os.name != "nt":
	global audio_available
	from Xlib import display, error
	try:
		d = display.Display()
		audio_available = True
	except error.DisplayNameError:
		audio_available = False
else:
	from colorama import init
	init()
	audio_available = True



# Dealing with user input
def on_press(key, player):
	if player.loaded:
		if key == "a":
			player.skip(-10)
		elif key == "d":
			player.skip(30)
		elif key == "e":
			player.stop()
			Screens.wipe_screen(player.termy)
		elif key == " ":
			player.play_pause()
		elif key == "w":
			# increase size
			pass
		elif key == "s":
			# decrease size
			pass
	else:
		if key == "w":
				player.decrement_cursor()
		elif key == "s":
				player.increment_cursor()
		elif key == " ":
			player.selector.toggle(player)
			#player.selector.toggle(player)
	if key == "q":
		if player.loaded:
			player.stop()
		Screens.wipe_screen(player.termy)
		print("\033[0m",end="\r")
		return False
	time.sleep(.05)
	return True


# Main loop
def main(player):
	kb = KBHit()
	player.selector.update_files()
	player.render_selector()
	loop = True
	while(loop):
		if player.audio_changed:
			player.audio_changed = False
			player.audio.pause()
		if player.play and player.loaded:
			player.next_frame()
		if kb.kbhit():
			loop = on_press(kb.getch(),player)
			if player.loaded == False and loop:
				player.render_selector()
	player.stop()
	kb.set_normal_term()
	print("\033[2J\033[H",end="")

	
if __name__ == '__main__':
	print("\033[2J",end="")
	media_location = os.path.join(os.getcwd(),"example_filesystem")
	player = Player(media_location,audio_available)
	main(player)
