from color_palette import *
import pygame,time,math,equip,particles
from random import randint
import common_functions as comfunc
import Time

screen=None
canvas=None
game=None
enemies=[]
player1pos=None
player=None
attacks=[]
spawned_loot=pygame.sprite.Group()

class ScareBoss(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.delta=Time.game_clock()
        self.image = pygame.image.load(r'media\boss\scareboss\scareboss.png').convert_alpha()
        self.rect=pygame.Rect(x,y,self.image.get_width(),self.image.get_height())
        self.pos=pygame.math.Vector2((self.rect.center))
        self.hp = (randint(10,25)+750)
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
        boss_sacaling=(75,75)
        self.trap_net=pygame.image.load(r'media\relics\fox\fox_net.png').convert_alpha()
        self.norm_image=pygame.image.load(r'media\boss\scareboss\scareboss.png').convert_alpha()
        self.white=pygame.image.load(r'media\boss\scareboss\scareboss_white.png').convert_alpha()
        self.timer_wheel_img=[]
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl00.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl01.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl02.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl03.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl04.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl05.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl06.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl07.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl08.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl09.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl10.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl11.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl12.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl13.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl14.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl15.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl16.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl17.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl18.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl19.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl20.png') ,boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl21.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl22.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl23.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl24.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl25.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl26.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl27.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl28.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl29.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl30.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl31.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl32.png'),boss_sacaling).convert_alpha())
        self.timer_wheel_img.append(pygame.transform.scale(pygame.image.load(r'media\twirl\twirl33.png'),boss_sacaling).convert_alpha())
        self.small_straw=pygame.image.load(r'media\deco\small_straw.png').convert_alpha()
        self.straw_stalk=pygame.image.load(r'media\deco\straw_stalk.png').convert_alpha()

    def loot_dropper(self):
        random_loot=randint(1,7)
        try:
            equip.equip_matrix[1][random_loot].rect[0]=self.x
            equip.equip_matrix[1][random_loot].rect[1]=self.y
            spawned_loot.add(equip.equip_matrix[1][random_loot])
            popped=equip.equip_matrix[1].pop(random_loot)
        except KeyError:
            pass

    def collision_check(self):
        pass

    def damage(self,damage):
        self.hp-=max(0,damage-self.defense)
        if self.hp<0:
            self.hp=0
        else:
            self.aux_state.append('health')
            self.aux_state.append('timerwheel')
            self.hpbar_ref_timer=Time.game_clock()+3
            self.hit_flash=Time.game_clock()+.1
            self.health_bar()

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
