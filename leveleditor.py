import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
tile_size = 25
cols = 48
row = 32
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * row) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

bg_tech = pygame.image.load('BackgroundGreen.jpg')
layer1 = pygame.image.load('grey.jpg')

layer1scaled = pygame.transform.scale(layer1, (1000, 700))


#load images
Passable_Tile = pygame.image.load('walktile.jpg')
Impassable_Tile = pygame.image.load('wall.jpg')
GreenDoor_Locked = pygame.image.load('greendoor.jpg')
YellowDoor_Locked = pygame.image.load('yellowdoor.jpg')
BlueDoor_Locked = pygame.image.load('bluedoor.jpg')
RedDoor_Locked = pygame.image.load('reddoor.jpg')
Blue_Key = pygame.image.load('bluekey.jpg')
Red_Key = pygame.image.load('redkey.jpg')
Green_Key = pygame.image.load('greenkey.jpg')
Yellow_key = pygame.image.load('yellowkey.jpg')
Com_Chip = pygame.image.load('chip.jpg')
End_gate = pygame.image.load('endgate.jpg')
End_tile = pygame.image.load('endtile.jpg')
Fire = pygame.image.load('fire.jpg')
Fire_Boots = pygame.image.load('fireboots.jpg')
Water = pygame.image.load('water.jpg')
Water_boots = pygame.image.load('waterboots.jpg')
Thief = pygame.image.load('thief.jpg')
slide_right = pygame.image.load('slideright.jpg')
slide_left = pygame.image.load('slideleft.jpg')
slide_down = pygame.image.load('slidedown.jpg')
slide_up = pygame.image.load('slideup.jpg')
slide_boots = pygame.image.load('slideboots.jpg')
ice_plain = pygame.image.load('ice.jpg')
ice_URcorner = pygame.image.load ('iceTR.jpg')
ice_ULcorner = pygame.image.load('iceTL.jpg')
ice_LRcorner = pygame.image.load('iceLR.jpg')
ice_LLcorner = pygame.image.load('iceLL.jpg')
ice_boots = pygame.image.load('iceboots.jpg')
save_img = pygame.image.load('save_btn.png')
load_img = pygame.image.load('load_btn.png')
mons = pygame.image.load('monster.jpg')
tp = pygame.image.load('tp.jpg')
tpr = pygame.image.load('tprec.jpg')


#define game variables
clicked = False
level = 1

#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(48):
	r = [0] * 48
	world_data.append(r)

# #create boundary
# for tile in range(0, 20):
# 	world_data[19][tile] = 2
# 	world_data[0][tile] = 1
# 	world_data[tile][0] = 1
# 	world_data[tile][19] = 1

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for c in range(49):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
	for r in range(33):
		#horizontal lines
		pygame.draw.line(screen, white, (0, r * tile_size), (screen_width, r * tile_size))

def draw_world():
	for row in range(32):
		for col in range(48):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					img = pygame.transform.scale(Passable_Tile, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					img = pygame.transform.scale(Impassable_Tile, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					img = pygame.transform.scale(GreenDoor_Locked, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 4:
					img = pygame.transform.scale(YellowDoor_Locked, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5:
					img = pygame.transform.scale(Green_Key, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 6:
					img = pygame.transform.scale(Yellow_key, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 7:
					img = pygame.transform.scale(Com_Chip, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 8:
					img = pygame.transform.scale(End_gate, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 9:
					img = pygame.transform.scale(End_tile, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 10:
					img = pygame.transform.scale(Fire, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 11:
					img = pygame.transform.scale(Fire_Boots, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 12:
					img = pygame.transform.scale(Water, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 13:
					img = pygame.transform.scale(Water_boots, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 14:
					img = pygame.transform.scale(Thief, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 15:
					img = pygame.transform.scale(slide_right, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 16:
					img = pygame.transform.scale(slide_left, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 17:
					img = pygame.transform.scale(slide_down, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 18:
					img = pygame.transform.scale(slide_up, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 19:
					img = pygame.transform.scale(slide_boots, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 20:
					img = pygame.transform.scale(ice_plain, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 21:
					img = pygame.transform.scale(ice_LLcorner, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 22:
					img = pygame.transform.scale(ice_LRcorner, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 23:
					img = pygame.transform.scale(ice_ULcorner, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 24:
					img = pygame.transform.scale(ice_URcorner, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 25:
					img = pygame.transform.scale(ice_boots, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 26:
					img = pygame.transform.scale(RedDoor_Locked, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 27:
					img = pygame.transform.scale(Red_Key, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 28:
					img = pygame.transform.scale(BlueDoor_Locked, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 29:
					img = pygame.transform.scale(Blue_Key, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 30:
					img = pygame.transform.scale(ice_plain, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 31:
					img = pygame.transform.scale(mons, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 32:
					img = pygame.transform.scale(tp, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 33:
					img = pygame.transform.scale(tpr, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create load and save buttons
save_button = Button(screen_width // 2 - 150, screen_height - 50, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 50, load_img)


#main game loop
run = True
while run:

	clock.tick(fps)

	#draw background
	screen.fill(green)
	screen.blit(bg_tech, (0, 0))
	screen.blit(layer1scaled, (100, 50))

	#load and save level
	if save_button.draw():
		#save level data
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)
			for row in world_data:
				print(row)



	#show the grid and draw the level tiles
	draw_grid()
	draw_world()


	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 50)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 30)

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < 48 and y < 32:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 33:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 33
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#update game display window
	pygame.display.update()

pygame.quit()