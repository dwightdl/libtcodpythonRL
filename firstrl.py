import libtcodpy as tcod

# window size
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

LIMIT_FPS = 20

class Object:
	# generic object represented by a character on screen

	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color

	def move(self, dx, dy):
		# move by the given amount
		self.x += dx
		self.y += dy

	def draw(self):
		# set the color and the draw the character that represents this object at its position
		tcod.console_set_default_foreground(con, self.color)
		tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

	def clear(self):
		#erase the character that represents this object
		tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)

def handle_keys():
	key = tcod.console_wait_for_keypress(True)

	if key.vk == tcod.KEY_ENTER and key.lalt:
		#Alt + Enter : toggle fullscreen
		tcod.console_set_fullscreen(not tcod.console_is_fullscreen())	

	elif key.vk == tcod.KEY_ESCAPE:
		return True #exit game
	
	# movement keys
	#up
	if tcod.console_is_key_pressed(tcod.KEY_UP):
	  player.move(0, -1)	

	#down
	elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
	  player.move(0, 1)	
	
	#left
	elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
	  player.move(-1, 0)	

	#right
	elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
	  player.move(1, 0)	




######
# INITIALIZATION AND MAIN GAME LOOP 
######

# init stuff 
tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
tcod.sys_set_fps(LIMIT_FPS)
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

# create object representing the player
player = Object(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, '@', tcod.white)

# create an NPC
npc = Object(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2, '@', tcod.yellow)

# the list of objects with those two
objects = [npc, player]

while not tcod.console_is_window_closed():

	# draw all objects in the list
	for object in objects:
		object.draw()

	# bit the contents of "con" to the root console and present it
	tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	tcod.console_flush()

	#erase all objects at their old locations, before they move
	for object in objects:
		object.clear()

	#handle keys and exit game if needed
	exit_game = handle_keys()
	if exit_game:
		break
