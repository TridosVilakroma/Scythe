from color_palette import GREEN, RED, WHITE
import pygame,time
from random import randint
import common_functions as comfunc

screen=None
enemies=[]
player1pos=None
attacks=[]

class Scarecrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('media\deco\scarecrow.png').convert_alpha()
        self.x=randint(0,968)
        self.y=randint(0,468)
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
        self.hp = randint(10,25)
        self.hp_ratio=self.rect.width/self.hp
        self.defense = randint(0,3)
        self.damage_ref_timer=time.time()
        self.hpbar_ref_timer=time.time()
        self.aux_state=[]
        self.timer_wheel_step=0
        self.image_loader()
    def image_loader(self):
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
        elif self.dust_start>=time.time()-1.2:
            screen.blit(self.straw_stalk,self.dust_pos)
            dust_rect=pygame.Rect((self.dust_pos),(32,32))
            attacks.append((.75,dust_rect))
        elif self.dust_start>=time.time()-1.3:
            screen.blit(self.small_straw,self.dust_pos)
        else:
           comfunc.clean_list(self.aux_state,'dust') 
    def vitality(self):
        if self.hp <= 0:
            self.kill()
    def auxillary(self):
        if 'health' in self.aux_state:
            self.health_bar()
        if 'timerwheel' in self.aux_state:
            self.timer_wheel()
        if 'dust' in self.aux_state:
            self.dust()
   
    def blit(self):
        screen.blit(self.image,(self.x,self.y))

    def update(self):
        self.blit()
        self.vitality()
        self.auxillary()
        
