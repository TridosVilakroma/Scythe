import pygame,sys
import pickle
from os import path
from random import randint


pygame.init()

clock = pygame.time.Clock()
fps = 60
#define game variables
white=(255,255,255)
#game window

tile_size = 10
cols = 100
screen_width = tile_size * cols
screen_height = screen_width//2
cells = (tile_size * cols)//2

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Level Editor')

#load images

#player
scyman=pygame.image.load(r'media\scyman_walk\down_walk\walkdown0.png')
#enemies
scarecrow = pygame.image.load(r'media\deco\scarecrow.png')
omnivine = pygame.image.load(r'media\enemies\ominvine.png')
nid = pygame.image.load(r'media\enemies\nid\idle\nid_idle1.png')
#Bosses
scareboss=pygame.image.load(r'media\boss\scareboss\scareboss.png')
#tiles
dirt_img1 = pygame.image.load(r'media\tile\tiles\dirt1.png')
dirt_img2 = pygame.image.load(r'media\tile\tiles\dirt2.png')
grass_img1 = pygame.image.load(r'media\tile\tiles\grass1.png')
grass_img2 = pygame.image.load(r'media\tile\tiles\grass2.png')
sand_img1 = pygame.image.load(r'media\tile\tiles\sand1.png')
sand_img2 = pygame.image.load(r'media\tile\tiles\sand2.png')
snow_img1 = pygame.image.load(r'media\tile\tiles\snow1.png')
snow_img2 = pygame.image.load(r'media\tile\tiles\snow2.png')
ice_img1 = pygame.image.load(r'media\tile\tiles\ice1.png')
ice_img2 = pygame.image.load(r'media\tile\tiles\ice2.png')
stone_img1 = pygame.image.load(r'media\tile\tiles\stone1.png')
stone_img2 = pygame.image.load(r'media\tile\tiles\stone2.png')

#roads
horzroad = pygame.image.load(r'media\tile\tiles\horzroad.png')
vertroad = pygame.image.load(r'media\tile\tiles\vertroad.png')
topleftcorner = pygame.image.load(r'media\tile\tiles\tlcorner.png')
toprightcorner = pygame.image.load(r'media\tile\tiles\trcornerroad.png')
bottomleftcorner = pygame.image.load(r'media\tile\tiles\blcornerroad.png')
bottomrightcorner = pygame.image.load(r'media\tile\tiles\brcornerroad.png')
teeup = pygame.image.load(r'media\tile\tiles\teeuproad.png')
teeright = pygame.image.load(r'media\tile\tiles\righttee.png')
teedown = pygame.image.load(r'media\tile\tiles\teedownroad.png')
teeleft = pygame.image.load(r'media\tile\tiles\leftteeroad.png')
crossroad = pygame.image.load(r'media\tile\tiles\crossroad.png')
topend = pygame.image.load(r'media\tile\tiles\topendroad.png')
rightend = pygame.image.load(r'media\tile\tiles\rightendroad.png')
leftend = pygame.image.load(r'media\tile\tiles\leftendroad.png')

#structure
block = pygame.image.load(r'level_editor\level_editor\mappack\PNG\mapTile_114.png')

#edges
top_left=pygame.image.load(r'media\tile\edge\topleft.png')
top=pygame.image.load(r'media\tile\edge\top.png')
top_right=pygame.image.load(r'media\tile\edge\topright.png')
left=pygame.image.load(r'media\tile\edge\left.png')
right=pygame.image.load(r'media\tile\edge\right.png')
bot_left=pygame.image.load(r'media\tile\edge\botleft.png')
bot=pygame.image.load(r'media\tile\edge\bot.png')
bot_right=pygame.image.load(r'media\tile\edge\botright.png')

#create empty tile list
world_data = []
for row in range(screen_height*3):
    r = [0] * screen_width*3
    world_data.append(r)

game_data = []
for row in range(screen_height*3):
    r = [0] * screen_width*3
    game_data.append(r)

