import pygame, time, random, sys,text

from sprite_animation import Spritesheet
from pygame.constants import JOYAXISMOTION, JOYBUTTONDOWN, JOYHATMOTION, MOUSEBUTTONDOWN
import common_functions as comfunc
import player_one as player
from color_palette import *

screen_width = 1000
screen_height = 500
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Scythe')

#image loading
corner_flair=pygame.image.load("media\Corner_flair.png")
botright_corner_bush=pygame.transform.rotate(corner_flair,90)
scyman=pygame.image.load('media\scyman.png')
windy_cloud=Spritesheet('media\windy_cloud\wc.png',[0,30],True)



#joystick handling
joysticks = (pygame.joystick.get_count())
if joysticks >0:
    P1 = pygame.joystick.Joystick(0)
    P1.init()
    if joysticks >1:
        P2 = pygame.joystick.Joystick(1)
        P2.init()

#player binding
scyman=player.PlayerOne(500,250)

#text loading
title_text =text.TextHandler("media\VecnaBold.ttf",LIGHT_LEATHER,'Welcome',150)
press_start_text =text.TextHandler('media\VecnaBold.ttf',LEATHER,'Press Start',50)


class GameElements():
    def __init__(self):
        self.focus= 'start'

    def start_screen(self):
        for event in pygame.event.get():
            comfunc.quit(event)
            if event.type == MOUSEBUTTONDOWN:
                self.focus='play'
            if event.type == JOYBUTTONDOWN:
                self.focus='play'
            if event.type == JOYAXISMOTION:
                print(event.value)
                print(event.axis)
        screen.fill((0, 95, 65))
        screen.blit(windy_cloud.image,windy_cloud.position,windy_cloud.frame)
        windy_cloud.update()
        screen.blit(corner_flair,(0,467))
        screen.blit(botright_corner_bush,(967,467))
        screen.blit(title_text.text_obj,((screen_width/2 -title_text.text_obj.get_width()/2,screen_height/4 -title_text.text_obj.get_height()/2)))
        screen.blit(press_start_text.text_obj,(screen_width/2 -press_start_text.text_obj.get_width()/2,screen_height/2 -press_start_text.text_obj.get_height()/2))
        press_start_text.shrink_pop(50)
        pygame.display.flip()

    def main_menu(self):
        for event in pygame.event.get():
            comfunc.quit(event)
        screen.fill((0, 95, 65))
        pygame.display.flip()

    def game_play(self):
        screen.fill((0, 95, 65))
        for event in pygame.event.get():
            comfunc.quit(event)
            scyman.move(delta,event)
        scyman.update(delta)
        screen.blit(scyman.image,(scyman.positionx,scyman.positiony))
        pygame.display.flip()

    def focus_switch(self):
        if self.focus == 'start':
            self.start_screen()
        elif self.focus == 'main':
            self.main_menu()
        elif self.focus == 'play':
            self.game_play()

game = GameElements()
delta_ref=time.time()
while True:
    clock.tick(60)
    delta=time.time()-delta_ref
    delta_ref=time.time()
    game.focus_switch()