import pygame, time, random, sys,text,enemies,equip,gui
from sprite_animation import Spritesheet
from pygame.constants import JOYAXISMOTION, JOYBUTTONDOWN, JOYHATMOTION, MOUSEBUTTONDOWN,MOUSEBUTTONUP
import common_functions as comfunc
import player_one as player
import level_loader as lev
from color_palette import *
from random import randint
import controller as con

screen_width = 1000
screen_height = 500
canvas_width = 3000
canvas_height = 1500
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height))
canvas = pygame.Surface((canvas_width,canvas_height))
pygame.display.set_caption('Scythe')
player.screen = screen
enemies.screen=screen
#image loading
corner_flair=pygame.image.load("media\Corner_flair.png")
botright_corner_bush=pygame.transform.rotate(corner_flair,90)
back_ground=pygame.image.load(r"levels\bg.jpg")
back_ground=pygame.transform.scale(back_ground,(screen_width,screen_height))
windy_cloud=Spritesheet('media\windy_cloud\wc.png',[0,30],True)
grass_clump=pygame.image.load('media\deco\grass_clump.png')
relic=equip.equip_matrix[1][randint(1,3)].image
randx=randint(0,1000)
randy=randint(0,500)
#button loading
start_button=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png'),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png'),(720,100),'map_loader')
multiplayer_button=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png'),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png'),(720,180))
settings_button=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png'),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png'),(720,260))
credits_button=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png'),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png'),(720,340))

#structure group
structures=pygame.sprite.Group()
#enemy loading
start_vine=enemies.Omnivine(randint(50,950),randint(50,450))

scarecrows=pygame.sprite.Group()
player.scarecrows=scarecrows
player.structures=structures
equip.scarecrows=scarecrows
enemies.enemies=scarecrows


#text loading
plug_in_text=text.TextHandler('media\VecnaBold.ttf',LEATHER,'Plug In Controller',50)
title_text =text.TextHandler("media\VecnaBold.ttf",LIGHT_LEATHER,'Scythe',150)
press_start_text =text.TextHandler('media\VecnaBold.ttf',LEATHER,'Press Start',50)
game_over_text =text.TextHandler("media\VecnaBold.ttf",DARK_RED,'Game Over',150)
pause_text=text.TextHandler('media\VecnaBold.ttf',LIGHT_GREY,'Pause',45)
play_text=text.TextHandler('media\VecnaBold.ttf',BLACK,'Play',35)
multiplayer_text=text.TextHandler('media\VecnaBold.ttf',BLACK,'Multiplayer',35)
settings_text=text.TextHandler('media\VecnaBold.ttf',BLACK,'Settings',35)
credits_text=text.TextHandler('media\VecnaBold.ttf',BLACK,'Credits',35)

