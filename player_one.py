import pygame,common_functions,time
import operator
#from pygame import*
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
        self.speed=180
        self.blink_distance=90
        self.blink_step_cooldown=.5
        self.blink_time_ref=time.time()
    
        
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
            if motiony>.5:
                if self.positionx<968:
                    if self.positiony<468:
                        self.positionx+=(self.speed*delta)*.75
                        self.positiony+=(self.speed*delta)*.75
                        self.animate_switch()
                        if P1.get_button(0):
                            self.blink_step('right',P1)
            elif motiony<-.5:
                if self.positionx<968:
                    if self.positiony>0:
                        self.positionx+=(self.speed*delta)*.75
                        self.positiony-=(self.speed*delta)*.75
                        self.animate_switch()
                        if P1.get_button(0):
                            self.blink_step('right',P1)
                       
            elif self.positionx<968:
                self.positionx+=self.speed*delta
                self.animate_switch()
                if P1.get_button(0):
                    self.blink_step('right',P1)
        elif motionx<-.5:
            if motiony>.5:
                if self.positionx>0:
                    if self.positiony<468:
                        self.positionx-=(self.speed*delta)*.75
                        self.positiony+=(self.speed*delta)*.75
                        self.animate_switch()
                        if P1.get_button(0):
                            self.blink_step('left',P1)
            elif motiony<-.5:
                if self.positionx>0:
                    if self.positiony>0:
                        self.positionx-=(self.speed*delta)*.75
                        self.positiony-=(self.speed*delta)*.75
                        self.animate_switch()
                        if P1.get_button(0):
                            self.blink_step('left',P1)
            elif self.positionx>0:
                self.positionx-=self.speed*delta
                self.animate_switch()
                if P1.get_button(0):
                    self.blink_step('left',P1)
        elif motiony>.5:
            if self.positiony<468:
                self.positiony+=self.speed*delta
                self.animate_switch()
                if P1.get_button(0):
                    self.blink_step('down',P1)
        elif motiony<-.5:
            if self.positiony>0:
                self.positiony-=self.speed*delta
                self.animate_switch()
                if P1.get_button(0):
                    self.blink_step('up',P1)
    def blink_step(self,direction,P1):
        motionx=P1.get_axis(0)
        motiony=P1.get_axis(1)
        time_stamp=time.time()
        if time_stamp>self.blink_time_ref:
            self.blink_time_ref=time_stamp+self.blink_step_cooldown
            if direction=='right':
                if motiony>.5:
                    self.positionx+=self.blink_distance/2
                    self.positiony+=self.blink_distance/2
                elif motiony<-.5:
                    self.positionx+=self.blink_distance/2
                    self.positiony-=self.blink_distance/2
                else:
                    self.positionx+=self.blink_distance
            if direction=='left':
                if motiony>.5:
                    self.positionx-=self.blink_distance/2
                    self.positiony+=self.blink_distance/2
                elif motiony<-.5:
                    self.positionx-=self.blink_distance/2
                    self.positiony-=self.blink_distance/2
                else:
                    self.positionx-=self.blink_distance
            if direction=='down':
                if motionx>.5:
                    self.positionx+=self.blink_distance/2
                    self.positiony+=self.blink_distance/2
                elif motionx<-.5:
                    self.positionx-=self.blink_distance/2
                    self.positiony+=self.blink_distance/2
                else:
                    self.positiony+=self.blink_distance
            if direction=='up':
                if motionx>.5:
                    self.positionx+=self.blink_distance/2
                    self.positiony-=self.blink_distance/2
                elif motionx<-.5:
                    self.positionx-=self.blink_distance/2
                    self.positiony-=self.blink_distance/2
                else:
                    self.positiony-=self.blink_distance
        
    def update(self,P1,delta):
        self.animate()
        self.traverse(P1,delta)