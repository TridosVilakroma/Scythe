import pygame,common_functions
import operator

from pygame.constants import JOYAXISMOTION, JOYHATMOTION, MOUSEBUTTONDOWN, K_a, K_d
class PlayerOne(pygame.sprite.Sprite):
    def __init__(self,pos_x, pos_y):
        super().__init__()
        self.animating=False
        self.sprites =[]
        self.sprites.append(pygame.image.load('media\scyman_walk\scymanwalk0.png'))
        self.sprites.append(pygame.image.load('media\scyman_walk\scymanwalk1.png'))
        self.sprites.append(pygame.image.load('media\scyman_walk\scymanwalk2.png'))
        self.sprites.append(pygame.image.load('media\scyman_walk\scymanwalk3.png'))
        self.current_sprite=0
        self.image=self.sprites[self.current_sprite]
        self.positionx=pos_x
        self.positiony=pos_y
        self.friction =.25
        self.x_velocity,self.y_velocity=0,0
        self.acceleration=75
        self.speed=.09
        self.gravity =.35     
        
    def animate_switch(self):
        self.animating=True   
    def animate(self):
        if self.animating==True:
            self.current_sprite+=self.speed
            if int(self.current_sprite)>=len(self.sprites):
                self.current_sprite=0
                self.animating=False
        self.image=self.sprites[int(self.current_sprite)]

    def move(self,delta,event):
        if event.type==JOYAXISMOTION:
            if event.axis==1 and event.value<-.2:
                if self.x_velocity>-225:
                    self.x_velocity-=self.acceleration
            if event.axis ==1 and event.value>.2:
                if self.x_velocity<225:
                    self.x_velocity+=self.acceleration
            if event.axis==0 and event.value<-.2:
                if self.y_velocity>225:
                    self.y_velocity+=self.acceleration
            if event.axis ==0 and event.value>.2:
                if self.y_velocity<-225:
                    self.y_velocity-=self.acceleration
            
    def update(self,delta):
        self.animate()
        if 0<=self.positionx<=1000:
            self.positionx+=int(self.x_velocity*delta)
        else:
            self.positionx=500
        self.x_velocity+=self.friction
        if 0<=self.positiony<=500:
            self.positiony+=int(self.y_velocity*delta)
        else:
            self.positiony=250
        self.y_velocity+=self.friction