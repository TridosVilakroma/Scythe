import pygame
import operator

from pygame.constants import JOYAXISMOTION
class ScymanWalk(pygame.sprite.Sprite):
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
        self.rect=self.image.get_rect()
        self.rect.center=[pos_x,pos_y]
        self.x_velocity=0
        self.y_velocity=0
        # self.left=[pos_x]
        # self.top=[pos_y]
        self.speed=4
        
    def animate(self):
        self.animating=True

    def move(self,controller,event):    
        x_axis = controller.get_axis(0)
        y_axis = controller.get_axis(1)
        if x_axis>0:
            if self.x_velocity<3:
                self.x_velocity+=1
        elif x_axis<0:
            if self.x_velocity>3:
                self.x_velocity-=1
        self.rect.left+=self.x_velocity*x_axis
        if y_axis>0:
            if self.y_velocity<3:
                self.y_velocity+=1
        elif y_axis<0:
            if self.y_velocity>3:
                self.y_velocity-=1
        self.rect.top+=self.y_velocity*y_axis

    def update(self,speed):
        if self.animating==True:
            self.current_sprite+=speed
            if int(self.current_sprite)>=len(self.sprites):
                self.current_sprite=0
                self.animating=False
        self.image=self.sprites[int(self.current_sprite)]