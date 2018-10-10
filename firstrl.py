import libtcodpy as tcod

# map size
MAP_WIDTH = 80
MAP_HEIGHT = 45

# window size
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# parameters for dungeon generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

# field of vision
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

LIMIT_FPS = 20

color_dark_wall = tcod.Color(0, 0, 100)
color_light_wall = tcod.Color(130, 110, 50)
color_dark_ground = tcod.Color(50, 50, 150)
color_light_ground = tcod.Color(200, 180, 50)

class Tile:
	# a tile of the map and its properties
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked

		#by default, if a tile is blocked, it also blocks sight
		block_sight = blocked if block_sight is None else None
		self.block_sight = block_sight

class Rect:
	# a rectangle on the map. used to characterize a room
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h

	def center(self):
		center_x = (self.x1 + self.x2) // 2
		center_y = (self.y1 + self.y2) // 2
		return (center_x, center_y)

	def intersect(self, other):
		# returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
						self.y1 <= other.y2 and self.y2 >= other.y1)

class Object:
	# generic object represented by a character on screen

	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color

	def move(self, dx, dy):
		# move by the given amount
		if not map[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy

	def draw(self):
		# set the color and the draw the character that represents this object at its position
		tcod.console_set_default_foreground(con, self.color)
		tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

	def clear(self):
		#erase the character that represents this object
		tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)
		

def create_room(room):
	global map
	# go through the tiles in the rectangle and make them passable
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			map[x][y].blocked = False
			map[x][y].block_sight = False
			

def create_h_tunnel(x1, x2, y):
	global map
	#horizontal tunne. min() and max() are used in case x1>x2
	for x in range(min(x1, x2), max(x1, x2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False


def create_v_tunnel(y1, y2, x):
	global map
	# vertical tunnel
	for y in range(min(y1, y2), max(y1, y2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False


def make_map():
	global map

	# fill map with "blocked" tiles
	map = [
		[Tile(True) for y in range(MAP_HEIGHT)]
		for x in range(MAP_WIDTH)
	]

	rooms = []
	num_rooms = 0

	for r in range(MAX_ROOMS):
		# random width and height
		w = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		# random position without going out of boundaries of the map
		x = tcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
		y = tcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

		# "Rect" class makes rectangles easier to work with
		new_room = Rect(x, y, w, h)

		# run through the other rooms and see if they intersect with this one
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break

		if not failed:
			# this means there are no intersections, so this room is valid
			# "paint" it to the map's tiles
			create_room(new_room)

			# center coordinates of new room, will be useful later
			(new_x, new_y) = new_room.center()
			# print "room number" to see how the map drawing worked
			'''
			room_no = Object(new_x, new_y, chr(65 + num_rooms), tcod.white)
			objects.insert(0, room_no)
			'''

			if num_rooms == 0:
				# this is the first room, will be useful later
				player.x = new_x
				player.y = new_y
			else:
				# all rooms after the first:
				# connect it to the previous room with a tunnel

				# center coordinates of previous room
				(prev_x, prev_y) = rooms[num_rooms - 1].center()

				# draw a coin (RND that is 0 or 1)
				if tcod.random_get_int(0, 0, 1) == 1:
					# first move horizontally, then vertically
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, new_x)
				else:
					# first move vertically, then horizontally
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)

			# append the new room to the list
			rooms.append(new_room)
			num_rooms += 1


def render_all():
	global color_light_wall
	global color_light_ground
	global fov_recompute

	if fov_recompute:
		#recompute FOV if needed (the player moved or something)
		fov_recompute = False
		tcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

		# go through all tiles, and set their background color according to the FOV
		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				visible = tcod.map_is_in_fov(fov_map, x, y)
				wall = map[x][y].block_sight
				if not visible:
					# out of FOV
					if wall:
						tcod.console_set_char_background(con, x, y, color_dark_wall, tcod.BKGND_SET)
					else:
						tcod.console_set_char_background(con, x, y, color_dark_ground, tcod.BKGND_SET)
				else:
					# in FOV
					if wall:
						tcod.console_set_char_background(con, x, y, color_light_wall, tcod.BKGND_SET)
					else:
						tcod.console_set_char_background(con, x, y, color_light_ground, tcod.BKGND_SET)


	# draw all objects in the list
	for object in objects:
		object.draw()

	# bit the contents of "con" to the root console and present it
	tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def handle_keys():
	global fov_recompute

	key = tcod.console_wait_for_keypress(True)

	if key.vk == tcod.KEY_ENTER and key.lalt:
		#Alt + Enter : toggle fullscreen
		tcod.console_set_fullscreen(not tcod.console_is_fullscreen())	

	elif key.vk == tcod.KEY_ESCAPE:
		return True #exit game
	
	# movement keys
	#up
	if key.vk == tcod.KEY_CHAR:
		if key.c == ord('k'):
			player.move(0, -1)	
			fov_recompute = True

	#down
	if key.vk == tcod.KEY_CHAR:
		if key.c == ord('j'):
			player.move(0, 1)	
			fov_recompute = True
	
	#left
	if key.vk == tcod.KEY_CHAR:
		if key.c == ord('h'):
			player.move(-1, 0)	
			fov_recompute = True

	#right
	if key.vk == tcod.KEY_CHAR:
		if key.c == ord('l'):
			player.move(1, 0)	
			fov_recompute = True

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

# generate map
make_map()

# create the FOV map, according to the generated map
fov_map = tcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
	for x in range(MAP_WIDTH):
		tcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

fov_recompute = True

while not tcod.console_is_window_closed():

	#render the screen
	render_all()

	tcod.console_flush()

	#erase all objects at their old locations, before they move
	for object in objects:
		object.clear()

	#handle keys and exit game if needed
	exit = handle_keys()
	if exit:
		break
