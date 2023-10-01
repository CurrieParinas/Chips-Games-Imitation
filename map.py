import pygame
import pygame.sprite
from pygame import mixer
import pickle
import random
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


"""
framerate elements
"""
clock = pygame.time.Clock()
fps = 60


"""
screen dimensions
"""
WIDTH = 1300
HEIGHT = 850


"""
display a window with the given dimensions and window caption
"""
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chip's Challenge!")


"""
load image for backgrounds and game buttons
"""
bg_tech = pygame.transform.scale(pygame.image.load('img/pixelbg.jpg'), (WIDTH, HEIGHT))
layer1 = pygame.image.load('img/grey.jpg')
black = pygame.image.load('img/black.jpg')
layer_1 = pygame.image.load('img/bg_try1.jpg')
trophy = pygame.transform.scale(pygame.image.load('img/trophy.png'), (150, 169))
title = pygame.transform.scale(pygame.image.load('img/ChipsChallengeTitle.png'), (750, 150))
bg = pygame.transform.scale(pygame.image.load('img/bg.png'), (170, 268))
infog = pygame.transform.scale(pygame.image.load('img/info.png'), (124, 132))
infog2 = pygame.transform.scale(pygame.image.load('img/info.png'), (100, 105))
board = pygame.transform.scale(pygame.image.load('img/board.png'), (900, 567))
guide = pygame.transform.scale(pygame.image.load('img/guide.png'), (900, 567))
layer1scaled = pygame.transform.scale(layer1, (1000, 700))
layer_1scaled = pygame.transform.scale(layer_1, (1000, 700))
layer2scaled = pygame.transform.scale(layer1, (410, 70))
layer3scaled = pygame.transform.scale(layer1, (450, 70))
layer4scaled = pygame.transform.scale(layer1, (170, 70))
layer5scaled = pygame.transform.scale(layer1, (150, 205))
black_Layer = pygame.transform.scale(black, (420, 80))
black_Layer2 = pygame.transform.scale(black, (460, 80))
black_Layer3 = pygame.transform.scale(black, (1010, 710))
black_Layer4 = pygame.transform.scale(black, (180, 80))
black_Layer5 = pygame.transform.scale(black, (160, 215))

restart = pygame.transform.scale(pygame.image.load('img/reset.png'), (205, 120))
start = pygame.transform.scale(pygame.image.load('img/start.png'), (205, 120))
quit_game = pygame.transform.scale(pygame.image.load('img/quit.png'), (205, 120))
back = pygame.transform.scale(pygame.image.load('img/back.png'), (100, 63))
back2 = pygame.transform.scale(pygame.image.load('img/back.png'), (100, 63))
next = pygame.transform.scale(pygame.image.load('img/next.png'), (205, 120))
menu = pygame.transform.scale(pygame.image.load('img/menu.png'), (100, 63))


"""
sound and sound effects
"""
pygame.mixer.music.load('music/igMusic.wav')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
get_chips = pygame.mixer.Sound('music/get.wav')
get_chips.set_volume(0.3)
teleport_fx = pygame.mixer.Sound('music/teleport.wav')
teleport_fx.set_volume(0.3)
nextlvl_fx = pygame.mixer.Sound('music/exit.wav')
nextlvl_fx.set_volume(0.3)
gm_fx = pygame.mixer.Sound('music/gover.wav')
gm_fx.set_volume(0.3)
door_open = pygame.mixer.Sound('music/dooropen.wav')
door_open.set_volume(0.4)
get_keys = pygame.mixer.Sound('music/keys.wav')
get_keys.set_volume(0.4)
pickup_fx = pygame.mixer.Sound('music/pickup.wav')
pickup_fx.set_volume(0.4)

"""
game variables
"""
tile_size = 25
gameover = 0
main_menu = True
level = 1
number_of_levels = 4
number_of_chips = 15
time = 100
last_count = pygame.time.get_ticks()
score = 1000
high_score = False
guide_panel = False


"""
font and color
"""
font = pygame.font.Font("font/04B_30__.ttf", 15)
font2 = pygame.font.Font("font/04B_30__.ttf", 25)
font3 = pygame.font.Font("font/04B_30__.ttf", 75)
black = (0,0,0)


"""
function for creating the game grid/lines
"""
# def draw_grid():
#     for line in range(0, 50):
#         pygame.draw.line(window, (255, 255, 255), (0, line * tile_size), (WIDTH, line * tile_size))
#         pygame.draw.line(window, (255, 255, 255), (line * tile_size, 0), (line * tile_size, HEIGHT))


