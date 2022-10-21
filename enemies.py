from color_palette import *
import pygame,time,math,equip,particles
from random import randint
import random
import common_functions as comfunc
import Time
from controller import ControllerReferences as refcon

screen=None
canvas=None
game=None
enemies=[]
player1pos=None
player=None
attacks=[]
spawned_loot=pygame.sprite.Group()
damage_text=pygame.sprite.Group()

class Scarecrow(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.delta=Time.game_clock()
        self.image = pygame.image.load('media\deco\scarecrow.png').convert_alpha()
        self.rect=pygame.Rect(x,y,self.image.get_width(),self.image.get_height())
        self.pos=pygame.math.Vector2((self.rect.center))
        self.hp = (randint(10,25)+75)
        self.hp_ratio=self.rect.width/self.hp
        self.defense = 0#randint(0,3)
        self.damage_ref_timer=Time.game_clock()
        self.hpbar_ref_timer=Time.game_clock()
        self.hit_flash=Time.game_clock()
        self.aux_state=[]
        self.timer_wheel_step=0
        self.image_loader()
        self.mask=pygame.mask.from_surface(self.image)
        self.dying=False

    @property
    def x(self):
        return self.rect.x
    @x.setter
    def x(self,value):
        self.rect.x=value
    @property
    def y(self):
        return self.rect.y
    @y.setter
    def y(self,value):
        self.rect.y=value
    @property
    def hit_box(self):
        bound_rect=self.image.get_bounding_rect()
        bound_rect[0]=bound_rect[0]+self.x
        bound_rect[1]=bound_rect[1]+self.y
        return (bound_rect)

    def image_loader(self):
        self.trap_net=pygame.image.load(r'media\relics\fox\fox_net.png').convert_alpha()
        self.norm_image=pygame.image.load('media\deco\scarecrow.png').convert_alpha()
        self.white=pygame.image.load('media\deco\scarecrow-white.png').convert_alpha()
        self.timer_wheel_img=[]
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl00.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl01.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl02.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl03.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl04.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl05.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl06.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl07.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl08.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl09.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl10.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl11.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl12.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl13.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl14.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl15.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl16.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl17.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl18.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl19.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl20.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl21.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl22.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl23.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl24.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl25.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl26.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl27.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl28.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl29.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl30.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl31.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl32.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl33.png').convert_alpha())
        self.small_straw=pygame.image.load(r'media\deco\small_straw.png').convert_alpha()
        self.straw_stalk=pygame.image.load(r'media\deco\straw_stalk.png').convert_alpha()

    def loot_dropper(self):
        loot=equip.standard_table()
        if loot is None:
            return
        loot.rect.topleft=self.rect.topleft
        spawned_loot.add(loot)

    def collision_check(self):
        pass

    def damage(self,damage):
        if damage>5:
            smrumble=damage*.1
            lgrumble=damage*.025
            refcon.rumble(refcon.P1,lgrumble,smrumble,100)
        self.hp-=max(0,damage-self.defense)
        if self.hp<0:
            self.hp=0
        else:
            self.aux_state.append('health')
            self.aux_state.append('timerwheel')
            self.hpbar_ref_timer=Time.game_clock()+3
            self.hit_flash=Time.game_clock()+.1
            self.health_bar()
            rand_pos=randint(self.x,self.rect.right),randint(self.y,self.rect.bottom)
            damage_text.add(particles.HoverText(rand_pos,damage,'rise',outline_size=1,outline_color=BLACK))

    def trap(self,duration):
        if 'trap' not in self.aux_state:
            self.trap_start=Time.game_clock()+duration
            self.aux_state.append('trap')
            self.trap_duration=duration
        if self.trap_start>Time.game_clock():
            canvas.blit(self.trap_net,self.rect.topleft)
        else:
            comfunc.clean_list(self.aux_state,'trap')

    def stun(self,duration):
        if 'stun' not in self.aux_state:
            self.stun_start=Time.game_clock()+duration
            self.aux_state.append('stun')
            self.stun_duration=duration
            self.stun_particles=particles.ParticleEmitter(.05,(self.pos[0]-10,self.pos[0]+10),
            (self.pos[1]-20,self.pos[1]),
            [RED,PALE_YELLOW,PALE_YELLOW,PALE_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW],
            2,'burst_emit20','halo_wave',square=True)
        if self.stun_start>Time.game_clock():
            self.stun_particles.update(canvas)
        else:
            comfunc.clean_list(self.aux_state,'stun')

    def bleed(self):
        if 'bleed' not in self.aux_state:
            self.bleed_start=Time.game_clock()
        self.aux_state.append('bleed')
        if self.bleed_start>Time.game_clock()-5:
            self.hp-=.05
            self.hpbar_ref_timer=Time.game_clock()+3
            self.health_bar()
        else:
            comfunc.clean_list(self.aux_state,'bleed')

    def health_bar_pop_up(self):
        self.hpbar_ref_timer=Time.game_clock()+3
        self.aux_state.append('health')
        self.health_bar()

    def health_bar(self):
        time_stamp=Time.game_clock()
        if time_stamp<self.hpbar_ref_timer:
            health_bar_thickness=3
            outline=pygame.Rect(self.rect.left-1,self.rect.top-health_bar_thickness-1,self.rect.width+2,5)
            health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.hp*self.hp_ratio,health_bar_thickness)
            missing_health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.rect.width,health_bar_thickness)
            pygame.draw.rect(canvas,WHITE,outline,0,1)
            pygame.draw.rect(canvas,RED,missing_health,0,1)
            pygame.draw.rect(canvas,GREEN,health,0,1)
        else:
            comfunc.clean_list(self.aux_state,'health')

    def timer_wheel(self):
        if 'dust' in self.aux_state:
            comfunc.clean_list(self.aux_state,'timerwheel')
        else:
            if int(self.timer_wheel_step)<=len(self.timer_wheel_img)-1:
                canvas.blit(self.timer_wheel_img[self.timer_wheel_step],self.rect.center)
                self.timer_wheel_step+=1
            else:
                self.aux_state.append('dust')
                self.dust_start=Time.game_clock()
                self.dust_pos=player1pos
                self.timer_wheel_step=0
                comfunc.clean_list(self.aux_state,'timerwheel')

    def dust(self):
        if self.dust_start>=Time.game_clock()-.6:
            canvas.blit(self.small_straw,self.dust_pos)
            self.aux_state.append('dust_particles')
            self.dust_particles=particles.ParticleEmitter(0,
            (self.dust_pos[0]+16,self.dust_pos[0]+16),(self.dust_pos[1]+32,self.dust_pos[1]+32),
            [PALE_YELLOW,WORN_YELLOW,BRIGHT_YELLOW,BROWN],1,
            'explode_up','move_to_dest','fast_shrink','shrink')
        elif self.dust_start>=Time.game_clock()-1.2:
            canvas.blit(self.straw_stalk,self.dust_pos)
            dust_rect=pygame.Rect((self.dust_pos),(32,32))
            attacks.append((.75,dust_rect))
            
        elif self.dust_start>=Time.game_clock()-1.3:
            canvas.blit(self.small_straw,self.dust_pos)

        else:
            comfunc.clean_list(self.aux_state,'dust')
            comfunc.clean_list(self.aux_state,'dust_particles')

    def chain_lightning(self,canvas,player):
        if 'chain' not in self.aux_state:
            self.chain_start=Time.game_clock()
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
        if self.chain_start>Time.game_clock()-1.5:
            self.hp-=.25
            self.hpbar_ref_timer=Time.game_clock()+3
            self.health_bar()
            for i in enemies:
                try:
                    i.lightning.update(canvas)
                    self.lightning_implosion.update(canvas)
                except AttributeError:
                    pass
        else:
            comfunc.clean_list(self.aux_state,'chain')

    def vitality(self):
        if self.hp <= 0:
            self.loot_dropper()
            self.kill()

    def death_animation(self):
        self.image=self.white
        if not self.dying:
            self.dying=True
            self.time_of_death=Time.game_clock()
            self.hit_flash=Time.game_clock()+.2
            self.death_particles=[]
            self.death_particles.append(particles.ParticleEmitter(
                0,
                (self.rect.centerx,self.rect.centerx),
                (self.rect.centery,self.rect.centery),
                [RED,BRIGHT_YELLOW,BROWN],
                1,
                'explode_up','move_to_dest','shrink','move_out'))
            self.death_particles.append(particles.ParticleEmitter(
                0,
                (self.rect.centerx,self.rect.centerx),
                (self.rect.centery,self.rect.centery),
                [PALE_YELLOW,WORN_YELLOW,BRIGHT_YELLOW,BROWN],
                1,
                'explode_up','move_to_dest','fast_shrink','shrink'))
            self.death_particles.append(particles.ParticleEmitter(
                0,
                (self.rect.centerx,self.rect.centerx),
                (self.rect.centery,self.rect.centery),
                [PALE_YELLOW,WORN_YELLOW,BRIGHT_YELLOW,BROWN],
                1,
                'explode','move_to_dest','fast_shrink','shrink','move_out'))
        else:
            if Time.game_clock()-self.time_of_death>.05:
                radius=200-(Time.game_clock()-self.time_of_death)*463
                pygame.draw.circle(canvas,WHITE,self.rect.center,radius,1)
            if Time.game_clock()-self.time_of_death>.48:
                for i in self.death_particles:
                    i.update(canvas)
            if Time.game_clock()-self.time_of_death>.78:
                self.vitality()

    def demo(self):
            self.image=pygame.transform.smoothscale(self.image,(25,25))

    def auxillary(self,canvas,player):
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
            self.chain_lightning(canvas,player)
        if 'trap' in self.aux_state:
            self.trap(self.trap_duration)
        if 'dust_particles' in self.aux_state:
            self.dust_particles.update(canvas)

    def blit(self):
        self.image=self.norm_image if self.hit_flash<Time.game_clock() else self.white
        canvas.blit(self.image,(self.x,self.y))

    def update(self,canvas,player,delta):
        self.delta=delta
        self.pos=pygame.math.Vector2((self.rect.center))
        self.blit()
        if self.hp<=0:
            self.death_animation()
        else:
            self.auxillary(canvas,player)

