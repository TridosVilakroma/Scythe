from color_palette import *
import pygame,time,math,equip,particles
from random import randint
import common_functions as comfunc

screen=None
enemies=[]
player1pos=None
attacks=[]
spawned_loot=pygame.sprite.Group()

class Scarecrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('media\deco\scarecrow.png').convert_alpha()
        self.x=randint(0,968)
        self.y=randint(0,468)
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
        self.pos=pygame.math.Vector2((self.rect.center))
        self.hp = (randint(10,25)+75)
        self.hp_ratio=self.rect.width/self.hp
        self.defense = 0#randint(0,3)
        self.damage_ref_timer=time.time()
        self.hpbar_ref_timer=time.time()
        self.aux_state=[]
        self.timer_wheel_step=0
        self.image_loader()
        self.mask=pygame.mask.from_surface(self.image)
        
   
    def image_loader(self):
        self.trap_net=pygame.image.load(r'media\relics\fox\fox_net.png').convert_alpha()
        self.timer_wheel_img=[]
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl00.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl01.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl02.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl03.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl04.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl05.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl06.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl07.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl08.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl09.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl10.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl11.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl12.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl13.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl14.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl15.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl16.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl17.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl18.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl19.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl20.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl21.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl22.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl23.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl24.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl25.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl26.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl27.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl28.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl29.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl30.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl31.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl32.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl33.png'))
        self.small_straw=pygame.image.load(r'media\deco\small_straw.png')
        self.straw_stalk=pygame.image.load(r'media\deco\straw_stalk.png')
   
    def loot_dropper(self):
        random_loot=randint(1,5)
        try:
            equip.equip_matrix[1][random_loot].rect[0]=self.x
            equip.equip_matrix[1][random_loot].rect[1]=self.y
            spawned_loot.add(equip.equip_matrix[1][random_loot])
            popped=equip.equip_matrix[1].pop(random_loot)
            print(popped)
        except KeyError:
            print('loot_dropper_error')
            pass
            
    def collision_check(self):
        pass
   
    def damage(self,damage):
        self.hp-=max(0,damage-self.defense)
        if self.hp<0:
            self.hp=0
        self.aux_state.append('health')
        self.aux_state.append('timerwheel')
        self.hpbar_ref_timer=time.time()+3
        self.health_bar()
   
    def trap(self,duration):
        if 'trap' not in self.aux_state:
            self.trap_start=time.time()+duration
            self.aux_state.append('trap')
            self.trap_duration=duration
        if self.trap_start>time.time():
            screen.blit(self.trap_net,self.rect.topleft)
        else:
            comfunc.clean_list(self.aux_state,'trap')

    def stun(self,duration):
        if 'stun' not in self.aux_state:
            self.stun_start=time.time()+duration
            self.aux_state.append('stun')
            self.stun_duration=duration
            self.stun_particles=particles.ParticleEmitter(.05,(self.pos[0]-10,self.pos[0]+10),
            (self.pos[1]-20,self.pos[1]),
            [RED,PALE_YELLOW,PALE_YELLOW,PALE_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW],
            2,'burst_emit20','halo_wave',square=True)
        if self.stun_start>time.time():
            self.stun_particles.update(screen)
        else:
            comfunc.clean_list(self.aux_state,'stun')

    def bleed(self):
        if 'bleed' not in self.aux_state:
            self.bleed_start=time.time()
        self.aux_state.append('bleed')
        if self.bleed_start>time.time()-5:
            self.hp-=.05
            self.hpbar_ref_timer=time.time()+3
            self.health_bar()
        else:
            comfunc.clean_list(self.aux_state,'bleed')

    def health_bar_pop_up(self):
        self.hpbar_ref_timer=time.time()+3
        self.aux_state.append('health')
        self.health_bar()

    def health_bar(self):
        time_stamp=time.time()
        if time_stamp<self.hpbar_ref_timer:
            health_bar_thickness=3
            outline=pygame.Rect(self.rect.left-1,self.rect.top-health_bar_thickness-1,self.rect.width+2,5)
            health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.hp*self.hp_ratio,health_bar_thickness)
            missing_health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.rect.width,health_bar_thickness)
            pygame.draw.rect(screen,WHITE,outline,0,1)
            pygame.draw.rect(screen,RED,missing_health,0,1)
            pygame.draw.rect(screen,GREEN,health,0,1)
        else:
            comfunc.clean_list(self.aux_state,'health')
   
    def timer_wheel(self):
        if int(self.timer_wheel_step)<=len(self.timer_wheel_img)-1:
            screen.blit(self.timer_wheel_img[self.timer_wheel_step],self.rect.center)
            self.timer_wheel_step+=1
        else:
            self.aux_state.append('dust')
            self.dust_start=time.time()
            self.dust_pos=player1pos
            self.timer_wheel_step=0
            comfunc.clean_list(self.aux_state,'timerwheel')
   
    def dust(self):
        if self.dust_start>=time.time()-.6:
            screen.blit(self.small_straw,self.dust_pos)
            self.aux_state.append('dust_particles')
            self.dust_particles=particles.ParticleEmitter(0,
            (self.dust_pos[0]+16,self.dust_pos[0]+16),(self.dust_pos[1]+32,self.dust_pos[1]+32),
            [PALE_YELLOW,WORN_YELLOW,BRIGHT_YELLOW,BROWN],1,
            'explode_up','move_to_dest','fast_shrink','shrink')
        elif self.dust_start>=time.time()-1.2:
            screen.blit(self.straw_stalk,self.dust_pos)
            dust_rect=pygame.Rect((self.dust_pos),(32,32))
            attacks.append((.75,dust_rect))
            
        elif self.dust_start>=time.time()-1.3:
            screen.blit(self.small_straw,self.dust_pos)

        else:
            comfunc.clean_list(self.aux_state,'dust')
            comfunc.clean_list(self.aux_state,'dust_particles')

    def chain_lightning(self,screen,player):
        if 'chain' not in self.aux_state:
            self.chain_start=time.time()
            self.aux_state.append('chain')
            self.chain_pos=pygame.Vector2(self.rect.center)
            enemy_counter=0
            for i in enemies:
                if 0<i.pos.distance_to(self.chain_pos)<115:
                    enemy_counter+=1

                    i.lightning=particles.ParticleEmitter(0,(i.pos[0],self.chain_pos[0]),
                    (i.pos[1],self.chain_pos[1]),(WHITE,BLUE),1,
                    'lightning_bolt','fast_decay','shake','move_to_dest','random_growth',square=True)

                    self.lightning_implosion=particles.ParticleEmitter(0,(self.rect.center[0],self.rect.center[0]),
                    (self.rect.center[1],self.rect.center[1]),[WHITE,BLUE],1,
                    'implode','move_to_dest_fast','fast_shrink','shrink')

                    i.damage(8)
        if self.chain_start>time.time()-1.5:
            self.hp-=.25
            self.hpbar_ref_timer=time.time()+3
            self.health_bar()
            for i in enemies:
                try:
                    i.lightning.update(screen)
                    self.lightning_implosion.update(screen)
                except AttributeError:
                    pass
        else:
            comfunc.clean_list(self.aux_state,'chain')

    def vitality(self):
        if self.hp <= 0:
            self.loot_dropper()
            self.kill()
  
    def auxillary(self,screen,player):
        if 'health' in self.aux_state:
            self.health_bar()
        if 'stun' in self.aux_state:
            self.stun(self.stun_duration)
        if 'stun' not in self.aux_state:
            if 'timerwheel' in self.aux_state:
                self.timer_wheel()
        if 'dust' in self.aux_state:
            self.dust()
        if 'bleed' in self.aux_state:
            self.bleed()
        if 'chain' in self.aux_state:
            self.chain_lightning(screen,player)
        if 'trap' in self.aux_state:
            self.trap(self.trap_duration)
        if 'dust_particles' in self.aux_state:
            self.dust_particles.update(screen)
   
    def blit(self):
        screen.blit(self.image,(self.x,self.y))

    def update(self,screen,player):
        self.pos=pygame.math.Vector2((self.rect.center))
        self.blit()
        self.vitality()
        self.auxillary(screen,player)
        

