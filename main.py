import Time,pygame
Time.init()
pygame.init()
screen_width = 1000
screen_height = 500
canvas_width = 3000
canvas_height = 1500
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width,screen_height))
canvas = pygame.Surface((canvas_width,canvas_height))
pygame.display.set_caption('Scythe')


import time, random, sys,text,enemies,equip,gui,boss
from sprite_animation import Spritesheet
from pygame.constants import JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, MOUSEBUTTONDOWN,MOUSEBUTTONUP
import common_functions as comfunc
import player_one as player
import level_loader as lev
from color_palette import *
from random import randint
import controller as con
from save_data import data_IO as dio


player.screen = screen
enemies.screen=screen
boss.screen=screen


#image loading
corner_flair=pygame.image.load("media\Corner_flair.png").convert_alpha()
botright_corner_bush=pygame.transform.rotate(corner_flair,90)
back_ground=pygame.image.load(r"levels\bg.jpg").convert_alpha()
back_ground=pygame.transform.scale(back_ground,(screen_width,screen_height))
windy_cloud=Spritesheet('media\windy_cloud\wc.png',[0,30],True)
grass_clump=pygame.image.load('media\deco\grass_clump.png').convert_alpha()
relic=equip.equip_matrix[1][randint(1,3)].image
randx=randint(0,1000)
randy=randint(0,500)
#button loading
start_button=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(720,100),'->Play<-','save_select')
multiplayer_button=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(720,180),'Multiplayer')
settings_button=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(720,260),'Settings')
credits_button=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(720,340),'Credits')
save_button_1=gui.Button(pygame.image.load(r'media\gui\main_menu\panel_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\panelInset_beige.png').convert_alpha(),(300,250),'File 1','map_loader',True)
save_button_2=gui.Button(pygame.image.load(r'media\gui\main_menu\panel_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\panelInset_beige.png').convert_alpha(),(500,250),'File 2','map_loader',True)
save_button_3=gui.Button(pygame.image.load(r'media\gui\main_menu\panel_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\panelInset_beige.png').convert_alpha(),(700,250),'File 3','map_loader',True)
#gui loading
player_menu_bg=pygame.transform.scale(pygame.image.load(r'media\gui\main_menu\panel_beige.png').convert_alpha(),(int(screen_width*.6),int(screen_height*.75)))
player_menu_details=gui.Label(pygame.transform.scale(pygame.image.load(r'media\gui\main_menu\panel_beigeLight.png').convert_alpha(),(310,250)),(587,330),'')
player_menu_label=gui.Label(pygame.transform.scale(pygame.image.load(r'media\gui\main_menu\panelInset_beigeLight.png').convert_alpha(),(300,50)),(585,380),'')
player_menu_back=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(275,450),'Close Menu','close')
player_menu_relic=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(320,130),'Relics','relic')
player_menu_armor=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(320,180),'Armor','armor')
player_menu_weapon=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(320,230),'Weapon','weapon')
player_menu_tool=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(320,280),'Tools','tool')
player_menu_status=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(320,330),'Status','status')
player_menu_save=gui.Button(pygame.image.load(r'media\gui\main_menu\buttonLong_beige.png').convert_alpha(),
    pygame.image.load(r'media\gui\main_menu\buttonLong_beige_pressed.png').convert_alpha(),(320,380),'Save Game','save')
#structure group
structures=pygame.sprite.Group()
#enemy loading
demo_enemies=pygame.sprite.Group()

for i in range(4):
    start_scarecrow=enemies.Scarecrow(randint(50,950),randint(50,450))
    demo_enemies.add(start_scarecrow)
    start_scarecrow=enemies.Scarecrow(randint(50,950),randint(50,450))
    demo_enemies.add(start_scarecrow)
    start_vine=enemies.Omnivine(randint(50,950),randint(50,450))
    demo_enemies.add(start_vine)
scyman=player.PlayerOne(0,0)
enemies.player=scyman
boss.player=scyman
scarecrows=pygame.sprite.Group()
player.scarecrows=scarecrows
player.structures=structures
equip.scarecrows=scarecrows
enemies.enemies=scarecrows
boss.enemies=scarecrows