"""
Description:    Removes all sprites, resetting their status and the player character,
                and loads a level
Arguments:
    level       numerical value that is needed in order to open the correct level of the map
Returns:
    world       a list variable that will be used in order to display the clean/fresh map
"""
def reset_level(level):
    player.reset(575, 325)
    walk.empty()
    wall.empty()
    GKEY.empty()
    GDOOR.empty()
    YKEY.empty()
    YDOOR.empty()
    RKEY.empty()
    RDOOR.empty()
    BKEY.empty()
    BDOOR.empty()
    _chips.empty()
    firegroup.empty()
    firebootsgroup.empty()
    watergroup.empty()
    waterbootsgroup.empty()
    slidebootsgroup.empty()
    slideupgroup.empty()
    slidedowngroup.empty()
    slideleftgroup.empty()
    sliderightgroup.empty()
    iceplaingroup.empty()
    icegroup_TL.empty()
    icegroup_TR.empty()
    icegroup_LL.empty()
    icegroup_LR.empty()
    icebootsgroup.empty()
    endtilegroup.empty()
    endgategroup.empty()
    thiefgroup.empty()
    monstergroup.empty()

    load_level = []
    if path.exists(f'level{level}_data'):
        file_open = open(f'level{level}_data', 'rb')
        load_level = pickle.load(file_open)
    world = World(load_level)

    return world


class Button:
    """
    Description:    Converts an image into a button that can be pressed
    Arguments:
        x           horizontal placement for the button
        y           vertical placement for the button
    """
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    """
    Description:    Main code that detects when the mouse is over/collides with the image
                    and whether if it was clicked.
    Returns:
        action      returns a boolean data type which signify whether the button is used
    """
    def draw(self):
        action = False

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        window.blit(self.image, self.rect)

        return action


