import pickle,pygame
from pygame.locals import *
from os import path

tile_size = 10
cols = 100
margin = 10
screen_width = tile_size * cols
screen_height = int((tile_size * (cols/2)) + margin)
num_lines = int((tile_size * cols)/2)
canvas_width = 3000
canvas_height = 1500

#load images
dirt_img1 = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_13.png')
dirt_img1 = pygame.transform.scale(dirt_img1, (tile_size, tile_size))
bg_img = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_14.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
dirt_img2 = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_14.png')
grass_img1 = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_57.png')
grass_img2 = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_58.png')
platform_x_img = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_56.png')
platform_y_img = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_55.png')
lava_img = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_54.png')
coin_img = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_53.png')
exit_img = pygame.image.load('level_editor\level_editor\kenney_medievalrtspack\PNG\Default size\Tile\medievalTile_52.png')
save_img = pygame.image.load('level_editor\level_editor\save_btn.png')
load_img = pygame.image.load('level_editor\level_editor\load_btn.png')
#edges
top_left=pygame.image.load(r'media\tile\edge\topleft.png')
top=pygame.image.load(r'media\tile\edge\top.png')
top_right=pygame.image.load(r'media\tile\edge\topright.png')
left=pygame.image.load(r'media\tile\edge\left.png')
right=pygame.image.load(r'media\tile\edge\right.png')
bot_left=pygame.image.load(r'media\tile\edge\botleft.png')
bot=pygame.image.load(r'media\tile\edge\bot.png')
bot_right=pygame.image.load(r'media\tile\edge\botright.png')

def load_level(level):
    if path.exists(f'levels\level{level}_data'):
        pickle_in = open(f'levels\level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
        pickle_in.close()
        return world_data


def create_canvas(world_data):
    canvas = pygame.Surface((canvas_width,canvas_height))
    canvas.fill((0,0,0))
    canvas.set_colorkey((0,0,0))
    for row in range(500):
        for col in range(500):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    #dirt blocks
                    img = pygame.transform.scale(dirt_img1, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 2:
                    #grass blocks
                    img = pygame.transform.scale(grass_img1, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 3:
                    #enemy blocks
                    img = pygame.transform.scale(grass_img2, (tile_size, int(tile_size * 0.75)))
                    canvas.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 4:
                    #horizontally moving platform
                    img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 5:
                    #vertically moving platform
                    img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 6:
                    #lava
                    img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
                    canvas.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                if world_data[row][col] == 7:
                    #coin
                    img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
                    canvas.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
                if world_data[row][col] == 8:
                    #exit
                    img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
                    canvas.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))
                    #edges
                if world_data[row][col] == 9:
                    #top left edge
                    img = pygame.transform.scale(top_left, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 10:
                    #top edge
                    img = pygame.transform.scale(top, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 11:
                    #top right edge
                    img = pygame.transform.scale(top_right, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 12:
                    #left edge
                    img = pygame.transform.scale(left, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 13:
                    #right edge
                    img = pygame.transform.scale(right, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 14:
                    #bottom left edge
                    img = pygame.transform.scale(bot_left, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 15:
                    #bottom edge
                    img = pygame.transform.scale(bot, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 16:
                    #bottom right edge
                    img = pygame.transform.scale(bot_right, (tile_size, tile_size))
                    canvas.blit(img, (col * tile_size, row * tile_size))
    return canvas