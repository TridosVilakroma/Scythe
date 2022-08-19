import pygame,time,particles,math
import common_functions as comfunc
import controller as con
from pygame.sprite import collide_mask, collide_rect, spritecollide
from color_palette import *
import Time

scarecrows=None#variable overwritten in main to add enemy access here

#Base equipment class
class Equipment(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.mask=pygame.mask.from_surface(image)
        self.rect=image.get_rect()

class Relic(Equipment):
    def __init__(self,mana_drain,image):
        super().__init__(image)
        self.mana_drain=mana_drain

class Armor(Equipment):
    def __init__(self,defense):
        super().__init__()
        self.defense=defense

class Weapon(Equipment):
    def __init__(self,damage,cooldown):
        super().__init__()
        self.damage=damage
        self.cooldown=cooldown

class Tool(Equipment):
    def __init__(self,function_unlock):
        super().__init__()
        self.function_unlock=function_unlock

"""
Unique equipment is further subclassed from 
the four basic equipment sub-classes defined above.
You will access individual equipment by it's double index,
e.g. equip_matrix[1=relics, 2=armor, 3=weapons, 4=tools][int here for index of 
nested dict]

"""
###############RELICS###############
class FakeRelic():
    #quick work around for player starting with no activated_relic error
    def __init__(self):
        self.name='no_relic'

class Skunk(Relic):
    def __init__(self):
        self.io_name='Skunk'
        self.name='Mephitidae_relic'
        mana_drain=.13
        self.image=pygame.image.load(r'media\relics\mephitidae_relic.png').convert_alpha()
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\skunk\skunk_neutral.png').convert_alpha()
        super().__init__(mana_drain,self.image)
        self.defense=0
        self.speed=200
        self.scythe_attack=0
        self.hp_regen=0
        self.attack_count=0
        self.last_hit=Time.game_clock()
        self.cloud=False
        self.cloud_start=Time.game_clock()-3

    def attack(self,screen,hits,player,P1):
        time_stamp=Time.game_clock()
        if time_stamp>self.last_hit+.15:
            self.attack_count+=1
            for i in hits:
                i.damage(1.75)
                player.hp+=1.75
                self.last_hit=Time.game_clock()
            if self.attack_count>=2:
                for i in hits:
                    i.bleed()
                    player.hp+=1.75
                self.attack_count=0

    def special_attack(self,screen,player):
        if not self.cloud_cooldown:
            self.cloud_start=Time.game_clock()
            self.cloud_pos=pygame.Vector2(self.rect.center)
            self.cloud_cooldown=True

    def right_stick(self,delta,player,P1):
        pass

    def passives(self,screen,scarecrows,player,P1):
        if self.cloud_start>Time.game_clock()-3:
            pygame.draw.circle(screen,PURPLE,self.cloud_pos,85,1)
            for i in scarecrows:
                if i.pos.distance_to(self.cloud_pos)<85:
                    i.hp-=.075
                    i.health_bar_pop_up()
        else:
            self.cloud_cooldown=False

    def walk_right_load(self):
        return (r'media\relics\skunk\skunk_right.png')
    def walk_left_load(self):
        return (r'media\relics\skunk\skunk_left.png')
    def walk_up_load(self):
        return (r'media\relics\skunk\skunk_up.png')
    def walk_down_load(self):
        return (r'media\relics\skunk\skunk_down.png')

Mephitidae_relic=Skunk()

class Fox(Relic):
    def __init__(self):
        self.io_name='Fox'
        self.name='vulpes_relic'
        mana_drain=.15
        self.image=pygame.image.load(r'media\relics\vulpes_relic.png').convert_alpha()
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\fox\fox_neutral.png').convert_alpha()
        self.fox_mine=comfunc.ItemSprite(pygame.image.load(r'media\relics\fox\fox_mine.png').convert_alpha())
        self.fox_arrow=pygame.image.load(r'media\relics\fox\fox_arrow.png').convert_alpha()
        super().__init__(mana_drain,self.image)
        self.defense=0
        self.speed=235
        self.scythe_attack=0
        self.hp_regen=0
        self.last_hit=Time.game_clock()
        self.mine_cooldown=Time.game_clock()
        self.mine=False
        self.arrows=pygame.sprite.Group()
        self.arrow_delay=Time.game_clock()
        
    def attack(self,screen,hits,player,P1):
        time_stamp=Time.game_clock()
        if time_stamp>self.last_hit+.3:
            for i in hits:
                i.trap(15)
                i.damage(0)
                player.mp+=7.5
                self.last_hit=Time.game_clock()

    def special_attack(self,screen,player):
        if not self.mine_cooldown:
            self.mine=True
            self.mine_start=Time.game_clock()
            self.mine_pos=pygame.Vector2(self.rect.center)
            self.mine_cooldown=True
            self.fox_mine.rect[0]=(self.mine_pos[0]-self.fox_mine.image.get_width()/2)
            self.fox_mine.rect[1]=(self.mine_pos[1]-self.fox_mine.image.get_height()/2)

    def right_stick(self,delta,player,P1):
        origin=pygame.math.Vector2(player.rect.center)
        arrow=self.Arrow(self.fox_arrow,origin,P1)
        arrow.rect.center=origin
        arrow.velocity_x,arrow.velocity_y=pygame.math.Vector2((arrow.speed*delta)*(P1.get_axis(3)*8),
        (arrow.speed*delta)*(P1.get_axis(4)*8))
        if len(self.arrows)<30 and self.arrow_delay<Time.game_clock():
            self.arrows.add(arrow)
            self.arrow_delay=Time.game_clock()+.2

    def passives(self,screen,scarecrows,player,P1):
        if self.mine and self.mine_start>Time.game_clock()-10:
            self.nuked=True
            screen.blit(self.fox_mine.image,(self.mine_pos[0]-self.fox_mine.image.get_width()/2,
            self.mine_pos[1]-self.fox_mine.image.get_height()/2))
            for i in pygame.sprite.spritecollide(self.fox_mine,scarecrows,False,collide_mask):
                self.mine_start=Time.game_clock()-10
                
        elif self.mine and self.mine_start>Time.game_clock()-10.5:
            pygame.draw.circle(screen,RED,self.mine_pos,45,1)
            if self.nuked==True:
                self.nuked=False
                for i in scarecrows:
                        if i.pos.distance_to(self.mine_pos)<45:
                            i.hp-=8
                            i.health_bar_pop_up()
        else:
            self.mine_cooldown=False
            self.nuked=False
            self.mine=False

        self.arrows=comfunc.sprite_decay(self.arrows)
        if self.arrows:
            hit_list=pygame.sprite.groupcollide(scarecrows,self.arrows,False,True,collide_mask)
            for i in hit_list:
                i.damage(2.75)
            for i in self.arrows:
                screen.blit(i.rotated_image,(i.rect.topleft))
                i.rect.x+=i.velocity_x
                i.rect.y+=i.velocity_y
   
    class Arrow(Equipment):
            def __init__(self, image,origin,P1):
                super().__init__(image)
                self.speed=150
                self.origin=origin
                self.image=image
                self.life_time=Time.game_clock()+2
                self.rotated_image=pygame.transform.rotozoom(self.image,con.joy_angle(P1,(3,4))*-1,1)
                self.velocity_x=0
                self.velocity_y=0

    def walk_right_load(self):
        return (r'media\relics\fox\fox_right.png')
    def walk_left_load(self):
        return (r'media\relics\fox\fox_left.png')
    def walk_up_load(self):
        return (r'media\relics\fox\fox_up.png')
    def walk_down_load(self):
        return (r'media\relics\fox\fox_down.png')

vulpes_relic=Fox()

class Eagle(Relic):
    def __init__(self):
        self.io_name='Eagle'
        self.name='aeetus_relic'
        mana_drain=.18
        self.image=pygame.image.load(r'media\relics\aeetos_relic.png').convert_alpha()
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\eagle\eagle_neutral.png').convert_alpha()
        self.eagle_feather=pygame.image.load(r'media\relics\eagle\eagle_feather.png').convert_alpha()
        super().__init__(mana_drain,self.image)
        self.defense=1
        self.speed=170
        self.scythe_attack=0
        self.hp_regen=0
        self.feathers=pygame.sprite.Group()
        self.feather_delay=Time.game_clock()
        self.entry_portal=self.Portal(pygame.image.load(r'media\relics\eagle\portal_0.png').convert_alpha(),PINK_PURPLE,PURPLE,DARK_PURPLE)
        self.exit_portal=self.Portal(pygame.image.load(r'media\relics\eagle\portal_1.png').convert_alpha(),GREEN,DARK_GREEN,LIGHT_GREEN)
        self.entry_portal_cooldown=Time.game_clock()
        self.entry_portal_lifetime=Time.game_clock()+30
        self.exit_portal_cooldown=Time.game_clock()
        self.exit_portal_lifetime=Time.game_clock()+30
        self.ghost_time=Time.game_clock()
        self.ghost_angle=10
        self.ghost_shrink=.9

    class Feather(Equipment):
            def __init__(self, image,origin,P1):
                super().__init__(image)
                self.speed=150
                self.origin=origin
                self.image=image
                self.life_time=Time.game_clock()+.5
                self.rotated_image=pygame.transform.rotozoom(self.image,con.joy_angle(P1,(3,4))*-1,1)
                self.velocity_x=0
                self.velocity_y=0
                
    class Portal(comfunc.ItemSprite):
        def __init__(self, image,*particle_colors):
            super().__init__(image)
            self.active=False
            self.particle_colors=particle_colors
            
    def attack(self,screen,hits,player,P1):
        time_stamp=Time.game_clock()
        if self.entry_portal_cooldown<time_stamp:
            self.entry_portal_lifetime=Time.game_clock()+30
            self.entry_portal_cooldown=Time.game_clock()+3
            self.entry_portal.active=True
            self.entry_portal.rect.center=self.rect.center
            
            self.entry_portal.particles=particles.ParticleEmitter(.1,(self.rect.left,self.rect.right),
            (self.rect.top,self.rect.bottom),self.entry_portal.particle_colors,2,
            'fire_fly','move_to_dest','shrink','slow_emit')

    def special_attack(self,screen,player):
        time_stamp=Time.game_clock()
        if self.exit_portal_cooldown<time_stamp:
            self.exit_portal_lifetime=Time.game_clock()+30
            self.exit_portal_cooldown=Time.game_clock()+3
            self.exit_portal.active=True
            self.exit_portal.rect.center=self.rect.center

            self.exit_portal.particles=particles.ParticleEmitter(.1,(self.rect.left,self.rect.right),
            (self.rect.top,self.rect.bottom),self.exit_portal.particle_colors,2,
            'fire_fly','move_to_dest','shrink','slow_emit')

    def right_stick(self,delta,player,P1):
        origin=pygame.math.Vector2(player.rect.center)
        feather=self.Feather(self.eagle_feather,origin,P1)
        feather.rect.center=origin
        feather.velocity_x,feather.velocity_y=pygame.math.Vector2((feather.speed*delta)*(P1.get_axis(3)*3),
        (feather.speed*delta)*(P1.get_axis(4)*3))
        if len(self.feathers)<30 and self.feather_delay<Time.game_clock():
            if player.hp<=50:
                feather.velocity_x,feather.velocity_y=pygame.math.Vector2((feather.speed*delta)*(P1.get_axis(3)*4),
                (feather.speed*delta)*(P1.get_axis(4)*4))
                feather.life_time+=.5
                self.feathers.add(feather)
                self.feather_delay=Time.game_clock()+.3
            else:
                self.feathers.add(feather)
                self.feather_delay=Time.game_clock()+.5

    def passives(self,screen,scarecrows,player,P1):
        time_stamp=Time.game_clock()
        if player.active_relic.name=='aeetus_relic':
            mana_regen=False
            hp_regen=False
            for i in scarecrows:
                if pygame.Vector2(player.rect.center).distance_to(i.rect.center)<=150:
                    mana_regen=True
            if mana_regen:
                player.mp+=.05
            else:#if hp_regen:
                player.hp+=.005


        if self.entry_portal.active:
            if self.entry_portal_lifetime>time_stamp:
                self.entry_portal.particles.update(screen)
                self.entry_portal_transparent = self.entry_portal.image.copy()
                alpha = comfunc.sine_pulse(.6,175,50)
                if alpha<0:
                    alpha = 0
                self.entry_portal_transparent.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                screen.blit(self.entry_portal_transparent,self.entry_portal.rect)
                if self.exit_portal.active:
                    if self.entry_portal.rect.colliderect(player.precise_rect):
                        self.ghost_time=Time.game_clock()+1.2
                        self.ghost_angle=10
                        self.ghost_shrink=.9
                        self.ghost_image=player.image.copy()
                        player.x_precise=self.exit_portal.rect.left
                        player.x=self.exit_portal.rect.left
                        player.y_precise=self.exit_portal.rect.top
                        player.y=self.exit_portal.rect.top
                    if self.ghost_time>time_stamp:
                        ghost_alpha = comfunc.sine_pulse(1,250,128)
                        self.ghost_angle+=1
                        self.ghost_shrink-=.005
                        if ghost_alpha<0:
                            ghost_alpha = 0
                        self.ghost_image_rotated=pygame.transform.rotozoom(self.ghost_image,self.ghost_angle,self.ghost_shrink)
                        self.ghost_image_rotated.fill((255, 255, 255, ghost_alpha), None, pygame.BLEND_RGBA_MULT)
                        screen.blit(self.ghost_image_rotated,self.entry_portal.rect.topleft)

            else:
              self.entry_portal.active=False  

        if self.exit_portal.active:
            if self.exit_portal_lifetime>time_stamp:
                self.exit_portal.particles.update(screen)
                self.exit_portal_transparent = self.exit_portal.image.copy()
                alpha = comfunc.cosine_pulse(.5,175,50)
                if alpha<0:
                    alpha = 0
                self.exit_portal_transparent.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                screen.blit(self.exit_portal_transparent,self.exit_portal.rect)

            else:
              self.exit_portal.active=False

        self.feathers=comfunc.sprite_decay(self.feathers)
        if self.feathers:
            hit_list=pygame.sprite.groupcollide(scarecrows,self.feathers,False,True,collide_mask)
            for i in hit_list:
                i.damage(8)
            for i in self.feathers:
                screen.blit(i.rotated_image,(i.rect.topleft))
                i.rect.x+=i.velocity_x
                i.rect.y+=i.velocity_y

    def walk_right_load(self):
        return (r'media\relics\eagle\eagle_right.png')
    def walk_left_load(self):
        return (r'media\relics\eagle\eagle_left.png')
    def walk_up_load(self):
        return (r'media\relics\eagle\eagle_up.png')
    def walk_down_load(self):
        return (r'media\relics\eagle\eagle_down.png')

aeetus_relic=Eagle()

class Bear(Relic):
    def __init__(self):
        self.io_name='Bear'
        self.name='Ursidae_relic'
        mana_drain=.125
        self.image=pygame.image.load(r'media\relics\Ursidae_relic.png').convert_alpha()
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\bear\bear_0.png').convert_alpha()
        super().__init__(mana_drain, self.image)
        self.defense=3
        self.speed=120
        self.scythe_attack=6
        self.hp_regen=0
        self.rage_mode=False
        self.rage_colors=(RED,RED,RED,RED,RED,DARK_RED,DARK_RED,DEEP_RED,ORANGE)

    def attack(self,screen,hits,player,P1):
        time_stamp=Time.game_clock()
        if time_stamp>player.slash_time_ref:
                    player.slash_time_ref=time_stamp+player.slash_cooldown
                    player.focus='slash'
                    if self.rage_mode:
                        for i in hits:
                            player.hp+=1
                            player.mp+=1

    def special_attack(self,screen,player):
        pass

    def right_stick(self,delta,player,P1):
        pass

    def passives(self,screen,scarecrows,player,P1):
        if player.recieved_damage:
            self.rage_mode=True
            self.rage_timer=Time.game_clock()+5
            self.rage_particles=particles.ParticleEmitter(.025,(self.rect.left,self.rect.right),
            (self.rect.top,self.rect.top),self.rage_colors,2,
            'ascend','fast_shrink','fast_emit','random_growth','vert_wave')
        if self.rage_mode and player.active_relic.name=='Ursidae_relic':
            player.speed=220
            player.defense=.6
            self.rage_particles.x_range=(self.rect.left-4,self.rect.right+4)
            self.rage_particles.y_range=(self.rect.top-2,self.rect.top+20)
            self.rage_particles.update(screen)


            if self.rage_timer<Time.game_clock():
                self.rage_mode=False
                player.speed=120
                player.defense=3
            


    def walk_right_load(self):
        return (r'media\relics\bear\bear_3.png')
    def walk_left_load(self):
        return (r'media\relics\bear\bear_2.png')
    def walk_up_load(self):
        return (r'media\relics\bear\bear_1.png')
    def walk_down_load(self):
        return (r'media\relics\bear\bear_4.png')

Ursidae_relic=Bear()

class Lion(Relic):
    def __init__(self):
        self.io_name='Lion'
        self.name='Panthera_relic'
        mana_drain=.095
        self.image=pygame.image.load(r'media\relics\panthera_relic.png').convert_alpha()
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\lion\lion_0.png').convert_alpha()
        super().__init__(mana_drain, self.image)
        self.defense=0
        self.speed=160
        self.scythe_attack=0
        self.hp_regen=0
        self.last_hit=Time.game_clock()
        self.chain_timer=Time.game_clock()-3
        self.roar_start=Time.game_clock()-3

    def attack(self,screen,hits,player,P1):
        time_stamp=Time.game_clock()
        if time_stamp>self.last_hit+.35:
            for i in hits:
                i.damage(3)
                self.last_hit=time_stamp
            if time_stamp>self.chain_timer+.7 and player.mp>5:
                if hits:
                    player.mp-=5
                    self.chain_timer=time_stamp
                for i in hits:
                    i.chain_lightning(screen,player)
                

    def special_attack(self,screen,player):
        if player.mp>10:
            if not self.roar_cooldown:
                self.roar_start=Time.game_clock()
                self.roar_cooldown=True
                player.mp-=10

    def right_stick(self,delta,player,P1):
        pass

    def passives(self,screen,scarecrows,player,P1):
        if self.roar_start>Time.game_clock()-.5:
            sine=math.sin(Time.game_clock()*5)
            cosine=math.cos(Time.game_clock()*5)
            reverse_sine=math.sin(Time.game_clock()*-5)
            reverse_cosine=math.cos(Time.game_clock()*-5)
            self.roar_pos=pygame.Vector2(player.rect.center)
            pygame.draw.circle(screen,BRIGHT_YELLOW,self.roar_pos,100,1)
            pygame.draw.circle(screen,PALE_YELLOW,self.roar_pos,sine*100,1)
            pygame.draw.circle(screen,PALE_YELLOW,self.roar_pos,cosine*100,1)
            pygame.draw.circle(screen,WORN_YELLOW,self.roar_pos,reverse_sine*100,1)
            pygame.draw.circle(screen,WORN_YELLOW,self.roar_pos,reverse_cosine*100,1)
            for i in scarecrows:
                if i.pos.distance_to(self.roar_pos)<100:
                    i.stun(6)
                    i.health_bar_pop_up()
        else:
            self.roar_cooldown=False


    def walk_right_load(self):
        return (r'media\relics\lion\lion_0.png')
    def walk_left_load(self):
        return (r'media\relics\lion\lion_0.png')
    def walk_up_load(self):
        return (r'media\relics\lion\lion_0.png')
    def walk_down_load(self):
        return (r'media\relics\lion\lion_0.png')

Panthera_relic=Lion()

class Turtle(Relic):
    def __init__(self):
        self.io_name='Turtle'
        self.name='Testudinidae_relic'
        mana_drain=.115
        self.image=pygame.image.load(r'media\relics\Testudinidae_relic.png').convert_alpha()
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\turtle\turtle.png').convert_alpha()
        super().__init__(mana_drain, self.image)
        self.defense=3
        self.speed=100
        self.scythe_attack=0
        self.hp_regen=.01
        self.last_hit=Time.game_clock()
        self.blockaded=False
        self.pushback=False
        self.pushback_start=Time.game_clock()

    def attack(self,screen,hits,player,P1):
        time_stamp=Time.game_clock()
        if time_stamp>self.last_hit+2:
            for i in hits:
                i.damage(20)
                i.stun(1)
                self.last_hit=Time.game_clock()

    def special_attack(self,screen,player):
        if 'blockade' not in player.aux_state:
            if player.mp>5:
                player.mp-=5
                player.aux_state.append('blockade')
                player.incoming_damage_tracked=True
                player.shield-=.5
                self.blockaded=True

    def right_stick(self,delta,player,P1):
        pass

    def passives(self,screen,scarecrows,player,P1):
        if player.active_relic.name!='Testudinidae_relic' and self.blockaded:
            comfunc.clean_list(player.aux_state,'blockade')
            player.incoming_damage_tracked=False
            player.incoming_damage=[]
            player.shield+=.5
            self.blockaded=False

        if self.blockaded and not P1.get_button(1):
            comfunc.clean_list(player.aux_state,'blockade')
            player.incoming_damage_tracked=False
            player.incoming_damage=[]
            player.shield+=.5
            self.blockaded=False
            self.pushback=True
            self.pushback_start=Time.game_clock()

        if self.pushback==True:
            timestamp=Time.game_clock()
            if self.pushback_start>timestamp-.5:
                pygame.draw.circle(screen,RED,self.rect.center,85,1)
                pygame.draw.circle(screen,BRIGHT_YELLOW,self.rect.center,(timestamp-self.pushback_start)*50,1)
                pygame.draw.circle(screen,BRIGHT_YELLOW,self.rect.center,(timestamp-self.pushback_start)*115,1)
                pygame.draw.circle(screen,BRIGHT_YELLOW,self.rect.center,(timestamp-self.pushback_start)*160,1)
                for i in scarecrows:
                    if i.pos.distance_to(player.rect.center)<85:
                        i.stun(.2)
            else:
              self.pushback=False 

        if P1.get_button(1) and self.blockaded==True:
            player.mp-=.02
            sine=math.sin(Time.game_clock())*4
            cosine=math.cos(Time.game_clock())*4
            pygame.draw.circle(screen,RED,self.rect.center,85,2)
            pygame.draw.circle(screen,DARK_RED,self.rect.center,60+sine,1)
            pygame.draw.circle(screen,DARK_RED,self.rect.center,40+cosine*2,1)
            pygame.draw.circle(screen,DARK_RED,self.rect.center,20+sine*1.5,1)
            pygame.draw.circle(screen,DARK_RED,self.rect.center,10+cosine*1.25,1)
            if player.incoming_damage:
                for i in scarecrows:
                    if i.pos.distance_to(player.rect.center)<85:
                        i.damage(sum(player.incoming_damage)*2)
                        player.incoming_damage=[]
                player.incoming_damage=[]
            


    def walk_right_load(self):
        return (r'media\relics\turtle\turtle.png')
    def walk_left_load(self):
        return (r'media\relics\turtle\turtle.png')
    def walk_up_load(self):
        return (r'media\relics\turtle\turtle.png')
    def walk_down_load(self):
        return (r'media\relics\turtle\turtle.png')

Testudinidae_relic=Turtle()

class Wolf(Relic):
    def __init__(self):
        self.io_name='Wolf'
        self.name='Canidae_relic'
        mana_drain=.115
        self.image=pygame.image.load(r'media\relics\canidae_relic.png').convert_alpha()
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\wolf\wolf.png').convert_alpha()
        super().__init__(mana_drain, self.image)
        self.defense=1
        self.speed=150
        self.scythe_attack=0
        self.hp_regen=0
        self.last_hit=Time.game_clock()
        self.counter_store_cooldown=Time.game_clock()
        self.counter_store=False
        self.stored_energy=0
        self.countered=False

    def attack(self,screen,hits,player,P1):
        time_stamp=Time.game_clock()
        if time_stamp>self.last_hit+.3:
            for i in hits:
                i.damage(10)
                if self.stored_energy:
                    i.damage(self.stored_energy)
                    self.stored_energy=0
                self.last_hit=Time.game_clock()

    def special_attack(self,screen,player):
        if Time.game_clock()>self.counter_store_cooldown:
            if player.mp>15:
                player.mp-=15
                self.counter_store_cooldown=Time.game_clock()+1
                player.incoming_damage_tracked=True
                player.shield-=1
                self.counter_store=True

    def right_stick(self,delta,player,P1):
        pass

    def passives(self,screen,scarecrows,player,P1):
            if self.counter_store==True:
                if self.counter_store_cooldown>Time.game_clock()+.85:
                   self.stored_energy+=(sum(player.incoming_damage)*2)
                   if player.incoming_damage:
                       self.countered=True
                   player.incoming_damage=[]
                else:
                    player.incoming_damage_tracked=False
                    player.incoming_damage=[]
                    player.shield+=1
                    self.counter_store=False
                    self.countered=False
            if self.countered==True:
                pygame.draw.circle(screen,PINK_PURPLE,self.rect.center,15,1)

    def walk_right_load(self):
        return (r'media\relics\wolf\wolf.png')
    def walk_left_load(self):
        return (r'media\relics\wolf\wolf.png')
    def walk_up_load(self):
        return (r'media\relics\wolf\wolf.png')
    def walk_down_load(self):
        return (r'media\relics\wolf\wolf.png')

Canidae_relic=Wolf()

class Lynx(Relic):
    def __init__(self):
        self.io_name='Lynx'
        self.name='Felidae_relic'
        mana_drain=.125
        self.image=pygame.image.load(r'media\relics\felidae_relic.png').convert_alpha()
        self.transparent=self.image.copy()
        self.transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.shape_shifted=pygame.image.load(r'media\relics\lynx\lynx.png').convert_alpha()
        super().__init__(mana_drain, self.image)
        self.defense=0
        self.speed=300
        self.scythe_attack=0
        self.hp_regen=0
        self.last_hit=Time.game_clock()
        self.attack_flag=False
        self.blink_hit_counter=0
        self.blinked_lynx_flag=False
        self.last_blink_time=Time.game_clock()

    def attack(self,screen,hits,player,P1):
        if self.attack_flag==False and P1.get_button(2):
            self.attack_flag=True
            for i in hits:
                i.damage(5)
                if player.blink_start>Time.game_clock()-.5:
                    player.mp+=5


    def special_attack(self,screen,player):
        pass

    def right_stick(self,delta,player,P1):
        pass

    def passives(self,screen,scarecrows,player,P1):
        timestamp=Time.game_clock()
        if self.attack_flag==True and not P1.get_button(2):
            self.attack_flag=False
        if player.active_relic.name =='Felidae_relic':
            player.blink_distance=135
            player.blink_step_cooldown=.3
            player.blink_mp_cost=5

            if player.blink_start>timestamp-.5:
                player.invulnerable=True
            else:
                player.invulnerable=False

            if self.last_blink_time<Time.game_clock()-.25:
                if P1.get_button(0) and player.mp>player.blink_mp_cost:
                    self.blinked_lynx_flag=True
                    self.ghostpos=(player.x,player.y)
                    self.last_blink_time=Time.game_clock()
            if self.blinked_lynx_flag:
                blink_path=(self.ghostpos,player.rect.center)
                pygame.draw.line(screen,GREY_BLUE,self.ghostpos,player.rect.center,5)
                for i in scarecrows:
                    if i.rect.clipline(blink_path):
                        i.damage(10)
                self.blink_hit_counter+=1
                if self.blink_hit_counter==6:
                    self.blinked_lynx_flag=False
                    self.blink_hit_counter=0
            
        else:
            player.blink_distance=90
            player.blink_step_cooldown=.5
            player.blink_mp_cost=0




    def walk_right_load(self):
        return (r'media\relics\lynx\lynx.png')
    def walk_left_load(self):
        return (r'media\relics\lynx\lynx.png')
    def walk_up_load(self):
        return (r'media\relics\lynx\lynx.png')
    def walk_down_load(self):
        return (r'media\relics\lynx\lynx.png')

Felidae_relic=Lynx()

relics={
    1:Mephitidae_relic,
    2:vulpes_relic,
    3:aeetus_relic,
    4:Ursidae_relic,
    5:Panthera_relic,
    6:Testudinidae_relic,
    7:Canidae_relic,
    8:Felidae_relic
}

###############ARMOR###############

armor={

}
###############WEAPONS###############

class Scythe(Weapon):
    def __init__(self, image, damage, cooldown):
        super().__init__(image, damage, cooldown)

weapons={

}
###############TOOLS###############

tools={

}


##################################
equip_matrix={
    1:relics,
    2:armor,
    3:weapons,
    4:tools
}

#Adding all equip into a sprite group
equip=[]
for equip_types in equip_matrix.values():
    for equipment in equip_types.values():
        try:
            equip.append(equipment)
        except:
            print(Exception)