class GameElements():
    def __init__(self,canvas):
        self.focus= 'start'
        self.switch = False
        self.loading=True
        self.level_loaded=False
        self.paused=False
        self.current_level=1
        self.canvas=canvas
        self.canvas_pos=pygame.math.Vector2(0,0)
        self.screen_top_left=pygame.math.Vector2(0,0)
        self.canvas_pos=pygame.math.Vector2(0,0)
        self.main_loaded=False

    def start_screen(self):
        global P1,scyman
        P1=con.joy_init()
        if self.loading:
            self.loading=False
            #player binding
            scyman=player.PlayerOne(0,0)#500,250
        for event in pygame.event.get():
            comfunc.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.focus='map_loader'
            elif event.type == MOUSEBUTTONDOWN:
                if P1:
                    self.switch = False
                    self.focus='main'
                else:
                    self.switch = True
            elif event.type == JOYBUTTONDOWN:
                if P1:
                    self.switch = False
                    self.focus='map_loader'
                else:
                    self.switch = True
        screen.fill((0, 95, 65))
        screen.blit(relic,(randx,randy))
        start_vine.demo()
        screen.blit(start_vine.image,(start_vine.rect.center))
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

    def pause(self):
        global delta_ref
        while True:
            if not self.paused:
                self.paused=True
                self.pause_background=screen.copy()
                self.pause_background=comfunc.surf_blur(self.pause_background,2)
            screen.blit(self.pause_background,(0,0))
            screen.blit(pause_text.text_obj,
                ((screen_width/2 -pause_text.text_obj.get_width()/2,
                screen_height/2 -pause_text.text_obj.get_height()/2)))
            pygame.display.flip()
            for event in pygame.event.get():
                comfunc.quit(event)
                if event.type == JOYBUTTONDOWN:
                    if P1.get_button(7):
                        self.paused=False
                        delta_ref=time.time()
                        return

    def main_menu(self):
        global P1,scyman
        if not self.main_loaded:
            self.main_loaded=True
            self.buttons=pygame.sprite.Group()
            self.buttons.add(start_button)
            self.buttons.add(multiplayer_button)
            self.buttons.add(settings_button)
            self.buttons.add(credits_button)

        screen.fill((0, 95, 65))
        screen.blit(relic,(randx,randy))
        start_vine.demo()
        screen.blit(start_vine.image,(start_vine.rect.center))
        screen.blit(windy_cloud.image,windy_cloud.position,windy_cloud.frame)
        windy_cloud.update()
        screen.blit(corner_flair,(0,467))
        screen.blit(botright_corner_bush,(967,467))
        screen.blit(title_text.text_obj,((screen_width/2 -title_text.
        text_obj.get_width()/2,screen_height -title_text.text_obj.get_height())))
        self.buttons.draw(screen)
        screen.blit(play_text.text_obj,(start_button.rect.center[0] - play_text.rect.width/2,start_button.rect.center[1] - play_text.rect.height/2))
        screen.blit(multiplayer_text.text_obj,(multiplayer_button.rect.center[0] - multiplayer_text.rect.width/2,multiplayer_button.rect.center[1] - multiplayer_text.rect.height/2))
        screen.blit(settings_text.text_obj,(settings_button.rect.center[0] - settings_text.rect.width/2,settings_button.rect.center[1] - settings_text.rect.height/2))
        screen.blit(credits_text.text_obj,(credits_button.rect.center[0] - credits_text.rect.width/2,credits_button.rect.center[1] - credits_text.rect.height/2))
        mouse_pos=pygame.mouse.get_pos()
        for event in pygame.event.get():
            comfunc.quit(event)
            if event.type == MOUSEBUTTONDOWN:
                for i in self.buttons:
                    if i.rect.collidepoint(mouse_pos):
                        i.image_swap()
                        i.clicked()
            if event.type==MOUSEBUTTONUP:
                for i in self.buttons:
                    if i.rect.collidepoint(mouse_pos):
                        if i.depressed:
                            temp=i.activate()
                            if temp:
                                self.focus=temp


            elif event.type == JOYBUTTONDOWN:
                pass
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
            i.update(screen,scyman)
        pygame.display.flip()

    def map_loader(self):
        if not self.level_loaded:
            structures.empty()
            scarecrows.empty()
            self.level_data,self.game_data=lev.load_level(self.current_level)
            self.level_loaded=True
            self.canvas_original,enemy_container,collidable_structures=lev.create_canvas(self.level_data,self.game_data)
            structures.add(collidable_structures)
            scarecrows.add(enemy_container)
        screen.blit(back_ground,(0,0))
        self.canvas=self.canvas_original.copy()
        player.canvas=self.canvas
        enemies.canvas=self.canvas
        enemies.player1pos=(scyman.positionx,scyman.positiony)
        enemies.spawned_loot.draw(self.canvas)
        scyman.update(P1,delta)
        for i in scarecrows:
            i.update(self.canvas,scyman)
        structures.draw(self.canvas)
        screen.blit(self.canvas,(self.canvas_movement()))
        if scyman.hp <=0:
            self.blur=screen.copy().convert_alpha()
            self.alpha=150
            self.blur.set_alpha(self.alpha)
            self.focus='gameover'
        scyman.update_gui()
        for event in pygame.event.get():
            comfunc.quit(event)
            if event.type==JOYBUTTONDOWN:
                if P1.get_button(7):
                    self.pause()
        pygame.display.flip()

    def canvas_movement(self):
        canvas_dest=pygame.math.Vector2(self.screen_top_left-scyman.rect.center+pygame.math.Vector2(screen_width/2,screen_height/2))
        if canvas_dest[0]>32:
            canvas_dest[0]=32
        if canvas_dest[1]>32:
            canvas_dest[1]=32
        if canvas_dest[0]<-2032:
            canvas_dest[0]=-2032
        if canvas_dest[1]<-1032:
            canvas_dest[1]=-1032
        canvas_vector_length=pygame.math.Vector2(canvas_dest-self.canvas_pos)
        if canvas_vector_length !=0:
            self.canvas_pos+=(canvas_dest-self.canvas_pos)*.15
        return self.canvas_pos

    def game_over(self):
        screen.fill(DEEP_RED)
        screen.blit(self.blur,(0,0))
        self.blur=comfunc.surf_blur(self.blur,1)
        self.blur.set_alpha(self.alpha)
        self.alpha-=.30
        
        for event in pygame.event.get():
            comfunc.quit(event)
            if event.type==JOYBUTTONDOWN:
                self.reset()
            if event.type==MOUSEBUTTONDOWN:
                self.reset()
        screen.blit(game_over_text.text_obj,((screen_width/2 -game_over_text.text_obj.get_width()/2,screen_height/4 -game_over_text.text_obj.get_height()/2)))
        pygame.display.flip()

    def reset(self):
        self.loading=True
        self.level_loaded=False
        self.focus='main'

    def focus_switch(self):
        if self.focus == 'start':
            self.start_screen()
        elif self.focus == 'main':
            self.main_menu()
        elif self.focus == 'play':
            self.game_play()
        elif self.focus=='gameover':
            self.game_over()
        elif self.focus=='map_loader':
            self.map_loader()
   
game = GameElements(canvas)
player.canvas=game.canvas
enemies.canvas=game.canvas
delta_ref=time.time()
while True:
    if pygame.joystick.get_count()==0:
        game.focus='start'
        game.switch=True
    clock.tick(60)
    # if scyman.hitlag:
    #     pygame.time.wait(40)
    #     delta_ref=delta_ref=time.time()
    #     scyman.hitlag=False
    delta=time.time()-delta_ref
    delta_ref=time.time()
    game.focus_switch()