class Omnivine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('media\enemies\omnivine_walk\sprite_0.png').convert_alpha()
        self.mask=pygame.mask.from_surface(self.image)
        self.x=randint(0,968)
        self.y=randint(0,468)
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
        self.pos=pygame.math.Vector2((self.rect.center))
        self.hp = randint(10,25)+50
        self.hp_ratio=self.rect.width/self.hp
        self.defense = randint(0,3)
        self.damage_ref_timer=time.time()
        self.hpbar_ref_timer=time.time()
        self.aux_state=[]
        self.timer_wheel_step=0
        self.image_loader()
        self.current_sprite=0
        self.animate_speed=.09
        self.bullet_speed=2.5
        self.chance_to_shoot=1,750 #chance is one in the second int
        self.bullet_air_time=3.25
   
    def image_loader(self):
        self.trap_net=pygame.image.load(r'media\relics\fox\fox_net.png').convert_alpha()
        self.neutral_stance= pygame.image.load('media\enemies\omnivine_walk\sprite_0.png').convert_alpha()
        self.timer_wheel_img=[]
        self.traverse_sprites=[]
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl00.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl01.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl02.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl03.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl04.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl05.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl06.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl07.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl08.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl09.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl10.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl11.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl12.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl13.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl14.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl15.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl16.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl17.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl18.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl19.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl20.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl21.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl22.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl23.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl24.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl25.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl26.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl27.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl28.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl29.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl30.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl31.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl32.png'))
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl33.png'))
        self.traverse_sprites.append(pygame.image.load(r'media\enemies\omnivine_walk\sprite_0.png'))
        self.traverse_sprites.append(pygame.image.load(r'media\enemies\omnivine_walk\sprite_1.png'))
        self.traverse_sprites.append(pygame.image.load(r'media\enemies\omnivine_walk\sprite_2.png'))
        self.traverse_sprites.append(pygame.image.load(r'media\enemies\omnivine_walk\sprite_3.png'))
        self.shoot0=pygame.image.load(r'media\enemies\ominvine_shoot\sprite_0.png')
        self.shoot1=pygame.image.load(r'media\enemies\ominvine_shoot\sprite_1.png')
        self.shoot2=pygame.image.load(r'media\enemies\ominvine_shoot\sprite_2.png')
        self.bullet=pygame.image.load(r'media\enemies\ominvine_shoot\outlined_bullet.png')
   
    def collision_check(self):
        pass
   
    def damage(self,damage):
        self.hp-=max(0,damage-self.defense)
        if self.hp<0:
            self.hp=0
        self.aux_state.append('health')
        self.aux_state.append('timerwheel')
        self.hpbar_ref_timer=time.time()+3
        self.health_bar()
    
    def trap(self,duration):
        if 'trap' not in self.aux_state:
            self.trap_start=time.time()+duration
            self.aux_state.append('trap')
            self.trap_duration=duration
        if self.trap_start>time.time():
            screen.blit(self.trap_net,self.rect.topleft)
        else:
            comfunc.clean_list(self.aux_state,'trap')

    def stun(self,duration):
        if 'stun' not in self.aux_state:
            self.stun_start=time.time()+duration
            self.aux_state.append('stun')
            self.stun_duration=duration
            self.stun_particles=particles.ParticleEmitter(.05,(self.pos[0]-10,self.pos[0]+10),
            (self.pos[1]-20,self.pos[1]),
            [RED,PALE_YELLOW,PALE_YELLOW,PALE_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW],
            2,'burst_emit20','halo_wave',square=True)
        if self.stun_start>time.time():
            self.stun_particles.update(screen)
        else:
            comfunc.clean_list(self.aux_state,'stun')

    def bleed(self):
        if 'bleed' not in self.aux_state:
            self.bleed_start=time.time()
            self.aux_state.append('bleed')
        if self.bleed_start>time.time()-5:
            self.hp-=.05
            self.hpbar_ref_timer=time.time()+3
            self.health_bar()
        else:
            comfunc.clean_list(self.aux_state,'bleed')

    def chain_lightning(self,screen,player):
        if 'chain' not in self.aux_state:
            self.chain_start=time.time()
            self.aux_state.append('chain')
            self.chain_pos=pygame.Vector2(self.rect.center)
            enemy_counter=0
            for i in enemies:
                if 0<i.pos.distance_to(self.chain_pos)<115:
                    enemy_counter+=1

                    i.lightning=particles.ParticleEmitter(0,(i.pos[0],self.chain_pos[0]),
                    (i.pos[1],self.chain_pos[1]),(WHITE,BLUE),1,
                    'lightning_bolt','fast_decay','shake','move_to_dest','random_growth',square=True)

                    self.lightning_implosion=particles.ParticleEmitter(0,(self.rect.center[0],self.rect.center[0]),
                    (self.rect.center[1],self.rect.center[1]),[WHITE,BLUE],1,
                    'implode','move_to_dest_fast','fast_shrink','shrink')

                    i.damage(8)
        if self.chain_start>time.time()-1.5:
            self.hp-=.25
            self.hpbar_ref_timer=time.time()+3
            self.health_bar()
            for i in enemies:
                try:
                    i.lightning.update(screen)
                    self.lightning_implosion.update(screen)
                except AttributeError:
                    pass
        else:
            comfunc.clean_list(self.aux_state,'chain')

    def health_bar_pop_up(self):
        self.hpbar_ref_timer=time.time()+3
        self.aux_state.append('health')
        self.health_bar()

    def health_bar(self):
        time_stamp=time.time()
        if time_stamp<self.hpbar_ref_timer:
            health_bar_thickness=3
            outline=pygame.Rect(self.rect.left-1,self.rect.top-health_bar_thickness-1,self.rect.width+2,5)
            health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.hp*self.hp_ratio,health_bar_thickness)
            missing_health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.rect.width,health_bar_thickness)
            pygame.draw.rect(screen,WHITE,outline,0,1)
            pygame.draw.rect(screen,RED,missing_health,0,1)
            pygame.draw.rect(screen,GREEN,health,0,1)
        else:
            comfunc.clean_list(self.aux_state,'health')
   
    def timer_wheel(self):
        if int(self.timer_wheel_step)<=len(self.timer_wheel_img)-1:
            screen.blit(self.timer_wheel_img[self.timer_wheel_step],self.rect.center)
            self.timer_wheel_step+=1
        else:
            self.aux_state.append('shoot')
            self.shoot_start=time.time()
            self.shoot_pos=player1pos
            self.timer_wheel_step=0
            comfunc.clean_list(self.aux_state,'timerwheel')
   
    def shoot(self):
        if self.shoot_start>=time.time()-.2:
            self.image=self.shoot0
        elif self.shoot_start>=time.time()-1.2:
            self.image=self.shoot1
        elif self.shoot_start>=time.time()-2:
            self.image=self.shoot2
            if not 'singleton' in self.aux_state:
                self.aux_state.append('bullet')
                self.aux_state.append('singleton')
        else:
            self.image=self.neutral_stance
            comfunc.clean_list(self.aux_state,'shoot')
            comfunc.clean_list(self.aux_state,'singleton')
   
    def bullet_trajectory(self):
        if 'switch' not in self.aux_state:
            self.bullet_time_stamp=time.time()+self.bullet_air_time
            self.aux_state.append('switch')
            self.bullet_origin=self.rect.center
            self.bullet_dest=player1pos
            self.bullet_pos=[self.bullet_origin[0]-self.bullet.get_width()/2,self.bullet_origin[1]-self.bullet.get_height()/2]
            self.bullet_radians=math.atan2(self.bullet_dest[1]-self.bullet_origin[1],self.bullet_dest[0]-self.bullet_origin[0])
            self.bullet_vector=(math.cos(self.bullet_radians) * self.bullet_speed,math.sin(self.bullet_radians) * self.bullet_speed)
        if 'switch' in self.aux_state:
            bullet_rect=pygame.Rect((self.bullet_pos),(32,32))
            player1_rect=pygame.Rect((player1pos),(32,32))
            attacks.append((20,bullet_rect))
            if bullet_rect.colliderect(player1_rect):
                comfunc.clean_list(self.aux_state,'switch')
                comfunc.clean_list(self.aux_state,'bullet')
                
            if self.bullet_time_stamp<time.time():
                comfunc.clean_list(self.aux_state,'switch')
                comfunc.clean_list(self.aux_state,'bullet')
        if 'switch' in self.aux_state:
            self.bullet_pos[0]+=self.bullet_vector[0]
            self.bullet_pos[1]+=self.bullet_vector[1]
            screen.blit(self.bullet,self.bullet_pos)

    def traverse(self):
        prox=(abs(player1pos[0]-self.rect.center[0]),abs(player1pos[1]-self.rect.center[1]))
        aggro_prox=200
        max_prox=50
        if prox[0]<=aggro_prox and prox[1]<=aggro_prox:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.traverse_sprites):
                    self.current_sprite=0
                self.image=self.traverse_sprites[int(self.current_sprite)]
                if 'trap' not in self.aux_state:
                    if player1pos[1]==self.y:
                        if player1pos[0]-max_prox>self.x:
                            self.x+=.5
                        elif player1pos[0]+max_prox<self.x:
                            self.x-=.5
                    if player1pos[1]!=self.y:
                        if player1pos[0]-max_prox>self.x:
                            self.x+=.375
                        elif player1pos[0]+max_prox<self.x:
                            self.x-=.375
                    if player1pos[0]==self.x:
                        if player1pos[1]-max_prox>self.y:
                            self.y+=.5
                        elif player1pos[1]+max_prox<self.y:
                            self.y-=.5
                    if player1pos[0]!=self.x:
                        if player1pos[1]-max_prox>self.y:
                            self.y+=.375
                        elif player1pos[1]+max_prox<self.y:
                            self.y-=.375
                self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())

    def vitality(self):
        if self.hp <= 0:
            self.kill()
  
    def auxillary(self,screen,player):
        if 'health' in self.aux_state:
            self.health_bar()
        if 'stun' in self.aux_state:
            self.stun(self.stun_duration)
        if 'stun' not in self.aux_state:
            if 'timerwheel' in self.aux_state:
                self.timer_wheel()
            if 'shoot' in self.aux_state:
                self.shoot()
            else:
                self.traverse()
            chance=randint(self.chance_to_shoot[0],self.chance_to_shoot[1])
            if chance ==1 and 'shoot' not in self.aux_state:
                self.aux_state.append('shoot')
                self.shoot_start=time.time()
                self.shoot_pos=player1pos
                self.timer_wheel_step=0
        if 'bullet' in self.aux_state:
            self.bullet_trajectory()
        if 'bleed' in self.aux_state:
            self.bleed()
        if 'trap' in self.aux_state:
            self.trap(self.trap_duration)
        
        if 'chain' in self.aux_state:
            self.chain_lightning(screen,player)
   
    def blit(self):
        screen.blit(self.image,(self.x,self.y))

    def update(self,screen,player):
        self.pos=pygame.Vector2((self.rect.center))
        self.blit()
        self.vitality()
        self.auxillary(screen,player)
        
