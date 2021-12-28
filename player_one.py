from pygame.constants import JOYBUTTONDOWN
import pygame,time,math

from pygame.sprite import collide_mask
import common_functions as comfunc
import enemies,equip
from color_palette import *
import controller as con
screen=None#variable overwritten in main to allow blit access from this module
canvas=None#variable overwritten in main to allow blit access from this module
scarecrows=None#variable overwritten in main to add enemy access here
attacks=[]
enemies.attacks=attacks
class PlayerOne(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y):
        super().__init__()
        self.list_init()
        self.hp=100
        self.hp_ratio=960/self.hp
        self.hp_regen=0
        self.hp_drain_length=100
        self.drain_ratio=960/self.hp_drain_length
        self.recieved_damage=False
        self.invulnerable=False
        self.mp=100
        self.mp_ratio=960/self.mp
        self.defense=0
        self.shield=1  #percent of damage allowed through   1==100%
        self.incoming_damage_tracked=False
        self.incoming_damage=[]
        self.focus = 'traverse'
        self.animating=False
        self.direction='right'
        self.right_blocked,self.left_blocked=False,False
        self.down_blocked,self.up_blocked=False,False
        self.image_loader()
        self.current_sprite=0
        self.image=self.walkrightsprites[self.current_sprite]
        self.positionx=pos_x
        self.positiony=pos_y
        self.rect=self.image.get_rect()
        self.animate_speed=.09
        self.speed=180
        self.blink_distance=90
        self.blink_step_cooldown=.5
        self.blink_mp_cost=0
        self.blink_time_ref=time.time()
        self.blink_start=time.time()
        self.scythe_angle=45
        self.scythe_time_ref=time.time()
        self.slash_time_ref=time.time()
        self.slash_cooldown=.8
        self.scythe_attack=2
        self.scythe_attack_flag=[0,0]
        self.mask=pygame.mask.from_surface(self.image)
        self.relic_cool_down=time.time()
        self.active_relic=equip.FakeRelic()
        self.scythe=self.Scythe(self.scythe_image,self.rect.center)
        self.hitlag=False
        self.blinked_lynx_flag=False
        self.blinked_lynx_flag2=False
        
    class Scythe(equip.Equipment):
        def __init__(self, image,origin):
            super().__init__(image)
            self.speed=150
            self.origin=origin
            self.image=image
            self.original_image=image
            self.life_time=time.time()+2
            self.rotated_image=image
            self.velocity_x=0
            self.velocity_y=0

    def image_loader(self):
        self.d_pad=pygame.image.load(r'media\gui\dpad\dpad_neutral.png')
        self.d_pad_up=pygame.image.load(r'media\gui\dpad\dpad_up.png')
        self.d_pad_up_right=pygame.image.load(r'media\gui\dpad\dpad_upright.png')
        self.d_pad_right=pygame.image.load(r'media\gui\dpad\dpad_right.png')
        self.d_pad_down_right=pygame.image.load(r'media\gui\dpad\dpad_downright.png')
        self.d_pad_down=pygame.image.load(r'media\gui\dpad\dpad_down.png')
        self.d_pad_down_left=pygame.image.load(r'media\gui\dpad\dpad_downleft.png')
        self.d_pad_left=pygame.image.load(r'media\gui\dpad\dpad_left.png')
        self.d_pad_up_left=pygame.image.load(r'media\gui\dpad\dpad_upleft.png')
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk0.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk1.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk2.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk3.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk0.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk1.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk0.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk2.png'))
        self.blinkrightsprites.append(pygame.image.load('media\scyman_walk\\blink\\rightblink1.png'))
        self.blinkleftsprites.append(pygame.image.load('media\scyman_walk\\blink\leftblink2.png'))
        self.blinkdownsprites.append(pygame.image.load(r'media\scyman_walk\blink\downblink.png'))
        self.blinkupsprites.append(pygame.image.load(r'media\scyman_walk\blink\upblink.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk1.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk2.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown0.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown1.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown2.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown3.png'))
        self.scythe_image=pygame.image.load(r'media\player_equip\wooden_scythe.png')
        self.scytheright=pygame.transform.rotozoom(self.scythe_image,-90,1)
        self.scytherightup=pygame.transform.rotozoom(self.scythe_image,-45,1)
        self.scytherightdown=pygame.transform.rotozoom(self.scythe_image,-135,1)
        self.scytheleft=pygame.transform.rotozoom(self.scythe_image,90,1)
        self.scytheleftup=pygame.transform.rotozoom(self.scythe_image,45,1)
        self.scytheleftdown=pygame.transform.rotozoom(self.scythe_image,135,1)
        self.scythedown=pygame.transform.rotozoom(self.scythe_image,180,1)
        self.scytheup=self.scythe_image.copy()
        self.mask_scytheright=pygame.mask.from_surface(self.scytheright)
        self.mask_scytherightup=pygame.mask.from_surface(self.scytherightup)
        self.mask_scytherightdown=pygame.mask.from_surface(self.scytherightdown)
        self.mask_scytheleft=pygame.mask.from_surface(self.scytheleft)
        self.mask_scytheleftup=pygame.mask.from_surface(self.scytheleftup)
        self.mask_scytheleftdown=pygame.mask.from_surface(self.scytheleftdown)
        self.mask_scythedown=pygame.mask.from_surface(self.scythedown)
        self.mask_scytheup=pygame.mask.from_surface(self.scytheup)

    def list_init(self):
        self.interactables=[]
        self.picked_up_items=[]
        self.relics=[equip.Testudinidae_relic,equip.Felidae_relic,equip.Panthera_relic]#equip.vulpes_relic,equip.Mephitidae_relic,equip.aeetus_relic,equip.Ursidae_relic,
       # equip.Panthera_relic
        self.armor=[]
        self.weapons=[]
        self.tools=[]
        self.aux_state=[]
        self.enemies_hit=[]
        self.walkrightsprites =[]
        self.walkleftsprites =[]
        self.walkdownsprites =[]
        self.walkupsprites =[]
        self.blinkrightsprites =[]
        self.blinkleftsprites =[]
        self.blinkdownsprites=[]
        self.blinkupsprites=[]

    def interact(self):
        for i in self.interactables:
            self.picked_up_items.append(i)
        pygame.sprite.spritecollide(self,enemies.spawned_loot,True)
        self.item_sorter()

    def item_sorter(self):
        for i in self.picked_up_items:
            if isinstance(i,equip.Relic):
                self.relics.append(i)
                self.picked_up_items.remove(i)
            if isinstance(i,equip.Armor):
                self.armor.append(i)
                self.picked_up_items.remove(i)
            if isinstance(i,equip.Weapon):
                self.weapons.append(i)
                self.picked_up_items.remove(i)
            if isinstance(i,equip.Tool):
                self.tools.append(i)
                self.picked_up_items.remove(i)

    def collide(self):
        collision_tolerence=5
        self.rect=pygame.Rect(self.positionx,self.positiony,self.image.get_width(),self.image.get_height())
        #screen boundaries
        if self.positionx<32:
            self.positionx=32
        if self.positionx>2936:
            self.positionx=2936
        if self.positiony<32:
            self.positiony=32
        if self.positiony>1436:
            self.positiony=1436
       #collision between player and enemies
        for i in scarecrows:
            if self.rect.colliderect(i):
                if abs(i.rect.left-self.rect.right)<collision_tolerence:
                    self.right_blocked=True
                if abs(i.rect.right-self.rect.left)<collision_tolerence:
                    self.left_blocked=True
                if abs(i.rect.top-self.rect.bottom)<collision_tolerence:
                    self.bottom_blocked=True
                if abs(i.rect.bottom-self.rect.top)<collision_tolerence:
                    self.top_blocked=True
        #collision between player and equipment
        self.interactables.clear()
        for i in pygame.sprite.spritecollide(self,enemies.spawned_loot,False):
            self.interactables.append(i)
  
    def animate_switch(self):
        self.animating=True   
  
    def traverse_animate(self):
        if self.direction=='right':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.walkrightsprites):
                    self.current_sprite=0
                self.animating=False
            self.image=self.walkrightsprites[int(self.current_sprite)]
        if self.direction=='left':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.walkleftsprites):
                    self.current_sprite=0
                self.animating=False
            self.image=self.walkleftsprites[int(self.current_sprite)]
        if self.direction=='up':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.walkupsprites):
                    self.current_sprite=0
                self.animating=False
            self.image=self.walkupsprites[int(self.current_sprite)]
        if self.direction=='down':
            if self.animating==True:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.walkdownsprites):
                    self.current_sprite=0
                self.animating=False
            self.image=self.walkdownsprites[int(self.current_sprite)]
  
    def blink_ghost(self):
        if self.blinked_lynx_flag==False and self.blinked_lynx_flag2==False:
            self.blinked_lynx_flag=True
            self.blinked_lynx_flag2=True
        if self.blink_start>time.time()-.25:
            self.ghost.set_alpha(50)
            self.ghost_trail=self.image.copy()
            self.ghost_trail.set_alpha(150)
            canvas.blit(self.ghost,self.ghostpos)
            canvas.blit(self.ghost_trail,(((self.blink_startposx+self.positionx)/2),((self.blink_startposy+self.positiony)/2)))
        else:
            self.blinked_lynx_flag2=False
            self.aux_state.remove('blink')
  
    def blink_animate(self,direction):
        self.ghostpos=(self.positionx,self.positiony)
        self.ghost=self.image.copy()
        self.aux_state.append('blink')
        if self.animating==True:
            if direction=='right':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkrightsprites):
                    self.current_sprite=0
                    self.animating=False
                self.image=self.blinkrightsprites[int(self.current_sprite)]
            elif direction=='left':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkleftsprites):
                    self.current_sprite=0
                    self.animating=False
                self.image=self.blinkleftsprites[int(self.current_sprite)]
            if direction=='down':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkdownsprites):
                    self.current_sprite=0
                    self.animating=False
                self.image=self.blinkdownsprites[int(self.current_sprite)]
            if direction=='up':
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.blinkupsprites):
                    self.current_sprite=0
                    self.animating=False
                self.image=self.blinkupsprites[int(self.current_sprite)]
        else:
            self.image=self.walkrightsprites[int(self.current_sprite)]
        self.blink_ghost()

    def health_bar(self):
        if self.hp>100:
            self.hp=100
        if self.hp<100:
            self.hp+=self.hp_regen
        if self.recieved_damage:
            self.hp_drain_length=self.hp_before_damage
            self.recieved_damage=False
        if self.hp_drain_length>self.hp:
            self.hp_drain_length-=.15
        drain=pygame.Rect(20,480,self.hp_drain_length*self.drain_ratio,3)
        outline=pygame.Rect(19,479,962,5)
        health=pygame.Rect(20,480,self.hp*self.hp_ratio,3)
        missing_health=pygame.Rect(20,480,960,3)
        pygame.draw.rect(screen,WHITE,outline,0,1)
        pygame.draw.rect(screen,DARK_RED,missing_health,0,1)
        pygame.draw.rect(screen,RED,drain,0,1)
        pygame.draw.rect(screen,GREEN,health,0,1)

    def mana_bar(self):
        mana_regen=.1
        if self.mp>100:
            self.mp=100
        if self.mp < 100:
            self.mp+=mana_regen
        outline=pygame.Rect(19,473,962,5)
        mana=pygame.Rect(20,474,self.mp*self.mp_ratio,3)
        missing_mana=pygame.Rect(20,474,960,3)
        pygame.draw.rect(screen,WHITE,outline,0,1)
        pygame.draw.rect(screen,PURPLE,missing_mana,0,1)
        pygame.draw.rect(screen,BABY_BLUE,mana,0,1)

    def damage(self):
        for i in attacks:
            if i[1].colliderect(self.rect):
                if self.incoming_damage_tracked:
                    self.incoming_damage.append(i[0])
                self.hp_before_damage=self.hp
                self.hp-=max(0,((i[0]-self.defense)*self.shield))
                self.hp_lost=abs(self.hp_before_damage-self.hp)
                self.recieved_damage=True
            comfunc.clean_list(attacks,i)

    def traverse(self,P1,delta):
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)
        directions=['up','right','down','left']
        angle=con.joy_angle(P1,(0,1))% 360
        up=0
        right=90
        down=180
        left=270
        if math.isclose(up, angle, abs_tol = 45):
            self.direction='up'
        if math.isclose(right, angle, abs_tol = 45):
            self.direction='right'
        if math.isclose(down, angle, abs_tol = 45):
            self.direction='down'
        if math.isclose(left, angle, abs_tol = 45):
            self.direction='left'
        if not comfunc.dead_zone(P1,(0,1)):
            self.animate_switch()
            self.traverse_animate()
            if motionx>0 and not self.right_blocked:
                self.positionx+=(self.speed*delta)*P1.get_axis(0)
            if motionx<0 and not self.left_blocked:
                self.positionx+=(self.speed*delta)*P1.get_axis(0)
            if motiony>0 and not self.bottom_blocked:
                self.positiony+=(self.speed*delta)*P1.get_axis(1)
            if motiony<0 and not self.top_blocked:
                self.positiony+=(self.speed*delta)*P1.get_axis(1)
            self.rect.center=(self.positionx+self.image.get_width()/2,
            self.positiony+self.image.get_height()/2)
        self.right_blocked,self.left_blocked,self.bottom_blocked,self.top_blocked=False,False,False,False
  
    def blink_step(self,P1):
        self.blink_startposx=self.positionx
        self.blink_startposy=self.positiony
        self.focus='traverse'
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)
        self.animating=True
        if motionx>.5:
            self.blink_start=time.time()
            self.blink_animate('right')
            if motiony>.5:
                self.positionx+=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            elif motiony<-.5:
                self.positionx+=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            else:
                self.positionx+=self.blink_distance
        elif motionx<-.5:
            self.blink_start=time.time()
            self.blink_animate('left')
            if motiony>.5:
                self.positionx-=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            elif motiony<-.5:
                self.positionx-=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            else:
                self.positionx-=self.blink_distance
        elif motiony>.5:
            self.blink_start=time.time()
            self.blink_animate('down')
            if motionx>.5:
                self.positionx+=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            elif motionx<-.5:
                self.positionx-=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            else:
                self.positiony+=self.blink_distance
        elif motiony<-.5:
            self.blink_start=time.time()
            self.blink_animate('up')
            if motionx>.5:
                self.positionx+=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            elif motionx<-.5:
                self.positionx-=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            else:
                self.positiony-=self.blink_distance
  
    def scythe_slash(self,P1):
        self.aux_state.append('scythe')
        self.focus='traverse'
        self.scythe_time_ref=time.time()
  
    def scythe_animate(self,P1):
        time_stamp=time.time()
        
        if time_stamp<self.scythe_time_ref+.2:

            scythe,position=comfunc.pivot(self.scythe.original_image,self.rect.center,
            (16,42),con.joy_angle(P1,(0,1)))
            self.scythe.image=scythe
            self.scythe.rect=position
            self.scythe.mask=pygame.mask.from_surface(scythe)
            canvas.blit(self.scythe.image,self.scythe.rect)
            hit_list=pygame.sprite.spritecollide(self.scythe,scarecrows,False,collide_mask)
            if hit_list:
                self.hitlag=True
         
            if self.scythe_attack_flag[0]==0:
                self.scythe_attack_flag[0]=1
                for i in hit_list:
                    i.damage(self.scythe_attack)
        elif time_stamp<self.scythe_time_ref+.5:
            if 'scythe_twist' not in self.aux_state:
                self.aux_state.append('scythe_twist')
                self.scythe_radius=0
            self.scythe_radius+=20
            scythe,position=comfunc.pivot(self.scythe.original_image,self.rect.center,
            (16,42),con.joy_angle(P1,(0,1))-self.scythe_radius)
            self.scythe.image=scythe
            self.scythe.rect=position
            self.scythe.mask=pygame.mask.from_surface(scythe)
            canvas.blit(self.scythe.image,self.scythe.rect)
            hit_list=pygame.sprite.spritecollide(self.scythe,scarecrows,False,collide_mask)
            if hit_list:
                self.hitlag=True
            if self.scythe_radius==100 or 180 or 280:
                self.scythe_attack_flag[1]=0
            if self.scythe_attack_flag[1]==0:
                self.scythe_attack_flag[1]=1
                for i in hit_list:
                    i.damage(self.scythe_attack*3)
        else:
                comfunc.clean_list(self.aux_state,'scythe')
                comfunc.clean_list(self.aux_state,'scythe_twist')
                self.scythe_time_ref=time_stamp
                self.scythe_attack_flag=[0,0]
        # if self.direction=='right':
        #     if time_stamp<self.scythe_time_ref+.2:
        #         screen.blit(self.scytheright,(self.rect.right-10,self.rect.center[1]-(self.scythe.get_height()/3)))
        #         hit_list=pygame.sprite.spritecollide(self,scarecrows,False)
        #         if self.scythe_attack_flag[0]==0:
        #             self.scythe_attack_flag[0]=1
        #             for i in hit_list:
        #                 i.damage(self.scythe_attack)
        #     elif time_stamp<self.scythe_time_ref+.5:
        #         screen.blit(self.scytherightup,(self.rect.right-15,self.rect.center[1]-(self.scythe.get_height()*.90)))
        #         hit_list=pygame.sprite.spritecollide(self,scarecrows,False)
        #         if self.scythe_attack_flag[1]==0:
        #             self.scythe_attack_flag[1]=1
        #             for i in hit_list:
        #                 i.damage(self.scythe_attack*3)
        #     else:
        #         comfunc.clean_list(self.aux_state,'scythe')
        #         self.scythe_time_ref=time_stamp
        #         self.scythe_attack_flag=[0,0]
        # elif self.direction=='left':
        #     if time_stamp<self.scythe_time_ref+.2:
        #         screen.blit(self.scytheleft,(self.rect.left-self.scythe.get_width()+5,self.rect.center[1]-(self.scythe.get_height()/1.75)))
        #         hit_list=pygame.sprite.spritecollide(self,scarecrows,False)
        #         if self.scythe_attack_flag[0]==0:
        #             self.scythe_attack_flag[0]=1
        #             for i in hit_list:
        #                 i.damage(self.scythe_attack)
        #     elif time_stamp<self.scythe_time_ref+.5:
        #         screen.blit(self.scytheleftdown,(self.rect.left-self.scythe.get_width(),self.rect.center[1]-(self.scythe.get_height()*.4)))
        #         hit_list=pygame.sprite.spritecollide(self,scarecrows,False)
        #         if self.scythe_attack_flag[1]==0:
        #             self.scythe_attack_flag[1]=1
        #             for i in hit_list:
        #                 i.damage(self.scythe_attack*3)
        #     else:
        #         comfunc.clean_list(self.aux_state,'scythe')
        #         self.scythe_time_ref=time_stamp
        #         self.scythe_attack_flag=[0,0]
        # elif self.direction=='down':
        #     if time_stamp<self.scythe_time_ref+.2:
        #         screen.blit(self.scythedown,(self.rect.center[0]-(self.scythe.get_width()*.6),self.rect.bottom-6))
        #         hit_list=pygame.sprite.spritecollide(self,scarecrows,False)
        #         if self.scythe_attack_flag[0]==0:
        #             self.scythe_attack_flag[0]=1
        #             for i in hit_list:
        #                 i.damage(self.scythe_attack)
        #     elif time_stamp<self.scythe_time_ref+.5:
        #         screen.blit(self.scytherightdown,(self.rect.center[0]-(self.scythe.get_width()*.45),self.rect.bottom-15))
        #         hit_list=pygame.sprite.spritecollide(self,scarecrows,False)
        #         if self.scythe_attack_flag[1]==0:
        #             self.scythe_attack_flag[1]=1
        #             for i in hit_list:
        #                 i.damage(self.scythe_attack*3)
        #     else:
        #         comfunc.clean_list(self.aux_state,'scythe')
        #         self.scythe_time_ref=time_stamp
        #         self.scythe_attack_flag=[0,0]
        # elif self.direction=='up':
        #     if time_stamp<self.scythe_time_ref+.2:
        #         screen.blit(self.scytheup,(self.rect.center[0]-(self.scythe.get_width()*.35),self.rect.top-self.scythe.get_height()+4))
        #         hit_list=pygame.sprite.spritecollide(self,scarecrows,False)
        #         if self.scythe_attack_flag[0]==0:
        #             self.scythe_attack_flag[0]=1
        #             for i in hit_list:
        #                 i.damage(self.scythe_attack)
        #     elif time_stamp<self.scythe_time_ref+.5:
        #         screen.blit(self.scytheleftup,(self.rect.center[0]-(self.
        #         scythe.get_width()*.9),self.rect.top-self.scythe.get_height()+2))
        #         hit_list=pygame.sprite.spritecollide(self,scarecrows,False)
        #         if self.scythe_attack_flag[1]==0:
        #             self.scythe_attack_flag[1]=1
        #             for i in hit_list:
        #                 i.damage(self.scythe_attack*3)
            # else:
            #     comfunc.clean_list(self.aux_state,'scythe')
            #     self.scythe_time_ref=time_stamp
            #     self.scythe_attack_flag=[0,0]

    def relic_select(self,P1):
        if 'dpad' not in self.aux_state:
            self.aux_state.append('dpad')
            self.dpad_timestamp=time.time()+.5
        elif self.dpad_timestamp>time.time():
            relic=self.relics
            try:
                canvas.blit(relic[0].transparent,(self.positionx-self.relics[0].rect[2],
                self.positiony))#left
            except IndexError:
                pass
            try:
                canvas.blit(relic[1].transparent,(self.positionx,
                self.positiony-self.relics[0].rect[3]))#up
            except IndexError:
                pass
            try:
                canvas.blit(relic[2].transparent,(self.positionx+32,
                self.positiony))#right
            except IndexError:
                pass
            try:
                canvas.blit(relic[3].transparent,(self.positionx,
                self.positiony+32))#down
            except IndexError:
                pass
            try:
                canvas.blit(relic[4].transparent,(self.positionx-self.relics[0].rect[2],
                self.positiony-self.relics[0].rect[3]))#upleft
            except IndexError:
                pass
            try:
                canvas.blit(relic[5].transparent,(self.positionx+32,
                self.positiony-self.relics[5].rect[3]))#upright
            except IndexError:
                pass
            try:
                canvas.blit(relic[7].transparent,(self.positionx-self.relics[0].rect[2],
                self.positiony+32))#downleft
            except IndexError:
                pass
            try:
                canvas.blit(relic[6].transparent,(self.positionx+32,
                self.positiony+32))#downright
            except IndexError:
                pass
        ##########controls##########
            cool_down=.75
            if P1.get_hat(0) == (0,0):
                canvas.blit(self.d_pad,self.rect.topleft)#neutral dpad
            elif P1.get_hat(0) == (0,1):
                canvas.blit(self.d_pad_up,self.rect.topleft)
                try:
                    canvas.blit(relic[1].image,(self.positionx,
                    self.positiony-self.relics[0].rect[3]))#up
                    if P1.get_button(4):
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=time.time()+cool_down
                        self.stat_archive()
                        self.activate_relic(1)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (1,1):
                canvas.blit(self.d_pad_up_right,self.rect.topleft)
                try:
                    canvas.blit(relic[5].image,(self.positionx+32,
                    self.positiony-self.relics[5].rect[3]))#upright
                    if P1.get_button(4):
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=time.time()+cool_down
                        self.stat_archive()
                        self.activate_relic(5)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (1,0):
                canvas.blit(self.d_pad_right,self.rect.topleft)
                try:
                    canvas.blit(relic[2].image,(self.positionx+32,
                    self.positiony))#right
                    if P1.get_button(4):
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=time.time()+cool_down
                        self.stat_archive()
                        self.activate_relic(2)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (1,-1):
                canvas.blit(self.d_pad_down_right,self.rect.topleft)
                try:
                    canvas.blit(relic[6].image,(self.positionx+32,
                    self.positiony+32))#downright
                    if P1.get_button(4):
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=time.time()+cool_down
                        self.stat_archive()
                        self.activate_relic(6)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (0,-1):
                canvas.blit(self.d_pad_down,self.rect.topleft)
                try:
                    canvas.blit(relic[3].image,(self.positionx,
                    self.positiony+32))#down
                    if P1.get_button(4):
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=time.time()+cool_down
                        self.stat_archive()
                        self.activate_relic(3)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (-1,-1):
                canvas.blit(self.d_pad_down_left,self.rect.topleft)
                try:
                    canvas.blit(relic[7].image,(self.positionx-self.relics[0].rect[2],
                    self.positiony+32))#downleft
                    if P1.get_button(4):
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=time.time()+cool_down
                        self.stat_archive()
                        self.activate_relic(7)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (-1,0):
                canvas.blit(self.d_pad_left,self.rect.topleft)
                try:
                    canvas.blit(relic[0].image,(self.positionx-self.relics[0].rect[2],
                    self.positiony))
                    if P1.get_button(4):
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=time.time()+cool_down
                        self.stat_archive()
                        self.activate_relic(0)
                except IndexError:
                    pass
            elif P1.get_hat(0) == (-1,1):
                canvas.blit(self.d_pad_up_left,self.rect.topleft)
                try:
                    canvas.blit(relic[4].image,(self.positionx-self.relics[0].rect[2],
                    self.positiony-self.relics[0].rect[3]))#upleft
                    if P1.get_button(4):
                        self.aux_state.append('relic')
                        comfunc.clean_list(self.aux_state,'dpad')
                        self.relic_activation_cool_down=time.time()+cool_down
                        self.stat_archive()
                        self.activate_relic(4)
                except IndexError:
                    pass
        else:
            comfunc.clean_list(self.aux_state,'dpad')
   
    def activate_relic(self,relic_index):
        relic=self.relics[relic_index]
        self.active_relic=relic
        self.activated_relic=relic_index
        self.defense=relic.defense
        self.speed=relic.speed
        self.scythe_attack=relic.scythe_attack
        self.hp_regen=relic.hp_regen
        self.attack=relic.attack

        self.walkrightsprites.clear()
        self.walkleftsprites.clear()
        self.walkupsprites.clear()
        self.walkdownsprites.clear()
        self.current_sprite=0
        self.image=relic.shape_shifted
        self.walkrightsprites.append(pygame.image.load(relic.walk_right_load()))
        self.walkleftsprites.append(pygame.image.load(relic.walk_left_load()))
        self.walkupsprites.append(pygame.image.load(relic.walk_up_load()))
        self.walkdownsprites.append(pygame.image.load(relic.walk_down_load()))

    def relic_effects(self,delta,relic_index,P1):
        relic=self.relics[relic_index]
        relic.rect.center=self.rect.center
        self.mp-=relic.mana_drain
        if P1.get_button(2):
            hits=pygame.sprite.spritecollide(self,scarecrows,False)
            if hits:
                self.hitlag=True
            relic.attack(canvas,hits,self,P1)
        if P1.get_button(1):
            relic.special_attack(canvas,self)

        if not comfunc.dead_zone(P1,(3,4)):
            relic.right_stick(delta,self,P1)

        
        if self.mp<-5:
            self.mp=0
            self.deactivate_relic()
        elif self.mp<1:
            self.mp-=.5  
         
    def stat_archive(self):
        self.defense_archive=self.defense
        self.speed_archive=self.speed
        self.scythe_attack_archive=self.scythe_attack
        self.hp_regen_archive=self.hp_regen

    def deactivate_relic(self):
        self.defense=self.defense_archive
        self.speed=self.speed_archive
        self.scythe_attack=self.scythe_attack_archive
        self.hp_regen=self.hp_regen_archive
        self.active_relic=equip.FakeRelic()
        comfunc.clean_list(self.aux_state,'relic')
        self.walkrightsprites.clear()
        self.walkleftsprites.clear()
        self.walkupsprites.clear()
        self.walkdownsprites.clear()
        self.current_sprite=0

        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk0.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk1.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk2.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk3.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk0.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk1.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk0.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk2.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk1.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk2.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown0.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown1.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown2.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown3.png'))
        self.image=self.walkdownsprites[0]
   
    def action(self,P1):
        time_stamp=time.time()
        if P1.get_button(1):
            pass
        if P1.get_button(0):
            if time_stamp>self.blink_time_ref:
                if self.mp>=self.blink_mp_cost:
                    self.mp-=self.blink_mp_cost
                    self.blink_time_ref=time_stamp+self.blink_step_cooldown
                    self.focus ='blink'
        if P1.get_button(2) and 'relic' not in self.aux_state:
                if time_stamp>self.slash_time_ref:
                    self.slash_time_ref=time_stamp+self.slash_cooldown
                    self.focus='slash'
        if P1.get_button(4):
            if 'relic' in self.aux_state:
                if time_stamp>self.relic_activation_cool_down:
                    self.deactivate_relic()
                    self.relic_cool_down=time.time()+.5
        if P1.get_button(3):
            self.interact()
        if P1.get_hat(0)[0] or P1.get_hat(0)[1]:
            if 'relic' in self.aux_state:
                pass
            else:
                if time_stamp>self.relic_cool_down:
                    self.dpad_timestamp=time.time()+.5
                    self.relic_select(P1)

    def draw(self):
        canvas.blit(self.image,(self.positionx,self.positiony))

    def focus_switch(self,P1,delta):
        self.traverse(P1,delta)
        
        if self.focus =='blink':
            self.blink_step(P1)
        elif self.focus=='slash':
            self.scythe_slash(P1)
  
    def auxillary(self,P1,delta):
        if 'blink' in self.aux_state:
            self.blink_ghost()
        if 'scythe' in self.aux_state:
            self.scythe_animate(P1)
        if 'relic' in self.aux_state:
            self.relic_effects(delta,self.activated_relic,P1)
        if not self.invulnerable:
            self.damage()
        else:
            for i in attacks:
                comfunc.clean_list(attacks,i)
        for i in self.relics:
            i.passives(canvas,scarecrows,self,P1)
        self.draw()
        if 'dpad' in self.aux_state:
            self.relic_select(P1)
        self.collide()
        
        # self.health_bar()
        # self.mana_bar()

    def update_gui(self):
        self.health_bar()
        self.mana_bar()    
         
    def update(self,P1,delta):
        if 'blockade' not in self.aux_state:
            self.focus_switch(P1,delta)
        self.action(P1)
        self.auxillary(P1,delta)