class Omnivine(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.delta=Time.game_clock()
        self.image = pygame.image.load('media\enemies\omnivine_walk\sprite_0.png').convert_alpha()
        self.mask=pygame.mask.from_surface(self.image)
        self.rect=pygame.Rect(x,y,self.image.get_width(),self.image.get_height())
        self.pos=pygame.Vector2((self.rect.center))
        self.demo_dest=pygame.Vector2((self.rect.center))
        self.hp = randint(10,25)+50
        self.hp_ratio=self.rect.width/self.hp
        self.defense = randint(0,3)
        self.damage_ref_timer=Time.game_clock()
        self.hpbar_ref_timer=Time.game_clock()
        self.hit_flash=Time.game_clock()
        self.aux_state=[]
        self.timer_wheel_step=0
        self.image_loader()
        self.current_sprite=0
        self.animate_speed=.09
        self.chance_to_shoot=1,750 #chance is one in the second int
        self.dest=pygame.Vector2((self.rect.center))
        self.vector=pygame.math.Vector2(0,0)
        self.speed=40
        self.bullets=pygame.sprite.Group()
        self.dying=False

    @property
    def x(self):
        return self.rect.x
    @x.setter
    def x(self,value):
        self.rect.x=value
    @property
    def y(self):
        return self.rect.y
    @y.setter
    def y(self,value):
        self.rect.y=value
    @property
    def hit_box(self):
        bound_rect=self.image.get_bounding_rect()
        bound_rect[0]=bound_rect[0]+self.x
        bound_rect[1]=bound_rect[1]+self.y
        return (bound_rect)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self,pos,delta) -> None:
            super().__init__()
            self.image=pygame.image.load(r'media\enemies\ominvine_shoot\outlined_bullet.png').convert_alpha()
            self.rect=pygame.Rect(pos[0],pos[1],self.image.get_width(),self.image.get_height())
            self.rect.center=(pos[0],pos[1])
            self.speed=200
            self.air_time=3.25
            self.time_stamp=Time.game_clock()+self.air_time
            self.dest=pygame.Vector2(player.rect.center)
            self.delta=delta
            self.pos=pygame.Vector2(self.rect.center)
            self.mask=pygame.mask.from_surface(self.image)

        def filter(self):
            if self.rect.colliderect(player):
                if pygame.sprite.collide_mask(self,player):
                    attacks.append((10,self.rect))
                    self.kill()
            if self.time_stamp<Time.game_clock():
                self.kill()

        def update(self,canvas):
            self.filter()
            self.vector=comfunc.vector_from_coords(self.rect.center,self.dest)
            if self.vector.length_squared()>0:
                self.vector.scale_to_length(self.speed*self.delta)
            self.dest+=self.vector
            self.pos+=self.vector
            self.rect.center=self.pos
            canvas.blit(self.image,self.rect.topleft)

    def image_loader(self):
        self.trap_net=pygame.image.load(r'media\relics\fox\fox_net.png').convert_alpha()
        self.neutral_stance= pygame.image.load('media\enemies\omnivine_walk\sprite_0.png').convert_alpha()
        self.timer_wheel_img=[]
        self.traverse_sprites=[]
        self.traverse_white=[]
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl00.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl01.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl02.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl03.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl04.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl05.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl06.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl07.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl08.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl09.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl10.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl11.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl12.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl13.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl14.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl15.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl16.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl17.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl18.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl19.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl20.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl21.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl22.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl23.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl24.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl25.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl26.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl27.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl28.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl29.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl30.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl31.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl32.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl33.png').convert_alpha())
        self.traverse_sprites.append(pygame.image.load(r'media\enemies\omnivine_walk\sprite_0.png').convert_alpha())
        self.traverse_sprites.append(pygame.image.load(r'media\enemies\omnivine_walk\sprite_1.png').convert_alpha())
        self.traverse_sprites.append(pygame.image.load(r'media\enemies\omnivine_walk\sprite_2.png').convert_alpha())
        self.traverse_sprites.append(pygame.image.load(r'media\enemies\omnivine_walk\sprite_3.png').convert_alpha())
        self.shoot0=pygame.image.load(r'media\enemies\ominvine_shoot\sprite_0.png').convert_alpha()
        self.shoot1=pygame.image.load(r'media\enemies\ominvine_shoot\sprite_1.png').convert_alpha()
        self.shoot2=pygame.image.load(r'media\enemies\ominvine_shoot\sprite_2.png').convert_alpha()
        self.traverse_white.append(pygame.image.load(r'media\enemies\omnivine_white\sprite_0.png').convert_alpha())
        self.traverse_white.append(pygame.image.load(r'media\enemies\omnivine_white\sprite_1.png').convert_alpha())
        self.traverse_white.append(pygame.image.load(r'media\enemies\omnivine_white\sprite_2.png').convert_alpha())
        self.traverse_white.append(pygame.image.load(r'media\enemies\omnivine_white\sprite_3.png').convert_alpha())
        self.shoot0_white=pygame.image.load(r'media\enemies\omnivine_white\sprite_4.png').convert_alpha()
        self.shoot1_white=pygame.image.load(r'media\enemies\omnivine_white\sprite_5.png').convert_alpha()
        self.shoot2_white=pygame.image.load(r'media\enemies\omnivine_white\sprite_6.png').convert_alpha()

    def loot_dropper(self):
        loot=equip.standard_table()
        if loot is None:
            return
        loot.rect.topleft=self.rect.topleft
        spawned_loot.add(loot)

    def collision_check(self):
        pass

    def damage(self,damage):
        if damage>5:
            smrumble=damage*.1
            lgrumble=damage*.025
            refcon.rumble(refcon.P1,lgrumble,smrumble,100)
        self.hp-=max(0,damage-self.defense)
        if self.hp<0:
            self.hp=0
        else:
            self.aux_state.append('health')
            self.aux_state.append('timerwheel')
            self.hpbar_ref_timer=Time.game_clock()+3
            self.hit_flash=Time.game_clock()+.1
            self.health_bar()
            rand_pos=randint(self.x,self.rect.right),randint(self.y,self.rect.bottom)
            damage_text.add(particles.HoverText(rand_pos,damage,'rise',outline_size=1,outline_color=BLACK))

    def trap(self,duration):
        if 'trap' not in self.aux_state:
            self.trap_start=Time.game_clock()+duration
            self.aux_state.append('trap')
            self.trap_duration=duration
        if self.trap_start>Time.game_clock():
            canvas.blit(self.trap_net,self.rect.topleft)
        else:
            comfunc.clean_list(self.aux_state,'trap')

    def stun(self,duration):
        if 'stun' not in self.aux_state:
            self.stun_start=Time.game_clock()+duration
            self.aux_state.append('stun')
            self.stun_duration=duration
            self.stun_particles=particles.ParticleEmitter(.05,(self.pos[0]-10,self.pos[0]+10),
            (self.pos[1]-20,self.pos[1]),
            [RED,PALE_YELLOW,PALE_YELLOW,PALE_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW],
            2,'burst_emit20','halo_wave',square=True)
        if self.stun_start>Time.game_clock():
            self.stun_particles.update(canvas)
        else:
            comfunc.clean_list(self.aux_state,'stun')

    def bleed(self):
        if 'bleed' not in self.aux_state:
            self.bleed_start=Time.game_clock()
            self.aux_state.append('bleed')
        if self.bleed_start>Time.game_clock()-5:
            self.hp-=.05
            self.hpbar_ref_timer=Time.game_clock()+3
            self.health_bar()
        else:
            comfunc.clean_list(self.aux_state,'bleed')

    def chain_lightning(self,canvas,player):
        if 'chain' not in self.aux_state:
            self.chain_start=Time.game_clock()
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
        if self.chain_start>Time.game_clock()-1.5:
            self.hp-=.25
            self.hpbar_ref_timer=Time.game_clock()+3
            self.health_bar()
            for i in enemies:
                try:
                    i.lightning.update(canvas)
                    self.lightning_implosion.update(canvas)
                except AttributeError:
                    pass
        else:
            comfunc.clean_list(self.aux_state,'chain')

    def health_bar_pop_up(self):
        self.hpbar_ref_timer=Time.game_clock()+3
        self.aux_state.append('health')
        self.health_bar()

    def health_bar(self):
        time_stamp=Time.game_clock()
        if time_stamp<self.hpbar_ref_timer:
            health_bar_thickness=3
            outline=pygame.Rect(self.rect.left-1,self.rect.top-health_bar_thickness-1,self.rect.width+2,5)
            health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.hp*self.hp_ratio,health_bar_thickness)
            missing_health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.rect.width,health_bar_thickness)
            pygame.draw.rect(canvas,WHITE,outline,0,1)
            pygame.draw.rect(canvas,RED,missing_health,0,1)
            pygame.draw.rect(canvas,GREEN,health,0,1)
        else:
            comfunc.clean_list(self.aux_state,'health')

    def timer_wheel(self):
        if 'shoot' in self.aux_state:
            comfunc.clean_list(self.aux_state,'timerwheel')
        else:
            if int(self.timer_wheel_step)<=len(self.timer_wheel_img)-1:
                canvas.blit(self.timer_wheel_img[self.timer_wheel_step],self.rect.center)
                self.timer_wheel_step+=1
            else:
                self.aux_state.append('shoot')
                self.shoot_start=Time.game_clock()
                self.timer_wheel_step=0
                comfunc.clean_list(self.aux_state,'timerwheel')

    def shoot(self):
        if self.shoot_start>=Time.game_clock()-.2:
            if self.hit_flash>Time.game_clock():
                self.image=self.shoot0_white
            else:
                self.image=self.shoot0
        elif self.shoot_start>=Time.game_clock()-1.2:
            if self.hit_flash>Time.game_clock():
                self.image=self.shoot1_white
            else:
                self.image=self.shoot1
        elif self.shoot_start>=Time.game_clock()-2:
            if self.image==self.shoot2 or self.image==self.shoot2_white:
                pass
            else:
                bullet=self.Bullet(self.rect.center,self.delta)
                self.bullets.add(bullet)
            if self.hit_flash>Time.game_clock():
                self.image=self.shoot2_white
            else:
                self.image=self.shoot2
        else:
            if self.hit_flash>Time.game_clock():
                self.image=self.shoot0_white
            else:
                self.image=self.neutral_stance
            comfunc.clean_list(self.aux_state,'shoot')

    def demo(self):
        self.current_sprite+=self.animate_speed
        if int(self.current_sprite)>=len(self.traverse_sprites):
            self.current_sprite=0
        self.image=self.traverse_sprites[int(self.current_sprite)]
        self.image=pygame.transform.smoothscale(self.image,(25,25))

        chance=randint(1,175)
        if chance==1:
            self.demo_dest=pygame.Vector2(
                random.randrange(max(50,self.rect.centerx-50),min(950,self.rect.centerx+50)),
                random.randrange(max(50,self.rect.centery-50),min(450,self.rect.centery+50)))

        v=comfunc.vector_from_coords(self.rect.center,self.demo_dest)
        if v.length_squared()>0:
            v.scale_to_length((self.speed*.7)*Time.abs_delta())
        self.dest+=v
        self.rect.center=self.dest

    def traverse(self):
        self_vector=pygame.Vector2(self.rect.center)
        player_vector=pygame.Vector2(player.rect.center)
        aggro_prox=350
        max_prox=100
        min_prox=95
        self.sprite_set=self.traverse_sprites if self.hit_flash<Time.game_clock() else self.traverse_white
        if self_vector.distance_to(player_vector)<min_prox:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.sprite_set):
                    self.current_sprite=0
                self.image=self.sprite_set[int(self.current_sprite)]
                if 'trap' not in self.aux_state:
                    v=comfunc.vector(player,self)
                    if v.length_squared()>0:
                        v.scale_to_length((self.speed*.9)*self.delta)
                    self.dest+=v
        elif self_vector.distance_to(player_vector)<aggro_prox:
            if self_vector.distance_to(player_vector)>max_prox:
                self.current_sprite+=self.animate_speed
                if int(self.current_sprite)>=len(self.sprite_set):
                    self.current_sprite=0
                self.image=self.sprite_set[int(self.current_sprite)]
                if 'trap' not in self.aux_state:
                    v=comfunc.vector(self,player)
                    if v.length_squared()>0:
                        v.scale_to_length(self.speed*self.delta)
                    self.dest+=v
        self.rect.center=self.dest

    def vitality(self):
        if self.hp <= 0:
            self.loot_dropper()
            self.kill()

    def death_animation(self):
        self.sprite_set=self.traverse_white
        self.image=self.sprite_set[int(self.current_sprite)]
        if not self.dying:
            self.dying=True
            self.time_of_death=Time.game_clock()
            self.hit_flash=Time.game_clock()+.2
            self.death_particles=[]
            self.death_particles.append(particles.ParticleEmitter(
                0,
                (self.rect.centerx,self.rect.centerx),
                (self.rect.centery,self.rect.centery),
                [DARK_RED,DEEP_RED,RED,LIGHT_GREEN],
                1,
                'explode','move_out_fast'))
            # self.death_particles.append(particles.ParticleEmitter(
            #     1,
            #     (self.rect.centerx,self.rect.centerx),
            #     (self.rect.centery,self.rect.centery),
            #     [FORREST_GREEN,RED,GREEN],
            #     3,
            #     'vine','timed_emit',
            #     emit_time=0,
            #     square=True))
            # self.death_particles.append(particles.ParticleEmitter(
            #     0,
            #     (self.rect.centerx,self.rect.centerx),
            #     (self.rect.centery,self.rect.centery),
            #     [RED,DARK_LEATHER,LEATHER,BROWN,GREEN],
            #     2,
            #     'halo_wave','burst_emit200','move_out_fast','explode_dest','shrink'))
        else:
            if Time.game_clock()-self.time_of_death>.05:
                radius=200-(Time.game_clock()-self.time_of_death)*463
                pygame.draw.circle(canvas,WHITE,self.rect.center,radius,1)
            if Time.game_clock()-self.time_of_death>.48:
                for i in self.death_particles:
                    i.update(canvas)
            if Time.game_clock()-self.time_of_death>.78:
                self.vitality()

    def auxillary(self,canvas,player):
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
            if chance==1:
                self.aux_state.append('shoot')
                self.shoot_start=Time.game_clock()
                self.timer_wheel_step=0
        if 'bleed' in self.aux_state:
            self.bleed()
        if 'trap' in self.aux_state:
            self.trap(self.trap_duration)
        if 'chain' in self.aux_state:
            self.chain_lightning(canvas,player)

    def blit(self):
        canvas.blit(self.image,(self.x,self.y))

    def update(self,canvas,player,delta):
        self.delta=delta
        self.pos=pygame.Vector2((self.rect.center))
        self.blit()
        if self.hp<=0:
            self.death_animation()
        else:
            self.auxillary(canvas,player)
        for i in self.bullets:
            i.update(canvas)

