import pickle,pygame,enemies
from pygame.locals import *
from os import path

tile_size = 30
cols = 100
screen_width = tile_size * cols
canvas_width = 3000
canvas_height = 1500
cells = (tile_size * cols)//2

#load images

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

collidable_structures=pygame.sprite.Group()
enemy_container=pygame.sprite.Group()

def load_level(level):
    collidable_structures.empty()
    enemy_container.empty()
    if path.exists(f'levels\level{level}_data'):
        pickle_in = open(f'levels\level{level}_data', 'rb')
        coupled_data = pickle.load(pickle_in)
        world_data,game_data = coupled_data[0],coupled_data[1]
        pickle_in.close()
        return world_data,game_data

class Structure(pygame.sprite.Sprite):
    def __init__(self,tile,x,y):
        super().__init__()
        self.image=tile
        self.mask=pygame.mask.from_surface(tile)
        self.rect=tile.get_rect()
        self.rect.x=x
        self.rect.y=y


def build(img,row,col):
    structure=Structure(img,col * tile_size,row * tile_size)
    collidable_structures.add(structure)


def spawn(enemy_type,row,col):
        enemy=eval(f'enemies.{enemy_type}({col * tile_size},{row * tile_size})')
        enemy_container.add(enemy)



def create_canvas(world_data,game_data):
    canvas = pygame.Surface((canvas_width,canvas_height), pygame.SRCALPHA)
    for row in range(cells):
        for col in range(cells):
            if world_data[row][col] > 0:
        ########world_data
                #tiles
                if world_data[row][col] == 1:
                    #dirt blocks
                    img = pygame.transform.scale(dirt_img1, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 2:
                    #grass blocks
                    img = pygame.transform.scale(grass_img1, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 3:
                    #sand blocks
                    img = pygame.transform.scale(sand_img1, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 4:
                    #snow blocks
                    img = pygame.transform.scale(snow_img1, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 5:
                    #ice blocks
                    img = pygame.transform.scale(ice_img1, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 6:
                    #stone blocks
                    img = pygame.transform.scale(stone_img1, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                #roads
                if world_data[row][col] == 7:
                    #horizontal road
                    img = pygame.transform.scale(horzroad, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 8:
                    #vertical road
                    img = pygame.transform.scale(vertroad, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 9:
                    #top left corner road
                    img = pygame.transform.scale(topleftcorner, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 10:
                    #top right corner road
                    img = pygame.transform.scale(toprightcorner, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 11:
                    #bottom right corner road
                    img = pygame.transform.scale(bottomrightcorner, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 12:
                    #bottom left corner road
                    img = pygame.transform.scale(bottomleftcorner, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 13:
                    #top tee road
                    img = pygame.transform.scale(teeup, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 14:
                    #right tee road
                    img = pygame.transform.scale(teedown, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 15:
                    #bottom tee road
                    img = pygame.transform.scale(teeright, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 16:
                    #left tee road
                    img = pygame.transform.scale(teeleft, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 17:
                    #top dead end road
                    img = pygame.transform.scale(topend, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 18:
                    #right dead end road
                    img = pygame.transform.scale(rightend, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 19:
                    #left dead end road
                    img = pygame.transform.scale(leftend, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
        ########game_data 
        ########enemies
                if game_data[row][col] == 200:
                    #scarecrow 
                    spawn('Scarecrow',row,col)
                if game_data[row][col] == 201:
                    #omnivine
                    spawn('Omnivine',row,col)
        ########structure
                if game_data[row][col] == 300:
                    img = pygame.transform.scale(block, (tile_size, tile_size))
                    # canvas.blit(img, (col * tile_size, row * tile_size))
                    build(img,row,col)

        ########edges
                if world_data[row][col] == 100:
                    #top left edge
                    img = pygame.transform.scale(top_left, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 101:
                    #top edge
                    img = pygame.transform.scale(top, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 102:
                    #top right edge
                    img = pygame.transform.scale(top_right, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 103:
                    #left edge
                    img = pygame.transform.scale(left, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 104:
                    #right edge
                    img = pygame.transform.scale(right, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 105:
                    #bottom left edge
                    img = pygame.transform.scale(bot_left, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 106:
                    #bottom edge
                    img = pygame.transform.scale(bot, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 107:
                    #bottom right edge
                    img = pygame.transform.scale(bot_right, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
    return canvas,enemy_container,collidable_structures