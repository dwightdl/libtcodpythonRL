import libtcodpy as tcod

######
# GLOBAL GAME SETTINGS
######
FULLSCREEN = False
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
# game controls
TURN_BASED = True

def initialize_game():
	# setup player
	global player_x, player_y
	player_x = SCREEN_WIDTH // 2
	player_y = SCREEN_HEIGHT // 2
	
	# setup font
	font_path = 'arial10x10.png'
	font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
	tcod.console_set_custom_font(font_path, font_flags)

	window_title = 'Python 3 libtcod tutorial'
	tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, FULLSCREEN)

	tcod.sys_set_fps(LIMIT_FPS)

######
# USER INPUT
######

def get_key_event(turn_based=None):
	if turn_based:
		# Turn-based game play; wait for a key stroke
		key = tcod.console_wait_for_keypress(True)
	else:
		key = tcod.console_check_for_keypress()
	return key

def handle_keys():
	global player_x, player_y

	key = tcod.console_check_for_keypress()

	if key.vk == tcod.KEY_ENTER and key.lalt:
		#Alt + Enter : toggle fullscreen
		tcod.console_set_fullscreen(not tcod.console_is_fullscreen())	

	elif key.vk == tcod.KEY_ESCAPE:
		return True #exit game
	
	# movement keys
	#up
	if tcod.console_is_key_pressed(tcod.KEY_UP):
		player_y = player_y - 1

	#down
	elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
		player_y = player_y + 1
	
	#left
	elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
		player_x = player_x - 1

	#right
	elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
		player_x = player_x + 1

######
# MAIN GAME LOOP 
######

def main():
	initialize_game()

	exit_game = False
	while not tcod.console_is_window_closed() and not exit_game:
		tcod.console_set_default_foreground(0, tcod.white)
		tcod.console_put_char(0, player_x, player_y, '@', tcod.BKGND_NONE)
		tcod.console_flush()
		tcod.console_put_char(0, player_x, player_y, ' ', tcod.BKGND_NONE)

		exit_game = handle_keys()

main()
