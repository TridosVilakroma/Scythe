import pygame,common_functions
import operator
from pygame import*
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
        self.animate_speed=.09
        self.speed=72
    
        
    def animate_switch(self):
        self.animating=True   
    def animate(self):
        if self.animating==True:
            self.current_sprite+=self.animate_speed
            if int(self.current_sprite)>=len(self.sprites):
                self.current_sprite=0
                self.animating=False
        self.image=self.sprites[int(self.current_sprite)]


    def traverse(self,P1,delta):
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)
        if motionx>.5:
            if self.positionx>0:
                self.positionx+=self.speed*delta
                self.animate_switch()
        if motionx<-.5:
            if self.positionx<1000:
                self.positionx-=self.speed*delta
                self.animate_switch()
        if motiony>.5:
            if self.positiony>0:
                self.positiony+=self.speed*delta
                self.animate_switch()
        if motiony<-.5:
            if self.positiony<500:
                self.positiony-=self.speed*delta
                self.animate_switch()



        
    def update(self,P1,delta):
        self.animate()
        self.traverse(P1,delta)