class Nid(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.delta=Time.game_clock()
        self.image = pygame.image.load(r'media\enemies\nid\idle\nid_idle1.png').convert_alpha()
        self.mask=pygame.mask.from_surface(self.image)
        self.rect=pygame.Rect(x,y,self.image.get_width(),self.image.get_height())
        self.pos=pygame.Vector2((self.rect.center))
        self.demo_dest=pygame.Vector2((self.rect.center))
        self.hp = randint(10,25)+10
        self.hp_ratio=self.rect.width/self.hp
        self.defense = randint(0,1)
        self.damage_ref_timer=Time.game_clock()
        self.hpbar_ref_timer=Time.game_clock()
        self.hit_flash=Time.game_clock()
        self.aux_state=[]
        self.timer_wheel_step=0
        self.image_loader()
        self.current_sprite=0
        self.animate_speed=.09
        self.chance_to_jump=1,300 #chance is one in the second int
        self.dest=pygame.Vector2((self.rect.center))
        self.vector=pygame.math.Vector2(0,0)
        self.speed=160
        self.webs=pygame.sprite.Group()
        self.dying=False
        self.jump_time=Time.Period()
        self.jump_time.grow(2.4)
        self.jump_particles=[]

    @property
    def x(self):
        return self.rect.x
    @x.setter
    def x(self,value):
        self.rect.x=value
    @property
    def y(self):
        return self.rect.y
    @y.setter
    def y(self,value):
        self.rect.y=value
    @property
    def hit_box(self):
        bound_rect=self.image.get_bounding_rect()
        if self.jump_time.frame(1.5,2.4):
            #no collision mid_air
            return bound_rect
        bound_rect[0]=bound_rect[0]+self.x
        bound_rect[1]=bound_rect[1]+self.y
        return (bound_rect)

    class Web(pygame.sprite.Sprite):
        def __init__(self,pos) -> None:
            super().__init__()
            self.image_loader()
            self.image=random.choice(self.webbings)
            self.rect=pygame.Rect(pos[0],pos[1],self.image.get_width(),self.image.get_height())
            self.rect.center=(pos[0],pos[1])
            self.life_time=Time.Period()
            self.pos=pygame.Vector2(self.rect.center)
            self.mask=pygame.mask.from_surface(self.image)
            self.slowdown=.1

        def image_loader(self):
            self.webbings=[]
            self.webbings.append(pygame.image.load(r'media\enemies\nid\webbing\nid_web1.png').convert_alpha())
            self.webbings.append(pygame.image.load(r'media\enemies\nid\webbing\nid_web2.png').convert_alpha())
            self.webbings.append(pygame.image.load(r'media\enemies\nid\webbing\nid_web3.png').convert_alpha())
            self.webbings.append(pygame.image.load(r'media\enemies\nid\webbing\nid_web4.png').convert_alpha())

        def filter(self):
            if self.rect.colliderect(player):
                if pygame.sprite.collide_mask(self,player):
                    player.slowdowns.append(self)
            if self.life_time.age(minimum=8+random.uniform(0.0,5.0)):
                comfunc.clean_list(player.slowdowns,self)
                self.kill()

        def update(self,canvas):
            self.filter()
            canvas.blit(self.image,self.rect.center)

    def image_loader(self):
        self.trap_net=pygame.image.load(r'media\relics\fox\fox_net.png').convert_alpha()
        self.neutral_stance= pygame.image.load(r'media\enemies\nid\idle\nid_idle1.png').convert_alpha()
        self.timer_wheel_img=[]
        self.idle_sprites=[]
        self.idle_white=[]
        self.jump_sprites=[]
        self.jump_white=[]
        self.jump_shadow=pygame.image.load(r'media\enemies\nid\jump\jump_shadow.png').convert_alpha()
        self.jump_shadow2=pygame.image.load(r'media\enemies\nid\jump\jump_shadow2.png').convert_alpha()
        self.jump_shadow3=pygame.image.load(r'media\enemies\nid\jump\jump_shadow3.png').convert_alpha()
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl00.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl01.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl02.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl03.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl04.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl05.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl06.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl07.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl08.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl09.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl10.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl11.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl12.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl13.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl14.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl15.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl16.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl17.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl18.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl19.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl20.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl21.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl22.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl23.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl24.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl25.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl26.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl27.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl28.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl29.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl30.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl31.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl32.png').convert_alpha())
        self.timer_wheel_img.append(pygame.image.load(r'media\twirl\twirl33.png').convert_alpha())
        self.idle_sprites.append(pygame.image.load(r'media\enemies\nid\idle\nid_idle1.png').convert_alpha())
        self.idle_sprites.append(pygame.image.load(r'media\enemies\nid\idle\nid_idle2.png').convert_alpha())
        self.idle_sprites.append(pygame.image.load(r'media\enemies\nid\idle\nid_idle3.png').convert_alpha())
        self.idle_sprites.append(pygame.image.load(r'media\enemies\nid\idle\nid_idle4.png').convert_alpha())
        self.jump_sprites.append(pygame.image.load(r'media\enemies\nid\jump\nid_jump1.png').convert_alpha())
        self.jump_sprites.append(pygame.image.load(r'media\enemies\nid\jump\nid_jump2.png').convert_alpha())
        self.jump_sprites.append(pygame.image.load(r'media\enemies\nid\jump\nid_jump3.png').convert_alpha())
        self.jump_sprites.append(pygame.image.load(r'media\enemies\nid\jump\nid_jump4.png').convert_alpha())
        self.idle_white.append(pygame.image.load(r'media\enemies\nid\idle_white\nid_idle1_white.png').convert_alpha())
        self.idle_white.append(pygame.image.load(r'media\enemies\nid\idle_white\nid_idle2_white.png').convert_alpha())
        self.idle_white.append(pygame.image.load(r'media\enemies\nid\idle_white\nid_idle3_white.png').convert_alpha())
        self.idle_white.append(pygame.image.load(r'media\enemies\nid\idle_white\nid_idle4_white.png').convert_alpha())
        self.jump_white.append(pygame.image.load(r'media\enemies\nid\jump_white\nid_jump1_white.png').convert_alpha())
        self.jump_white.append(pygame.image.load(r'media\enemies\nid\jump_white\nid_jump2_white.png').convert_alpha())
        self.jump_white.append(pygame.image.load(r'media\enemies\nid\jump_white\nid_jump3_white.png').convert_alpha())
        self.jump_white.append(pygame.image.load(r'media\enemies\nid\jump_white\nid_jump4_white.png').convert_alpha())

    def loot_dropper(self):
        loot=equip.standard_table()
        if loot is None:
            return
        loot.rect.topleft=self.rect.topleft
        spawned_loot.add(loot)

    def collision_check(self):
        pass

    def damage(self,damage):
        if not self.jump_time.frame(1.5,2.4):
            if damage>5:
                smrumble=damage*.1
                lgrumble=damage*.025
                refcon.rumble(refcon.P1,lgrumble,smrumble,100)
            self.hp-=max(0,damage-self.defense)
            if self.hp<0:
                self.hp=0
            else:
                self.aux_state.append('health')
                self.aux_state.append('timerwheel')
                self.hpbar_ref_timer=Time.game_clock()+3
                self.hit_flash=Time.game_clock()+.1
                self.health_bar()
                rand_pos=randint(self.x,self.rect.right),randint(self.y,self.rect.bottom)
                damage_text.add(particles.HoverText(rand_pos,damage,'rise',outline_size=1,outline_color=BLACK))

    def trap(self,duration):
        if 'trap' not in self.aux_state:
            self.trap_start=Time.game_clock()+duration
            self.aux_state.append('trap')
            self.trap_duration=duration
        if self.trap_start>Time.game_clock():
            canvas.blit(self.trap_net,self.rect.topleft)
        else:
            comfunc.clean_list(self.aux_state,'trap')

    def stun(self,duration):
        if 'stun' not in self.aux_state:
            self.stun_start=Time.game_clock()+duration
            self.aux_state.append('stun')
            self.stun_duration=duration
            self.stun_particles=particles.ParticleEmitter(.05,(self.pos[0]-10,self.pos[0]+10),
            (self.pos[1]-20,self.pos[1]),
            [RED,PALE_YELLOW,PALE_YELLOW,PALE_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW,BRIGHT_YELLOW],
            2,'burst_emit20','halo_wave',square=True)
        if self.stun_start>Time.game_clock():
            self.stun_particles.update(canvas)
        else:
            comfunc.clean_list(self.aux_state,'stun')

    def bleed(self):
        if 'bleed' not in self.aux_state:
            self.bleed_start=Time.game_clock()
            self.aux_state.append('bleed')
        if self.bleed_start>Time.game_clock()-5:
            self.hp-=.05
            self.hpbar_ref_timer=Time.game_clock()+3
            self.health_bar()
        else:
            comfunc.clean_list(self.aux_state,'bleed')

    def chain_lightning(self,canvas,player):
        if 'chain' not in self.aux_state:
            self.chain_start=Time.game_clock()
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
        if self.chain_start>Time.game_clock()-1.5:
            self.hp-=.25
            self.hpbar_ref_timer=Time.game_clock()+3
            self.health_bar()
            for i in enemies:
                try:
                    i.lightning.update(canvas)
                    self.lightning_implosion.update(canvas)
                except AttributeError:
                    pass
        else:
            comfunc.clean_list(self.aux_state,'chain')

    def health_bar_pop_up(self):
        self.hpbar_ref_timer=Time.game_clock()+3
        self.aux_state.append('health')
        self.health_bar()

    def health_bar(self):
        time_stamp=Time.game_clock()
        if time_stamp<self.hpbar_ref_timer:
            health_bar_thickness=3
            outline=pygame.Rect(self.rect.left-1,self.rect.top-health_bar_thickness-1,self.rect.width+2,5)
            health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.hp*self.hp_ratio,health_bar_thickness)
            missing_health=pygame.Rect(self.rect.left,self.rect.top-health_bar_thickness,self.rect.width,health_bar_thickness)
            pygame.draw.rect(canvas,WHITE,outline,0,1)
            pygame.draw.rect(canvas,RED,missing_health,0,1)
            pygame.draw.rect(canvas,GREEN,health,0,1)
        else:
            comfunc.clean_list(self.aux_state,'health')

    def timer_wheel(self):
        if 'jump' in self.aux_state:
            comfunc.clean_list(self.aux_state,'timerwheel')
        else:
            if int(self.timer_wheel_step)<=len(self.timer_wheel_img)-1:
                canvas.blit(self.timer_wheel_img[self.timer_wheel_step],self.rect.center)
                self.timer_wheel_step+=1
            else:
                self.aux_state.append('jump')
                self.jump_time=Time.Period()
                self.timer_wheel_step=0
                comfunc.clean_list(self.aux_state,'timerwheel')

    def jump(self):
        self.sprite_set=self.jump_sprites if self.hit_flash<Time.game_clock() else self.jump_white
        if self.jump_time.age(max=.25):
            self.current_sprite=0#pre-jump
        elif self.jump_time.age(max=1.5):
            self.current_sprite=1#squash pre-jump
            if self.jump_time.frame(1.4,1.5):
                self.webs.add(self.Web((random.randint(self.x,self.rect.right),random.randint(self.y,self.rect.bottom))))
            jump_angle=comfunc.get_angle(player.rect.center,self.rect.center)
            jump_angle+=random.uniform(-60.0,60.0)
            self.jump_v=comfunc.vector_from_coords(
                self.rect.center,
                comfunc.move(player.rect.center,randint(100,250),jump_angle))
        elif self.jump_time.age(max=2.4):
            self.current_sprite=2#stretch in-air jump
            if 'trap' not in self.aux_state:
                if self.jump_v.length_squared()>0:
                    self.jump_v.scale_to_length(self.speed*self.delta)
                self.dest+=self.jump_v
                self.rect.center=self.dest
                #jump shadow animation
                if self.jump_time.age(max=1.54):
                    canvas.blit(self.jump_shadow,self.rect.bottomleft)
                elif self.jump_time.age(max=1.58):
                    canvas.blit(self.jump_shadow2,self.rect.bottomleft)
                elif self.jump_time.age(max=2.30):
                    canvas.blit(self.jump_shadow3,self.rect.bottomleft)
                elif self.jump_time.age(max=2.34):
                    canvas.blit(self.jump_shadow2,self.rect.bottomleft)
                elif self.jump_time.age(max=2.4):
                    canvas.blit(self.jump_shadow,self.rect.bottomleft)
        elif self.jump_time.age(max=3.15):
            self.current_sprite=3#squash post-jump
            if self.jump_time.frame(2.4,2.45):
                if self.jump_time.frame(2.4,2.42):
                    self.webs.add(self.Web((random.randint(self.x,self.rect.right),random.randint(self.y,self.rect.bottom))))
                self.jump_particles.append(
                    particles.ParticleEmitter(
                        0,
                        (self.x,self.rect.right),
                        (self.rect.centery,self.rect.bottom),
                        [WHITE,LIGHT_GREY],
                        1,
                        'move_to_dest_fast','explode','fast_decay'))
            if 'trap' not in self.aux_state:
                if self.jump_v.length_squared()>0:
                    self.jump_v.scale_to_length(self.speed*self.delta*.2)
                self.dest+=self.jump_v
                self.rect.center=self.dest
        else:
            comfunc.clean_list(self.aux_state,'jump')
        self.image=self.sprite_set[int(self.current_sprite)]

    def demo(self):
        self.current_sprite+=self.animate_speed
        if int(self.current_sprite)>=len(self.idle_sprites):
            self.current_sprite=0
        self.image=self.idle_sprites[int(self.current_sprite)]
        self.image=pygame.transform.smoothscale(self.image,(25,25))

        chance=randint(1,175)
        if chance==1:
            self.demo_dest=pygame.Vector2(
                random.randrange(max(50,self.x-50),min(950,self.x+50)),
                random.randrange(max(50,self.y-50),min(450,self.y+50)))

        v=comfunc.vector_from_coords(self.rect.center,self.demo_dest)
        if v.length_squared()>0:
            v.scale_to_length((self.speed*.7)*Time.abs_delta())
        self.dest+=v
        self.rect.center=self.dest

    def idle(self):
        self.sprite_set=self.idle_sprites if self.hit_flash<Time.game_clock() else self.idle_white
        self.current_sprite+=self.animate_speed
        if int(self.current_sprite)>=len(self.sprite_set):
            self.current_sprite=0
        self.image=self.sprite_set[int(self.current_sprite)]

    def vitality(self):
        if self.hp <= 0:
            self.loot_dropper()
            self.kill()

    def death_animation(self):
        self.sprite_set=self.idle_white
        self.image=self.sprite_set[int(self.current_sprite)]
        if not self.dying:
            self.dying=True
            self.time_of_death=Time.game_clock()
            self.hit_flash=Time.game_clock()+.2
            self.death_particles=[]
            self.death_particles.append(
                particles.ParticleEmitter(
                    0,
                    (self.x,self.rect.right),
                    (self.rect.centery,self.rect.bottom),
                    [WHITE,LIGHT_GREY],
                    1,
                    'move_to_dest_fast','explode','shrink','slow_emit','fast_emit','move_out_fast'))
        else:
            if Time.game_clock()-self.time_of_death>.05:
                radius=200-(Time.game_clock()-self.time_of_death)*463
                pygame.draw.circle(canvas,WHITE,self.rect.center,radius,1)
            if Time.game_clock()-self.time_of_death>.48:
                for i in self.death_particles:
                    i.update(canvas)
            if Time.game_clock()-self.time_of_death>.78:
                self.vitality()

    def auxillary(self,canvas,player):
        if 'health' in self.aux_state:
            self.health_bar()
        if 'stun' in self.aux_state:
            self.stun(self.stun_duration)
        if 'stun' not in self.aux_state:
            if 'timerwheel' in self.aux_state:
                self.timer_wheel()
            if 'jump' in self.aux_state:
                self.jump()
            else:
                self.idle()
            if 'jump' not in self.aux_state:
                chance=randint(self.chance_to_jump[0],self.chance_to_jump[1])
                if chance==1:
                    self.aux_state.append('jump')
                    self.jump_time=Time.Period()
                    self.timer_wheel_step=0
        if 'bleed' in self.aux_state:
            self.bleed()
        if 'trap' in self.aux_state:
            self.trap(self.trap_duration)
        if 'chain' in self.aux_state:
            self.chain_lightning(canvas,player)
        for i in self.jump_particles:
            i.update(canvas)

    def blit(self):
        canvas.blit(self.image,(self.x,self.y))

    def update(self,canvas,player,delta):
        self.delta=delta
        self.pos=pygame.Vector2((self.rect.center))
        for i in self.webs:
            i.update(canvas)
        self.blit()
        if self.hp<=0:
            self.death_animation()
        else:
            self.auxillary(canvas,player)
