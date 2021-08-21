import pygame
import random

class Spritesheet():
    def __init__(self,file,position=[0,0],rng=False,speed=6):
        self.file=file
        self.image=pygame.image.load(file)
        self.position=[0,0]
        self.frame=[0,0,32,32]
        self.limit=self.image.get_rect()[2]
        self.speed=speed
        self.timer=0
        self.position=position
        self.rng=rng
        self.rng_range_lower=-.5
        self.rng_range_upper=.5
    
    def advance_frame(self):
        if self.frame[0]>=self.limit-32:
            self.frame[0]=0
        self.frame[0]+=32
    
    def movex(self):
        self.position[0]+=.4
        if self.position[0]>1030:
            self.position[0]=-30
    
    def movey(self):
        if self.rng:
            if self.timer>=10:
                if self.position[1]>=0:
                    self.position[1]+=random.uniform(self.rng_range_lower,self.rng_range_upper)
                else:
                    self.position[1]+=random.uniform(0,self.rng_range_upper)
    
    def update(self):
        self.timer +=self.speed
        if self.timer>=60:
            self.advance_frame()
            self.timer=0
        self.movex()
        self.movey()



