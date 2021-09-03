from color_palette import GREEN, RED, WHITE
import pygame,time
from random import randint
import common_functions as comfunc

screen=None
enemies=[]

class Scarecrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('media\deco\scarecrow.png').convert_alpha()
        self.x=randint(0,968)
        self.y=randint(0,468)
        self.rect=pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())
        self.hp = randint(3,10)
        self.hp_ratio=self.rect.width/self.hp
        self.defense = randint(0,3)
        self.damage_ref_timer=time.time()
        self.hpbar_ref_timer=time.time()
        self.aux_state=[]
    def collision_check(self):
        pass
    def damage(self,damage):
        self.hp-=max(0,damage-self.defense)
        if self.hp<0:
            self.hp=0
        self.aux_state.append('health')
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

    def vitality(self):
        if self.hp <= 0:
            self.kill()
        
    def auxillary(self):
        if 'health' in self.aux_state:
            self.health_bar()    
    def update(self):
        self.vitality()
        self.auxillary()
        