#blank template [y][x]
def blank_template():
    for row in range(50):
        for column in range(100):
            world_data[row][column] = 2
    world_data[0][0] = 100
    world_data[0][99] = 102
    world_data[49][0] = 105
    world_data[49][99] = 107
    for tile in range(1,99):
        #top
        world_data[0][tile] = 101
        #bottom
        world_data[49][tile] = 106
    for tile in range(1,49):
        #left
        world_data[tile][0] = 103
        #right
        world_data[tile][99] = 104

blank_template()
def draw_grid():
    for c in range(cells):
        #vertical lines
        pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height))
        #horizontal lines
        pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))

class world_edit():
    def __init__(self):
        self.self=self
        self.unique_tiles=9
        self.tileset_first=0
        self.tileset_last=6
        self.level=1
        self.clicked=False
        self.data_set=world_data

    def draw_world(self):
        for row in range(cells):
            for col in range(cells):
                if world_data[row][col] > 0:
                #####tiles
                    if world_data[row][col] == 1:
                        #dirt blocks
                        img = pygame.transform.scale(dirt_img1, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 2:
                        #grass blocks
                        img = pygame.transform.scale(grass_img1, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 3:
                        #sand blocks
                        img = pygame.transform.scale(sand_img1, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 4:
                        #snow blocks
                        img = pygame.transform.scale(snow_img1, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 5:
                        #ice blocks
                        img = pygame.transform.scale(ice_img1, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 6:
                        #stone blocks
                        img = pygame.transform.scale(stone_img1, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                #####roads
                    if world_data[row][col] == 7:
                        #horizontal road
                        img = pygame.transform.scale(horzroad, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 8:
                        #vertical road
                        img = pygame.transform.scale(vertroad, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 9:
                        #top left corner road
                        img = pygame.transform.scale(topleftcorner, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 10:
                        #top right corner road
                        img = pygame.transform.scale(toprightcorner, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 11:
                        #bottom right corner road
                        img = pygame.transform.scale(bottomrightcorner, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 12:
                        #bottom left corner road
                        img = pygame.transform.scale(bottomleftcorner, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 13:
                        #top tee road
                        img = pygame.transform.scale(teeup, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 14:
                        #right tee road
                        img = pygame.transform.scale(teedown, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 15:
                        #bottom tee road
                        img = pygame.transform.scale(teeright, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 16:
                        #left tee road
                        img = pygame.transform.scale(teeleft, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 17:
                        #top dead end road
                        img = pygame.transform.scale(topend, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 18:
                        #right dead end road
                        img = pygame.transform.scale(rightend, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 19:
                        #left dead end road
                        img = pygame.transform.scale(leftend, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    #structure
                    if game_data[row][col] == 300:
                        # img = pygame.transform.scale(grass_img1, (tile_size, tile_size))
                        # screen.blit(img, (col * tile_size, row * tile_size))
                        img = pygame.transform.scale(block, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                        #game_data[row][col]=300

                #####edges
                    if world_data[row][col] == 100:
                        #top left edge
                        img = pygame.transform.scale(top_left, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 101:
                        #top edge
                        img = pygame.transform.scale(top, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 102:
                        #top right edge
                        img = pygame.transform.scale(top_right, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 103:
                        #left edge
                        img = pygame.transform.scale(left, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 104:
                        #right edge
                        img = pygame.transform.scale(right, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 105:
                        #bottom left edge
                        img = pygame.transform.scale(bot_left, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 106:
                        #bottom edge
                        img = pygame.transform.scale(bot, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if world_data[row][col] == 107:
                        #bottom right edge
                        img = pygame.transform.scale(bot_right, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))

                #####enemies
                    if game_data[row][col] == 200:
                        #scarecrow 
                        img = pygame.transform.scale(scarecrow, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if game_data[row][col] == 201:
                        #omnivine
                        img = pygame.transform.scale(omnivine, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                    if game_data[row][col] == 202:
                        #nid
                        img = pygame.transform.scale(nid, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))
                #####bosses
                    if game_data[row][col] == 800:
                        #scareboss
                        img = pygame.transform.scale(scareboss, (tile_size*3, tile_size*3))
                        screen.blit(img, ((col-2) * tile_size, (row-2) * tile_size))
                #####player
                    if game_data[row][col] == 1000:
                        #scyman
                        img = pygame.transform.scale(scyman, (tile_size, tile_size))
                        screen.blit(img, (col * tile_size, row * tile_size))

    def event_handler(self):
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouseclicks to change tiles
            if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                self.clicked = True
                pos = pygame.mouse.get_pos()
                x = pos[0] // tile_size
                y = pos[1] // tile_size
                #check that the coordinates are within the tile area
                if x < screen_width and y < screen_height:
                    #update tile value
                    if pygame.mouse.get_pressed()[0] == 1:
                        if self.data_set[y][x] > self.tileset_last or self.data_set[y][x] < self.tileset_first:
                            self.data_set[y][x] = self.tileset_first
                        else:
                            self.data_set[y][x] += 1
                        if self.data_set[y][x] > self.tileset_last:
                            self.data_set[y][x] = self.tileset_first
                    elif pygame.mouse.get_pressed()[2] == 1:
                        if self.data_set[y][x] > self.tileset_last or self.data_set[y][x] < self.tileset_first:
                            self.data_set[y][x] = self.tileset_first
                        else:
                            self.data_set[y][x] -= 1
                        if self.data_set[y][x] < self.tileset_first:
                            self.data_set[y][x] = self.tileset_last
            if event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
            #up and down key presses to change level number
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.level += 1
                    self.console_output()
                elif event.key == pygame.K_DOWN and self.level > 1:
                    self.level -= 1
                    self.console_output()
                if event.key == pygame.K_RETURN:
                    self.save_level()
                    print(f'Saved Level: {self.level}')
                if event.key == pygame.K_SPACE:
                    self.load_level()
                    print(f'Loaded Level: {self.level}')
            #change tile set
                if event.key == pygame.K_1:
                    #standard tiles
                    self.data_set=world_data
                    self.tileset_first=1
                    self.tileset_last=6
                    print('Standard tiles selected')
                if event.key == pygame.K_2:
                    #road tiles
                    self.data_set=world_data
                    self.tileset_first=7
                    self.tileset_last=19
                    print('Road tiles selected')
                if event.key == pygame.K_3:
                    #structures
                    self.data_set=game_data
                    self.tileset_first=300
                    self.tileset_last=301
                    print('Structures selected')
                if event.key == pygame.K_8:
                    #player placement
                    self.data_set=game_data
                    self.tileset_first=1000
                    self.tileset_last=1001
                    print('Player position')
                if event.key == pygame.K_9:
                    #enemy placement
                    self.data_set=game_data
                    self.tileset_first=200
                    self.tileset_last=203
                    print('Enemies selected')
                if event.key == pygame.K_0:
                    #boss placement
                    self.data_set=game_data
                    self.tileset_first=800
                    self.tileset_last=801
                    print('Bosses selected')

    def save_level(self):
        pickle_out = open(f'levels\level{self.level}_data', 'wb')
        pickle.dump((world_data,game_data), pickle_out)
        pickle_out.close()

    def load_level(self):
        global world_data,game_data
        if path.exists(f'levels\level{self.level}_data'):
            pickle_in = open(f'levels\level{self.level}_data', 'rb')
            coupled_data = pickle.load(pickle_in)
            world_data,game_data = coupled_data[0],coupled_data[1]
            pickle_in.close()
    #console output for current level
    def console_output(self):
        print(f'Level: {self.level}')

    def update(self):
        self.event_handler()
        self.draw_world()


editor=world_edit()
#main game loop
while True:
    clock.tick(fps)
    #draw background
    screen.fill((100,100,100))
    #show the grid and draw the level tiles
    editor.update()
    draw_grid()
    #update game display window
    pygame.display.update()