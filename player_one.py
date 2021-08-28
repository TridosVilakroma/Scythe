from pygame.constants import JOYBUTTONDOWN
from enemies import Scarecrow
import pygame,time
class PlayerOne(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y):
        super().__init__()
        self.hp=10
        self.focus = 'traverse'
        self.animating=False
        self.direction='right'
        self.walkrightsprites =[]
        self.walkleftsprites =[]
        self.walkdownsprites =[]
        self.walkupsprites =[]
        self.blinkrightsprites =[]
        self.blinkleftsprites =[]
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk0.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk1.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk2.png'))
        self.walkrightsprites.append(pygame.image.load('media\scyman_walk\scymanwalk3.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk0.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk1.png'))
        self.walkleftsprites.append(pygame.image.load('media\scyman_walk\left_walk\left_walk2.png'))
       # self.blinkrightsprites.append(pygame.image.load('media\scyman_walk\\blink\\rightblink0.png'))
        self.blinkrightsprites.append(pygame.image.load('media\scyman_walk\\blink\\rightblink1.png'))
        #self.blinkrightsprites.append(pygame.image.load('media\scyman_walk\\blink\\rightblink1.png'))
        #self.blinkrightsprites.append(pygame.image.load('media\scyman_walk\\blink\\rightblink2.png'))
        #self.blinkrightsprites.append(pygame.image.load('media\scyman_walk\\blink\leftblink1.png'))
        self.blinkleftsprites.append(pygame.image.load('media\scyman_walk\\blink\leftblink2.png'))
        self.blinkleftsprites.append(pygame.image.load('media\scyman_walk\\blink\leftblink3.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk1.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk0.png'))
        self.walkupsprites.append(pygame.image.load(r'media\scyman_walk\up_walk\upwalk2.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown0.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown1.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown2.png'))
        self.walkdownsprites.append(pygame.image.load(r'media\scyman_walk\down_walk\walkdown3.png'))
        self.current_sprite=0
        self.image=self.walkrightsprites[self.current_sprite]
        self.positionx=pos_x
        self.positiony=pos_y
        self.animate_speed=.09
        self.speed=180
        self.blink_distance=90
        self.blink_step_cooldown=.5
        self.blink_time_ref=time.time()  
        self.rect=self.image.get_rect()    
    def collide(self):
        pass

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
    def blink_animate(self):
        if self.animating==True:
            self.current_sprite+=self.animate_speed
            if int(self.current_sprite)>=len(self.blinkrightsprites):
                self.current_sprite=0
                self.animating=False
            self.image=self.blinkrightsprites[int(self.current_sprite)]
        else:
            self.image=self.walkrightsprites[int(self.current_sprite)]
    def vitality(self):
        pass    
    def traverse(self,P1,delta):
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)

        if motionx>.5:
            if motiony>.5:#moving right down
                if self.positionx<968:
                    if self.positiony<468:
                        self.positionx+=(self.speed*delta)*.75
                        self.positiony+=(self.speed*delta)*.75
                        self.animate_switch()
            elif motiony<-.5:#moving right up
                if self.positionx<968:
                    if self.positiony>0:
                        self.positionx+=(self.speed*delta)*.75
                        self.positiony-=(self.speed*delta)*.75
                        self.animate_switch()            
            elif self.positionx<968:#moving right
                self.positionx+=self.speed*delta
                self.animate_switch()
            self.direction='right'
        elif motionx<-.5:
            if motiony>.5:#moving left down
                if self.positionx>0:
                    if self.positiony<468:
                        self.positionx-=(self.speed*delta)*.75
                        self.positiony+=(self.speed*delta)*.75
                        self.animate_switch()
            elif motiony<-.5:#moving left up
                if self.positionx>0:
                    if self.positiony>0:
                        self.positionx-=(self.speed*delta)*.75
                        self.positiony-=(self.speed*delta)*.75
                        self.animate_switch()
            elif self.positionx>0:#moving left
                self.positionx-=self.speed*delta
                self.animate_switch()
            self.direction='left'
        elif motiony>.5:#moving down
            if self.positiony<468:
                self.positiony+=self.speed*delta
                self.animate_switch()
            self.direction='down'
        elif motiony<-.5:#moving up
            if self.positiony>0:
                self.positiony-=self.speed*delta
                self.animate_switch()           
            self.direction='up'
        self.traverse_animate()

    def blink_step(self,P1):
        self.focus='traverse'
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)
        self.animating=True
        self.blink_animate()
        if motionx>.5:
            if motiony>.5:
                self.positionx+=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            elif motiony<-.5:
                self.positionx+=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            else:
                self.positionx+=self.blink_distance
        elif motionx<-.5:
            if motiony>.5:
                self.positionx-=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            elif motiony<-.5:
                self.positionx-=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            else:
                self.positionx-=self.blink_distance
        elif motiony>.5:
            if motionx>.5:
                self.positionx+=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            elif motionx<-.5:
                self.positionx-=self.blink_distance/2
                self.positiony+=self.blink_distance/2
            else:
                self.positiony+=self.blink_distance
        elif motiony<-.5:
            if motionx>.5:
                self.positionx+=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            elif motionx<-.5:
                self.positionx-=self.blink_distance/2
                self.positiony-=self.blink_distance/2
            else:
                self.positiony-=self.blink_distance
    
    def scythe_slash(self,):
        pass
    def action(self,P1):
        time_stamp=time.time()
        if P1.get_button(0):
            if time_stamp>self.blink_time_ref:
                self.blink_time_ref=time_stamp+self.blink_step_cooldown
                self.focus ='blink'
        elif P1.get_button(2):
            self.focus='slash'  

    def focus_switch(self,P1,delta):
        if self.focus == 'traverse':
            self.traverse(P1,delta)
        elif self.focus =='blink':
            self.blink_step(P1)
        elif self.focus=='slash':
            self.scythe_slash()

    def update(self,P1,delta):
        self.focus_switch(P1,delta)
        self.action(P1)