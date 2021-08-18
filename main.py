import pygame, time, random, sys,text
import common_functions as comfunc
import sprite_animation as sa
from color_palette import *

screen_width = 1000
screen_height = 500
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Scythe')

#image loading
corner_flair=pygame.image.load("media\Corner_flair.png")
scyman=pygame.image.load('media\scyman.png')

#joystick handling
joysticks = (pygame.joystick.get_count())
if joysticks >0:
    P1 = pygame.joystick.Joystick(0)
    P1.init()
    if joysticks >1:
        P2 = pygame.joystick.Joystick(1)
        P2.init()

#sprite loading
scyman_walking=sa.ScymanWalk(500,250)
scyman_walking_animation=pygame.sprite.Group()
scyman_walking_animation.add(scyman_walking)

#text loading
title_text =text.TextHandler("media\VecnaBold.ttf",LIGHT_LEATHER,'Welcome',150)
press_start_text =text.TextHandler('media\VecnaBold.ttf',LEATHER,'Press Start',50)

# press_start_text= comfunc.scale_bounce(press_start_text)

class GameElements():
    def __init__(self):
        self.focus= 'start'

    def start_screen(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            comfunc.quit(event)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.joy == 0:
                   self.focus='play'
                elif event.joy == 1:
                    print('test')
            
        screen.fill((0, 95, 65))
        screen.blit(corner_flair,(0,467))
        screen.blit(title_text.text_obj,((screen_width/2 -title_text.text_obj.get_width()/2,screen_height/4 -title_text.text_obj.get_height()/2)))
        screen.blit(press_start_text.text_obj,(screen_width/2 -press_start_text.text_obj.get_width()/2,screen_height/2 -press_start_text.text_obj.get_height()/2))
        press_start_text.shrink_pop(50)
        pygame.display.flip()

    def main_menu(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            comfunc.quit(event)
        screen.fill((0, 95, 65))
        pygame.display.flip()
        print()

    def game_play(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            comfunc.quit(event)
            if event.type == pygame.JOYAXISMOTION:
                if not comfunc.dead_zone(P1):
                    scyman_walking.animate()
                    scyman_walking.move(P1,event)
        screen.fill((0, 95, 65))
        scyman_walking_animation.draw(screen)
        scyman_walking_animation.update(.09)
        pygame.display.flip()

    def focus_switch(self):
        if self.focus == 'start':
            self.start_screen()
        elif self.focus == 'main':
            self.main_menu()
        elif self.focus == 'play':
            self.game_play()


game = GameElements()
while True:
    clock.tick(60)
    game.focus_switch()