#text loading
standad_font='media\VecnaBold.ttf'
font=pygame.font.Font(standad_font,35)
plug_in_text=text.TextHandler(standad_font,LEATHER,'Plug In Controller',50)
title_text =text.TextHandler(standad_font,LIGHT_LEATHER,'Scythe',150)
press_start_text =text.TextHandler(standad_font,LEATHER,'Press Start',50)
game_over_text =text.TextHandler(standad_font,DARK_RED,'Game Over',150)
pause_text=text.TextHandler(standad_font,LIGHT_GREY,'Pause',45)
play_text=text.TextHandler(standad_font,BLACK,'Play',35)
multiplayer_text=text.TextHandler(standad_font,BLACK,'Multiplayer',35)
settings_text=text.TextHandler(standad_font,BLACK,'Settings',35)
credits_text=text.TextHandler(standad_font,BLACK,'Credits',35)
button_select_left=text.TextHandler(standad_font,LIGHT_LEATHER,'->',50)
button_select_right=text.TextHandler(standad_font,LIGHT_LEATHER,'<-',50)

class GameElements():
    def __init__(self,canvas):
        self.focus= 'start'
        self.aux_state=[]
        self.events=[]
        self.switch = False
        self.loading=True
        self.level_loaded=False
        self.current_level=1
        self.canvas=canvas
        self.canvas_pos=pygame.math.Vector2(0,0)
        self.screen_top_left=pygame.math.Vector2(0,0)
        self.main_loaded=False
        self.save_select_loaded=False
        self.player_menu_loaded=False
        self.game_over_loaded=False
        self.save_slot=0
        self.game_over_blur=0
        self.alpha=255
        self.button_action=False

    def start_screen(self):
        global P1,scyman
        P1=con.joy_init()
        if self.loading:
            self.loading=False
        for event in game.events:
            comfunc.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.focus='map_loader'
            elif event.type == MOUSEBUTTONDOWN:
                self.focus='main'
            elif event.type == JOYBUTTONDOWN:
                if not  event.__dict__['button']==1:
                    if P1:
                        self.switch = False
                        self.focus='main'
                    else:
                        self.switch = True
        screen.fill((0, 95, 65))
        screen.blit(relic,(randx,randy))
        for i in demo_enemies:
            i.demo()
        demo_enemies.draw(screen)
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

    def pause(self):
        global delta_ref
        Time.stop_clock()
        self.pause_background=screen.copy()
        self.pause_background=comfunc.surf_blur(self.pause_background,2)
        def draw(self):
            screen.blit(self.pause_background,(0,0))
            screen.blit(pause_text.text_obj,
                ((screen_width/2 -pause_text.text_obj.get_width()/2,
                screen_height/2 -pause_text.text_obj.get_height()/2)))
        while True:
            draw(self)
            game.events=pygame.event.get()
            Time.update()
            clock.tick(60)
            for event in game.events:
                comfunc.quit(event)
                if event.type == JOYBUTTONDOWN:
                    if event.__dict__['button']==6:
                        self.aux_state.append('player_menu')
                    if event.__dict__['button']==7:
                        game.events.remove(event)
                        comfunc.clean_list(self.aux_state,'player_menu')
                        self.player_menu_loaded=False
                        player_menu_label.set_text('')
                        Time.start_clock()
                        delta_ref=time.time()
                        return
            if 'player_menu' in self.aux_state:
                self.player_menu()
            pygame.display.flip()

    def player_menu(self):
        if not self.player_menu_loaded:
            self.scroll=gui.ScrollY((0,0),0,[('brown','body')])
            self.scroll_offset=0
            self.player_menu_tween_size=25
            self.player_menu_loaded=True
            self.reset_joystick_needed=False
            self.button_6_reset=False
            player_menu_details.set_clipping_image(self.scroll.surface,(0,self.scroll_offset),
                (0,11,player_menu_details.rect.width*.9,player_menu_details.rect.height*.917))
            self.player_menu_buttons=pygame.sprite.Group()
            self.player_menu_buttons.add(player_menu_back)
            self.player_menu_buttons.add(player_menu_relic)
            self.player_menu_buttons.add(player_menu_armor)
            self.player_menu_buttons.add(player_menu_weapon)
            self.player_menu_buttons.add(player_menu_tool)
            self.player_menu_buttons.add(player_menu_status)
            self.player_menu_buttons.add(player_menu_save)
            self.player_menu_button_order=[
                player_menu_back,
                player_menu_relic,
                player_menu_armor,
                player_menu_weapon,
                player_menu_tool,
                player_menu_status,
                player_menu_save]
            self.button_focus=0

        bg_rect=comfunc.center_image(screen,player_menu_bg)
        mouse_pos=pygame.mouse.get_pos()
        for i in self.player_menu_buttons:
            if not self.button_focus==self.player_menu_button_order.index(i):
                if i.depressed:
                    i.image_swap()
                    i.clicked()
            if i.rect.collidepoint(mouse_pos):
                self.button_focus=self.player_menu_button_order.index(i)

        tween_size=self.player_menu_tween_size
        if tween_size<350:
            self.player_menu_tween_size+=tween_size*Time.delta()*(tween_size*.3)
            x,y=int(tween_size*1.65),int(tween_size)
            screen.blit(pygame.transform.scale(player_menu_bg,(x,y)),(int(bg_rect[0]),int(bg_rect[1])))
        else:
            screen.blit(player_menu_bg,(bg_rect[0],bg_rect[1]))
            self.player_menu_buttons.draw(screen)
            player_menu_details.draw(screen)
            player_menu_label.draw(screen)
            screen.blit(
                button_select_left.text_obj,
                (self.player_menu_button_order[self.button_focus].rect.left-button_select_left.width,
                self.player_menu_button_order[self.button_focus].rect.top))
            screen.blit(
                button_select_right.text_obj,
                (self.player_menu_button_order[self.button_focus].rect.right,
                self.player_menu_button_order[self.button_focus].rect.top))
            current_button=self.player_menu_button_order[self.button_focus]

        for event in game.events:
            comfunc.quit(event)
            if event.type == MOUSEBUTTONDOWN:
                for i in self.player_menu_buttons:
                    if i.rect.collidepoint(mouse_pos):
                        i.image_swap()
                        i.clicked()
            if event.type==MOUSEBUTTONUP:
                for i in self.player_menu_buttons:
                    if i.rect.collidepoint(mouse_pos):
                        if i.depressed:
                            i.image_swap()
                            i.clicked()
                            self.button_action=i.activate()
                    if i.depressed:
                        i.depressed=False
                        i.image_swap()
            elif event.type == JOYBUTTONDOWN:
                if event.__dict__['button']==0:
                    current_button.image_swap()
                    current_button.clicked()
                if event.__dict__['button']==1:
                    self.button_focus=0
                    current_button=self.player_menu_button_order[self.button_focus]
                    current_button.image_swap()
                    current_button.clicked()
                if event.__dict__['button']==6:
                    if self.button_6_reset==True:
                        self.button_focus=0
                        current_button=self.player_menu_button_order[self.button_focus]
                        current_button.image_swap()
                        current_button.clicked()

            elif event.type == JOYBUTTONUP:
                if event.__dict__['button']==0:
                    if current_button.depressed:
                        current_button.image_swap()
                        current_button.clicked()
                        self.button_action=current_button.activate()
                if event.__dict__['button']==1:
                    if current_button.depressed:
                        current_button.image_swap()
                        current_button.clicked()
                        self.button_action=current_button.activate()
                if event.__dict__['button']==6:
                    if self.button_6_reset==False:
                        self.button_6_reset=True
                    else:
                        if current_button.depressed:
                            current_button.image_swap()
                            current_button.clicked()
                            self.button_action=current_button.activate()


            elif event.type == JOYHATMOTION:
                if event.__dict__['hat']==0:
                    if event.__dict__['value'][1]==-1:
                        self.button_focus+=1
                        if self.button_focus>len(self.player_menu_button_order)-1:
                            self.button_focus=0
                    if event.__dict__['value'][1]==1:
                        self.button_focus-=1
                        if self.button_focus<0:
                            self.button_focus=len(self.player_menu_button_order)-1
            elif event.type == JOYAXISMOTION:
                if not self.reset_joystick_needed and not comfunc.dead_zone(P1,single_axis=1):
                    if event.__dict__['axis']==1:
                        if event.__dict__['value']>.95:
                            self.reset_joystick_needed=True
                            self.button_focus+=1
                            if self.button_focus>len(self.player_menu_button_order)-1:
                                self.button_focus=0
                        if event.__dict__['value']<-.95:
                            self.reset_joystick_needed=True
                            self.button_focus-=1
                            if self.button_focus<0:
                                self.button_focus=len(self.player_menu_button_order)-1
                elif comfunc.dead_zone(P1,single_axis=1,tolerance=.85):
                    self.reset_joystick_needed=False

        if self.button_action:
            player_menu_label.set_text(self.button_action)

            if self.button_action=='close':
                comfunc.clean_list(self.aux_state,'player_menu')
                self.player_menu_loaded=False
                player_menu_label.set_text('')

            if self.button_action=='relic':
                self.scroll_offset=0
                player_menu_label.set_text(f'Aquired {len(scyman.relics)}/8 Relics',27)
                relic_list=[]
                color=['blue','beige','brown','grey']
                for index,i in enumerate(scyman.relics):
                    while index>=len(color):
                        index-=len(color)
                    relic_list.append((color[index],'header',f'{i.name[:-6]}',30,(i.image,(5,6))))
                    relic_list.append((color[index],'body',f'{i.details}',28))
                self.scroll=gui.ScrollY(
                    player_menu_details.rect.topleft,
                    player_menu_details.rect.width,
                    relic_list)
                player_menu_details.set_clipping_image(self.scroll.surface,(0,self.scroll_offset),
                    (0,11,player_menu_details.rect.width*.9,player_menu_details.rect.height*.917))

            if self.button_action=='armor':
                self.scroll_offset=0
                player_menu_label.set_text(f'Total Aquired Armor: {len(scyman.armor)}',27)
                armor_list=[]
                color=['blue','beige','brown','grey']
                for index,i in enumerate(scyman.armor):
                    while index>=len(color):
                        index-=len(color)
                    armor_list.append((color[index],'header',f'{i.name[:-6]}',30,(i.image,(5,6))))
                    armor_list.append((color[index],'body',f'{i.details}',28))
                self.scroll=gui.ScrollY(
                    player_menu_details.rect.topleft,
                    player_menu_details.rect.width,
                    armor_list)
                player_menu_details.set_clipping_image(self.scroll.surface,(0,self.scroll_offset),
                    (0,11,player_menu_details.rect.width*.9,player_menu_details.rect.height*.917))

            if self.button_action=='weapon':
                self.scroll_offset=0
                player_menu_label.set_text(f'Current Weapon: Scythe',27)
                player_menu_details.set_text('Will show weapon info here',27)

            if self.button_action=='tool':
                self.scroll_offset=0
                player_menu_label.set_text(f'Aquired {len(scyman.tools)} Tools',27)
                tool_list=[]
                color=['blue','beige','brown','grey']
                if scyman.tools:
                    for index,i in enumerate(scyman.tool):
                        while index>=len(color):
                            index-=len(color)
                        tool_list.append((color[index],'header',f'{i.name[:-6]}',30,(i.image,(5,6))))
                        tool_list.append((color[index],'body',f'{i.details}',28))
                    self.scroll=gui.ScrollY(
                        player_menu_details.rect.topleft,
                        player_menu_details.rect.width,
                        tool_list)
                    player_menu_details.set_clipping_image(self.scroll.surface,(0,self.scroll_offset),
                        (0,11,player_menu_details.rect.width*.9,player_menu_details.rect.height*.917))

            if self.button_action=='status':
                self.scroll_offset=0
                player_menu_label.set_text(f'Status',27)
                player_menu_details.set_text('Will show status info here',27)

            if self.button_action=='save':
                self.save_game()
                player_menu_label.set_text('Game Saved!')
                player_menu_details.set_text(f'')

            self.button_action=False

        axis_val=P1.get_axis(4)
        if abs(axis_val)>.3:
            self.scroll_offset+=(axis_val*-1)*Time.delta()*350
            if self.scroll_offset<-self.scroll.surface.get_height()+((player_menu_details.rect.height/4)*3):
                self.scroll_offset=-self.scroll.surface.get_height()+((player_menu_details.rect.height/4)*3)
            if self.scroll_offset>player_menu_details.rect.height/4:
                self.scroll_offset=player_menu_details.rect.height/4
            player_menu_details.set_clipping_image(self.scroll.surface,(0,self.scroll_offset),
                (0,11,player_menu_details.rect.width*.9,player_menu_details.rect.height*.917))


    def main_menu(self):
        global P1,scyman
        if not self.main_loaded:
            self.button_0_reset=False
            self.button_7_reset=False
            self.main_loaded=True
            self.buttons=pygame.sprite.Group()
            self.buttons.add(start_button)
            self.buttons.add(multiplayer_button)
            self.buttons.add(settings_button)
            self.buttons.add(credits_button)
            self.button_order=[
                start_button,
                multiplayer_button,
                settings_button,
                credits_button]
            self.button_focus=0
            self.reset_joystick_needed=False
            for i in self.buttons:
                if i.depressed:
                    i.image_swap()
                    i.clicked()

        screen.fill((0, 95, 65))
        screen.blit(relic,(randx,randy))
        for i in demo_enemies:
            i.demo()
        demo_enemies.draw(screen)
        screen.blit(windy_cloud.image,windy_cloud.position,windy_cloud.frame)
        windy_cloud.update()
        screen.blit(corner_flair,(0,467))
        screen.blit(botright_corner_bush,(967,467))
        screen.blit(title_text.text_obj,((screen_width/2 -title_text.
            text_obj.get_width()/2,screen_height -title_text.text_obj.get_height())))
        self.buttons.draw(screen)

        mouse_pos=pygame.mouse.get_pos()
        for i in self.buttons:
            if not self.button_focus==self.button_order.index(i):
                if i.depressed:
                    i.image_swap()
                    i.clicked()
            if i.rect.collidepoint(mouse_pos):
                self.button_focus=self.button_order.index(i)
        screen.blit(
            button_select_left.text_obj,
            (self.button_order[self.button_focus].rect.left-button_select_left.width,
            self.button_order[self.button_focus].rect.top))
        screen.blit(
            button_select_right.text_obj,
            (self.button_order[self.button_focus].rect.right,
            self.button_order[self.button_focus].rect.top))
        current_button=self.button_order[self.button_focus]
        for event in game.events:
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
                                self.main_loaded=False
                    if i.depressed:
                        i.depressed=False
                        i.image_swap()
            elif event.type == JOYBUTTONDOWN:
                if event.__dict__['button']==0 or event.__dict__['button']==7:
                    current_button.image_swap()
                    current_button.clicked()

            elif event.type == JOYBUTTONUP:
                if event.__dict__['button']==0 or event.__dict__['button']==7:
                    if not self.button_0_reset or not self.button_7_reset:
                        self.button_0_reset=True
                        self.button_7_reset=True
                    else:
                        if current_button.depressed:
                            current_button.image_swap()
                            current_button.clicked()
                            temp=self.button_order[self.button_focus].activate()
                            if temp:
                                self.focus=temp
                                self.main_loaded=False
                if event.__dict__['button']==1:

                    self.focus='start'
                    self.main_loaded=False
            elif event.type == JOYHATMOTION:
                if event.__dict__['hat']==0:
                    if event.__dict__['value'][1]==-1:
                        self.button_focus+=1
                        if self.button_focus>len(self.button_order)-1:
                            self.button_focus=0
                    if event.__dict__['value'][1]==1:
                        self.button_focus-=1
                        if self.button_focus<0:
                            self.button_focus=len(self.button_order)-1
            elif event.type == JOYAXISMOTION:
                if not self.reset_joystick_needed and not comfunc.dead_zone(P1,single_axis=1):
                    if event.__dict__['axis']==1:
                        if event.__dict__['value']>.95:
                            self.reset_joystick_needed=True
                            self.button_focus+=1
                            if self.button_focus>len(self.button_order)-1:
                                self.button_focus=0
                        if event.__dict__['value']<-.95:
                            self.reset_joystick_needed=True
                            self.button_focus-=1
                            if self.button_focus<0:
                                self.button_focus=len(self.button_order)-1
                elif comfunc.dead_zone(P1,single_axis=1,tolerance=.85):
                    self.reset_joystick_needed=False

    def save_select(self):
        global P1,scyman
        if not self.save_select_loaded:
            self.save_select_loaded=True
            self.buttons=pygame.sprite.Group()
            self.buttons.add(save_button_1)
            self.buttons.add(save_button_2)
            self.buttons.add(save_button_3)
            self.button_order=[
                save_button_1,
                save_button_2,
                save_button_3]
            self.button_focus=0
            self.reset_joystick_needed=False
            for i in self.buttons:
                if i.depressed:
                    i.image_swap()
                    i.clicked()

        screen.fill((0, 95, 65))
        screen.blit(relic,(randx,randy))
        for i in demo_enemies:
            i.demo()
        demo_enemies.draw(screen)
        screen.blit(windy_cloud.image,windy_cloud.position,windy_cloud.frame)
        windy_cloud.update()
        screen.blit(corner_flair,(0,467))
        screen.blit(botright_corner_bush,(967,467))
        screen.blit(title_text.text_obj,((screen_width/2 -title_text.
            text_obj.get_width()/2,screen_height -title_text.text_obj.get_height())))
        self.buttons.draw(screen)

        mouse_pos=pygame.mouse.get_pos()
        for i in self.buttons:
            if not self.button_focus==self.button_order.index(i):
                if i.depressed:
                    i.image_swap()
                    i.clicked()
            if i.rect.collidepoint(mouse_pos):
                self.button_focus=self.button_order.index(i)
        screen.blit(
            button_select_left.text_obj,
            (self.button_order[self.button_focus].rect.left-button_select_left.width,
            self.button_order[self.button_focus].rect.centery-button_select_left.height/2))
        screen.blit(
            button_select_right.text_obj,
            (self.button_order[self.button_focus].rect.right,
            self.button_order[self.button_focus].rect.centery-button_select_right.height/2))
        current_button=self.button_order[self.button_focus]
        for event in game.events:
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
                                self.save_slot=int(i.text[5])
                                self.load_game()
                                self.focus=temp
                                self.save_select_loaded=False

            elif event.type == JOYBUTTONDOWN:
                if event.__dict__['button']==0 or event.__dict__['button']==7:
                    current_button.image_swap()
                    current_button.clicked()

            elif event.type == JOYBUTTONUP:
                if event.__dict__['button']==0 or event.__dict__['button']==7:
                    if current_button.depressed:
                        current_button.image_swap()
                        current_button.clicked()
                        temp=self.button_order[self.button_focus].activate()
                        if temp:
                            self.save_slot=int(current_button.text[5])
                            self.load_game()
                            self.focus=temp
                            self.save_select_loaded=False
                if event.__dict__['button']==1:
                    self.focus='main'
                    self.save_select_loaded=False

            elif event.type == JOYHATMOTION:
                if event.__dict__['hat']==0:
                    if event.__dict__['value'][0]==1:
                        self.button_focus+=1
                        if self.button_focus>len(self.button_order)-1:
                            self.button_focus=0
                    if event.__dict__['value'][0]==-1:
                        self.button_focus-=1
                        if self.button_focus<0:
                            self.button_focus=len(self.button_order)-1

            elif event.type == JOYAXISMOTION:
                if not self.reset_joystick_needed and not comfunc.dead_zone(P1,single_axis=0):
                    if event.__dict__['axis']==0:
                        if event.__dict__['value']>.95:
                            self.reset_joystick_needed=True
                            self.button_focus+=1
                            if self.button_focus>len(self.button_order)-1:
                                self.button_focus=0
                        if event.__dict__['value']<-.95:
                            self.reset_joystick_needed=True
                            self.button_focus-=1
                            if self.button_focus<0:
                                self.button_focus=len(self.button_order)-1
                elif comfunc.dead_zone(P1,single_axis=0,tolerance=.85):
                    self.reset_joystick_needed=False

    def game_play(self):
        screen.fill((0, 95, 65))
        if scyman.hp <=0:
            self.focus='gameover'
        for event in game.events:
            comfunc.quit(event)

        enemies.player1pos=(scyman.x,scyman.y)

        screen.blit(grass_clump,(randx,randy))
        enemies.spawned_loot.draw(screen)
        scyman.update(P1,Time.delta())
        for i in scarecrows:
            i.update(screen,scyman,Time.delta())

    def map_loader(self):
        if not self.level_loaded:
            structures.empty()
            scarecrows.empty()
            self.level_data,self.game_data=lev.load_level(self.current_level)
            self.level_loaded=True
            self.canvas_original,enemy_container,collidable_structures,player_pos=lev.create_canvas(self.level_data,self.game_data)
            structures.add(collidable_structures)
            scarecrows.add(enemy_container)
            scyman.x,scyman.y=player_pos
            scyman.x_precise,scyman.y_precise=player_pos
        screen.blit(back_ground,(0,0))
        if not scarecrows:
            self.current_level+=1
            self.level_loaded=False
        self.canvas=self.canvas_original.copy()
        player.canvas=self.canvas
        enemies.canvas=self.canvas
        boss.canvas=self.canvas
        enemies.player1pos=(scyman.x,scyman.y)
        for i in scarecrows:
            if hasattr(i,'early_blit'):
                i.early_blit()
        enemies.spawned_loot.draw(self.canvas)
        boss.player1pos=(scyman.x,scyman.y)
        boss.spawned_loot.draw(self.canvas)
        scyman.update(P1,Time.delta())
        for i in scarecrows:
            i.update(self.canvas,scyman,Time.delta())
        structures.draw(self.canvas)
        screen.blit(self.canvas,(self.canvas_movement()))
        scyman.update_gui(screen,self)
        for event in game.events:
            comfunc.quit(event)
            if event.type==JOYBUTTONDOWN:
                if 'player_menu' not in self.aux_state:
                        if P1.get_button(6):
                            self.aux_state.append('player_menu')
                if event.__dict__['button']==7:
                    game.events.remove(event)
                    self.pause()

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
        if not self.game_over_loaded:
            self.game_over_loaded=True
            self.game_over_buttons_reset=False
            self.game_over_time=Time.Period()
            self.alpha=255
            self.game_over_blur=0

        comfunc.clean_list(self.aux_state,'player_menu')
        screen.blit(back_ground,(0,0))
        if self.alpha>0:
            self.game_over_blur+=int((Time.game_clock()-scyman.time_of_death)*.75)
            for i in scarecrows:
                i.update(self.canvas,scyman,Time.delta())
            structures.draw(self.canvas)
            screen.blit(self.canvas,(self.canvas_movement()))
            scyman.update_gui(screen,self)
            self.blur=screen.copy().convert_alpha()
            self.blur=comfunc.surf_blur(self.blur,min(self.game_over_blur,10))
        screen.fill(DEEP_RED)
        for event in game.events:
            comfunc.quit(event)
            if event.type==JOYBUTTONDOWN:
                if self.game_over_buttons_reset==False:
                    self.game_over_buttons_reset=True
                else:
                    self.reset()
            if event.type==JOYBUTTONUP:
                if self.game_over_buttons_reset==False:
                    self.game_over_buttons_reset=True
                else:
                    self.reset()
            if event.type==MOUSEBUTTONDOWN:
                self.reset()
        self.blur.set_alpha(self.alpha)
        screen.blit(self.blur,(0,0))
        self.alpha-=self.game_over_blur*.75
        screen.blit(game_over_text.text_obj,((screen_width/2 -game_over_text.text_obj.get_width()/2,screen_height/4 -game_over_text.text_obj.get_height()/2)))
        if self.game_over_time.age(3.75):
            screen.blit(press_start_text.text_obj,(screen_width/2 -press_start_text.
            text_obj.get_width()/2,screen_height/2 -press_start_text.text_obj.get_height()/2))
            press_start_text.shrink_pop(100)

    def reset(self):
        global scyman
        scyman=player.PlayerOne(0,0)
        enemies.player=scyman
        self.level_loaded=False
        self.focus='main'
        self.game_over_loaded=False

    def save_game(self):
        player_data={
            1:[i.io_name for i in scyman.relics],
            2:[i.io_name for i in scyman.armor],
            3:[i.io_name for i in scyman.weapons],
            4:[i.io_name for i in scyman.tools]
        }
        # for i in scyman.relics:
        #     player_data[1].append(i.io_name)
        # for i in scyman.armor:
        #     player_data[2].append(i.io_name)
        # for i in scyman.weapons:
        #     player_data[3].append(i.io_name)
        # for i in scyman.tools:
        #     player_data[4].append(i.io_name)
        equipment_data={
            1:[i.io_name for i in equip.equip]
        }
        # for i in equip.equip:
        #     equipment_data[1].append(i.io_name)
        enemy_data={
        }
        for index,i in enumerate(enemies.spawned_loot,start=1):
            name=i.io_name
            enemy_data[index]=name
        game_data={
            1:self.current_level
        }
        data_archive={
            1:player_data,
            2:equipment_data,
            3:enemy_data,
            4:game_data
        }
        dio.save(data_archive,self.save_slot)

    def load_game(self):
        try:
            data_archive=dio.load(self.save_slot)
            player_data,equipment_data,enemy_data,game_data=data_archive[1],data_archive[2],data_archive[3],data_archive[4]
            #player data
            for i in player_data[1]:
                relic=eval(f'equip.{i}()')
                scyman.relics.append(relic)
            for i in player_data[2]:
                armor=eval(f'equip.{i}()')
                scyman.armor.append(armor)
            for i in player_data[3]:
                weapon=eval(f'equip.{i}()')
                scyman.weapons.append(weapon)
            for i in player_data[4]:
                tool=eval(f'equip.{i}()')
                scyman.tools.append(tool)
            #equip data
            for i in equipment_data[1]:
                equipment=eval(f'equip.{i}()')
                equip.equip.append(equipment)
            #enemy data
            for i in enemy_data.values():
                loot=eval(f'equip.{i}()')
                enemies.spawned_loot.add(loot)
            #game data
            self.current_level=game_data[1]
        except TypeError:
            self.save_game()

    def focus_switch(self):
        if self.focus == 'start':
            self.start_screen()
        elif self.focus == 'main':
            self.main_menu()
        elif self.focus == 'save_select':
            self.save_select()
        elif self.focus == 'play':
            self.game_play()
        elif self.focus=='gameover':
            self.game_over()
        elif self.focus=='map_loader':
            self.map_loader()
        elif self.focus=='pause':
            self.pause()
        else:
            raise ValueError(f'Invalid GameElements.focus set: "{self.focus}"')

    def auxillary(self):
        if 'player_menu' in self.aux_state:
            self.player_menu()

game = GameElements(canvas)
player.game=game
enemies.game=game
boss.game=game
player.canvas=game.canvas
enemies.canvas=game.canvas
boss.canvas=game.canvas
delta_ref=time.time()
while True:
    game.events=pygame.event.get()
    clock.tick(60)
    Time.update()
    game.focus_switch()
    game.auxillary()
    pygame.display.flip()