"""
Player characteristics. Code for Player dimensions, movement, and location.
"""
class Player(pygame.sprite.Sprite):
    """
    Description:    starting position of the player
    Arguments:
        x     horizontal location of the player
        y     vertical location of the player
    """
    def __init__(self, x, y):
        self.reset(x, y)

    """
    Description:    When called, resets all the status of the items, and the character location.
    Arguments:
        x     horizontal location of the player
        y     vertical location of the player
    """
    def reset(self, x, y):
        self.player_down = pygame.transform.scale(pygame.image.load('img/movedown.png'), (tile_size, tile_size))
        self.player_left = pygame.transform.scale(pygame.image.load('img/moveleft.png'), (tile_size, tile_size))
        self.player_right = pygame.transform.scale(pygame.image.load('img/moveright.png'), (tile_size, tile_size))
        self.player_up = pygame.transform.scale(pygame.image.load('img/moveup.png.'), (tile_size, tile_size))
        self.image = pygame.transform.scale(self.player_down, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        dead_player = pygame.image.load('img/dead.png')
        self.dead_image = pygame.transform.scale(dead_player, (tile_size, tile_size))
        self.hasgkey = 0
        self.hasykey = 0
        self.hasrkey = 0
        self.hasbkey = 0
        self.chipscollected = 0
        self.fireboots = False
        self.waterboots = False
        self.slideboots = False
        self.iceboots = False
        self.gameover = 0

    """
    Description:    function for collecting the GREEN key and displaying it as an item. 
                    When the player touches/collides with the GREEN key sprite, it disappears
                    from the map and shows in the player's inventory with its corresponding amount.
    Arguments:
        spritegroup it is the sprite that is considered as the "GREEN KEY"
    """

    def gkey_collect(self, spritegroup):
        Green_Key = pygame.image.load('img/greenkey.jpg')
        if pygame.sprite.spritecollide(self, spritegroup, True):
            get_keys.play()
            self.hasgkey += 1

        if self.hasgkey > 0:
            img = pygame.transform.scale(Green_Key, (tile_size*1.5, tile_size*1.5))
            display_keys = font.render(str(self.hasgkey), True, black)
            window.blit(img, (50, 795))
            window.blit(display_keys, (75, 797))

    """
    Description:    function for collecting the YELLOW key and displaying it as an item. 
                    When the player touches/collides with the YELLOW key sprite, it disappears
                    from the map and shows in the player's inventory with its corresponding amount.
    Arguments:
        spritegroup it is the sprite that is considered as the "YELLOW KEY"
    """

    def ykey_collect(self, spritegroup):
        Yellow_key = pygame.image.load('img/yellowkey.jpg')
        if pygame.sprite.spritecollide(self, spritegroup, True):
            get_keys.play()
            self.hasykey += 1

        if self.hasykey > 0:
            img = pygame.transform.scale(Yellow_key, (tile_size*1.5, tile_size*1.5))
            display_keys = font.render(str(self.hasykey), True, black)
            window.blit(img, (100, 795))
            window.blit(display_keys, (125, 797))

    """
    Description:    function for collecting the RED key and displaying it as an item. 
                    When the player touches/collides with the RED key sprite, it disappears
                    from the map and shows in the player's inventory with its corresponding amount.
    Arguments:
        spritegroup it is the sprite that is considered as the "RED KEY"
    """

    def rkey_collect(self, spritegroup):
        Red_Key = pygame.image.load('img/redkey.jpg')
        if pygame.sprite.spritecollide(self, spritegroup, True):
            get_keys.play()
            self.hasrkey += 1

        if self.hasrkey > 0:
            img = pygame.transform.scale(Red_Key, (tile_size*1.5, tile_size*1.5))
            display_keys = font.render(str(self.hasrkey), True, black)
            window.blit(img, (150, 795))
            window.blit(display_keys, (175, 797))

    """
    Description:    function for collecting the BLUE key and displaying it as an item. 
                    When the player touches/collides with the BLUE key sprite, it disappears
                    from the map and shows in the player's inventory with its corresponding amount.
    Arguments:
        spritegroup it is the sprite that is considered as the "BLUE KEY"
    """

    def bkey_collect(self, spritegroup):
        Blue_Key = pygame.image.load('img/bluekey.jpg')
        if pygame.sprite.spritecollide(self, spritegroup, True):
            get_keys.play()
            self.hasbkey += 1

        if self.hasbkey > 0:
            img = pygame.transform.scale(Blue_Key, (tile_size*1.5, tile_size*1.5))
            display_keys = font.render(str(self.hasbkey), True, black)
            window.blit(img, (200, 795))
            window.blit(display_keys, (225, 797))

    """
    Description:    function for collecting the chips. It displays the  amount of chips the player has 
                    and the total amount of chips needed.
    Arguments:
        spritegroup it is the sprite that is considered as the "Computer Chips"
    """

    def chips_collect(self, spritegroup):
        chips_text = ("Chips Collected:")
        chips_ingame = ("Chips in the Board:")
        text = font2.render(chips_text, True, black)
        text2 = font2.render(chips_ingame, True, black)
        window.blit(text, (510, 775))
        window.blit(text2, (510, 800))
        display_chipscollect = font2.render(str(self.chipscollected), True, black)
        display_chipgoal = font2.render(str(number_of_chips), True, black)

        if pygame.sprite.spritecollide(self, spritegroup, True):
            self.chipscollected += 1
            get_chips.play()

        if self.chipscollected > 0:
            window.blit(display_chipscollect, (900, 775))

        window.blit(display_chipgoal, (900, 800))

    """
    Description:    function for collecting the FIRE RESISTANCE BOOTS and displaying it as an item. 
                    When the player touches/collides with the FIRE RESISTANCE BOOTS sprite, it 
                    disappears from the map and shows in the player's inventory.
                    Can only keep one boot at a time.
    Arguments:
        spritegroup it is the sprite that is considered as the "FIRE RESISTANCE BOOTS"
    """

    def Fboots_collect(self, spritegroup):
        Fire_Boots = pygame.image.load('img/fireboots.jpg')
        if pygame.sprite.spritecollide(self, spritegroup, True):
            pickup_fx.play()
            self.fireboots = True
            self.waterboots = False
            self.slideboots = False
            self.iceboots = False

        if self.fireboots:
            img = pygame.transform.scale(Fire_Boots, (tile_size*1.5, tile_size*1.5))
            window.blit(img, (250, 795))

    """
    Description:    function for collecting the SWIMMING FINS and displaying it as an item. 
                    When the player touches/collides with the SWIMMING FINS sprite, it 
                    disappears from the map and shows in the player's inventory. 
                    Can only keep one boot at a time.
    Arguments:
        spritegroup it is the sprite that is considered as the "SWIMMING FINS"
    """

    def Wboots_collect(self, spritegroup):
        Water_boots = pygame.image.load('img/waterboots.jpg')
        if pygame.sprite.spritecollide(self, spritegroup, True):
            pickup_fx.play()
            self.waterboots = True
            self.fireboots = False
            self.slideboots = False
            self.iceboots = False

        if self.waterboots:
            img = pygame.transform.scale(Water_boots, (tile_size*1.5, tile_size*1.5))
            window.blit(img, (300, 795))

    """
    Description:    function for collecting the ANTI-SLIDDING BOOTS and displaying it as an item. 
                    When the player touches/collides with the ANTI-SLIDDING BOOTS sprite, it 
                    disappears from the map and shows in the player's inventory. 
                    Can only keep one boot at a time.
    Arguments:
        spritegroup it is the sprite that is considered as the "ANTI-SLIDDING BOOTS"
    """

    def Sboots_collect(self, spritegroup):
        slide_boots = pygame.image.load('img/slideboots.jpg')
        if pygame.sprite.spritecollide(self, spritegroup, True):
            pickup_fx.play()
            self.slideboots = True
            self.fireboots = False
            self.waterboots = False
            self.iceboots = False

        if self.slideboots:
            img = pygame.transform.scale(slide_boots, (tile_size*1.5, tile_size*1.5))
            window.blit(img, (350, 795))

    """
    Description:    function for collecting the FIGURE SKATES and displaying it as an item. 
                    When the player touches/collides with the FIGURE SKATES sprite, it 
                    disappears from the map and shows in the player's inventory. 
                    Can only keep one boot at a time.
    Arguments:
        spritegroup it is the sprite that is considered as the "FIGURE SKATES"
    """

    def Iboots_collect(self, spritegroup):
        ice_boots = pygame.image.load('img/iceboots.jpg')
        if pygame.sprite.spritecollide(self, spritegroup, True):
            pickup_fx.play()
            self.iceboots = True
            self.waterboots = False
            self.slideboots = False
            self.fireboots = False

        if self.iceboots:
            img = pygame.transform.scale(ice_boots, (tile_size*1.5, tile_size*1.5))
            window.blit(img, (400, 795))

    """
    Description:        function for moving the character with keyboard keys and effects of
                        different tiles to the player movement.
    Arguments:
        gameover        an int variable that is used to verify whether the character can be move.
    Returns:
        gameover        an int variable that corresponds to a specific game event

    """

    def update(self, gameover):

        dx = 0
        dy = 0
        walk_cooldown = 0
        delta = clock.tick(10)
        walk_cooldown -= delta

        if gameover == 0:
            if walk_cooldown <= 0:
                key = pygame.key.get_pressed()
                if key[pygame.K_LEFT] or key[pygame.K_a]:
                    player.image = player.player_left
                    dx -= 25
                if key[pygame.K_RIGHT] or key[pygame.K_d]:
                    player.image = player.player_right
                    dx += 25
                if key[pygame.K_UP] or key[pygame.K_w]:
                    player.image = player.player_up
                    dy -= 25
                if key[pygame.K_DOWN] or key[pygame.K_s]:
                    player.image = player.player_down
                    dy += 25

            self.rect.x += dx
            self.rect.y += dy

            if pygame.sprite.spritecollide(self, wall, False):
                self.rect.x -= dx
                self.rect.y -= dy

            if pygame.sprite.spritecollide(self, GDOOR, False):
                if self.hasgkey == 0:
                    self.rect.x -= dx
                    self.rect.y -= dy
                if self.hasgkey > 0:
                    door_open.play()
                    walktile = Walk_tiles(self.rect.x, self.rect.y)
                    walk.add(walktile)
                    pygame.sprite.spritecollide(self, GDOOR, True)
                    self.hasgkey -= 1

            if pygame.sprite.spritecollide(self, YDOOR, False):
                if self.hasykey == 0:
                    self.rect.x -= dx
                    self.rect.y -= dy
                if self.hasykey > 0:
                    door_open.play()
                    walktile = Walk_tiles(self.rect.x, self.rect.y)
                    walk.add(walktile)
                    pygame.sprite.spritecollide(self, YDOOR, True)
                    self.hasykey -= 1

            if pygame.sprite.spritecollide(self, RDOOR, False):
                if self.hasrkey == 0:
                    self.rect.x -= dx
                    self.rect.y -= dy
                if self.hasrkey > 0:
                    door_open.play()
                    walktile = Walk_tiles(self.rect.x, self.rect.y)
                    walk.add(walktile)
                    pygame.sprite.spritecollide(self, RDOOR, True)
                    self.hasrkey -= 1

            if pygame.sprite.spritecollide(self, BDOOR, False):
                if self.hasbkey == 0:
                    self.rect.x -= dx
                    self.rect.y -= dy
                if self.hasbkey > 0:
                    door_open.play()
                    walktile = Walk_tiles(self.rect.x, self.rect.y)
                    walk.add(walktile)
                    pygame.sprite.spritecollide(self, BDOOR, True)
                    self.hasbkey -= 1

            if pygame.sprite.spritecollide(self, firegroup, False):
                if not self.fireboots:
                    gm_fx.play()
                    gameover = -1

            if pygame.sprite.spritecollide(self, watergroup, False):
                if not self.waterboots:
                    gm_fx.play()
                    gameover = -1

            if pygame.sprite.spritecollide(self, slideupgroup, False):
                if not self.slideboots:
                    self.rect.y -= 25

            if pygame.sprite.spritecollide(self, slidedowngroup, False):
                if not self.slideboots:
                    self.rect.y += 25

            if pygame.sprite.spritecollide(self, slideleftgroup, False):
                if not self.slideboots:
                    self.rect.x -= 25

            if pygame.sprite.spritecollide(self, sliderightgroup, False):
                if not self.slideboots:
                    self.rect.x += 25

            if pygame.sprite.spritecollide(self, iceplaingroup, False):
                if not self.iceboots:
                    while pygame.sprite.spritecollide(self, iceplaingroup, False):
                        if dx < 0: #Left
                            self.rect.x -= 25
                        if dx > 0: #Right
                            self.rect.x += 25
                        if dy < 0: #Up
                            self.rect.y -= 25
                        if dy > 0: #Down
                            self.rect.y += 25

            if pygame.sprite.spritecollide(self, icegroup_LR, False):
                if not self.iceboots:
                    if dy > 0:
                        self.rect.x -= 25
                    if dx > 0:
                        self.rect.y -= 25

            if pygame.sprite.spritecollide(self, icegroup_LL, False):
                if not self.iceboots:
                    if dy > 0:
                        self.rect.x += 25
                    if dx < 0:
                        self.rect.y -= 25

            if pygame.sprite.spritecollide(self, icegroup_TR, False):
                if not self.iceboots:
                    if dy < 0:
                        self.rect.x -= 25
                    if dx > 0:
                        self.rect.y += 25

            if pygame.sprite.spritecollide(self, icegroup_TL, False):
                if not self.iceboots:
                    if dy < 0:
                        self.rect.x += 25
                    if dx < 0:
                        self.rect.y += 25


            if pygame.sprite.spritecollide(self, thiefgroup, False):
                self.hasgkey = 0
                self.hasykey = 0
                self.hasrkey = 0
                self.hasbkey = 0
                self.chipscollected = 0
                self.fireboots = False
                self.waterboots = False
                self.slideboots = False
                self.iceboots = False
                gm_fx.play()
                gameover = -1

            if pygame.sprite.spritecollide(self, monstergroup, False):
                gm_fx.play()
                gameover = -1

            if pygame.sprite.spritecollide(self, teleportgroup, False):
                teleport_fx.play()
                new_positionx = tprx
                new_positiony = tpry
                self.rect.x = new_positionx
                self.rect.y = new_positiony + 25

            if pygame.sprite.spritecollide(self, teleportreceivergroup, False):
                teleport_fx.play()
                new_positionx = tpx
                new_positiony = tpy
                self.rect.x = new_positionx
                self.rect.y = new_positiony + 25


            if pygame.sprite.spritecollide(self, endgategroup, False):
                if number_of_chips != self.chipscollected:
                    self.rect.x -= dx
                    self.rect.y -= dy

            walktile = Walk_tiles(self.rect.x, self.rect.y)
            walk.add(walktile)


            if pygame.sprite.spritecollide(self, endtilegroup, False):
                if number_of_chips == self.chipscollected:
                    nextlvl_fx.play()
                    gameover = 1


        if gameover == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        window.blit(self.image, self.rect)

        return gameover

"""
Description:        World generation. It displays the map with the different game elements.
"""
class World:
    """
    Description:        World generation. It displays the map with the different game tiles.
                        A specific number corresponds to a specific tile.
    Arguments:
        data            list that will be used to replace the "numbers" into "picture" or tiles.
    """
    def __init__(self, data):
        self.tile_list = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1: #Plain Tiles
                    walktile = Walk_tiles(col_count * tile_size, row_count * tile_size)
                    walk.add(walktile)
                elif tile == 2: #Pure Walls
                    walltile = Wall_tiles(col_count * tile_size, row_count * tile_size)
                    wall.add(walltile)
                elif tile == 3:
                    greendoor = GreenDoor(col_count * tile_size, row_count * tile_size)
                    GDOOR.add(greendoor)
                elif tile == 4:
                    yellowdoor = YellowDoor(col_count * tile_size, row_count * tile_size)
                    YDOOR.add(yellowdoor)
                elif tile == 5:
                    greenkey = GreenKey(col_count * tile_size, row_count * tile_size)
                    GKEY.add(greenkey)
                elif tile == 6:
                    yellowkey = YellowKey(col_count * tile_size, row_count * tile_size)
                    YKEY.add(yellowkey)
                elif tile == 7:
                    comchip = Chips(col_count * tile_size, row_count * tile_size)
                    _chips.add(comchip)
                elif tile == 8:
                    egate = EndGate(col_count * tile_size, row_count * tile_size)
                    endgategroup.add(egate)
                elif tile == 9:
                    end = EndTile(col_count * tile_size, row_count * tile_size)
                    endtilegroup.add(end)
                elif tile == 10:
                    firetiles = Fire_tiles(col_count * tile_size, row_count * tile_size)
                    firegroup.add(firetiles)
                elif tile == 11:
                    fireboots = FireBoots(col_count * tile_size, row_count * tile_size)
                    firebootsgroup.add(fireboots)
                elif tile == 12:
                    water = Water_tiles(col_count * tile_size, row_count * tile_size)
                    watergroup.add(water)
                elif tile == 13:
                    waterboots = Water_Boots(col_count * tile_size, row_count * tile_size)
                    waterbootsgroup.add(waterboots)
                elif tile == 14:
                    thief = ThiefTiles(col_count * tile_size, row_count * tile_size)
                    thiefgroup.add(thief)
                elif tile == 15:
                    sright = SlideRight(col_count * tile_size, row_count * tile_size)
                    sliderightgroup.add(sright)
                elif tile == 16:
                    sleft = SlideLeft(col_count * tile_size, row_count * tile_size)
                    slideleftgroup.add(sleft)
                elif tile == 17:
                    sdown = SlideDown(col_count * tile_size, row_count * tile_size)
                    slidedowngroup.add(sdown)
                elif tile == 18:
                    sup = SlideUp(col_count * tile_size, row_count * tile_size)
                    slideupgroup.add(sup)
                elif tile == 19:
                    sboots = SlideBoots(col_count * tile_size, row_count * tile_size)
                    slidebootsgroup.add(sboots)
                elif tile == 20:
                    icep = IcePlain(col_count * tile_size, row_count * tile_size)
                    iceplaingroup.add(icep)
                elif tile == 21:
                    icell = IceLL(col_count * tile_size, row_count * tile_size)
                    icegroup_LL.add(icell)
                elif tile == 22:
                    icelr = IceLR(col_count * tile_size, row_count * tile_size)
                    icegroup_LR.add(icelr)
                elif tile == 23:
                    icetl = IceTL(col_count * tile_size, row_count * tile_size)
                    icegroup_TL.add(icetl)
                elif tile == 24:
                    icetr = IceTR(col_count * tile_size, row_count * tile_size)
                    icegroup_TR.add(icetr)
                elif tile == 25:
                    iceboots = IceBoots(col_count * tile_size, row_count * tile_size)
                    icebootsgroup.add(iceboots)
                elif tile == 26:
                    reddoor = RedDoor(col_count * tile_size, row_count * tile_size)
                    RDOOR.add(reddoor)
                elif tile == 27:
                    redkey = RedKey(col_count * tile_size, row_count * tile_size)
                    RKEY.add(redkey)
                elif tile == 28:
                    bluedoor = BlueDoor(col_count * tile_size, row_count * tile_size)
                    BDOOR.add(bluedoor)
                elif tile == 29:
                    bluekey = BlueKey(col_count * tile_size, row_count * tile_size)
                    BKEY.add(bluekey)
                elif tile == 30:
                    icep = IcePlain(col_count * tile_size, row_count * tile_size)
                    iceplaingroup.add(icep)
                elif tile == 31:
                    walktile = Walk_tiles(col_count * tile_size, row_count * tile_size)
                    walk.add(walktile)
                    monsterg = monster(col_count * tile_size, row_count * tile_size)
                    monstergroup.add(monsterg)
                elif tile == 32:
                    locx = col_count * tile_size
                    locy = row_count * tile_size
                    tpv = teleport(locx, locy)
                    teleportgroup.add(tpv)
                    global tpx
                    tpx = locx
                    global tpy
                    tpy = locy
                elif tile == 33:
                    locx = col_count * tile_size
                    locy = row_count * tile_size
                    tprv = teleport_receiver(locx, locy)
                    teleportreceivergroup.add(tprv)
                    global tprx
                    tprx = locx
                    global tpry
                    tpry = locy

                col_count += 1
            row_count += 1

    """
    Description:        Displays the tile from the previous tile iteration.
    """
    def draw(self):
        for tile in self.tile_list:
            window.blit(self, tile)

"""
Description:        Import an image that will be used as the Walkable tiles. Game element that the 
                    character can easily pass (doesn't need any special requirement)
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class Walk_tiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/walktile.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the Wall tiles. 
                    Game element that the character cannot pass through.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class Wall_tiles(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/wall.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the green key, a game element 
                    that the character can collect.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class GreenKey(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/greenkey.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the green door, a game element that the 
                    character can unlock if the right key is collected.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class GreenDoor(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/greendoor.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the yellow key game element 
                    that the character can collect.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""



class YellowKey(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/yellowkey.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the yellow door game element that 
                    the character can unlock if the right key is collected.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class YellowDoor(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/yellowdoor.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the red key game element that the 
                    character can collect.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class RedKey(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/redkey.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the red door, a game element that the 
                    character can unlock if the right key is collected.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class RedDoor(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/reddoor.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the blue key, a game element 
                    that the character can collect.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class BlueKey(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/bluekey.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the blue door game element that the
                    character can unlock if the right key is collected.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class BlueDoor(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/bluedoor.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the computer chips 
                    game element that the character can collect and win the game.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class Chips(pygame.sprite.Sprite):
    """
    Takes the position as arguments (x = horizontal, y = vertical)
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/chip.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the fire tile that the character can 
                    cross if the correct shoes is in the inventory.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class Fire_tiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/fire.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the fire boots that the character 
                    can collect and be immune to fire tiles.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class FireBoots(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/fireboots.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the water tile that the character 
                    can cross if the correct shoes is in the inventory.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class Water_tiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/water.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the water boots that the character 
                    can collect and be able to cross water tiles.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class Water_Boots(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/waterboots.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the tile responsible for moving the 
                    player 1 tile above if the correct shoes is not in the inventory.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class SlideUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/slideup.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the tile responsible for moving the 
                    player 1 tile below if the correct shoes is not in the inventory.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class SlideDown(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/slidedown.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the tile responsible for moving the player
                    1 tile to the right if the correct shoes is not in the inventory.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class SlideRight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/slideright.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the tile responsible for moving the player 
                    1 tile to the left if the correct shoes is not in the inventory.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class SlideLeft(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/slideleft.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the anti-slide boots that can be 
                    collected and be immune to the slide tile effects.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class SlideBoots(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/slideboots.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the plain ice that lets you 
                    slide no matter what the direction you are coming from.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class IcePlain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/ice.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the corner ice tile that lets you slide from a specific direction.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class IceTL(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/iceTL.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the corner ice tile that lets you slide from a specific direction.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class IceTR(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/iceTR.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the corner ice tile that lets you slide from a specific direction.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class IceLL(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/iceLL.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the corner ice tile that lets you slide from a specific direction.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class IceLR(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/iceLR.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the ice boots, can be collected 
                    and makes the player immune to the effects of the ice tiles.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class IceBoots(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/iceboots.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the thief tile which removes all the 
                    player's item in their inventory and causes the game to end if touched.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class ThiefTiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/thief.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the end gate tile which acts as a wall 
                    until you have the right amount of key to pass through.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""


class EndGate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/endgate.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the end tile which lets the player move 
                    unto the next level if the correct amount of chips are collected.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""



class EndTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/endtile.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the teleport tile which transport the player 
                    to the other teleport tile.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""



class teleport(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/tp.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the teleport receiver tile which also 
                    transport the player to the other teleport tile.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""



class teleport_receiver(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/tprec.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""
Description:        Import an image that will be used as the monster tile that moves and 
                    if it touches the player, the player loses. It also has function which makes itself
                    move a specific set of tiles.
Arguments:
    x               Horizontal location of the tile
    y               Vertical location of the tile
"""



class monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/monster.jpg')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 25

    def update(self):
        wc = 0
        wc -= 10
        if wc <= 0:
            self.rect.x += self.move_direction
            self.move_counter += 1
            wc += 10
            if abs(self.move_counter) >= 2:
                self.move_direction *= -1
                self.move_counter *= -1

"""
Description:        It functions as a reader of a specified file
Returns:
    f.read()        method that is used to read the specified file
"""


def gethighscore():
    with open("High Score.txt", "r") as f:
        return f.read()


"""
Description:        Displays a text in the window.
Arguments:
    text            a string data type which contains the text that will be displayed
    font            a variable containing the assigned font with its size
    x               horizontal location of the text
    y               vertical location of the text
"""


def display_text(text, font, x, y):
    img = font.render(text, True, black)
    window.blit(img, (x, y))

"""
Description:        block of code that adds all the sprite into a sprite group.
"""
player = Player(575, 325)
walk = pygame.sprite.Group()
wall = pygame.sprite.Group()
GKEY = pygame.sprite.Group()
GDOOR = pygame.sprite.Group()
YKEY = pygame.sprite.Group()
YDOOR = pygame.sprite.Group()
RKEY = pygame.sprite.Group()
RDOOR = pygame.sprite.Group()
BKEY = pygame.sprite.Group()
BDOOR = pygame.sprite.Group()
_chips = pygame.sprite.Group()
firegroup = pygame.sprite.Group()
firebootsgroup = pygame.sprite.Group()
watergroup = pygame.sprite.Group()
waterbootsgroup = pygame.sprite.Group()
slidebootsgroup = pygame.sprite.Group()
slideupgroup = pygame.sprite.Group()
slidedowngroup = pygame.sprite.Group()
slideleftgroup = pygame.sprite.Group()
sliderightgroup = pygame.sprite.Group()
iceplaingroup = pygame.sprite.Group()
icegroup_TL = pygame.sprite.Group()
icegroup_TR = pygame.sprite.Group()
icegroup_LL = pygame.sprite.Group()
icegroup_LR = pygame.sprite.Group()
icebootsgroup = pygame.sprite.Group()
endtilegroup =  pygame.sprite.Group()
endgategroup =  pygame.sprite.Group()
thiefgroup =  pygame.sprite.Group()
monstergroup = pygame.sprite.Group()
teleportgroup = pygame.sprite.Group()
teleportreceivergroup = pygame.sprite.Group()

#loading highscore
highest_score = int(gethighscore())

#load level
load_level = []
if path.exists(f'level{level}_data'):
    file_open = open(f'level{level}_data', 'rb')
    load_level = pickle.load(file_open)
world = World(load_level)

#buttons
reset_button = Button(500, 350, restart)
start_button = Button(325, 500, start)
quit_button = Button(675, 500, quit_game)
score_board = Button(1130, 150, trophy)
info = Button(1145, 510, infog)
info2 = Button(1155, 450, infog2)
back = Button(550, 550, back)
back_1 = Button(850, 625, back2)
nextB = Button(700, 500, next)
menu_button = Button(1183, 765, menu)


"""
Description:        Main game loop
"""

run = True
while run:

    clock.tick(fps)

    window.blit(bg_tech, (0, 0))
    window.blit(black_Layer3, (95, 45))
    window.blit(layer1scaled, (100, 50))

    if main_menu == True:
        window.blit(layer_1scaled, (100, 50))
        window.blit(title, (225, 200))
        window.blit(bg, (1120, 95))
        window.blit(bg, (1120, 440))
        if score_board.draw():
            high_score = True
        if info.draw():
            guide_panel = True
        if start_button.draw():
            main_menu = False
        if quit_button.draw():
            run = False

        if high_score:
            window.blit(board, (150, 100))
            highest_score = int(gethighscore())
            display_text(str(highest_score), font3, 500, 400)
            if back.draw():
                high_score = False

        if guide_panel:
            window.blit(guide, (150, 150))
            if back_1.draw():
                guide_panel = False

    else:
        world.draw()
        window.blit(black_Layer, (35, 760))
        window.blit(layer2scaled, (40, 765))
        window.blit(black_Layer2, (490, 760))
        window.blit(layer3scaled, (495, 765))
        display_text("Items:", font2, 45, 765)
        window.blit(black_Layer4, (985, 760))
        window.blit(layer4scaled, (990, 765))
        display_text("Timer:", font2, 1025, 770)
        window.blit(black_Layer5, (1125, 100))
        window.blit(layer5scaled, (1130, 105))
        window.blit(black_Layer5, (1125, 400))
        window.blit(layer5scaled, (1130, 405))

        walk.draw(window)
        wall.draw(window)

        GKEY.draw(window)
        GDOOR.draw(window)
        player.gkey_collect(GKEY)

        YKEY.draw(window)
        YDOOR.draw(window)
        player.ykey_collect(YKEY)

        RKEY.draw(window)
        RDOOR.draw(window)
        player.rkey_collect(RKEY)

        BKEY.draw(window)
        BDOOR.draw(window)
        player.bkey_collect(BKEY)

        _chips.draw(window)
        player.chips_collect(_chips)

        firegroup.draw(window)
        firebootsgroup.draw(window)
        player.Fboots_collect(firebootsgroup)

        watergroup.draw(window)
        waterbootsgroup.draw(window)
        player.Wboots_collect(waterbootsgroup)

        slidebootsgroup.draw(window)
        slideupgroup.draw(window)
        slidedowngroup.draw(window)
        slideleftgroup.draw(window)
        sliderightgroup.draw(window)
        player.Sboots_collect(slidebootsgroup)

        iceplaingroup.draw(window)
        icebootsgroup.draw(window)
        icegroup_TL.draw(window)
        icegroup_TR.draw(window)
        icegroup_LL.draw(window)
        icegroup_LR.draw(window)
        player.Iboots_collect(icebootsgroup)

        endgategroup.draw(window)
        endtilegroup.draw(window)

        monstergroup.draw(window)
        monstergroup.update()

        teleportgroup.draw(window)
        teleportreceivergroup.draw(window)

        thiefgroup.draw(window)

        gameover = player.update(gameover)

        if info2.draw():
            guide_panel = True

        if guide_panel:
            window.blit(guide, (150, 100))
            if back_1.draw():
                guide_panel = False

        if menu_button.draw():
            main_menu = True
            load_level = []
            world = reset_level(level)
            gameover = 0
            time = 100
            score = 1000

        if time > 0 and gameover == 0:
            display_text(str(time), font2, 1058, 800)
            count_timer = pygame.time.get_ticks()
            # print(count_timer)
            if count_timer - last_count > 1000:
                time -= 1
                last_count = count_timer
                score -= random.randrange(1, 5)
                if time <= 0:
                    gm_fx.play()
                    gameover = -1

        display_text("Score:", font2, 1150, 125)
        display_text(str(score), font2, 1170, 165)
        display_text("High", font2, 1160, 200)
        display_text("Score:", font2, 1150, 225)
        display_text(str(highest_score), font2, 1170, 260)

        if gameover == -1:
            if reset_button.draw():
                load_level = []
                world = reset_level(level)
                gameover = 0
                time = 100
                score = 1000

        if gameover == 1:
            level += 1
            time = 100
            last_score = score
            score = 1000
            if highest_score < last_score:
                highest_score = last_score
            with open("High Score.txt", "w") as f:
                f.write(str(highest_score))

            if level <= number_of_levels:
                load_level = []
                world = reset_level(level)
                gameover = 0
            else:
                if reset_button.draw():
                    level = 1
                    load_level = []
                    world = reset_level(level)
                    gameover = 0

        # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()