import pygame, time, random, sys,text,enemies,equip
from sprite_animation import Spritesheet
from pygame.constants import JOYAXISMOTION, JOYBUTTONDOWN, JOYHATMOTION, MOUSEBUTTONDOWN
import common_functions as comfunc
import player_one as player
from color_palette import *
from random import randint
import controller as con

screen_width = 1000
screen_height = 500
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Scythe')
player.screen = screen
enemies.screen=screen
#image loading
corner_flair=pygame.image.load("media\Corner_flair.png")
botright_corner_bush=pygame.transform.rotate(corner_flair,90)
#scyman=pygame.image.load('media\scyman.png')
windy_cloud=Spritesheet('media\windy_cloud\wc.png',[0,30],True)
grass_clump=pygame.image.load('media\deco\grass_clump.png')
relic=equip.equip_matrix[1][randint(1,3)].image
randx=randint(0,1000)
randy=randint(0,500)
#enemy loading
scarecrows=pygame.sprite.Group()
for i in range(10):
    i=enemies.Scarecrow()
    scarecrows.add(i)
    enemies.enemies.append(i)
# for i in range(5):
#     i=enemies.Omnivine()
#     scarecrows.add(i)
player.scarecrows=scarecrows

#player binding
scyman=player.PlayerOne(500,250)

#text loading
plug_in_text=text.TextHandler('media\VecnaBold.ttf',LEATHER,'Plug In Controller',50)
title_text =text.TextHandler("media\VecnaBold.ttf",LIGHT_LEATHER,'Scythe',150)
press_start_text =text.TextHandler('media\VecnaBold.ttf',LEATHER,'Press Start',50)
game_over_text =text.TextHandler("media\VecnaBold.ttf",DARK_RED,'Game Over',150)

class GameElements():
    def __init__(self):
        self.focus= 'start'
        self.switch = False

    def start_screen(self):
        global P1
        P1=con.joy_init()
        
        for event in pygame.event.get():
            comfunc.quit(event)
            if event.type == MOUSEBUTTONDOWN:
                if P1:
                    self.switch = False
                    self.focus='play'
                else:
                    self.switch = True
            if event.type == JOYBUTTONDOWN:
                if P1:
                    self.switch = False
                    self.focus='play'
                else:
                    self.switch = True
        screen.fill((0, 95, 65))
        screen.blit(relic,(randx,randy))
        screen.blit(windy_cloud.image,windy_cloud.position,windy_cloud.frame)
        windy_cloud.update()
        screen.blit(corner_flair,(0,467))
        screen.blit(botright_corner_bush,(967,467))
        screen.blit(title_text.text_obj,((screen_width/2 -title_text.
        text_obj.get_width()/2,screen_height/4 -title_text.text_obj.get_height()/2)))
        if self.switch == False:
            screen.blit(press_start_text.text_obj,(screen_width/2 -press_start_text.
            text_obj.get_width()/2,screen_height/2 -press_start_text.text_obj.get_height()/2))
            press_start_text.shrink_pop(50)
        else:
            screen.blit(plug_in_text.text_obj,(screen_width/2 -plug_in_text.
            text_obj.get_width()/2,screen_height/2 -plug_in_text.text_obj.get_height()/2))
            plug_in_text.shrink_pop(50)
            if P1:
                self.switch=False
        pygame.display.flip()

    def main_menu(self):
        for event in pygame.event.get():
            comfunc.quit(event)
        screen.fill((0, 95, 65))
        pygame.display.flip()

    def game_play(self):
        screen.fill((0, 95, 65))
        if scyman.hp <=0:
            self.focus='gameover'
        for event in pygame.event.get():
            comfunc.quit(event)

        
        enemies.player1pos=(scyman.positionx,scyman.positiony)
        
        screen.blit(grass_clump,(randx,randy))
        enemies.spawned_loot.draw(screen)
        scyman.update(P1,delta)
        for i in scarecrows:
            i.update(screen)
        pygame.display.flip()

    def game_over(self):
        screen.fill(DEEP_RED)
        for event in pygame.event.get():
            comfunc.quit(event)
            if event.type==JOYBUTTONDOWN:
                self.focus='start'
                scyman.hp=100
            if event.type==MOUSEBUTTONDOWN:
                self.focus='start'
                scyman.hp=100
        screen.blit(game_over_text.text_obj,((screen_width/2 -game_over_text.text_obj.get_width()/2,screen_height/4 -game_over_text.text_obj.get_height()/2)))
        pygame.display.flip()
            
    def focus_switch(self):
        if self.focus == 'start':
            self.start_screen()
        elif self.focus == 'main':
            self.main_menu()
        elif self.focus == 'play':
            self.game_play()
        elif self.focus=='gameover':
            self.game_over()
   
game = GameElements()
delta_ref=time.time()
while True:
    if pygame.joystick.get_count()==0:
        game.focus='start'
        game.switch=True
    clock.tick(60)
    if scyman.hitlag:
        pygame.time.wait(40)
        delta_ref=delta_ref=time.time()
        scyman.hitlag=False
    delta=time.time()-delta_ref
    delta_ref=time.time()
    game.focus_switch()